# tiered-voice

A prototype of a voice assistant, Buddy, that splits each turn across three tiers.

- **Tier 0, glasses.** Wake word and a few fixed commands. Here the laptop microphone stands in for the glasses, and every utterance counts as a wake.
- **Tier 1, phone.** Silero VAD, Smart Turn v3 endpointing, Whisper ASR, and an intent router. The router answers simple requests on the device: the time, take a photo, call a contact. Here the laptop stands in for the phone.
- **Tier 2, cloud.** Everything else goes to Gemini, either Gemini Live native audio or a text cascaded pipeline. Both get the same text log of earlier turns from every tier. A call or photo that the cloud asks for is always confirmed on the phone first.

Photos and calls are mocked.

## Setup

You need macOS on Apple Silicon (Whisper runs on MLX, and replies use the `say` voices) and [uv](https://docs.astral.sh/uv/).

```sh
uv sync
export GEMINI_API_KEY=...   # in your shell, never in a file here
```

The first run downloads Whisper large-v3-turbo (about 1.6 GB) and a multilingual MiniLM model for the router (about 0.5 GB).

## Run it

```sh
uv run app.py --language en               # or hi
uv run app.py --language en --noise 10    # pink noise in the mic at about 10 dB SNR
```

With `GEMINI_API_KEY` set, the cloud tier is Gemini Live. Without it, cloud turns only print what they would send. RNNoise cleans the mic input in both commands. `uv run app.py --help` lists the other options.

Wait for Buddy to finish speaking before you talk. There is no echo cancellation, so the microphone is muted while Buddy speaks.

Latency here does not represent a phone. Whisper large-v3-turbo runs after the end of speech and takes about 3 s per turn on a laptop. A phone build would use streaming ASR.

## Logs

Each run of `app.py` writes `logs/run-YYYYmmdd-HHMMSS.log`, and `logs/latest.log` points to the newest one. The log has the command line, every turn, and Pipecat's DEBUG lines.

A spoken turn prints two lines:

```
you> take a photo   [turn end and ASR 3120 ms after the VAD stop · SNR 11 dB]
  [local · take_photo · grammar 1.00 · router 4 ms]
buddy> Photo taken.
```

The first line gives the transcript, the time from the VAD stop to the transcript, and the measured SNR when `--noise` is on. The second line gives the route (`local`, `ask`, `cloud` or `offline`), the intent, the source of the decision (`grammar`, `classifier` or `banned`), its score, and the router time.

## Eval

`eval.py` tests the router on 262 sentences that it never saw in training, in English, Hindi and Hinglish. With `--audio`, it also speaks them with macOS voices, adds pink noise at three levels (office 25 dB, street 15 dB and auto-rickshaw 5 dB SNR), and runs Whisper on the raw audio and after RNNoise. Full results are in [`results/eval.md`](results/eval.md).

- On typed text, call recall is 70% in English and 88% in Hindi. 2 of 79 English photo or call actions that ran locally were wrong, and 0 of 76 in Hindi.
- On clean synthetic speech, call recall is 46% in English and 54% in Hindi. On raw audio with street noise, it is 41% and 51%. With auto-rickshaw noise, it is 26% and 24%.
- RNNoise before Whisper raised the word error rate in every noisy profile, by 17% to 58%. It helped a little only on clean English. It did not add wrong local actions.
- Wrong local actions stay rare, because an unsure command goes to the cloud.
- The sets are too small to show a 99.5% target for sensitive actions. That needs about 600 clean decisions per language.
- The voices are synthetic and the noise is static pink noise, so the speech results only check that the pipeline works. They do not predict accuracy for real users, which needs real recordings from the glasses.
