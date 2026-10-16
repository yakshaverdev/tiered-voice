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
uv run eval.py   # trains the router into models/router.joblib (about a minute); app.py and the tests need it
```

The first speech run downloads Whisper large-v3-turbo (about 1.6 GB). The router downloads a multilingual MiniLM model (about 0.5 GB) the first time it trains.

For the cloud tier, export `GEMINI_API_KEY` in your shell. Do not put it in a file in this folder. `GEMINI_LIVE_MODEL` and `GEMINI_MODEL` select the models. Without a key, a text cloud turn prints what it would send, and `--cloud live` and `handoff.py` refuse to start.

## Run it

| Scenario | Command |
|:--|:--|
| Typed turns, no microphone | `uv run app.py --text` |
| Typed turns, cloud in Gemini Live (`say` speaks each turn) | `uv run app.py --text --cloud live` |
| Speak, local turns only | `uv run app.py --offline` |
| Speak, cloud as a text cascaded pipeline | `uv run app.py --cloud text` |
| Speak, cloud in Gemini Live | `uv run app.py --cloud live` |
| Speak with pink noise at about 10 dB SNR | `uv run app.py --noise 10` |
| Same noise, with RNNoise on the input | `uv run app.py --noise 10 --denoise` |
| Faster ASR for a demo, language fixed | `uv run app.py --whisper small --language en` (or `hi`) |
| Fixed 400 ms endpoint in place of Smart Turn v3 | `uv run app.py --endpoint fixed` |
| Router eval on typed text | `uv run eval.py` |
| Router eval on synthetic noisy speech too (about an hour) | `uv run eval.py --audio` |
| Hand-off between tiers, both cloud modes (needs a key) | `uv run handoff.py` |
| Tests | `uv run pytest -q` |

`--noise` starts against a typical speech level. After the first turn, it follows the speaker's measured level, so later turns get the SNR you asked for.

Wait for Buddy to finish speaking before you talk. There is no echo cancellation and no barge-in, so the microphone is muted while Buddy speaks.

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

`eval.py` tests the router on 262 sentences that it never saw in training, in English, Hindi and Hinglish. With `--audio`, it also speaks them with macOS voices, adds pink noise, and runs Whisper on the raw and the denoised audio. Full results are in [`results/eval.md`](results/eval.md).

- On typed text, call recall is 70% in English and 88% in Hindi. 2 of 79 English photo or call actions that ran locally were wrong, and 0 of 76 in Hindi.
- On speech, recall drops as the noise rises, most of all in Hindi. Wrong local actions stay rare, because an unsure command goes to the cloud.
- The sets are too small to show a 99.5% target for sensitive actions. That needs about 600 clean decisions per language. All voices are synthetic, so the results say little about real users.
