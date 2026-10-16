"""Train the router and measure it on held-out text, and optionally on noisy synthetic speech.

    uv run eval.py            # train, then text eval -> results/eval.md
    uv run eval.py --audio    # also speak the test set with macOS voices, add noise, run Whisper raw and after RNNoise
"""

import argparse
import re
import subprocess
import wave
from collections import Counter
from pathlib import Path

import numpy as np

from data import INTENTS, SENSITIVE, expand
from router import FLOOR, GRAMMAR, THRESHOLD, Router, banned, normalise, train

OUT = Path(__file__).parent / "results"
WHISPER = "mlx-community/whisper-large-v3-turbo"
# Test utterances that share a word with a local intent but must go to the cloud.
NEAR_MISS_WORDS = {"foto", "ketchup", "gocha", "photo", "picture", "call", "time", "camera",
                   "फोटो", "कॉल", "समय", "फोन"}
# Pink noise at an SNR for each place: synthetic stand-ins for recordings.
PROFILES = [("clean", None), ("office", 25), ("street", 15), ("auto-rickshaw", 5)]
LATIN = re.compile(r"[a-z]", re.I)


def edits(a, b):
    """Word edit distance: substitutions, insertions and deletions."""
    row = list(range(len(b) + 1))
    for i, x in enumerate(a, 1):
        prev, row[0] = row[0], i
        for j, y in enumerate(b, 1):
            prev, row[j] = row[j], min(row[j] + 1, row[j - 1] + 1, prev + (x != y))
    return row[-1]


def wer(pairs):
    """Word error rate over (reference, transcript) pairs: all word edits / all reference words, after normalise."""
    pairs = [(normalise(a).split(), normalise(b).split()) for a, b in pairs]
    return sum(edits(a, b) for a, b in pairs) / sum(len(a) for a, _ in pairs)


def wer_scored(r):
    """Hinglish is written in Latin script, and Whisper with language hi writes Devanagari, so its WER would
    count the script. WER covers English and Devanagari Hindi only."""
    return r["lang"] == "en" or not LATIN.search(r.get("spoken", r["text"]))


def near_misses(rows, preds):
    """Cloud utterances that share a word with a local intent, and those of them that ran locally."""
    near = [(r, b) for r, b in zip(rows, preds)
            if r["intent"] == "other" and NEAR_MISS_WORDS & set(normalise(r["text"]).split())]
    return near, [r["text"] for r, b in near if b != "other"]


def predict(p, norm, sensitive_threshold=None):
    """Local intent the router would run, else 'other' (cloud), for a given sensitive threshold."""
    if norm in GRAMMAR:
        return GRAMMAR[norm]
    if banned(norm):
        return "other"
    intent, score = INTENTS[int(p.argmax())], float(p.max())
    th = sensitive_threshold if (sensitive_threshold and intent in SENSITIVE) else THRESHOLD.get(intent)
    if intent == "other" or score < FLOOR or score < th:
        return "other"
    return intent


def report(title, rows, preds):
    y = [r["intent"] for r in rows]
    lines = [f"### {title} (n={len(rows)})", "", "| Intent | n | Precision | Recall |", "|:--|--:|--:|--:|"]
    for c in INTENTS:
        tp = sum(a == c and b == c for a, b in zip(y, preds))
        pp, ap = preds.count(c), y.count(c)
        lines.append(f"| {c} | {ap} | {tp / pp:.1%} ({tp}/{pp}) | {tp / ap:.1%} ({tp}/{ap}) |" if pp
                     else f"| {c} | {ap} | none predicted | 0/{ap} |")
    sens = [(a, b) for a, b in zip(y, preds) if b in SENSITIVE]
    if sens:
        n = len(sens)
        right = sum(a == b for a, b in sens)
        # The 3/n rule holds only with zero failures, so a set with a failure gets no bound.
        lines += ["", f"Sensitive local decisions: {right}/{n} correct, {n - right} wrong. "
                      + (f"With no failures in n={n}, the 95% upper bound on the error rate is about "
                         f"3/n = {3 / n:.1%}, so this set cannot show the 99.5% target (that needs about "
                         f"600 clean decisions). The bound is optimistic: each call template appears once "
                         f"per contact name, so decisions are not independent." if right == n else
                         "The 3/n bound needs zero failures, so it does not apply here.")]
    near, leaks = near_misses(rows, preds)
    lines += ["", f"Near misses (cloud utterances that share a word with a local intent): "
                  f"{len(near) - len(leaks)}/{len(near)} stayed off the phone."
                  + (f" Leaked: {', '.join(leaks)}." if leaks else "")]
    cm = Counter(zip(y, preds))
    lines += ["", "| true \\ routed | " + " | ".join(INTENTS) + " |", "|:--|" + "--:|" * len(INTENTS)]
    lines += [f"| {a} | " + " | ".join(str(cm[(a, b)]) for b in INTENTS) + " |" for a in INTENTS]
    return lines + [""]


def sweep(rows, probs):
    y = [r["intent"] for r in rows]
    lines = ["### Threshold sweep for sensitive intents (photo, call)", "",
             "| Threshold | Precision | Recall |", "|--:|--:|--:|"]
    for t in [0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.98, 0.99]:
        preds = [predict(p, normalise(r["text"]), t) for r, p in zip(rows, probs)]
        local = [(a, b) for a, b in zip(y, preds) if b in SENSITIVE]
        true = [(a, b) for a, b in zip(y, preds) if a in SENSITIVE]
        prec = sum(a == b for a, b in local) / len(local) if local else float("nan")
        rec = sum(a == b for a, b in true) / len(true)
        lines.append(f"| {t:.2f} | {prec:.1%} | {rec:.1%} |")
    return lines + [""]


def evaluate(title, rows, router):
    probs = router.probs([r["text"] for r in rows])
    preds = [predict(p, normalise(r["text"])) for r, p in zip(rows, probs)]
    lines = [f"## {title}", ""]
    for lang in ["en", "hi"]:
        idx = [i for i, r in enumerate(rows) if r["lang"] == lang]
        lines += report(f"{title}, {lang}", [rows[i] for i in idx], [preds[i] for i in idx])
    lines += sweep(rows, probs)
    misses = [f"- “{r['text']}” ({r['intent']}) → {p}" for r, p in zip(rows, preds) if r["intent"] != p]
    return lines + ["Misrouted:", ""] + (misses or ["- none"]) + [""], preds


def speech_table(lang, runs):
    """One row per noise profile and audio path, for one language."""
    lines = [f"### Speech, {lang}", "", "| Profile | Audio | WER | WER change from RNNoise | Call recall | "
             "Photo recall | Time recall | Wrong photo or call run locally | Near misses kept off the phone |",
             "|:--|:--|--:|--:|--:|--:|--:|--:|--:|"]
    for (profile, audio), (rows, preds) in runs.items():
        idx = [i for i, r in enumerate(rows) if r["lang"] == lang]
        rows, preds = [rows[i] for i in idx], [preds[i] for i in idx]
        w = wer([(r["spoken"], r["text"]) for r in rows if wer_scored(r)])
        if audio == "raw":
            base = w
        change = "" if audio == "raw" else f"{(w - base) / base:+.0%}" if base else "n/a"
        recall = [sum(r["intent"] == p == c for r, p in zip(rows, preds)) / sum(r["intent"] == c for r in rows)
                  for c in ["call_contact", "take_photo", "time"]]
        local = [r["intent"] == p for r, p in zip(rows, preds) if p in SENSITIVE]
        near, leaks = near_misses(rows, preds)
        lines.append(f"| {profile} | {audio} | {w:.1%} | {change} | " + " | ".join(f"{x:.0%}" for x in recall)
                     + f" | {local.count(False)} of {len(local)} | {len(near) - len(leaks)} of {len(near)} |")
    return lines + [""]


def speak(text, lang, path):
    if not path.exists():
        voice = "Lekha" if re.search(r"[ऀ-ॿ]", text) else ("Rishi" if lang == "en" else "Aman")
        subprocess.run(["say", "-v", voice, "--file-format=WAVE", "--data-format=LEI16@16000",
                        "-o", str(path), text], check=True)
    with wave.open(str(path)) as w:
        return np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768


def add_noise(audio, snr_db, rng):
    """Pink noise at the given SNR. Synthetic, so a stand-in for street and auto-rickshaw recordings."""
    spectrum = np.fft.rfft(rng.standard_normal(len(audio)))
    spectrum /= np.sqrt(np.arange(1, len(spectrum) + 1))
    noise = np.fft.irfft(spectrum, len(audio))
    noise *= np.sqrt(np.mean(audio ** 2) / np.mean(noise ** 2) / 10 ** (snr_db / 10))
    return (audio + noise).astype(np.float32)


def transcribe(audio, lang):
    import mlx.core as mx
    import mlx_whisper

    mx.random.seed(0)  # Whisper samples when it falls back to a higher temperature; same draws for both paths
    # The phone knows the user's language setting; detection on short clips picks the wrong one.
    return mlx_whisper.transcribe(audio, path_or_hf_repo=WHISPER, language=lang)["text"].strip()


def audio_rows(rows, snr_db):
    """Each sentence spoken and noised once, then through Whisper raw and after the live app's RNNoise filter."""
    from app import denoise

    rng = np.random.default_rng(0)
    (OUT / "audio").mkdir(parents=True, exist_ok=True)
    raw, denoised = [], []
    for i, r in enumerate(rows):
        audio = speak(r["text"], r["lang"], OUT / "audio" / f"{i:04d}.wav")
        if snr_db is not None:
            audio = add_noise(audio, snr_db, rng)
        pcm = np.clip(audio * 32768, -32768, 32767).astype(np.int16)  # 16-bit at 16 kHz, as the mic gives it
        for out, x in [(raw, pcm), (denoised, np.frombuffer(denoise(pcm.tobytes()), np.int16))]:
            out.append({**r, "text": transcribe(x.astype(np.float32) / 32768, r["lang"]), "spoken": r["text"]})
    return raw, denoised


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--audio", action="store_true")
    args = ap.parse_args()

    train_rows = expand("train")
    temperature = train(train_rows)
    router = Router()
    test = expand("test")

    lines = ["# Router eval", "", f"Train {len(train_rows)} rows. Temperature {temperature:.2f}, fitted on "
             f"5-fold held-out scores. Test {len(test)} rows with templates and contact names the router "
             f"never saw. Thresholds: {THRESHOLD}, floor {FLOOR}. Online mode, so the gray zone goes "
             f"to the cloud.", ""]
    lines += evaluate("Typed text", test, router)[0]
    if args.audio:
        runs, details = {}, []
        for profile, snr in PROFILES:
            label = profile if snr is None else f"{profile}, pink noise at {snr} dB SNR"
            for audio, rows in zip(["raw", "RNNoise"], audio_rows(test, snr)):
                section, preds = evaluate(f"Synthetic speech through Whisper, {label}, {audio}", rows, router)
                runs[(label, audio)] = rows, preds
                details += section + ["Sample transcripts:", ""]
                details += [f"- “{r['spoken']}” → “{r['text']}”" for r in rows[::40]] + [""]
        hinglish = [r["text"] for r in test if not wer_scored(r)]
        lines += ["## Synthetic speech through Whisper, raw and after RNNoise", "",
                  "Each sentence is spoken and noised once per profile; Whisper then runs on the raw audio and on "
                  "the same audio through the live app's RNNoise filter. WER is word edits over reference words, "
                  "after the router's normalise. Recall and decisions count every sentence of the language.", ""]
        lines += speech_table("en", runs) + speech_table("hi", runs)
        lines += [f"Hindi WER covers the {sum(r['lang'] == 'hi' for r in test) - len(hinglish)} sentences written "
                  f"in Devanagari. It leaves out the {len(hinglish)} Hinglish sentences, which are written in Latin "
                  f"script while Whisper with language hi writes Devanagari, so their WER would count the script: "
                  + ", ".join(hinglish) + ".", ""]
        lines += details
    OUT.mkdir(exist_ok=True)
    (OUT / "eval.md").write_text("\n".join(lines))
    print("\n".join(lines))


if __name__ == "__main__":
    main()
