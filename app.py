"""Buddy's phone tier, with the laptop microphone standing in for the glass.

    uv run app.py --language en      # mic -> RNNoise -> Silero VAD -> Whisper (MLX) -> router -> tool or cloud
    uv run app.py --language hi --noise 10   # with pink noise mixed into the mic at about 10 dB SNR

The cloud is Gemini Live when GEMINI_API_KEY is set. `--help` lists the options for experiments.

Every run also writes logs/run-YYYYmmdd-HHMMSS.log (and logs/latest.log): the turns and Pipecat's DEBUG lines.
"""

import argparse
import asyncio
import logging
import os
import re
import shlex
import subprocess
import sys
import tempfile
import time
import traceback
import wave
from pathlib import Path

import numpy as np

from buddy import Buddy
from cloud import IN_RATE, OUT_RATE, LIVE_MODEL, LiveTurn, api_key, escalate
from data import CONTACTS

VOICE = {"hi": "Lekha", "en": "Rishi"}
WHISPER = {"turbo": "mlx-community/whisper-large-v3-turbo", "small": "mlx-community/whisper-small-mlx"}
# Endpointing. smart: Silero hears 200 ms of silence, Smart Turn v3 reads the
# turn's audio, and the turn ends anyway after MAX_WAIT of silence. fixed: the turn ends at a 400 ms VAD stop.
VAD_STOP = {"smart": 0.2, "fixed": 0.4}
MAX_WAIT = 0.6
LOGS = Path(__file__).parent / "logs"
# Whisper's prompt: the contact names, so it spells them (heard as "Colpria" without it). Names only:
# Whisper can repeat its prompt on noise, and a hallucinated call still asks by name.
PROMPT = {"en": "Call " + ", ".join(latin for latin, _ in CONTACTS) + ".",
          "hi": ", ".join(deva for _, deva in CONTACTS) + " को कॉल करो।"}
SPEECH_DBFS = -26  # --noise starts against a typical speech level, then follows the speaker's measured level


def voice(text):
    return VOICE["hi" if re.search(r"[ऀ-ॿ]", text) else "en"]


def say_pcm(text):
    """16 kHz 16-bit PCM of `text` in a macOS voice, standing in for the user's speech."""
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        subprocess.run(["say", "-v", voice(text), "--file-format=WAVE", "--data-format=LEI16@16000",
                        "-o", f.name, text], check=True)
        with wave.open(f.name) as w:
            return w.readframes(w.getnframes())


def smart_turn():
    """Smart Turn v3 with Pipecat's bundled ONNX model. Its stop_secs counts silence after the VAD stop."""
    from pipecat.audio.turn.smart_turn.base_smart_turn import SmartTurnParams
    from pipecat.audio.turn.smart_turn.local_smart_turn_v3 import LocalSmartTurnAnalyzerV3

    return LocalSmartTurnAnalyzerV3(params=SmartTurnParams(stop_secs=round(MAX_WAIT - VAD_STOP["smart"], 3)))


def rnnoise():
    """Pipecat's RNNoise filter. Without pyrnnoise the filter passes noisy audio
    through and only logs an error, so fail here."""
    from pipecat.audio.filters import rnnoise_filter

    if rnnoise_filter.RNNoise is None:
        raise ImportError("--denoise needs pyrnnoise: uv sync")
    return rnnoise_filter.RNNoiseFilter()


def denoise(pcm, rate=IN_RATE):
    """16-bit PCM through the live filter, offline, in the transport's 20 ms frames. Five frames of
    silence at the end push out the 12 ms that the filter holds back."""
    async def run(f):
        await f.start(rate)
        frame = rate // 50 * 2
        audio = pcm + bytes(5 * frame)
        out = [await f.filter(audio[i:i + frame]) for i in range(0, len(audio), frame)]
        await f.stop()
        return b"".join(out)

    return asyncio.run(run(rnnoise()))


class Tee:
    """stdout to the terminal and the run log. It has no fileno, so input() writes its prompt here too."""

    def __init__(self, *streams):
        self.streams = streams

    def write(self, s):
        for stream in self.streams:
            stream.write(s)
            stream.flush()
        return len(s)

    def flush(self):
        for stream in self.streams:
            stream.flush()

    def isatty(self):
        return self.streams[0].isatty()


def open_log(argv, logs=LOGS):
    """A new log per run, with logs/latest.log pointing at it. Prints, Pipecat's loguru lines, stdlib
    warnings and the final traceback go to one line-buffered file, in time order, as they happen."""
    from loguru import logger

    logs.mkdir(exist_ok=True)
    path = logs / time.strftime("run-%Y%m%d-%H%M%S.log")
    f = path.open("a", buffering=1, encoding="utf-8")
    f.write(f"# {shlex.join(argv)}\n")
    (logs / "latest.log").unlink(missing_ok=True)
    (logs / "latest.log").symlink_to(path.name)
    logger.add(f, level="DEBUG")
    logging.basicConfig(level=logging.WARNING, handlers=[logging.StreamHandler(), logging.StreamHandler(f)])
    hook = sys.excepthook
    sys.excepthook = lambda *e: (traceback.print_exception(*e, file=f), hook(*e))
    sys.stdout = Tee(sys.stdout, f)
    return f


def show(reply, d, ms):
    if d:
        print(f"  [{d.route} · {d.intent} · {d.source} {d.score:.2f} · router {ms:.0f} ms]")
    print(f"buddy> {reply}")


def show_cloud(live, action):
    if live and live.ms:
        print(f"  [live · {LIVE_MODEL} · " + " · ".join(f"{k} {v} ms" for k, v in live.ms.items()) + "]")
    if action:
        print(f"  [cloud asked for {action[0]}({action[1]}); the phone confirms]")


async def run_text(buddy, cloud, log):
    import pyaudio

    out = pyaudio.PyAudio().open(format=pyaudio.paInt16, channels=1, rate=OUT_RATE, output=True)

    async def play(chunk):
        await asyncio.to_thread(out.write, chunk)

    while True:
        try:
            text = (await asyncio.to_thread(input, "you> ")).strip()
        except EOFError:
            return
        log.write(text + "\n")  # the terminal echoes what the user types; the log needs it written
        # The wake opens the session, so connecting and seeding overlap the "speech" below.
        live = LiveTurn(buddy.log) if cloud == "live" and buddy.online else None
        pcm = await asyncio.to_thread(say_pcm, text) if live else None
        t0 = time.perf_counter()
        reply = await asyncio.to_thread(buddy.handle, text)
        ms = (time.perf_counter() - t0) * 1000
        if reply is None:
            reply, action, _ = await escalate(buddy.log, text, live, pcm, play)
            reply = buddy.from_cloud(text, reply, action)
            show_cloud(live, action)
        elif live:
            live.drop()
        show(reply, buddy.last, ms)


async def run_live(buddy, language, cloud, whisper, endpoint, audio_filter, snr, log):
    from loguru import logger
    from pipecat.audio.vad.silero import SileroVADAnalyzer
    from pipecat.audio.vad.vad_analyzer import VADParams
    from pipecat.frames.frames import (Frame, InputAudioRawFrame, OutputAudioRawFrame, TranscriptionFrame,
                                       VADUserStoppedSpeakingFrame)
    from pipecat.pipeline.pipeline import Pipeline
    from pipecat.pipeline.worker import PipelineWorker
    from pipecat.processors.audio.vad_processor import VADProcessor
    from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
    from pipecat.services.whisper.stt import WhisperSTTServiceMLX
    from pipecat.transcriptions.language import Language
    from pipecat.transports.local.audio import LocalAudioTransport, LocalAudioTransportParams
    from pipecat.turns.user_start import VADUserTurnStartStrategy
    from pipecat.turns.user_stop import SpeechTimeoutUserTurnStopStrategy, TurnAnalyzerUserTurnStopStrategy
    from pipecat.turns.user_turn_processor import UserTurnProcessor
    from pipecat.turns.user_turn_strategies import UserTurnStrategies
    from pipecat.utils.time import time_now_iso8601
    from pipecat.workers.runner import WorkerRunner

    class Mic(FrameProcessor):
        """The glass's audio path, before VAD: optional pink noise, then RNNoise, then a mute while Buddy
        speaks. The laptop has no echo cancellation, so without the mute Whisper transcribes Buddy's own
        replies as user turns. The cost is no barge-in, which this prototype does not support anyway."""

        def __init__(self, audio_filter, snr):
            super().__init__()
            self.filter, self.until, self.started = audio_filter, 0.0, False
            self.levels = []  # (time, mean power of the clean 20 ms frame), for the measured SNR
            self.noise = self.noise_power = None
            self.target = snr
            if snr is not None:
                rng = np.random.default_rng(0)
                spectrum = np.fft.rfft(rng.standard_normal(10 * IN_RATE))
                spectrum /= np.sqrt(np.arange(1, len(spectrum) + 1))
                noise = np.fft.irfft(spectrum, 10 * IN_RATE)
                self.noise_power = (32768 * 10 ** (SPEECH_DBFS / 20)) ** 2 / 10 ** (snr / 10)
                self.noise = noise * np.sqrt(self.noise_power / np.mean(noise ** 2))
                self.at = 0

        async def process_frame(self, frame: Frame, direction: FrameDirection):
            await super().process_frame(frame, direction)
            if isinstance(frame, InputAudioRawFrame):
                x = np.frombuffer(frame.audio, np.int16).astype(np.float32)
                self.levels = self.levels[-1500:] + [(time.perf_counter(), float(np.mean(x ** 2)))]
                if self.noise is not None:
                    i = (self.at + np.arange(len(x))) % len(self.noise)
                    self.at = (self.at + len(x)) % len(self.noise)
                    x = x + self.noise[i]
                audio = np.clip(x, -32768, 32767).astype(np.int16).tobytes()
                if self.filter:
                    if not self.started:
                        await self.filter.start(IN_RATE)
                        self.started = True
                    audio = await self.filter.filter(audio)
                if time.perf_counter() < self.until:
                    audio = bytes(len(audio))
                frame.audio = audio
            await self.push_frame(frame, direction)

        def snr(self, t0, t1):
            """Measured SNR of the speech between t0 and t1 against the added noise, or None."""
            p = [x for t, x in self.levels if t0 <= t <= t1]
            if self.noise is None or not p:
                return None
            measured = 10 * np.log10(max(np.mean(p), 1.0) / self.noise_power)
            # Voices and mic distances differ, so the noise follows the speaker: the next turn gets the target SNR.
            gain = 10 ** ((measured - self.target) / 20)
            self.noise, self.noise_power = self.noise * gain, self.noise_power * gain ** 2
            return measured

    class Whisper(WhisperSTTServiceMLX):
        """Pipecat's MLX Whisper with the contact-name prompt. It runs once per VAD segment, in order, and
        keeps each segment's text (empty too), so a turn can collect exactly its own segments."""

        def __init__(self, prompt, **kw):
            super().__init__(**kw)
            self.prompt, self.results = prompt, []

        async def run_stt(self, audio: bytes):
            import mlx_whisper

            x = np.frombuffer(audio, np.int16).astype(np.float32) / 32768
            r = await asyncio.to_thread(mlx_whisper.transcribe, x, path_or_hf_repo=self._settings.model,
                                        temperature=0.0, language=self._settings.language,
                                        initial_prompt=self.prompt)
            text = " ".join(seg["text"].strip() for seg in r["segments"] if seg["no_speech_prob"] < 0.6).strip()
            self.results.append(text)
            if not text:
                return
            logger.debug(f"Transcription: [{text}]")
            yield TranscriptionFrame(text, self._user_id, time_now_iso8601(), self._settings.language)

    class BuddyProcessor(UserTurnProcessor):
        """Buffers each turn, routes its transcript, and either speaks a local reply or hands the
        buffered audio to the cloud. The turn strategy decides when the turn ends.

        A turn may hold several VAD segments. Whisper keeps one result per segment, and the turn joins
        the results of its own segments."""

        def __init__(self, stop):
            # No barge-in here. Whisper can take 5 s after a VAD stop, the default turn timeout.
            super().__init__(user_turn_strategies=UserTurnStrategies(
                start=[VADUserTurnStartStrategy(enable_interruptions=False)], stop=[stop]),
                user_turn_stop_timeout=10)
            self.add_event_handler("on_user_turn_started", self.started)
            self.add_event_handler("on_user_turn_stopped", self.stopped)
            self.end_of_speech = self.turn_start = time.perf_counter()
            self.stops = self.first = 0  # VAD segments so far, and the first segment of this turn
            self.preroll = b""  # VAD fires about 200 ms into speech, so keep the last 500 ms
            self.utterance = None  # audio of the current turn, from its buffered start
            self.speech_end = 0  # chunks of the utterance up to the last VAD stop
            self.live = None

        async def process_frame(self, frame: Frame, direction: FrameDirection):
            if isinstance(frame, InputAudioRawFrame):
                if self.utterance is not None:
                    self.utterance.append(frame.audio)
                self.preroll = (self.preroll + frame.audio)[-IN_RATE:]
            elif isinstance(frame, VADUserStoppedSpeakingFrame):
                self.end_of_speech, self.speech_end = time.perf_counter(), len(self.utterance or [])
                self.stops += 1
            await super().process_frame(frame, direction)

        async def push_frame(self, frame: Frame, direction: FrameDirection = FrameDirection.DOWNSTREAM):
            if not isinstance(frame, InputAudioRawFrame):  # the mic audio stops here
                await super().push_frame(frame, direction)

        async def started(self, _, strategy):
            self.first, self.turn_start = self.stops, time.perf_counter()
            self.utterance = [self.preroll]
            if self.live:
                self.live.drop()
            # The wake: open and seed the cloud session while the user is still talking.
            self.live = LiveTurn(buddy.log) if cloud == "live" and buddy.online else None

        async def stopped(self, _, strategy):
            # The strategy ends the turn on the first transcript after Smart Turn says "complete". After a
            # pause, a later segment's transcript is still in Whisper, so wait for it (or give up after 5 s).
            # A new turn can start while this one waits, so take this turn's state first.
            first, last, end = self.first, self.stops, self.end_of_speech
            snr = mic.snr(self.turn_start - 0.5, end)
            pcm, self.utterance = b"".join((self.utterance or [])[:self.speech_end]), None
            live, self.live = self.live, None
            deadline = time.perf_counter() + 5
            while len(stt.results) < last and time.perf_counter() < deadline:
                await asyncio.sleep(0.02)
            text = " ".join(t for t in stt.results[first:last] if t)
            if not text:
                if live:
                    live.drop()
                return
            now = time.perf_counter()
            print(f"you> {text}   [turn end and ASR {(now - end) * 1000:.0f} ms after the VAD stop"
                  + (f" · SNR {snr:.0f} dB" if snr is not None else "") + "]")
            await self.turn(text, pcm, live)

        async def turn(self, text, pcm, live):
            now = time.perf_counter()
            reply = await asyncio.to_thread(buddy.handle, text)
            ms = (time.perf_counter() - now) * 1000
            if reply is None:
                reply, action, played = await escalate(buddy.log, text, live, pcm, self.play)
                reply = buddy.from_cloud(text, reply, action)
                show_cloud(live, action)
                if played and not action:
                    reply = None  # already heard in Gemini's voice
            elif live:
                live.drop()
            show(reply or buddy.log[-1][1], buddy.last, ms)
            await self.say(reply)

        async def play(self, chunk):
            await self.push_frame(OutputAudioRawFrame(audio=chunk, sample_rate=OUT_RATE, num_channels=1))
            start = max(time.perf_counter(), mic.until - 0.3)
            mic.until = start + len(chunk) / (2 * OUT_RATE) + 0.3

        async def say(self, reply):
            if not reply or reply.startswith("["):
                return
            mic.until = float("inf")
            proc = await asyncio.create_subprocess_exec("say", "-v", voice(reply), reply)

            async def done():
                await proc.wait()
                mic.until = time.perf_counter() + 0.3

            asyncio.create_task(done())

    transport = LocalAudioTransport(LocalAudioTransportParams(
        audio_in_enabled=True, audio_in_sample_rate=IN_RATE, audio_out_enabled=True, audio_out_sample_rate=OUT_RATE))
    mic = Mic(audio_filter, snr)  # VAD, Smart Turn, Whisper and the cloud all get its output
    # Smart Turn decides at each VAD stop; with no "complete", the turn ends at MAX_WAIT of silence.
    stop = (TurnAnalyzerUserTurnStopStrategy(turn_analyzer=smart_turn()) if endpoint == "smart"
            else SpeechTimeoutUserTurnStopStrategy(user_speech_timeout=0))
    vad = VADProcessor(vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=VAD_STOP[endpoint])))
    stt = Whisper(PROMPT.get(language), settings=WhisperSTTServiceMLX.Settings(
        model=whisper, language=Language(language) if language else None))
    import mlx_whisper
    mlx_whisper.transcribe(np.zeros(IN_RATE, np.float32), path_or_hf_repo=whisper)  # the first call is about 5 s slower
    pipeline = Pipeline([transport.input(), mic, vad, stt, BuddyProcessor(stop), transport.output()])
    extras = [x for x, on in [("RNNoise", audio_filter), (f"pink noise at about {snr} dB SNR", snr is not None)] if on]
    print(f"Listening{' with ' + ' and '.join(extras) if extras else ''}. The mic is muted while Buddy speaks. "
          f"Log: {os.path.relpath(log.name)}")
    print("Try “what time is it”, “take a photo”, “Priya ko call karo”, or any question.")
    runner = WorkerRunner()
    await runner.add_workers(PipelineWorker(pipeline, cancel_on_idle_timeout=False))
    await runner.run()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--text", action="store_true", help="type turns instead of using the microphone")
    ap.add_argument("--cloud", choices=["text", "live"], default=None,
                    help="live (the default with GEMINI_API_KEY): Gemini Live native audio; text: Gemini text cascade")
    ap.add_argument("--offline", action="store_true", help="no cloud model")
    ap.add_argument("--language", default=None, help="fix Whisper's language (en or hi); default detects")
    ap.add_argument("--endpoint", choices=VAD_STOP, default="smart",
                    help="smart: Silero VAD with Smart Turn v3 and a 600 ms maximum wait; fixed: one 400 ms wait")
    ap.add_argument("--whisper", choices=WHISPER, default="turbo",
                    help="turbo is what eval.py measures; small is about 5x faster on a laptop, weaker in Hindi")
    ap.add_argument("--denoise", action=argparse.BooleanOptionalAction, default=True,
                    help="RNNoise on the microphone input (live mode only)")
    ap.add_argument("--noise", type=float, default=None, metavar="SNR_DB",
                    help="mix pink noise into the microphone at about this SNR in dB (live mode only)")
    args = ap.parse_args()
    args.cloud = args.cloud or ("live" if api_key() else "text")
    if args.cloud == "live" and not api_key():
        sys.exit("--cloud live needs GEMINI_API_KEY")
    log = open_log(["app.py", *sys.argv[1:]])
    buddy = Buddy(online=not args.offline)
    if args.text:
        print(f"Log: {os.path.relpath(log.name)}")
        asyncio.run(run_text(buddy, args.cloud, log))
    else:
        asyncio.run(run_live(buddy, args.language, args.cloud, WHISPER[args.whisper], args.endpoint,
                             rnnoise() if args.denoise else None, args.noise, log))


if __name__ == "__main__":
    main()
