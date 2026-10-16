"""The rules that must not break. Run after `uv run eval.py` has trained the router: uv run pytest -q"""

import asyncio
import shutil
import sys
from datetime import datetime

import pytest

import cloud
from buddy import Buddy, Pending, lang_of
from cloud import ToolCall, escalate
from router import Route, Router, Source, mask_names, normalise, resolve_contact


@pytest.fixture(scope="module")
def router():
    return Router()


def buddy(router, online=True):
    return Buddy(router, online=online, now=lambda: datetime(2026, 10, 16, 16, 5))


def test_normalise_keeps_devanagari_and_drops_fillers():
    assert normalise("Hey Buddy, take a photo!") == "take a photo"
    assert normalise("ज़रा समय बताओ।") == "जरा समय बताओ"


def test_contacts_resolve_in_both_scripts():
    assert resolve_contact("call Deepak") == "Deepak"
    assert resolve_contact("दीपक को कॉल करो") == "Deepak"
    assert resolve_contact("अभी क्या टाइम है") is None


def test_fuzzy_names_only_inside_the_contact_lookup(router):
    assert resolve_contact("call Deepa") == "Deepak"  # close spelling, found by the lookup
    assert mask_names(normalise("call mira")) == "call mira"  # the intent path sees no sound match
    assert router.decide("priya").source == Source.CLASSIFIER  # a bare name is no grammar match
    b = buddy(router)
    assert b.from_cloud("call Deepa", "", ToolCall("initiate_call", {"name": "Deepa"})) == "Call Deepak?"
    assert b.handle("no") == "Okay, cancelled."


@pytest.mark.parametrize("text", ["foto", "ketchup", "gocha", "maine kal photo dekhi", "the call dropped",
                                  "foto khincho", "take a foto", "foto lo", "catch up with priya"])
def test_near_misses_never_run_locally(router, text):
    assert router.decide(text).route == Route.CLOUD
    assert router.decide(text, online=False).route == Route.OFFLINE


def test_grammar_match_runs_without_the_classifier(router):
    d = router.decide("Take a photo")
    assert (d.route, d.intent, d.source) == (Route.LOCAL, "take_photo", Source.GRAMMAR)
    assert router.decide("take a photo", online=False).route == Route.LOCAL


def test_time_uses_a_template_in_the_user_language(router):
    assert buddy(router).handle("what time is it") == "It's 4:05 PM."
    assert buddy(router).handle("टाइम क्या हुआ") == "अभी 4 बजकर 5 मिनट हुए हैं।"


def test_calls_always_ask_by_name_and_ask_once(router):
    b = buddy(router)
    assert b.handle("call Priya") == "Call Priya?"
    assert b.handle("yes") == "Calling Priya."
    assert b.handle("call Priya") == "Call Priya?"
    assert b.handle("no") == "Okay, cancelled."
    assert b.pending is None


def test_another_request_while_asking_drops_the_question(router):
    b = buddy(router)
    assert b.handle("call Priya") == "Call Priya?"
    assert b.handle("what time is it") == "It's 4:05 PM."  # a new turn, not an answer
    assert b.pending is None
    assert b.handle("yes") != "Calling Priya."  # nothing is pending, so "yes" calls no one


def test_offline_refuses_open_questions(router):
    assert buddy(router, online=False).handle("what's the capital of france") == "I need the internet for that."


def test_offline_gray_zone_asks_once(router, capsys):
    """A sensitive intent between FLOOR and its threshold goes to the cloud online, and asks first offline."""
    assert router.decide("photo").route == Route.CLOUD
    d = router.decide("photo", online=False)
    assert (d.route, d.intent) == (Route.ASK, "take_photo") and 0.5 <= d.score < 0.95, d
    b = buddy(router, online=False)
    assert b.handle("photo") == "Take a photo?"
    assert "[tool]" not in capsys.readouterr().out
    assert b.handle("yes") == "Photo taken."
    assert b.pending is None


def test_an_ignored_turn_leaves_no_log(router):
    b = buddy(router)
    assert b.handle("um.") == ""
    assert b.from_cloud("tell me a joke", "", None) == ""  # Live audio with no transcript
    assert b.log == [("user", "tell me a joke")]


def test_cloud_tool_calls_are_confirmed_on_the_phone(router):
    b = buddy(router)
    assert b.handle("Deepak said he'll be late. What should I tell him?") is None  # a cloud turn
    assert b.from_cloud("Deepak said he'll be late. What should I tell him?", "Tell him no worries.", None)
    assert b.recent_contact() == "Deepak"
    assert b.from_cloud("call him", "", ToolCall("initiate_call", {"name": "Deepak"})) == "Call Deepak?"
    assert b.handle("yes") == "Calling Deepak."
    assert b.from_cloud("call the plumber", "", ToolCall("initiate_call", {"name": "plumber"})) == "I didn't catch the name."
    assert b.pending is None
    assert [r for r, _ in b.log] == ["user", "model"] * 4


def test_a_cloud_photo_is_asked_not_taken(router, capsys):
    b = buddy(router)
    assert b.from_cloud("take a quick picture of this", "", ToolCall("take_photo", {})) == "Take a photo?"
    assert b.pending == Pending("take_photo", None, "en")
    assert "[tool]" not in capsys.readouterr().out


class StubLive:
    """The parts of cloud.LiveTurn that escalate() uses."""

    def __init__(self, error=None):
        self.out, self.error, self.transcript, self.action = asyncio.Queue(), error, "", None
        self.dropped = False
        if error:
            self.out.put_nowait(None)

    def escalate(self, pcm):
        pass

    def drop(self):
        self.dropped = True


@pytest.mark.parametrize("error", [RuntimeError("socket closed"), None])
def test_escalate_falls_back_to_the_text_cascade(monkeypatch, error):
    """A Live error, or no Live output within LIVE_TIMEOUT, gives the text cascade's reply."""
    monkeypatch.setattr(cloud, "ask_text", lambda log, text: ("From the text model.", None))
    monkeypatch.setattr(cloud, "api_key", lambda: "test")
    monkeypatch.setattr(cloud, "LIVE_TIMEOUT", 0.05)

    async def run():
        live = StubLive(error)
        return live, await escalate([], "hello", live, b"", lambda chunk: None)

    live, result = asyncio.run(run())
    assert result == ("From the text model.", None, False)
    assert live.dropped == (error is None)  # a timeout closes the session


def test_lang_of_hinglish():
    assert lang_of("Priya ko call karo") == "hi"
    assert lang_of("call Priya") == "en"


@pytest.mark.parametrize("text", ["deepak", "pooja?", "haan meera", "दीपक", "suresh ji"])
def test_a_bare_name_is_not_a_call(router, text):
    d = router.decide(text)
    assert not (d.route == Route.LOCAL and d.intent == "call_contact"), d


def test_call_and_a_name_is_a_local_call(router):
    assert router.decide("call priya").route == Route.LOCAL


def test_unknown_cloud_tools_are_rejected_and_logged(router, caplog):
    b = buddy(router)
    assert b.from_cloud("order a cab", "", ToolCall("book_cab", {"to": "airport"})) == "I can't do that yet."
    assert "book_cab" in caplog.text
    assert b.pending is None


def test_eval_gives_the_3_over_n_bound_only_with_no_failures():
    from eval import report

    rows = [{"text": "call deepak", "intent": "call_contact"}, {"text": "who is calling", "intent": "other"}]
    assert "3/n = " in "\n".join(report("t", rows, ["call_contact", "other"]))
    assert "3/n = " not in "\n".join(report("t", rows, ["call_contact", "call_contact"]))


def test_smart_turn_loads_offline_and_decides():
    """Smart Turn v3 on synthetic speech from `say`: it gives a decision at the VAD stop, and silence
    up to the maximum wait ends the turn anyway."""
    import asyncio
    from importlib.resources import files

    from app import MAX_WAIT, VAD_STOP, say_pcm, smart_turn
    from pipecat.audio.turn.base_turn_analyzer import EndOfTurnState

    if not (files("pipecat.audio.turn.smart_turn.data") / "smart-turn-v3.2-cpu.onnx").is_file():
        pytest.skip("the bundled Smart Turn model is not installed")
    if not shutil.which("say"):
        pytest.skip("needs the macOS say command")
    analyzer = smart_turn()
    analyzer.set_sample_rate(16000)
    frame, silence = 640, bytes(640)  # 20 ms of 16-bit audio at 16 kHz
    speech = say_pcm("what time is it")
    for i in range(0, len(speech), frame):
        analyzer.append_audio(speech[i:i + frame], True)
    analyzer.append_audio(silence, False)  # the VAD has stopped
    state, result = asyncio.run(analyzer.analyze_end_of_turn())
    assert state in (EndOfTurnState.COMPLETE, EndOfTurnState.INCOMPLETE)
    assert 0 <= result.probability <= 1

    analyzer.append_audio(speech[-frame:], True)
    wait = round((MAX_WAIT - VAD_STOP["smart"]) * 50)  # 20 ms frames after the VAD stop
    states = [analyzer.append_audio(silence, False) for _ in range(wait)]
    assert states[-1] == EndOfTurnState.COMPLETE and EndOfTurnState.COMPLETE not in states[:-1]


def test_wer_counts_word_edits_after_normalise():
    from eval import wer

    assert wer([("Take a photo!", "take a photo")]) == 0
    assert wer([("call deepak now", "call deepa now")]) == pytest.approx(1 / 3)
    # two inserted words, then two dropped words, over four reference words
    assert wer([("call deepak", "please call deepak now"), ("time now", "")]) == pytest.approx(4 / 4)


def test_rnnoise_filter_runs_offline_on_say_audio():
    pytest.importorskip("pyrnnoise")
    if not shutil.which("say"):
        pytest.skip("needs the macOS say command")
    from app import denoise, say_pcm

    pcm = say_pcm("take a photo")
    out = denoise(pcm)
    assert len(pcm) <= len(out) <= len(pcm) + 3200 and out != pcm  # at most the 100 ms of flush silence more


def test_each_run_writes_its_own_log(tmp_path, monkeypatch):
    from loguru import logger

    from app import open_log

    monkeypatch.setattr(sys, "stdout", sys.stdout)
    monkeypatch.setattr(sys, "excepthook", sys.excepthook)
    open_log(["app.py", "--text"], tmp_path)
    print("buddy> hello")
    logger.debug("VAD stopped")
    lines = (tmp_path / "latest.log").read_text().splitlines()
    assert lines[0] == "# app.py --text" and lines[1] == "buddy> hello" and "VAD stopped" in lines[2]
