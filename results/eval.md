# Router eval

Train 280 rows. Temperature 0.67, fitted on 5-fold held-out scores. Test 262 rows with templates and contact names the router never saw. Thresholds: {'take_photo': 0.95, 'call_contact': 0.95, 'time': 0.8}, floor 0.5. Online mode, so the gray zone goes to the cloud.

## Typed text

### Typed text, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 87.5% (7/8) | 70.0% (7/10) |
| call_contact | 100 | 98.6% (70/71) | 70.0% (70/100) |
| other | 24 | 38.9% (21/54) | 87.5% (21/24) |

Sensitive local decisions: 77/79 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: time flies, picture this.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 70 | 30 |
| other | 1 | 1 | 1 | 21 |

### Typed text, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 77.8% (7/9) | 70.0% (7/10) |
| take_photo | 10 | 100.0% (6/6) | 60.0% (6/10) |
| call_contact | 80 | 100.0% (70/70) | 87.5% (70/80) |
| other | 18 | 48.5% (16/33) | 88.9% (16/18) |

Sensitive local decisions: 76/76 correct, 0 wrong. With no failures in n=76, the 95% upper bound on the error rate is about 3/n = 3.9%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 8/10 stayed off the phone. Leaked: time pass kar raha hoon, समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 7 | 0 | 0 | 3 |
| take_photo | 0 | 6 | 0 | 4 |
| call_contact | 0 | 0 | 70 | 10 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 97.3% | 90.0% |
| 0.60 | 97.8% | 89.5% |
| 0.70 | 98.4% | 89.5% |
| 0.80 | 98.2% | 84.0% |
| 0.90 | 98.7% | 77.5% |
| 0.95 | 98.7% | 76.5% |
| 0.98 | 100.0% | 70.0% |
| 0.99 | 100.0% | 49.0% |

Misrouted:

- “click this” (take_photo) → other
- “take one picture” (take_photo) → other
- “take a snap” (take_photo) → other
- “connect me to Deepak” (call_contact) → other
- “connect me to Pooja” (call_contact) → other
- “connect me to Sanjay” (call_contact) → other
- “connect me to Meera” (call_contact) → other
- “connect me to Karan” (call_contact) → other
- “connect me to Divya” (call_contact) → other
- “connect me to Suresh” (call_contact) → other
- “connect me to Ishaan” (call_contact) → other
- “connect me to Lakshmi” (call_contact) → other
- “connect me to Farhan” (call_contact) → other
- “call Deepak now” (call_contact) → other
- “call Pooja now” (call_contact) → other
- “call Sanjay now” (call_contact) → other
- “call Meera now” (call_contact) → other
- “call Karan now” (call_contact) → other
- “call Divya now” (call_contact) → other
- “call Suresh now” (call_contact) → other
- “call Ishaan now” (call_contact) → other
- “call Lakshmi now” (call_contact) → other
- “call Farhan now” (call_contact) → other
- “put me through to Deepak” (call_contact) → other
- “put me through to Pooja” (call_contact) → other
- “put me through to Sanjay” (call_contact) → other
- “put me through to Meera” (call_contact) → other
- “put me through to Karan” (call_contact) → other
- “put me through to Divya” (call_contact) → other
- “put me through to Suresh” (call_contact) → other
- “put me through to Ishaan” (call_contact) → other
- “put me through to Lakshmi” (call_contact) → other
- “put me through to Farhan” (call_contact) → other
- “time flies” (other) → time
- “picture this” (other) → take_photo
- “who is calling” (other) → call_contact
- “zara time batana” (time) → other
- “kitne baj gaye” (time) → other
- “कितना बजा है” (time) → other
- “photo click karo” (take_photo) → other
- “jaldi photo lo” (take_photo) → other
- “iski photo lo” (take_photo) → other
- “tasveer khincho” (take_photo) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पूजा से बात कराओ” (call_contact) → other
- “संजय से बात कराओ” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करण से बात कराओ” (call_contact) → other
- “दिव्या से बात कराओ” (call_contact) → other
- “सुरेश से बात कराओ” (call_contact) → other
- “ईशान से बात कराओ” (call_contact) → other
- “लक्ष्मी से बात कराओ” (call_contact) → other
- “फ़रहान से बात कराओ” (call_contact) → other
- “time pass kar raha hoon” (other) → time
- “समय बहुत कम है” (other) → time

## Synthetic speech through Whisper, clean

### Synthetic speech through Whisper, clean, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 87.5% (7/8) | 70.0% (7/10) |
| call_contact | 100 | 97.9% (46/47) | 46.0% (46/100) |
| other | 24 | 26.9% (21/78) | 87.5% (21/24) |

Sensitive local decisions: 53/55 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: Time flies, Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 46 | 54 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, clean, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 71.4% (5/7) | 50.0% (5/10) |
| take_photo | 10 | 100.0% (4/4) | 40.0% (4/10) |
| call_contact | 80 | 100.0% (43/43) | 53.8% (43/80) |
| other | 18 | 25.0% (16/64) | 88.9% (16/18) |

Sensitive local decisions: 47/47 correct, 0 wrong. With no failures in n=47, the 95% upper bound on the error rate is about 3/n = 6.4%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 7/8 stayed off the phone. Leaked: समय बहुत कम है..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 5 | 0 | 0 | 5 |
| take_photo | 0 | 4 | 0 | 6 |
| call_contact | 0 | 0 | 43 | 37 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.7% | 71.5% |
| 0.60 | 96.6% | 70.0% |
| 0.70 | 97.2% | 69.0% |
| 0.80 | 97.0% | 65.0% |
| 0.90 | 98.2% | 55.0% |
| 0.95 | 98.0% | 50.0% |
| 0.98 | 100.0% | 43.0% |
| 0.99 | 100.0% | 38.5% |

Misrouted:

- “Click this.” (take_photo) → other
- “Take one picture” (take_photo) → other
- “take a snap” (take_photo) → other
- “Call up Mira.” (call_contact) → other
- “Call up Eshan.” (call_contact) → other
- “Please call Puja.” (call_contact) → other
- “Please call Ishan.” (call_contact) → other
- “Connect me to Deepak.” (call_contact) → other
- “Connect me to Pooja.” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to Mira.” (call_contact) → other
- “Connect me to current.” (call_contact) → other
- “Connect me to Divya.” (call_contact) → other
- “Connect me to Suresh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Farhan.” (call_contact) → other
- “Start a call with the puck.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Ringat Puja.” (call_contact) → other
- “Ring at Mira.” (call_contact) → other
- “Bring up current.” (call_contact) → other
- “Ringat Devya.” (call_contact) → other
- “Ring up Ishan.” (call_contact) → other
- “Ring at Lakshmi.” (call_contact) → other
- “Bring up Farhan.” (call_contact) → other
- “Dayal Pooja for me.” (call_contact) → other
- “Dayal Sanjay for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Di Valdivia for me.” (call_contact) → other
- “Dayal Suresh for me.” (call_contact) → other
- “Dial E-Shan for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call Pooja now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me now.” (call_contact) → other
- “Call Karan now.” (call_contact) → other
- “Call Divya now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call Ishan now.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Farhan now.” (call_contact) → other
- “Could you phone the puck?” (call_contact) → other
- “Could you phone Puja?” (call_contact) → other
- “Could you phone me, La?” (call_contact) → other
- “Put me through to the puck.” (call_contact) → other
- “Put me through to Puja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Put me through to Mira.” (call_contact) → other
- “Put me through two currents.” (call_contact) → other
- “Put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “कितने बजगे?” (time) → other
- “या का इम होगया.” (time) → other
- “कितना बजा है।” (time) → other
- “जरा समें बताव.” (time) → other
- “ताम बताना” (time) → other
- “Foto klickar och” (take_photo) → other
- “पेसा की फोटो लो.” (take_photo) → other
- “तस्वी उचिचों” (take_photo) → other
- “फो तो कि इच दो?” (take_photo) → other
- “एक तस्वेर लो.” (take_photo) → other
- “जल्दी फोतो लो” (take_photo) → other
- “फुरिंका रो?” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो.” (call_contact) → other
- “मीरा को रिंग करो.” (call_contact) → other
- “करन को रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंकारो” (call_contact) → other
- “इशान को रिंग करो.” (call_contact) → other
- “लक्ष्मी को रिंग करो.” (call_contact) → other
- “फरहान को रिंग करो” (call_contact) → other
- “जारा संजे को कॉल कर दो” (call_contact) → other
- “जारा इशान को कॉल कर डियो” (call_contact) → other
- “जारा फरहान को को” (call_contact) → other
- “संजे को फोन कर दो” (call_contact) → other
- “को फो फो न का दो” (call_contact) → other
- “संजे को DL करो.” (call_contact) → other
- “मेरा को कॉल कर दो” (call_contact) → other
- “लक्षमी को कॉल कर दो.” (call_contact) → other
- “संजे को फुन कर दो” (call_contact) → other
- “सुरिष को फून कर दो” (call_contact) → other
- “लक्षमी को फोन कर दो” (call_contact) → other
- “फर्हान को फोन कर दो” (call_contact) → other
- “जरा संजे को कॉल लगाओ” (call_contact) → other
- “जरा मेरा को कॉल लगाओ.” (call_contact) → other
- “जरा दिवाको को लगाव?” (call_contact) → other
- “जरा सुरेश को लगाव?” (call_contact) → other
- “जरा फर्हान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ.” (call_contact) → other
- “पूजा से बात कराओ।” (call_contact) → other
- “संजेजी बात कर आओ” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करंसी बात कराओ” (call_contact) → other
- “दिव्यासी बात कराव” (call_contact) → other
- “सुरिष सिबाद कराव” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लक्षमी से बात कराओ.” (call_contact) → other
- “फरहान से बात कराओ.” (call_contact) → other
- “टाइम पास कर रहा हूँ.” (other) → time
- “समय बहुत कम है.” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to Deepak.”
- “dial Deepak for me” → “Dial Deepak for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तस्वेर लो.”
- “Suresh ko dial karo” → “सुरेश को डायल करो.”
- “सुरेश से बात कराओ” → “सुरिष सिबाद कराव”

## Synthetic speech through Whisper, pink noise at 10 dB SNR

### Synthetic speech through Whisper, pink noise at 10 dB SNR, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 100.0% (6/6) | 60.0% (6/10) |
| call_contact | 100 | 97.5% (39/40) | 39.0% (39/100) |
| other | 24 | 25.3% (22/87) | 91.7% (22/24) |

Sensitive local decisions: 45/46 correct, 1 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/10 stayed off the phone. Leaked: Time flies..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 6 | 0 | 4 |
| call_contact | 0 | 0 | 39 | 61 |
| other | 1 | 0 | 1 | 22 |

### Synthetic speech through Whisper, pink noise at 10 dB SNR, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 66.7% (4/6) | 40.0% (4/10) |
| take_photo | 10 | 100.0% (1/1) | 10.0% (1/10) |
| call_contact | 80 | 100.0% (35/35) | 43.8% (35/80) |
| other | 18 | 21.1% (16/76) | 88.9% (16/18) |

Sensitive local decisions: 36/36 correct, 0 wrong. With no failures in n=36, the 95% upper bound on the error rate is about 3/n = 8.3%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 5/6 stayed off the phone. Leaked: समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 4 | 0 | 0 | 6 |
| take_photo | 0 | 1 | 0 | 9 |
| call_contact | 0 | 0 | 35 | 45 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.4% | 59.0% |
| 0.60 | 96.5% | 55.0% |
| 0.70 | 98.1% | 52.0% |
| 0.80 | 98.0% | 48.5% |
| 0.90 | 98.9% | 43.5% |
| 0.95 | 98.8% | 40.5% |
| 0.98 | 100.0% | 29.0% |
| 0.99 | 100.0% | 25.0% |

Misrouted:

- “Super picture.” (take_photo) → other
- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “take a snap.” (take_photo) → other
- “Call up D-Pack.” (call_contact) → other
- “Call up to Jack.” (call_contact) → other
- “Call us Mira.” (call_contact) → other
- “call up Surish.” (call_contact) → other
- “Call up Yishan.” (call_contact) → other
- “Please call me now.” (call_contact) → other
- “Please call Ishan.” (call_contact) → other
- “Connect me to the button.” (call_contact) → other
- “Connect me to Pooja.” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to me lah.” (call_contact) → other
- “Connect me to current.” (call_contact) → other
- “Connect me to Divya.” (call_contact) → other
- “Connect me to Suresh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Farhan.” (call_contact) → other
- “I want to call the pastor.” (call_contact) → other
- “I want to call Puja.” (call_contact) → other
- “I want to call Mila.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with Mira.” (call_contact) → other
- “Start a call with Tarhan.” (call_contact) → other
- “Ring out the bug.” (call_contact) → other
- “Ring of Puja.” (call_contact) → other
- “Ring Art Mira.” (call_contact) → other
- “Ring Art Current” (call_contact) → other
- “Ring of Divya” (call_contact) → other
- “Ringatsu Reis” (call_contact) → other
- “Ring at Ishan.” (call_contact) → other
- “Die all the path for me.” (call_contact) → other
- “Dial Puja for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Daival Divya for me.” (call_contact) → other
- “that I also raised for me.” (call_contact) → other
- “Dial E-Shan for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call to John now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me now.” (call_contact) → other
- “he's going to be this one.” (call_contact) → other
- “Call Divya now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call me Sean now.” (call_contact) → other
- “Call up me now.” (call_contact) → other
- “Call Sarhan now.” (call_contact) → other
- “Could you phone me back?” (call_contact) → other
- “Could you found the via?” (call_contact) → other
- “Could you found Lakshmi?” (call_contact) → other
- “Put me through too deep up.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “of me, too, too, me, l'ah.” (call_contact) → other
- “put me through to current” (call_contact) → other
- “put me through two divya.” (call_contact) → other
- “put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “Who is calling?” (other) → call_contact
- “ताइम क्या हो बैख” (time) → other
- “कि पनी बच्चिग” (time) → other
- “याग नाइन होगया” (time) → other
- “किपना बजा है।” (time) → other
- “ताइम बसाना.” (time) → other
- “अभी कितने बच रहे हैं।” (time) → other
- “एक फो तो कि निच्ट दो” (take_photo) → other
- “पोडो क्लिका रो” (take_photo) → other
- “वेसा की फोतो लो” (take_photo) → other
- “तस्वी उचिचों” (take_photo) → other
- “पोट पीजड़ दो” (take_photo) → other
- “एक तखी लूप” (take_photo) → other
- “इसकी फोतो लो” (take_photo) → other
- “पोटो फ्लिक करो” (take_photo) → other
- “जल्डी पो तो लो” (take_photo) → other
- “पुरीं करो” (call_contact) → other
- “पूजा को रिंकारो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रेंग करो” (call_contact) → other
- “कर आंको रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंग करो” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “Lakshmi Koren Karo” (call_contact) → other
- “फर्हान को विंग करो” (call_contact) → other
- “जार इशान को कॉल कर दियो” (call_contact) → other
- “साल अफाल हान को को” (call_contact) → other
- “बीपको पॉन का दो” (call_contact) → other
- “मीरा तो कोन का दो” (call_contact) → other
- “कोफोन का दो” (call_contact) → other
- “दिव्या को फोंका दो” (call_contact) → other
- “Lakshmiko Fonkado.” (call_contact) → other
- “संजे को डियल करो” (call_contact) → other
- “परहान को डियल करो” (call_contact) → other
- “दीपट को कॉल कर दो.” (call_contact) → other
- “दिवा कुल का दूप” (call_contact) → other
- “सुलिष को कोल का दो” (call_contact) → other
- “नक्षमी को कॉल कर दो” (call_contact) → other
- “बीपत को फोंका दो” (call_contact) → other
- “पुजा को फुम कदो” (call_contact) → other
- “संजय कुपून कर दूग” (call_contact) → other
- “मीरा को सों कदो” (call_contact) → other
- “कर रंको फों का दो” (call_contact) → other
- “इव्या कुपों का दूख” (call_contact) → other
- “सुलीश को फोंक दो” (call_contact) → other
- “लग्ष्मी को फोंका दो” (call_contact) → other
- “पर्षान को सून कर दो” (call_contact) → other
- “जर जिवाकु को अल लगाओ” (call_contact) → other
- “जर असुरीश को प्कोल लगाव” (call_contact) → other
- “जरा लग्ष्मीको को लगाव” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पुजास दिबात कराओ।” (call_contact) → other
- “संजे सी बात कराओ” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करन्सी बात कराओ” (call_contact) → other
- “इवाज इबाज कराओ” (call_contact) → other
- “शुरिष प्रिवाग कराओ” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लगश्मी से बात कराओ.” (call_contact) → other
- “फरहान सी बात कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to the button.”
- “dial Deepak for me” → “Die all the path for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तखी लूप”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “शुरिष प्रिवाग कराओ”

## Synthetic speech through Whisper, pink noise at 0 dB SNR

### Synthetic speech through Whisper, pink noise at 0 dB SNR, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 100.0% (9/9) | 90.0% (9/10) |
| take_photo | 10 | 80.0% (4/5) | 40.0% (4/10) |
| call_contact | 100 | 100.0% (12/12) | 12.0% (12/100) |
| other | 24 | 19.5% (23/118) | 95.8% (23/24) |

Sensitive local decisions: 16/17 correct, 1 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 8/9 stayed off the phone. Leaked: picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 9 | 0 | 0 | 1 |
| take_photo | 0 | 4 | 0 | 6 |
| call_contact | 0 | 0 | 12 | 88 |
| other | 0 | 1 | 0 | 23 |

### Synthetic speech through Whisper, pink noise at 0 dB SNR, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 50.0% (1/2) | 10.0% (1/10) |
| take_photo | 10 | 100.0% (1/1) | 10.0% (1/10) |
| call_contact | 80 | 100.0% (7/7) | 8.8% (7/80) |
| other | 18 | 15.7% (17/108) | 94.4% (17/18) |

Sensitive local decisions: 8/8 correct, 0 wrong. With no failures in n=8, the 95% upper bound on the error rate is about 3/n = 37.5%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 2/3 stayed off the phone. Leaked: समय बहुत कम से.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 1 | 0 | 0 | 9 |
| take_photo | 0 | 1 | 0 | 9 |
| call_contact | 0 | 0 | 7 | 73 |
| other | 1 | 0 | 0 | 17 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 90.2% | 23.0% |
| 0.60 | 91.5% | 21.5% |
| 0.70 | 93.2% | 20.5% |
| 0.80 | 94.6% | 17.5% |
| 0.90 | 93.9% | 15.5% |
| 0.95 | 96.0% | 12.0% |
| 0.98 | 100.0% | 8.5% |
| 0.99 | 100.0% | 5.0% |

Misrouted:

- “Any idea what sign it is?” (time) → other
- “I think the photo of you are” (take_photo) → other
- “Not a fool” (take_photo) → other
- “Capture the food” (take_photo) → other
- “like this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “and I can't really think of the same one.” (take_photo) → other
- “So you have to eat up.” (call_contact) → other
- “All of you, John.” (call_contact) → other
- “Call up Sunday.” (call_contact) → other
- “So happy that.” (call_contact) → other
- “Call up seven.” (call_contact) → other
- “Hold up to it.” (call_contact) → other
- “T. T.” (call_contact) → other
- “on the back and back.” (call_contact) → other
- “So I have to go hard.” (call_contact) → other
- “Please call these artists.” (call_contact) → other
- “Please call to John.” (call_contact) → other
- “Please follow Sanjay.” (call_contact) → other
- “He's so young.” (call_contact) → other
- “and you can like to see the next one.” (call_contact) → other
- “people give ya” (call_contact) → other
- “Leave for Yishan.” (call_contact) → other
- “Please call Sarhan.” (call_contact) → other
- “to make me too big up.” (call_contact) → other
- “connect me to Uja” (call_contact) → other
- “connect me to some games.” (call_contact) → other
- “Connect me to me live.” (call_contact) → other
- “Connect me to a second.” (call_contact) → other
- “connected to the vehicle.” (call_contact) → other
- “Connect me to Isurayesh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Luxury” (call_contact) → other
- “Connect me to Salhan.” (call_contact) → other
- “I want to call you back.” (call_contact) → other
- “I want to call you John” (call_contact) → other
- “I want to call some game.” (call_contact) → other
- “I want to call me back.” (call_contact) → other
- “I want to call Vivian” (call_contact) → other
- “I want to phone Yishan” (call_contact) → other
- “start a call with two jobs” (call_contact) → other
- “start a call with me now.” (call_contact) → other
- “Start a call with Kevin” (call_contact) → other
- “start a call with India” (call_contact) → other
- “start at all with Suresh” (call_contact) → other
- “You are the first.” (call_contact) → other
- “Ring of Suja.” (call_contact) → other
- “Ring of Sanjay.” (call_contact) → other
- “Rengar Cunigar” (call_contact) → other
- “Ring art covering” (call_contact) → other
- “In Australia” (call_contact) → other
- “Bring up to it.” (call_contact) → other
- “Being a key sign.” (call_contact) → other
- “Bring out luxury.” (call_contact) → other
- “Ring at Salhan.” (call_contact) → other
- “Die will be past for me.” (call_contact) → other
- “Dying I can get for you” (call_contact) → other
- “Dylang Sanjay for me” (call_contact) → other
- “Dying on me not falling” (call_contact) → other
- “Dying on coming for me.” (call_contact) → other
- “guy will be here for me” (call_contact) → other
- “Don't you like to raise for me?” (call_contact) → other
- “That is the reason for me.” (call_contact) → other
- “Dying I left me for me.” (call_contact) → other
- “Dying on some hands for me.” (call_contact) → other
- “Call the tough now.” (call_contact) → other
- “So you can stand out.” (call_contact) → other
- “Go something now.” (call_contact) → other
- “Oh, you mean I know.” (call_contact) → other
- “I've only got a minute now.” (call_contact) → other
- “I'll give you an hour.” (call_contact) → other
- “Call police now.” (call_contact) → other
- “I'm going to be chan now.” (call_contact) → other
- “Call you up to me now.” (call_contact) → other
- “it's so much so” (call_contact) → other
- “to you for only doctor.” (call_contact) → other
- “Could you phone food up?” (call_contact) → other
- “Could you phone some day?” (call_contact) → other
- “Could you call me, ah?” (call_contact) → other
- “to use all the time.” (call_contact) → other
- “Could you call Vivian?” (call_contact) → other
- “to view from Suresh.” (call_contact) → other
- “Could you phone me, Sean?” (call_contact) → other
- “Could you call Luxembourg?” (call_contact) → other
- “Could you fall so high?” (call_contact) → other
- “Put me through to the party.” (call_contact) → other
- “It means you can continue the job.” (call_contact) → other
- “It's me too to someday” (call_contact) → other
- “with me, with me, with me, with me, with me,” (call_contact) → other
- “with me to be the other.” (call_contact) → other
- “with me to be here.” (call_contact) → other
- “It took me to the stage.” (call_contact) → other
- “It took me through to Ishan.” (call_contact) → other
- “Put me through to luxury.” (call_contact) → other
- “It took me to do something hard.” (call_contact) → other
- “picture this.” (other) → take_photo
- “विपना का इम हुआ” (time) → other
- “आइ जाओ गया” (time) → other
- “जरा काइन बताना” (time) → other
- “इपनी बाखिन” (time) → other
- “यह जगाइ जोगे हा” (time) → other
- “कितना बजा है।” (time) → other
- “जरा समय बचाल” (time) → other
- “काइं बचाना” (time) → other
- “अब ही ठिपने बच रहे हैं.” (time) → other
- “एक बोड़ बीटो जो” (take_photo) → other
- “पोटो प्लिक करो” (take_photo) → other
- “किसा की पो दो लो” (take_photo) → other
- “तस्यूपी चूब” (take_photo) → other
- “पोई लोग लो” (take_photo) → other
- “इसकी दो” (take_photo) → other
- “इपकी फोचलो” (take_photo) → other
- “पोचो खिख रूख रूख” (take_photo) → other
- “जल्वी पोचो लो” (take_photo) → other
- “पुरींपरो” (call_contact) → other
- “प्रिंजर खोगे इंटरो” (call_contact) → other
- “संदे को रिंग करो” (call_contact) → other
- “वी लाको बेंटरो” (call_contact) → other
- “कर दो दो दो दो” (call_contact) → other
- “विजया को रही चानो” (call_contact) → other
- “प्रेश को रेंगा लो” (call_contact) → other
- “निशान को रिल करो” (call_contact) → other
- “लग्ष्मी ओूवें करों” (call_contact) → other
- “परहान को विंकरो” (call_contact) → other
- “जा दिप पासको तो प्रावाँ जाओ” (call_contact) → other
- “जरा फूज अपोल का दो” (call_contact) → other
- “जारसंदे को कौन का दोगी” (call_contact) → other
- “जरा मिरा तो कंट दो” (call_contact) → other
- “जरा करन को को जड़ो” (call_contact) → other
- “ज़रा दिखिया तो कॉल कर दो” (call_contact) → other
- “जरा सुरेश को को जो” (call_contact) → other
- “जाय इशान को कॉल कर दियो” (call_contact) → other
- “जरा लट्षमी को ओो खाजो” (call_contact) → other
- “लान अपलान कुका” (call_contact) → other
- “इपको पूंटाओो” (call_contact) → other
- “फुजा तो पॉंका दो” (call_contact) → other
- “San Diego Pongka Do” (call_contact) → other
- “मिरा तो पूंता लो” (call_contact) → other
- “पो पुट अजो” (call_contact) → other
- “ते विवा को उन्तावा” (call_contact) → other
- “उरेश को पूंका दो” (call_contact) → other
- “इशान पूपन तरो” (call_contact) → other
- “लट्ष्मी को पूंट जो” (call_contact) → other
- “500 पूंका दो” (call_contact) → other
- “संजे को भी अंसरो” (call_contact) → other
- “इविवा को देल परो” (call_contact) → other
- “सुरेश को टायल करो” (call_contact) → other
- “पाहन को दिया लगरो” (call_contact) → other
- “इपक पुकों कर दो” (call_contact) → other
- “प्याज प्याज को जब दो” (call_contact) → other
- “या को जगो” (call_contact) → other
- “करन को कौन कर दो” (call_contact) → other
- “जिया कुछ चाल का दूट” (call_contact) → other
- “तुरिज पो झाल रुट रुट रुट” (call_contact) → other
- “इशान को कॉल का दूख” (call_contact) → other
- “लच्षी को को जड़ो” (call_contact) → other
- “वादान कुप और दूख वादा रूश रूब” (call_contact) → other
- “इपको को नगदो” (call_contact) → other
- “जुज पूफूं जड़ों जड़ों” (call_contact) → other
- “तंजे कुष्व कर दूँ” (call_contact) → other
- “मिरा को वो जगा यो” (call_contact) → other
- “करन कुपूं का दूट” (call_contact) → other
- “इवा कुष नच्ट रदू रदू” (call_contact) → other
- “वेश पुष्वान का दूख” (call_contact) → other
- “इशान कुछों का दूख” (call_contact) → other
- “नच्छी को फोंका दो” (call_contact) → other
- “पर्खान कुसून का जुख” (call_contact) → other
- “जरा दीपत को सौन नगाओ करें” (call_contact) → other
- “जरा पूचा कुछ को लगाओ” (call_contact) → other
- “जनक संजय को को लगाओ” (call_contact) → other
- “जड़ बीड़ पुग गजग जगो” (call_contact) → other
- “ज़रा करन को कॉल नगाओ” (call_contact) → other
- “जर दिल्या को अगाओ” (call_contact) → other
- “जरा तुरीश को जना गाओ” (call_contact) → other
- “जड़ा इशान को स्कॉई नगाओ” (call_contact) → other
- “बेरा नक्ष्मी को को नगाओ” (call_contact) → other
- “जरख बहान को को नगाओ” (call_contact) → other
- “इपस्पिवाट कराओ” (call_contact) → other
- “प्रुचा सिवाट पराओ” (call_contact) → other
- “संजें सी बाइग कर आओ” (call_contact) → other
- “मिरा कि वाज कराओ” (call_contact) → other
- “करन्स भाज कराओ” (call_contact) → other
- “जिल्यास इबाइ करा।” (call_contact) → other
- “प्रीष औिवाज करा।” (call_contact) → other
- “इशांसी वास कराओ” (call_contact) → other
- “लगष्मीजी वास कराओ” (call_contact) → other
- “वखान्जी वाग कराओ” (call_contact) → other
- “समय बहुत कम से” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “to make me too big up.”
- “dial Deepak for me” → “Die will be past for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “इसकी दो”
- “Suresh ko dial karo” → “सुरेश को टायल करो”
- “सुरेश से बात कराओ” → “प्रीष औिवाज करा।”
