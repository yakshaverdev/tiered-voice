"""Phone-side router: normalise, grammar match, classifier, else the cloud."""

import difflib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import joblib
import numpy as np

from data import CONTACTS, INTENTS, SENSITIVE

EMBEDDER = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
MODEL_PATH = Path(__file__).parent / "models" / "router.joblib"

# Starting thresholds: high for photo and call, which act in the world, lower for time,
# which only speaks. Below FLOOR nothing runs locally.
THRESHOLD = {"take_photo": 0.95, "call_contact": 0.95, "time": 0.80}
FLOOR = 0.50

FILLERS = {"um", "umm", "uh", "hmm", "er", "ah", "hey", "buddy", "ok", "okay", "arre", "yaar",
           "अरे", "यार"}


def normalise(text, fillers=FILLERS):
    """Lowercase, drop nuktas, punctuation and fillers. Both scripts survive as they are."""
    text = unicodedata.normalize("NFD", text.lower()).replace("़", "")
    text = unicodedata.normalize("NFC", text)
    text = re.sub(r"['’]", "", text)
    # By Unicode category, because \w drops Devanagari vowel signs.
    text = "".join(" " if unicodedata.category(c)[0] in "PS" else c for c in text)
    return " ".join(w for w in text.split() if w not in fillers)


# Closed list of fixed phrases. The whole utterance must match, so "maine kal photo dekhi" never does.
GRAMMAR = {normalise(p): intent for intent, phrases in {
    "time": ["what time is it", "what's the time", "time kya hua", "time kya hua hai",
             "kitne baje hain", "टाइम क्या हुआ", "कितने बजे हैं", "समय क्या हुआ"],
    "take_photo": ["take a photo", "take a picture", "photo lo", "photo khincho", "फोटो लो",
                   "फोटो खींचो"],
}.items() for p in phrases}

# Near-miss words never run locally, whatever the classifier says: ASR turns them into commands.
BANNED = {normalise(w) for w in ["foto", "ketchup", "gocha", "gotcha", "catch up", "फोटू"]}


def banned(norm):
    """True when any whole word or banned phrase of the turn is a near miss, so "take a foto" never fires."""
    return any(f" {w} " in f" {norm} " for w in BANNED)


def sounds(word):
    """A rough sound key, so ASR spellings of one name meet: Meera and Mira, Pooja and Puja, Ishaan and Ishan."""
    for a, b in (("ee", "i"), ("oo", "u"), ("w", "v")):
        word = word.replace(a, b)
    return re.sub(r"(.)\1+", r"\1", word)


# Sound key of each contact name, in both scripts, to its display name. Only resolve_contact reads it.
NAMES = {sounds(normalise(x)): latin for latin, deva in CONTACTS for x in (latin, deva)}
EXACT_NAMES = {normalise(x) for pair in CONTACTS for x in pair}


def mask_names(norm):
    """Swap exact contact names for one placeholder, so an unseen name does not move the embedding.

    Exact words only: a fuzzy or sound match here would let near misses look like calls.
    """
    return " ".join("someone" if w in EXACT_NAMES else w for w in norm.split())


@dataclass
class Decision:
    route: str  # local | ask | cloud | offline | ignore
    intent: str = "other"
    score: float = 0.0
    source: str = ""  # grammar | classifier
    contact: str | None = None
    probs: dict = field(default_factory=dict)


def resolve_contact(text):
    """Latin display name of the contact named in the text, or None.

    The contact lookup is the only place with fuzzy matching, because ASR spells names many ways.
    Callers run it only after the call intent is picked, and the call always confirms by name.
    """
    words = [sounds(w) for w in normalise(text).split()]
    for w in words:
        if w in NAMES:
            return NAMES[w]
    for w in words:
        # ponytail: sound key plus fuzzy match; a real phonetic index when the contact list is large.
        close = difflib.get_close_matches(w, NAMES, n=1, cutoff=0.85)
        if close:
            return NAMES[close[0]]
    return None


class Router:
    def __init__(self, path=MODEL_PATH):
        from sentence_transformers import SentenceTransformer

        saved = joblib.load(path)
        self.clf, self.temperature = saved["clf"], saved["temperature"]
        self.embedder = SentenceTransformer(EMBEDDER, device="cpu")

    def probs(self, texts):
        """Calibrated probabilities, columns in INTENTS order."""
        x = self.embedder.encode([mask_names(normalise(t)) for t in texts], normalize_embeddings=True)
        logits = self.clf.decision_function(x) / self.temperature
        p = np.exp(logits - logits.max(axis=1, keepdims=True))
        p /= p.sum(axis=1, keepdims=True)
        order = [list(self.clf.classes_).index(i) for i in INTENTS]
        return p[:, order]

    def decide(self, text, online=True, p=None):
        norm = normalise(text)
        if not norm:
            return Decision("ignore")
        if norm in GRAMMAR:
            return self._local(GRAMMAR[norm], 1.0, "grammar", text)
        if banned(norm):
            return Decision("cloud" if online else "offline", "other", 1.0, "banned")
        p = self.probs([text])[0] if p is None else p
        probs = dict(zip(INTENTS, p.round(3).tolist()))
        intent = INTENTS[int(p.argmax())]
        score = float(p.max())
        if intent == "other" or score < FLOOR:
            return Decision("cloud" if online else "offline", "other", score, "classifier", probs=probs)
        # Above 0.95 a calibrated score already implies a clear gap to the runner-up.
        if score >= THRESHOLD[intent]:
            d = self._local(intent, score, "classifier", text)
        elif online:
            d = Decision("cloud", intent, score, "classifier")
        elif intent in SENSITIVE:
            contact = resolve_contact(text) if intent == "call_contact" else None
            d = Decision("ask", intent, score, "classifier", contact)
        else:
            d = self._local(intent, score, "classifier", text)
        d.probs = probs
        return d

    @staticmethod
    def _local(intent, score, source, text):
        contact = resolve_contact(text) if intent == "call_contact" else None
        return Decision("local", intent, score, source, contact)


def train(rows, path=MODEL_PATH):
    """Logistic regression on frozen multilingual MiniLM embeddings, temperature fitted on held-out scores.

    Each row's held-out score comes from 5-fold cross-validation. A single 20% dev split had no
    errors on some seeds, which drove the temperature to its lower bound and every score to 1.
    """
    from scipy.optimize import minimize_scalar
    from sentence_transformers import SentenceTransformer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import StratifiedKFold, cross_val_predict

    embedder = SentenceTransformer(EMBEDDER, device="cpu")
    x = embedder.encode([mask_names(normalise(r["text"])) for r in rows], normalize_embeddings=True)
    labels = [r["intent"] for r in rows]
    model = lambda: LogisticRegression(C=10, max_iter=2000, class_weight="balanced")
    clf = model().fit(x, labels)

    folds = StratifiedKFold(5, shuffle=True, random_state=0).split(x, [r["intent"] + r["lang"] for r in rows])
    logits = cross_val_predict(model(), x, labels, cv=list(folds), method="decision_function")
    y = np.array([list(clf.classes_).index(i) for i in labels])

    def nll(t):
        z = logits / t
        z = z - z.max(axis=1, keepdims=True)
        return float(-(z[np.arange(len(y)), y] - np.log(np.exp(z).sum(axis=1))).mean())

    temperature = minimize_scalar(nll, bounds=(0.05, 20), method="bounded").x
    path.parent.mkdir(exist_ok=True)
    joblib.dump({"clf": clf, "temperature": temperature}, path)
    return temperature
