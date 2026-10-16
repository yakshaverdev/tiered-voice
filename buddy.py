"""Turn handling on the phone: local tools, confirmations and template replies. Cloud turns go to cloud.py."""

import logging
import re
import time
from datetime import datetime
from typing import NamedTuple

from router import Route, Router, normalise, resolve_contact

log = logging.getLogger(__name__)

YES = {"yes", "yeah", "yep", "sure", "ok", "okay", "haan", "han", "ha", "haanji", "ji", "हाँ", "हां", "हा", "जी"}
NO = {"no", "nope", "cancel", "nahi", "nahin", "mat", "नहीं", "मत"}
HINDI_WORDS = {"kya", "hai", "hain", "karo", "lo", "ko", "baje", "batao", "kitne", "abhi", "ek",
               "khincho", "lagao", "kar", "do", "hua", "se", "zara", "jara", "iski", "jaldi"}

REPLY = {
    "time": {"en": "It's {t}.", "hi": "अभी {h} बजकर {m} मिनट हुए हैं।"},
    "photo_done": {"en": "Photo taken.", "hi": "फोटो ले ली।"},
    "photo_ask": {"en": "Take a photo?", "hi": "फोटो लूँ?"},
    "call_ask": {"en": "Call {name}?", "hi": "{name} को कॉल करूँ?"},
    "call_done": {"en": "Calling {name}.", "hi": "{name} को कॉल लग रही है।"},
    "no_name": {"en": "I didn't catch the name.", "hi": "नाम समझ नहीं आया।"},
    "cancelled": {"en": "Okay, cancelled.", "hi": "ठीक है, रद्द कर दिया।"},
    "offline": {"en": "I need the internet for that.", "hi": "इसके लिए इंटरनेट चाहिए।"},
    "unknown_tool": {"en": "I can't do that yet.", "hi": "यह अभी नहीं हो सकता।"},
}


class Pending(NamedTuple):
    """An action Buddy has asked about once, waiting for yes or no."""
    intent: str
    contact: str | None
    lang: str


def lang_of(text):
    if re.search(r"[ऀ-ॿ]", text):
        return "hi"
    return "hi" if HINDI_WORDS & set(normalise(text).split()) else "en"


def take_photo():
    print(f"  [tool] take_photo -> photo_{int(time.time())}.jpg (mocked)")


def initiate_call(name):
    print(f"  [tool] initiate_call -> {name} (mocked)")


class Buddy:
    def __init__(self, router=None, online=True, now=datetime.now):
        self.router = router or Router()
        self.online, self.now = online, now
        self.log = []  # (role, text): the phone's one text log, for both tiers
        self.pending: Pending | None = None
        self.last = None  # Decision of the last turn, for logging

    def handle(self, text):
        """The reply, or None when the turn goes to the cloud. The caller then calls from_cloud()."""
        lang = lang_of(text)
        self.last = None
        reply = self._confirm(text) if self.pending else None
        if reply is None:
            reply = self._route(text, lang)
        if reply:  # an ignored turn ("") leaves no trace
            self.remember(text, reply)
        return reply

    def remember(self, text, reply):
        """Log a turn. An empty reply (Live audio with no transcript) logs the user's words only."""
        self.log += [("user", text)] + ([("model", reply)] if reply else [])

    def from_cloud(self, text, reply, action):
        """Record a cloud turn. `action` is a cloud.ToolCall or None. A tool call from the cloud
        never runs directly; the phone asks first."""
        lang = lang_of(text)
        if action and action.name == "initiate_call":
            contact = resolve_contact(action.args.get("name", ""))
            reply = self._ask("call_contact", contact, lang) if contact else REPLY["no_name"][lang]
        elif action and action.name == "take_photo":
            reply = self._ask("take_photo", None, lang)
        elif action:  # schema check: an unknown tool name never runs
            log.warning("cloud asked for unknown tool %r; rejected", action.name)
            reply = REPLY["unknown_tool"][lang]
        self.remember(text, reply)
        return reply

    def _ask(self, intent, contact, lang):
        self.pending = Pending(intent, contact, lang)
        if intent == "call_contact":
            return REPLY["call_ask"][lang].format(name=contact)
        return REPLY["photo_ask"][lang]

    def recent_contact(self):
        """The last contact named on either tier, so "call him" works after a cloud turn."""
        for _, text in reversed(self.log):
            if name := resolve_contact(text):
                return name
        return None

    def _confirm(self, text):
        words = set(normalise(text, fillers=()).split())
        pending, self.pending = self.pending, None  # Buddy asks once only
        if words & YES:
            return self._run(pending.intent, pending.contact, pending.lang)
        if words & NO:
            return REPLY["cancelled"][pending.lang]
        return None  # anything else is a new turn

    def _route(self, text, lang):
        d = self.last = self.router.decide(text, online=self.online)
        if d.route == Route.IGNORE:
            return ""
        if d.route == Route.OFFLINE:
            return REPLY["offline"][lang]
        if d.route == Route.CLOUD:
            return None
        if d.intent == "call_contact":  # calls always ask by name, so a wrong guess is caught
            contact = d.contact or self.recent_contact()
            if not contact:
                return REPLY["no_name"][lang]
            return self._ask(d.intent, contact, lang)
        if d.route == Route.ASK:
            return self._ask(d.intent, None, lang)
        return self._run(d.intent, d.contact, lang)

    def _run(self, intent, contact, lang):
        if intent == "time":
            now = self.now()
            h = now.hour % 12 or 12
            return REPLY["time"][lang].format(t=now.strftime("%-I:%M %p"), h=h, m=now.minute)
        if intent == "take_photo":
            take_photo()
            return REPLY["photo_done"][lang]
        initiate_call(contact)
        return REPLY["call_done"][lang].format(name=contact)
