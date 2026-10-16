"""The cloud tier. Both modes answer an escalated turn from the phone's one text log.

    text  a cascade: Whisper's transcript in, Gemini text out, the phone speaks the reply
    live  Gemini Live native audio: the phone opens the session at the wake, seeds the log as
          text turns that ask for no reply, then sends the user's own audio from its buffered start
"""

import asyncio
import os
import time

from google import genai
from google.genai import types

TEXT_MODEL = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
LIVE_MODEL = os.getenv("GEMINI_LIVE_MODEL", "gemini-3.8-live")
SYSTEM = ("You are Buddy, the voice assistant on a pair of smart glasses. Reply in one or two short "
          "spoken sentences, in the language the user spoke. Earlier turns may have been answered on "
          "the phone; treat them as your own.")
IN_RATE, OUT_RATE = 16000, 24000
# The cloud may ask for these, but the phone always confirms first, so a cloud mistake never acts alone.
TOOLS = [types.Tool(function_declarations=[
    types.FunctionDeclaration(
        name="initiate_call", description="Phone one of the user's contacts.",
        parameters=types.Schema(type=types.Type.OBJECT, required=["name"],
                                properties={"name": types.Schema(type=types.Type.STRING)})),
    types.FunctionDeclaration(name="take_photo", description="Take a photo with the glasses camera."),
])]


def api_key():
    return os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")


def contents(log):
    return [types.Content(role=r, parts=[types.Part(text=t)]) for r, t in log]


def ask_text(log, text):
    """The cascade. Returns (reply, action), where action is a requested tool call or None."""
    if not api_key():
        return f"[cloud, dry run: would send {len(log) // 2} earlier turns and “{text}” to {TEXT_MODEL}]", None
    resp = genai.Client(api_key=api_key()).models.generate_content(
        model=TEXT_MODEL, contents=contents(log + [("user", text)]),
        config=types.GenerateContentConfig(system_instruction=SYSTEM, tools=TOOLS))
    if resp.function_calls:
        fc = resp.function_calls[0]
        return "", (fc.name, dict(fc.args or {}))
    return (resp.text or "").strip(), None


class LiveTurn:
    """A possible cloud turn. Opened at the wake so that connecting and seeding overlap the user's
    speech; the phone then either escalates with the turn's audio or drops it unused."""

    def __init__(self, log):
        self.log = list(log)
        self.out: asyncio.Queue[bytes | None] = asyncio.Queue()  # 24 kHz PCM chunks, then None
        self.transcript = ""
        self.action = None  # a requested tool call, which the phone confirms
        self.error = None
        self.ms = {}
        self._t0 = time.perf_counter()
        self._audio = asyncio.get_running_loop().create_future()
        self._task = asyncio.create_task(self._run())

    def escalate(self, pcm):
        self._t_escalate = time.perf_counter()
        self._audio.set_result(pcm)

    def drop(self):
        self._task.cancel()

    def _mark(self, name, since):
        self.ms.setdefault(name, round((time.perf_counter() - since) * 1000))

    async def _run(self):
        config = types.LiveConnectConfig(
            response_modalities=[types.Modality.AUDIO],
            system_instruction=SYSTEM,
            tools=TOOLS,
            # The phone endpoints every turn, so Gemini's own voice detection is off.
            realtime_input_config=types.RealtimeInputConfig(
                automatic_activity_detection=types.AutomaticActivityDetection(disabled=True)),
            output_audio_transcription=types.AudioTranscriptionConfig(),
        )
        try:
            async with genai.Client(api_key=api_key()).aio.live.connect(model=LIVE_MODEL, config=config) as s:
                self._mark("connect", self._t0)
                if self.log:  # earlier turns from both tiers, as context with no reply
                    await s.send_client_content(turns=contents(self.log), turn_complete=False)
                self._mark("seeded", self._t0)
                pcm = await self._audio
                await s.send_realtime_input(activity_start=types.ActivityStart())
                for i in range(0, len(pcm), IN_RATE // 5):  # 100 ms of 16-bit audio per message
                    await s.send_realtime_input(audio=types.Blob(data=pcm[i:i + IN_RATE // 5],
                                                                 mime_type=f"audio/pcm;rate={IN_RATE}"))
                await s.send_realtime_input(activity_end=types.ActivityEnd())
                async for msg in s.receive():
                    if msg.tool_call and msg.tool_call.function_calls:
                        fc = msg.tool_call.function_calls[0]
                        self.action = (fc.name, dict(fc.args or {}))
                        break  # the session ends here; the phone asks the user itself
                    if msg.data:
                        self._mark("first_audio", self._t_escalate)
                        self.out.put_nowait(msg.data)
                    sc = msg.server_content
                    if sc and sc.output_transcription and sc.output_transcription.text:
                        self.transcript += sc.output_transcription.text
                    if sc and sc.turn_complete:
                        break
                self._mark("done", self._t_escalate)
        except asyncio.CancelledError:
            pass
        except Exception as e:  # the caller falls back to the text cascade
            self.error = e
        finally:
            self.out.put_nowait(None)


async def escalate(log, text, live, pcm, play):
    """Answer a cloud turn, playing Live audio through `play`.

    Returns (reply, action, played): the reply text for the log, a requested tool call or None,
    and whether the user has already heard the reply."""
    if live:
        live.escalate(pcm)
        played = False
        while (chunk := await live.out.get()) is not None:
            await play(chunk)
            played = True
        if not live.error:
            return live.transcript.strip(), live.action, played
        print(f"  [live failed: {live.error!r}; falling back to the text cascade]")
    reply, action = await asyncio.to_thread(ask_text, log, text)
    return reply, action, False
