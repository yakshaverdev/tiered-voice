"""Labelled utterances for the router, written by us.

Train and test use different templates and different contact names, so the
test numbers measure phrasing the classifier has not seen. Real labels come
later from Gemini Live's tool choices on opt-in transcripts.
"""

import random

INTENTS = ["time", "take_photo", "call_contact", "other"]
SENSITIVE = {"take_photo", "call_contact"}

# (Latin, Devanagari). Train and test names do not overlap.
TRAIN_NAMES = [("Priya", "प्रिया"), ("Rahul", "राहुल"), ("Amit", "अमित"), ("Neha", "नेहा"),
               ("Rohan", "रोहन"), ("Sunita", "सुनीता"), ("Vikram", "विक्रम"), ("Anjali", "अंजलि"),
               ("Arjun", "अर्जुन"), ("Kavya", "काव्या")]
TEST_NAMES = [("Deepak", "दीपक"), ("Pooja", "पूजा"), ("Sanjay", "संजय"), ("Meera", "मीरा"),
              ("Karan", "करण"), ("Divya", "दिव्या"), ("Suresh", "सुरेश"), ("Ishaan", "ईशान"),
              ("Lakshmi", "लक्ष्मी"), ("Farhan", "फ़रहान")]
CONTACTS = TRAIN_NAMES + TEST_NAMES

# {n} is a Latin name, {d} a Devanagari one.
TEMPLATES = {
    "train": {
        "en": {
            "time": ["what time is it", "what's the time", "tell me the time", "time please",
                     "what time is it now", "do you know what time it is", "current time",
                     "what's the time right now", "could you tell me the time", "time check"],
            "take_photo": ["take a photo", "take a picture", "click a photo", "snap a picture",
                           "capture this", "take a pic", "photo please", "click a picture of this",
                           "take a quick photo", "grab a photo of this"],
            "call_contact": ["call {n}", "call {n} please", "phone {n}", "dial {n}", "ring {n}",
                             "give {n} a call", "make a call to {n}", "can you call {n}",
                             "place a call to {n}", "get {n} on the phone"],
            "other": ["what's the weather today", "tell me a joke", "who won the match yesterday",
                      "what am i looking at", "read this sign for me", "how far is the airport",
                      "translate this to hindi", "i called her yesterday", "that photo was great",
                      "what time does the shop close", "play some music", "ketchup", "gotcha",
                      "let's catch up later", "i'll call you back", "photos from the trip",
                      "what's the time difference with london", "take a break", "take a seat",
                      "call of duty is fun", "how do i take a good photo", "the call dropped",
                      "who called me", "describe what you see", "set an alarm for six",
                      "start meeting mode", "how long will it take to get there", "foto",
                      # A bare name is not a call request, so it goes to the cloud.
                      "priya", "rahul?", "amit", "haan priya", "neha ji", "rohan here"],
        },
        "hi": {
            "time": ["time kya hua hai", "kitne baje hain", "abhi kitne baje hain", "time batao",
                     "samay kya hai", "kya time ho raha hai", "टाइम क्या हुआ", "कितने बजे हैं",
                     "समय बताओ", "अभी क्या टाइम है"],
            "take_photo": ["photo lo", "photo khincho", "ek photo lo", "photo le lo", "tasveer lo",
                           "picture lo", "फोटो लो", "एक फोटो खींचो", "तस्वीर लो", "फोटो ले लो"],
            "call_contact": ["{n} ko call karo", "{n} ko phone karo", "{n} ko phone lagao",
                             "{n} ko call lagao", "{n} se baat karao", "{d} को कॉल करो",
                             "{d} को फोन लगाओ", "{d} को फ़ोन करो"],
            "other": ["mausam kaisa hai", "ek joke sunao", "ye kya hai", "maine kal photo dekhi",
                      "usne mujhe call kiya tha", "time nahi hai mere paas", "photo bahut acchi hai",
                      "मौसम कैसा है", "ये क्या है", "मैंने कल फोटो देखी", "कोई गाना बजाओ",
                      "dukaan kitne baje band hoti hai", "gocha", "call center ka number kya hai",
                      "kal ki meeting kab hai", "ye board padh ke batao", "airport kitni door hai",
                      "हिंदी में अनुवाद करो", "photo wali dukaan kahan hai", "उसने फोटो भेजी थी",
                      "प्रिया", "राहुल?", "haan amit", "हाँ नेहा", "arjun ji", "kavya"],
        },
    },
    "test": {
        "en": {
            "time": ["what is the time", "give me the time", "can you check the time",
                     "tell me what time it is", "what's the current time",
                     "hey what time is it right now", "time now", "what time is it at the moment",
                     "any idea what time it is", "what's the time now please"],
            "take_photo": ["take a photograph", "snap a photo", "shoot a picture", "capture a photo",
                           "click this", "get a picture of this", "take one picture",
                           "picture please", "can you take a photo", "take a snap"],
            "call_contact": ["call up {n}", "please call {n}", "connect me to {n}",
                             "i want to call {n}", "start a call with {n}", "ring up {n}",
                             "dial {n} for me", "call {n} now", "could you phone {n}",
                             "put me through to {n}"],
            "other": ["how's the weather in delhi", "what's this building", "tell me something interesting",
                      "how much is a cab to the station", "what does this menu say",
                      "she took a photo of me", "what time zone is tokyo in", "time flies",
                      "call me maybe is a song", "can you see this", "ketchup please", "picture this",
                      "who is calling", "take it easy", "how long is the movie",
                      "summarise my meeting", "what's a good camera phone", "the photo is blurry",
                      "i missed a call", "what's the capital of france", "is it time to leave",
                      "how do i reach the metro", "remind me to buy milk", "photo"],
        },
        "hi": {
            "time": ["kitna time hua", "time kya ho gaya", "abhi time kya hai", "zara time batana",
                     "kitne baj gaye", "क्या टाइम हो गया", "कितना बजा है", "ज़रा समय बताओ",
                     "टाइम बताना", "अभी कितने बज रहे हैं"],
            "take_photo": ["ek photo khinch do", "photo click karo", "jaldi photo lo", "iski photo lo",
                           "tasveer khincho", "फोटो खींच दो", "एक तस्वीर लो", "इसकी फोटो लो",
                           "फोटो क्लिक करो", "जल्दी फोटो लो"],
            "call_contact": ["{n} ko ring karo", "zara {n} ko call kar do", "{n} ko phone kar do",
                             "{n} ko dial karo", "{d} को कॉल कर दो", "{d} को फोन कर दो",
                             "ज़रा {d} को कॉल लगाओ", "{d} से बात कराओ"],
            "other": ["aaj baarish hogi kya", "kuch interesting batao", "ye building kaunsi hai",
                      "usne photo bheji thi", "kisne call kiya tha", "time pass kar raha hoon",
                      "photo frame kahan milega", "आज बारिश होगी क्या", "ये किसकी फोटो है",
                      "मुझे किसने फोन किया", "station kitna door hai", "menu padh ke batao",
                      "ketchup lao", "समय बहुत कम है", "कॉल ड्रॉप हो गई", "mera din kaisa tha",
                      "foto", "kal kitne baje uthna hai"],
        },
    },
}


def expand(split, per_intent=None, seed=0):
    """Rows of {text, intent, lang}. With per_intent, sample that many per intent and language."""
    names = TRAIN_NAMES if split == "train" else TEST_NAMES
    rng = random.Random(seed)
    rows = []
    for lang, by_intent in TEMPLATES[split].items():
        for intent, templates in by_intent.items():
            if intent == "call_contact":
                texts = [t.format(n=n, d=d) for t in templates for n, d in names]
            else:
                texts = list(templates)
            if per_intent and len(texts) > per_intent:
                texts = rng.sample(texts, per_intent)
            rows += [{"text": t, "intent": intent, "lang": lang} for t in texts]
    return rows
