"""Does context survive the hand-off between the phone and the cloud, in both directions?

Runs short scripted conversations through the phone tier with each cloud mode and checks the
turn that depends on the other tier. Typed turns are spoken by `say` for the Live mode, so Gemini
Live hears audio exactly as it would from the glass.

    uv run handoff.py                 # both cloud modes -> results/handoff.md
    uv run handoff.py --cloud live
"""

import argparse
import asyncio
import time
from datetime import datetime
from pathlib import Path

from app import say_pcm
from buddy import Buddy
from cloud import LIVE_MODEL, TEXT_MODEL, LiveTurn, api_key, escalate
from router import Router

NOW = datetime(2026, 10, 16, 16, 5)  # 16:05 IST is 11:35 in London (BST until 25 October)


def has(*words):
    return lambda reply: any(w in reply.lower() for w in words)


# (name, turns, index of the turn to check, check). Local replies are fixed; cloud replies vary.
SCENARIOS = [
    ("Local turn, then a cloud follow-up", ["what time is it", "And in London?"], 1, has("11:35", "11.35", "eleven thirty")),
    ("Same, in Hindi", ["टाइम क्या हुआ", "और लंदन में?"], 1, has("11", "ग्यारह", "साढ़े")),
    ("Local action, then a cloud question about it", ["take a photo", "what did I just do?"], 1, has("photo", "picture", "फोटो")),
    ("Cloud turn, then a call the cloud asks for, confirmed on the phone",
     ["Deepak said he'll be late for dinner. What should I tell him?", "call him", "yes"], 2,
     lambda r: r == "Calling Deepak."),
    ("Cloud asks for a call, the user says no", ["Farhan ko phone lagao, urgent hai", "nahi"], 1,
     lambda r: r == "ठीक है, रद्द कर दिया।"),
]
PAD = [("user", "what's the weather like"), ("model", "Warm and humid, about 31 degrees.")]


async def nothing(chunk):
    pass


async def turn(buddy, text, cloud, timings):
    live = LiveTurn(buddy.log) if cloud == "live" else None  # opened at the wake
    pcm = await asyncio.to_thread(say_pcm, text) if live else None
    reply = buddy.handle(text)
    if reply is not None:
        if live:
            live.drop()
        return reply, "phone"
    t0 = time.perf_counter()
    reply, action, _ = await escalate(buddy.log, text, live, pcm, nothing)
    timings.append(live.ms if live else {"done": round((time.perf_counter() - t0) * 1000)})
    reply = buddy.from_cloud(text, reply, action)
    return reply + (f"  (cloud asked for {action.name})" if action else ""), "cloud"


async def run(router, cloud):
    lines = [f"## Cloud mode: {cloud} ({LIVE_MODEL if cloud == 'live' else TEXT_MODEL})", ""]
    timings, passed = [], 0
    for name, turns, check_at, check in SCENARIOS:
        buddy = Buddy(router, now=lambda: NOW)
        replies = []
        lines += [f"**{name}**", ""]
        for text in turns:
            reply, tier = await turn(buddy, text, cloud, timings)
            replies.append(reply.split("  (cloud asked")[0])
            lines.append(f"- you: “{text}” → {tier}: “{reply}”")
        ok = check(replies[check_at])
        passed += ok
        lines += [f"- {'PASS' if ok else 'FAIL'}", ""]
    lines += [f"Passed {passed}/{len(SCENARIOS)}.", ""]

    keys = sorted({k for t in timings for k in t}, key=["connect", "seeded", "first_audio", "done"].index)
    lines += ["Cloud turn timings in ms (connect and seeded count from the wake; first audio and done "
              "count from the escalation, after the transcript):", "",
              "| " + " | ".join(keys) + " |", "|" + "--:|" * len(keys)]
    lines += ["| " + " | ".join(str(t.get(k, "")) for k in keys) + " |" for t in timings]

    if cloud == "live":  # does a longer seeded log slow the first audio?
        lines += ["", "First audio against the length of the seeded log:", "",
                  "| Earlier turns | connect | seeded | first_audio |", "|--:|--:|--:|--:|"]
        pcm = await asyncio.to_thread(say_pcm, "And in London?")
        for n in [0, 10, 40]:
            live = LiveTurn(PAD * n + [("user", "what time is it"), ("model", "It's 4:05 PM.")])
            await asyncio.sleep(1)  # the user is still speaking
            await escalate([], "", live, pcm, nothing)
            lines.append(f"| {n + 1} | {live.ms.get('connect')} | {live.ms.get('seeded')} | {live.ms.get('first_audio')} |")
    return lines + [""]


async def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cloud", choices=["text", "live"], nargs="+", default=["text", "live"])
    args = ap.parse_args()
    if not api_key():
        raise SystemExit("handoff.py needs GEMINI_API_KEY")
    router = Router()
    lines = ["# Hand-off between the phone and the cloud", "",
             f"Each conversation starts fresh, with the clock fixed at {NOW:%H:%M} IST. "
             "Both modes seed the cloud from the phone's one text log.", ""]
    for cloud in args.cloud:
        lines += await run(router, cloud)
    out = Path(__file__).parent / "results" / "handoff.md"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(main())
