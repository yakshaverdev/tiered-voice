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

## Synthetic speech through Whisper, raw and after RNNoise

Each sentence is spoken and noised once per profile; Whisper then runs on the raw audio and on the same audio through the live app's RNNoise filter. WER is word edits over reference words, after the router's normalise. Recall and decisions count every sentence of the language.

### Speech, en

| Profile | Audio | WER | WER change from RNNoise | Call recall | Photo recall | Time recall | Wrong photo or call run locally | Near misses kept off the phone |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| clean | raw | 9.2% |  | 46% | 70% | 100% | 2 of 55 | 9 of 11 |
| clean | RNNoise | 8.4% | -9% | 48% | 70% | 100% | 2 of 57 | 9 of 11 |
| office, pink noise at 25 dB SNR | raw | 9.1% |  | 52% | 70% | 100% | 2 of 61 | 9 of 11 |
| office, pink noise at 25 dB SNR | RNNoise | 10.6% | +17% | 43% | 70% | 100% | 2 of 52 | 9 of 11 |
| street, pink noise at 15 dB SNR | raw | 13.3% |  | 41% | 60% | 100% | 2 of 49 | 8 of 10 |
| street, pink noise at 15 dB SNR | RNNoise | 18.5% | +39% | 30% | 60% | 100% | 2 of 38 | 8 of 10 |
| auto-rickshaw, pink noise at 5 dB SNR | raw | 28.4% |  | 26% | 50% | 100% | 1 of 32 | 9 of 10 |
| auto-rickshaw, pink noise at 5 dB SNR | RNNoise | 35.3% | +24% | 20% | 50% | 100% | 2 of 27 | 6 of 8 |

### Speech, hi

| Profile | Audio | WER | WER change from RNNoise | Call recall | Photo recall | Time recall | Wrong photo or call run locally | Near misses kept off the phone |
|:--|:--|--:|--:|--:|--:|--:|--:|--:|
| clean | raw | 21.9% |  | 54% | 40% | 50% | 0 of 47 | 7 of 8 |
| clean | RNNoise | 21.9% | +0% | 57% | 50% | 30% | 0 of 51 | 8 of 10 |
| office, pink noise at 25 dB SNR | raw | 24.0% |  | 52% | 30% | 40% | 0 of 45 | 7 of 8 |
| office, pink noise at 25 dB SNR | RNNoise | 32.6% | +36% | 42% | 40% | 40% | 0 of 38 | 6 of 8 |
| street, pink noise at 15 dB SNR | raw | 31.8% |  | 51% | 20% | 60% | 0 of 43 | 7 of 8 |
| street, pink noise at 15 dB SNR | RNNoise | 50.4% | +58% | 28% | 10% | 50% | 0 of 23 | 5 of 5 |
| auto-rickshaw, pink noise at 5 dB SNR | raw | 57.4% |  | 24% | 20% | 20% | 0 of 21 | 4 of 5 |
| auto-rickshaw, pink noise at 5 dB SNR | RNNoise | 80.2% | +40% | 9% | 0% | 20% | 0 of 7 | 1 of 1 |

Hindi WER covers the 55 sentences written in Devanagari. It leaves out the 63 Hinglish sentences, which are written in Latin script while Whisper with language hi writes Devanagari, so their WER would count the script: kitna time hua, time kya ho gaya, abhi time kya hai, zara time batana, kitne baj gaye, ek photo khinch do, photo click karo, jaldi photo lo, iski photo lo, tasveer khincho, Deepak ko ring karo, Pooja ko ring karo, Sanjay ko ring karo, Meera ko ring karo, Karan ko ring karo, Divya ko ring karo, Suresh ko ring karo, Ishaan ko ring karo, Lakshmi ko ring karo, Farhan ko ring karo, zara Deepak ko call kar do, zara Pooja ko call kar do, zara Sanjay ko call kar do, zara Meera ko call kar do, zara Karan ko call kar do, zara Divya ko call kar do, zara Suresh ko call kar do, zara Ishaan ko call kar do, zara Lakshmi ko call kar do, zara Farhan ko call kar do, Deepak ko phone kar do, Pooja ko phone kar do, Sanjay ko phone kar do, Meera ko phone kar do, Karan ko phone kar do, Divya ko phone kar do, Suresh ko phone kar do, Ishaan ko phone kar do, Lakshmi ko phone kar do, Farhan ko phone kar do, Deepak ko dial karo, Pooja ko dial karo, Sanjay ko dial karo, Meera ko dial karo, Karan ko dial karo, Divya ko dial karo, Suresh ko dial karo, Ishaan ko dial karo, Lakshmi ko dial karo, Farhan ko dial karo, aaj baarish hogi kya, kuch interesting batao, ye building kaunsi hai, usne photo bheji thi, kisne call kiya tha, time pass kar raha hoon, photo frame kahan milega, station kitna door hai, menu padh ke batao, ketchup lao, mera din kaisa tha, foto, kal kitne baje uthna hai.

## Synthetic speech through Whisper, clean, raw

### Synthetic speech through Whisper, clean, raw, en (n=144)

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

### Synthetic speech through Whisper, clean, raw, hi (n=118)

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

## Synthetic speech through Whisper, clean, RNNoise

### Synthetic speech through Whisper, clean, RNNoise, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 87.5% (7/8) | 70.0% (7/10) |
| call_contact | 100 | 98.0% (48/49) | 48.0% (48/100) |
| other | 24 | 27.6% (21/76) | 87.5% (21/24) |

Sensitive local decisions: 55/57 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: Time flies, Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 48 | 52 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, clean, RNNoise, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 60.0% (3/5) | 30.0% (3/10) |
| take_photo | 10 | 100.0% (5/5) | 50.0% (5/10) |
| call_contact | 80 | 100.0% (46/46) | 57.5% (46/80) |
| other | 18 | 25.8% (16/62) | 88.9% (16/18) |

Sensitive local decisions: 51/51 correct, 0 wrong. With no failures in n=51, the 95% upper bound on the error rate is about 3/n = 5.9%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 8/10 stayed off the phone. Leaked: Time Pass कर रहा हूँ., समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 3 | 0 | 0 | 7 |
| take_photo | 0 | 5 | 0 | 5 |
| call_contact | 0 | 0 | 46 | 34 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.8% | 73.5% |
| 0.60 | 96.6% | 71.0% |
| 0.70 | 97.3% | 71.0% |
| 0.80 | 97.1% | 67.5% |
| 0.90 | 98.3% | 57.5% |
| 0.95 | 98.1% | 53.0% |
| 0.98 | 100.0% | 44.0% |
| 0.99 | 100.0% | 38.5% |

Misrouted:

- “Click this.” (take_photo) → other
- “Take one picture” (take_photo) → other
- “Take a snap.” (take_photo) → other
- “Call up Mira.” (call_contact) → other
- “Call up Devya.” (call_contact) → other
- “Call up Ishan.” (call_contact) → other
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
- “Ringat Devya.” (call_contact) → other
- “Ring up Ishan.” (call_contact) → other
- “Ring at Lakshmi.” (call_contact) → other
- “Dayal Pooja for me.” (call_contact) → other
- “Daival Sanjay for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Dival Divya for me.” (call_contact) → other
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
- “Call Yishan now.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Farhan now.” (call_contact) → other
- “Could you phone the puck?” (call_contact) → other
- “Could you phone me, La?” (call_contact) → other
- “Put me through to the puck.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Put me through to Mira.” (call_contact) → other
- “Put me through two current.” (call_contact) → other
- “Put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “कितना दाइम हुआ?” (time) → other
- “ताइम क्या हो गया” (time) → other
- “कितने बज़ गे?” (time) → other
- “क्या का इम होगया” (time) → other
- “कितना बजा है?” (time) → other
- “जरा समें बताव” (time) → other
- “ताइम बताना” (time) → other
- “photo klickar och” (take_photo) → other
- “तस्वी उचिचों” (take_photo) → other
- “फो तो कि इच दो?” (take_photo) → other
- “एक तस्वेलो” (take_photo) → other
- “जल दी फोतो लो” (take_photo) → other
- “वुरिंका रो?” (call_contact) → other
- “पूजा को रिंग करो.” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रिंग करो” (call_contact) → other
- “करंको रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंकारो?” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “लक्ष्मी को रिंग करो.” (call_contact) → other
- “फरहान को रिंग करो” (call_contact) → other
- “जारह इशान को कॉल कर डियो” (call_contact) → other
- “दारा फर्हान को को” (call_contact) → other
- “संजे को फोन कर दो” (call_contact) → other
- “संजे को DL करो” (call_contact) → other
- “मेरा को कॉल कर दो” (call_contact) → other
- “लक्षमी को कॉल कर दो” (call_contact) → other
- “संजे को फुन कर दो” (call_contact) → other
- “सुरिष को फो न कर दो” (call_contact) → other
- “फर्हान को फोन कर दो” (call_contact) → other
- “जरा संजे को कॉल लगाओ.” (call_contact) → other
- “ज़रा मेरा को कॉल लगाओ” (call_contact) → other
- “जरा दिवाको को लगाव?” (call_contact) → other
- “जरा सुरेश को को लगाव?” (call_contact) → other
- “जरा परहान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पूजा से बात कराओ।” (call_contact) → other
- “संजेजी बात कर आओ” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करंसी बात कराओ” (call_contact) → other
- “दिव्यासी बात कराव” (call_contact) → other
- “सुरिश से बात कराव” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लक्षमी से बात कराओ.” (call_contact) → other
- “फरहान से बात कराओ” (call_contact) → other
- “Time Pass कर रहा हूँ.” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to Deepak.”
- “dial Deepak for me” → “Dial Deepak for me”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तस्वेलो”
- “Suresh ko dial karo” → “सुरेश को डायल करो.”
- “सुरेश से बात कराओ” → “सुरिश से बात कराव”

## Synthetic speech through Whisper, office, pink noise at 25 dB SNR, raw

### Synthetic speech through Whisper, office, pink noise at 25 dB SNR, raw, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 87.5% (7/8) | 70.0% (7/10) |
| call_contact | 100 | 98.1% (52/53) | 52.0% (52/100) |
| other | 24 | 29.2% (21/72) | 87.5% (21/24) |

Sensitive local decisions: 59/61 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: Time flies., Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 52 | 48 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, office, pink noise at 25 dB SNR, raw, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 66.7% (4/6) | 40.0% (4/10) |
| take_photo | 10 | 100.0% (3/3) | 30.0% (3/10) |
| call_contact | 80 | 100.0% (42/42) | 52.5% (42/80) |
| other | 18 | 23.9% (16/67) | 88.9% (16/18) |

Sensitive local decisions: 45/45 correct, 0 wrong. With no failures in n=45, the 95% upper bound on the error rate is about 3/n = 6.7%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 7/8 stayed off the phone. Leaked: समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 4 | 0 | 0 | 6 |
| take_photo | 0 | 3 | 0 | 7 |
| call_contact | 0 | 0 | 42 | 38 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 95.3% | 71.5% |
| 0.60 | 96.5% | 69.5% |
| 0.70 | 97.2% | 69.0% |
| 0.80 | 97.1% | 66.5% |
| 0.90 | 98.3% | 57.5% |
| 0.95 | 98.1% | 52.0% |
| 0.98 | 100.0% | 43.5% |
| 0.99 | 100.0% | 37.5% |

Misrouted:

- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “Take a snap.” (take_photo) → other
- “Call up Mira.” (call_contact) → other
- “Call up Ishan.” (call_contact) → other
- “Please call me Ra.” (call_contact) → other
- “Please call Ishan.” (call_contact) → other
- “Connect me to the park.” (call_contact) → other
- “Connect me to Pooja.” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to Mira.” (call_contact) → other
- “Connect me to current.” (call_contact) → other
- “Connect me to Divya.” (call_contact) → other
- “Connect Me to Surish.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Farhan.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Ringat Puja.” (call_contact) → other
- “Ring at Mira.” (call_contact) → other
- “Ring up current” (call_contact) → other
- “Ring up Ishan.” (call_contact) → other
- “Dival Puja for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Dival Divya for me.” (call_contact) → other
- “Dayal Suresh for me.” (call_contact) → other
- “Dial E-Shan for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call Puja now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me right now.” (call_contact) → other
- “Call Karan now.” (call_contact) → other
- “Call Divya now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call Yishan now.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Farhan now.” (call_contact) → other
- “Could you phone me, La?” (call_contact) → other
- “Could you found a via?” (call_contact) → other
- “put me through to Deepak.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Put me through two mira.” (call_contact) → other
- “Put me through two currents.” (call_contact) → other
- “Put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “ताइम क्या हो गया” (time) → other
- “कितने बच गे?” (time) → other
- “या का इम होगया.” (time) → other
- “कितना बजा है।” (time) → other
- “जरा समें बताव.” (time) → other
- “ताम बताना” (time) → other
- “photo klickar och” (take_photo) → other
- “पेसा की फोटो लो.” (take_photo) → other
- “तस्वी जोग जो” (take_photo) → other
- “फटो कि इच दो?” (take_photo) → other
- “एक तस विर लो.” (take_photo) → other
- “इसकी फोतो लो” (take_photo) → other
- “जल दी फो तो लो” (take_photo) → other
- “प्रुद रिंकारो” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रेंग करो” (call_contact) → other
- “कर आंको रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंकारो” (call_contact) → other
- “इशान को रिंग करो.” (call_contact) → other
- “लक्ष्मी को रिंग करो.” (call_contact) → other
- “फरहान को रिंग करो” (call_contact) → other
- “जारा संजे को कॉल कर दो” (call_contact) → other
- “जारा इशान को कॉल कर डियो” (call_contact) → other
- “Zara Farhan को को.” (call_contact) → other
- “संजे को फोन कर दो” (call_contact) → other
- “को फो फो न कर दो” (call_contact) → other
- “संजे को DL करो” (call_contact) → other
- “दीपट को कॉल कर दो” (call_contact) → other
- “लक्षमी को कॉल कर दो” (call_contact) → other
- “दीपट को फोन कर दो” (call_contact) → other
- “संजय को पून कर दूख” (call_contact) → other
- “सुरिष को फून कर दो” (call_contact) → other
- “लक्षमी को फून कर दो” (call_contact) → other
- “परहान को फोन कर दो” (call_contact) → other
- “जरा मेरा को कॉल लगाओ” (call_contact) → other
- “जरा दिवाको को लगाव?” (call_contact) → other
- “जरा सुरेश को लगाव?” (call_contact) → other
- “जरा लक्ष्मी को को लगाव?” (call_contact) → other
- “जरा पर्हान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पूजा से बात कराओ।” (call_contact) → other
- “संजेजी बात कराव” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करंसी बात कराओ” (call_contact) → other
- “दिव्यासी बात कराव” (call_contact) → other
- “सुरिश सी बात कराओ” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लक्षमी से बात कराओ” (call_contact) → other
- “फरहान से बात कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ.” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to the park.”
- “dial Deepak for me” → “Dial Deepak for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तस विर लो.”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “सुरिश सी बात कराओ”

## Synthetic speech through Whisper, office, pink noise at 25 dB SNR, RNNoise

### Synthetic speech through Whisper, office, pink noise at 25 dB SNR, RNNoise, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 87.5% (7/8) | 70.0% (7/10) |
| call_contact | 100 | 97.7% (43/44) | 43.0% (43/100) |
| other | 24 | 25.9% (21/81) | 87.5% (21/24) |

Sensitive local decisions: 50/52 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: Time flies, Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 43 | 57 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, office, pink noise at 25 dB SNR, RNNoise, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 66.7% (4/6) | 40.0% (4/10) |
| take_photo | 10 | 100.0% (4/4) | 40.0% (4/10) |
| call_contact | 80 | 100.0% (34/34) | 42.5% (34/80) |
| other | 18 | 21.6% (16/74) | 88.9% (16/18) |

Sensitive local decisions: 38/38 correct, 0 wrong. With no failures in n=38, the 95% upper bound on the error rate is about 3/n = 7.9%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 6/8 stayed off the phone. Leaked: Time Pass कर रहा हूँ., समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 4 | 0 | 0 | 6 |
| take_photo | 0 | 4 | 0 | 6 |
| call_contact | 0 | 0 | 34 | 46 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.2% | 65.0% |
| 0.60 | 96.0% | 60.5% |
| 0.70 | 96.7% | 59.5% |
| 0.80 | 96.6% | 57.0% |
| 0.90 | 98.0% | 50.0% |
| 0.95 | 97.8% | 44.0% |
| 0.98 | 100.0% | 37.5% |
| 0.99 | 100.0% | 34.5% |

Misrouted:

- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “Take a snap.” (take_photo) → other
- “Call up Mira.” (call_contact) → other
- “Call up the VR.” (call_contact) → other
- “Call up Ishan.” (call_contact) → other
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
- “I want to call Puja.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Bring out Puja.” (call_contact) → other
- “Bring up Sanjay.” (call_contact) → other
- “Bring up Mira.” (call_contact) → other
- “Bring up current.” (call_contact) → other
- “Ring out the VR.” (call_contact) → other
- “Bring up Suresh” (call_contact) → other
- “Ring up Ishan.” (call_contact) → other
- “Bring up Lakshmi.” (call_contact) → other
- “Bring up Farhan.” (call_contact) → other
- “Dial Puja for me.” (call_contact) → other
- “Daival Sanjay for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Dival Divya for me.” (call_contact) → other
- “Dayo al-Suresh poor me.” (call_contact) → other
- “Dial E-Shan for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Dial Parhan for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call Puja now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me now.” (call_contact) → other
- “Call current now.” (call_contact) → other
- “Call DVR now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call each other now.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Farhan now.” (call_contact) → other
- “Could you phone me, la?” (call_contact) → other
- “Could you phone DVR?” (call_contact) → other
- “Put me through to the puck.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Put me through two mira.” (call_contact) → other
- “Put me through two current.” (call_contact) → other
- “Put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “ताइम क्या हो गया” (time) → other
- “कितने बच गे?” (time) → other
- “क्या का इम होगया” (time) → other
- “कितना बजा है?” (time) → other
- “जरा समें बताव” (time) → other
- “ताइम बताना” (time) → other
- “पोड़ो लेकारो” (take_photo) → other
- “तस्वीय की जो” (take_photo) → other
- “पो तो किच दो?” (take_photo) → other
- “एक तस विर लो” (take_photo) → other
- “इसकी पोटो लो” (take_photo) → other
- “जल दी पो तो लो” (take_photo) → other
- “वुलिंकारो?” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रेंग करो” (call_contact) → other
- “करंगो रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंकारो” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “Lakshmi को रिंग करो” (call_contact) → other
- “परहान को रिंग करो” (call_contact) → other
- “दारसंजे को कॉल कर दो” (call_contact) → other
- “जारा इशान को कॉल कर डियो” (call_contact) → other
- “दारा फरहान को को” (call_contact) → other
- “दी पको फोन का दो” (call_contact) → other
- “संजे को फोन कर दो” (call_contact) → other
- “को फो फो न का दो” (call_contact) → other
- “दिविया को फोन का दो” (call_contact) → other
- “संजे को DL करो” (call_contact) → other
- “परहान को डियल करो” (call_contact) → other
- “लक्षमी को कॉल कर दो” (call_contact) → other
- “परहान को कॉल कर दो” (call_contact) → other
- “दिपट को पॉन कर दो” (call_contact) → other
- “पूजा को पून कर दो.” (call_contact) → other
- “संजय को पून कर दो” (call_contact) → other
- “मीरा को पूंग कर दो” (call_contact) → other
- “करन को पून कर दो” (call_contact) → other
- “दिव्या को पून कर दो” (call_contact) → other
- “सुरिश को पूंकर दो” (call_contact) → other
- “इशान को पून कर दो” (call_contact) → other
- “लक्ष्मी को पून कर दो” (call_contact) → other
- “पर्हान को पून कर दो” (call_contact) → other
- “जरा मेरा को कॉल लगाओ” (call_contact) → other
- “दरा दिव्याको को लगाउ?” (call_contact) → other
- “जर दो रसुरेश को लगाव?” (call_contact) → other
- “जरा लक्ष्मी को को लगाव?” (call_contact) → other
- “जरा पर्हान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पूजा सिबात कराओ” (call_contact) → other
- “संजेजी बात कर आओ” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करंटी बात कराओ” (call_contact) → other
- “दिवास दिबाद कराव” (call_contact) → other
- “सुरिष थीबाद कराव” (call_contact) → other
- “इशान्ट से बात कराओ।” (call_contact) → other
- “लक्षमी से बात कराओ.” (call_contact) → other
- “परहान दिबात कराओ” (call_contact) → other
- “Time Pass कर रहा हूँ.” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to Deepak.”
- “dial Deepak for me” → “Dial Deepak for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तस विर लो”
- “Suresh ko dial karo” → “सुरेश को डायल करो.”
- “सुरेश से बात कराओ” → “सुरिष थीबाद कराव”

## Synthetic speech through Whisper, street, pink noise at 15 dB SNR, raw

### Synthetic speech through Whisper, street, pink noise at 15 dB SNR, raw, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 85.7% (6/7) | 60.0% (6/10) |
| call_contact | 100 | 97.6% (41/42) | 41.0% (41/100) |
| other | 24 | 25.0% (21/84) | 87.5% (21/24) |

Sensitive local decisions: 47/49 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 8/10 stayed off the phone. Leaked: Time flies., picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 6 | 0 | 4 |
| call_contact | 0 | 0 | 41 | 59 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, street, pink noise at 15 dB SNR, raw, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 75.0% (6/8) | 60.0% (6/10) |
| take_photo | 10 | 100.0% (2/2) | 20.0% (2/10) |
| call_contact | 80 | 100.0% (41/41) | 51.2% (41/80) |
| other | 18 | 23.9% (16/67) | 88.9% (16/18) |

Sensitive local decisions: 43/43 correct, 0 wrong. With no failures in n=43, the 95% upper bound on the error rate is about 3/n = 7.0%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 7/8 stayed off the phone. Leaked: समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 6 | 0 | 0 | 4 |
| take_photo | 0 | 2 | 0 | 8 |
| call_contact | 0 | 0 | 41 | 39 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.9% | 65.5% |
| 0.60 | 96.2% | 62.5% |
| 0.70 | 97.6% | 61.0% |
| 0.80 | 97.5% | 59.0% |
| 0.90 | 98.1% | 50.5% |
| 0.95 | 97.8% | 45.0% |
| 0.98 | 100.0% | 36.0% |
| 0.99 | 100.0% | 31.0% |

Misrouted:

- “Super picture.” (take_photo) → other
- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “Take a snap.” (take_photo) → other
- “Call up D-Path.” (call_contact) → other
- “Call up Mira.” (call_contact) → other
- “Call up Surish.” (call_contact) → other
- “Call up Ishan.” (call_contact) → other
- “Please call me up.” (call_contact) → other
- “Please call Ishan.” (call_contact) → other
- “Connect me to the path.” (call_contact) → other
- “Connect me to Pooja.” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to me lah.” (call_contact) → other
- “Connect me to current.” (call_contact) → other
- “Connect me to Divya.” (call_contact) → other
- “Connect me to Suresh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Farhan.” (call_contact) → other
- “I want to call Puja.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with Mira.” (call_contact) → other
- “Ring of the Puff.” (call_contact) → other
- “Ring at Puja.” (call_contact) → other
- “Ring Atmila.” (call_contact) → other
- “Ring Art Current” (call_contact) → other
- “Ring of Divya.” (call_contact) → other
- “Ringatsu Raish” (call_contact) → other
- “Ring at Ishan.” (call_contact) → other
- “Bring out Lakshmi.” (call_contact) → other
- “Bring up Farhan.” (call_contact) → other
- “Dial the path for me.” (call_contact) → other
- “Dial Puja for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Die Waldivia for me.” (call_contact) → other
- “D'Aual Suresh for me.” (call_contact) → other
- “Dial E-Shan for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call Pooja now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me right now.” (call_contact) → other
- “Call Karen now.” (call_contact) → other
- “Call Divya now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call Yishan now.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Farhan now.” (call_contact) → other
- “Could you phone the path?” (call_contact) → other
- “Could you found it via?” (call_contact) → other
- “Could you found Lakshmi?” (call_contact) → other
- “Put me through to the pub.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “put me through two miras.” (call_contact) → other
- “Put me through two currents.” (call_contact) → other
- “put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “ताइम क्या हो बैख” (time) → other
- “कितने बच गे?” (time) → other
- “याग आम होगया” (time) → other
- “किपना बजा है।” (time) → other
- “photo klickar och” (take_photo) → other
- “वे सकी फोतो लोग” (take_photo) → other
- “तस्वीय की जो” (take_photo) → other
- “पोटो कि इच्ट दो” (take_photo) → other
- “एक तस वी लूग्” (take_photo) → other
- “इसकी फोतो लो” (take_photo) → other
- “फोटो फ्लिक करो” (take_photo) → other
- “जल्बी पो तो लो” (take_photo) → other
- “पुर नंकारो” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रेंग करो” (call_contact) → other
- “कर आंको रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंग करो” (call_contact) → other
- “इशान को रिंग करो,” (call_contact) → other
- “Lakshmi Korenkarov” (call_contact) → other
- “फरहान को रिंग करो” (call_contact) → other
- “जारा इशान को कॉल कर दियो” (call_contact) → other
- “सार वारान को को” (call_contact) → other
- “दीपक को पॉन का दो” (call_contact) → other
- “को फो न कर दो” (call_contact) → other
- “संजे को डियल करो” (call_contact) → other
- “दीपट को कॉल कर दो.” (call_contact) → other
- “दिव्या कुल कर दो” (call_contact) → other
- “सुरीश को कोल का दो” (call_contact) → other
- “लक्षमी को कॉल कर दो” (call_contact) → other
- “परहान को कॉल कर दो” (call_contact) → other
- “संजय को पूं कर दूट” (call_contact) → other
- “मीरा को सोन कर दो” (call_contact) → other
- “कर रंको फूं कर दो” (call_contact) → other
- “सुलिष को फूंक दो” (call_contact) → other
- “पर्हान को सून कर दो” (call_contact) → other
- “जरा दिव्याकु को लगाओ” (call_contact) → other
- “जरा सुरेश को को लगाव?” (call_contact) → other
- “जरा लक्ष्मी को को लगाव?” (call_contact) → other
- “जरा पर्हान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पुजा सी बात कराओ।” (call_contact) → other
- “संजे सी बात कराव” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करन्सी बात कराओ” (call_contact) → other
- “दिवाजी बाज कराओ” (call_contact) → other
- “शुरीश थी बाज कराओ” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लप्षमी से बात कराओ.” (call_contact) → other
- “परहान से बात कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ.” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to the path.”
- “dial Deepak for me” → “Dial the path for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “एक तस वी लूग्”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “शुरीश थी बाज कराओ”

## Synthetic speech through Whisper, street, pink noise at 15 dB SNR, RNNoise

### Synthetic speech through Whisper, street, pink noise at 15 dB SNR, RNNoise, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 85.7% (6/7) | 60.0% (6/10) |
| call_contact | 100 | 96.8% (30/31) | 30.0% (30/100) |
| other | 24 | 22.1% (21/95) | 87.5% (21/24) |

Sensitive local decisions: 36/38 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 8/10 stayed off the phone. Leaked: Time flies., Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 6 | 0 | 4 |
| call_contact | 0 | 0 | 30 | 70 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, street, pink noise at 15 dB SNR, RNNoise, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 83.3% (5/6) | 50.0% (5/10) |
| take_photo | 10 | 100.0% (1/1) | 10.0% (1/10) |
| call_contact | 80 | 100.0% (22/22) | 27.5% (22/80) |
| other | 18 | 19.1% (17/89) | 94.4% (17/18) |

Sensitive local decisions: 23/23 correct, 0 wrong. With no failures in n=23, the 95% upper bound on the error rate is about 3/n = 13.0%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 5/5 stayed off the phone.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 5 | 0 | 0 | 5 |
| take_photo | 0 | 1 | 0 | 9 |
| call_contact | 0 | 0 | 22 | 58 |
| other | 1 | 0 | 0 | 17 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 91.6% | 49.0% |
| 0.60 | 93.8% | 45.0% |
| 0.70 | 97.8% | 44.5% |
| 0.80 | 97.6% | 40.5% |
| 0.90 | 97.3% | 35.5% |
| 0.95 | 96.7% | 29.5% |
| 0.98 | 100.0% | 24.0% |
| 0.99 | 100.0% | 19.5% |

Misrouted:

- “tube a picture” (take_photo) → other
- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “Take a snap.” (take_photo) → other
- “Call up D-Pack” (call_contact) → other
- “Paul Apsanjay” (call_contact) → other
- “Call at Mira.” (call_contact) → other
- “Fall Up Current” (call_contact) → other
- “Paul Absuresh” (call_contact) → other
- “All up Ishan.” (call_contact) → other
- “Please call Puja.” (call_contact) → other
- “Please call me Ra.” (call_contact) → other
- “Please call Ishan.” (call_contact) → other
- “Please call Parhan.” (call_contact) → other
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
- “I want to call Puja.” (call_contact) → other
- “I want to call Tarhan.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with Parhan.” (call_contact) → other
- “Bring out Puja.” (call_contact) → other
- “Bring up Sanjay.” (call_contact) → other
- “Ring at Mira.” (call_contact) → other
- “Ring up current.” (call_contact) → other
- “Ring of Divya” (call_contact) → other
- “Ringgotsu Reish” (call_contact) → other
- “Ring out Ishan.” (call_contact) → other
- “Bring out Lakshmi.” (call_contact) → other
- “Bring up Farhan.” (call_contact) → other
- “Daywal Pooja for me.” (call_contact) → other
- “Daywal Sanjee for me.” (call_contact) → other
- “Dial Mira for me.” (call_contact) → other
- “Dial current for me.” (call_contact) → other
- “Dival Divya for me.” (call_contact) → other
- “Dayal Suresh for me.” (call_contact) → other
- “Die will eat shunt for me.” (call_contact) → other
- “Dayal Lakshmi for me.” (call_contact) → other
- “Dial Parhan for me.” (call_contact) → other
- “Fall deep up now.” (call_contact) → other
- “Call Puja now.” (call_contact) → other
- “Call Sanjay now.” (call_contact) → other
- “Call me right now.” (call_contact) → other
- “Paul Cullen now.” (call_contact) → other
- “Paul Divya now.” (call_contact) → other
- “Paul Suresh now.” (call_contact) → other
- “Oh, you should know.” (call_contact) → other
- “Call Lakshmi now.” (call_contact) → other
- “Call Parhan now.” (call_contact) → other
- “Could you phone the path?” (call_contact) → other
- “Would you phone me, La?” (call_contact) → other
- “to do phone current” (call_contact) → other
- “put you found the were” (call_contact) → other
- “Purdue Phones Uresh” (call_contact) → other
- “Would you phone Ishan?” (call_contact) → other
- “Could you pawn Lakshmi?” (call_contact) → other
- “Would you phone Parhan?” (call_contact) → other
- “Put me through to Deepak.” (call_contact) → other
- “Put me through to Kuja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Put me through two mila.” (call_contact) → other
- “Put me through two currents.” (call_contact) → other
- “Put me through to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “ताइं कि आओब आ” (time) → other
- “कितने बच्च गे?” (time) → other
- “या ताइम होगा” (time) → other
- “किपना बजा है?” (time) → other
- “ताम बताना” (time) → other
- “पोडो ख्लिक करो” (take_photo) → other
- “जल्दी पोटो लो” (take_photo) → other
- “जसकी पोडोलो” (take_photo) → other
- “तस्वी उचिचों” (take_photo) → other
- “पुर्तों की जो?” (take_photo) → other
- “इत तस विर लो” (take_photo) → other
- “इसकी पूर्टो लो” (take_photo) → other
- “पुट प्लिक करो” (take_photo) → other
- “जल्बी को तोलो” (take_photo) → other
- “वर रिंका रो?” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मीरा को रेंकरो” (call_contact) → other
- “कर आंको रिंकारो” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “तुरेश को रिंकारो” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “Lakshmiko Rincaro” (call_contact) → other
- “परहान को रिंग करो” (call_contact) → other
- “दारसंजे को कॉल कर दो” (call_contact) → other
- “जार इशान को कॉल कर डियो” (call_contact) → other
- “दारव फरहान को को” (call_contact) → other
- “इपको पॉन का दो” (call_contact) → other
- “संजे को पौन कर दो” (call_contact) → other
- “मीना कुपोन कर दो” (call_contact) → other
- “पोपन का दो” (call_contact) → other
- “दिव्या को पौन का दो” (call_contact) → other
- “सुरेश को पून कर दो” (call_contact) → other
- “इशान को पून का दो” (call_contact) → other
- “Lakshmiko Pongka Do” (call_contact) → other
- “परहान कुपोन कर दो” (call_contact) → other
- “डीपक को डायल करो.” (call_contact) → other
- “संजे को DL करो” (call_contact) → other
- “परहान को डियल करो” (call_contact) → other
- “नीरा को कॉल कर दो.” (call_contact) → other
- “दिव्या को कोल कर दो” (call_contact) → other
- “तुरिश को कोल कर दो” (call_contact) → other
- “लप्षमी को कॉल कर दो” (call_contact) → other
- “पर्हान को कॉल कर दो” (call_contact) → other
- “इपको कुण का दो” (call_contact) → other
- “पूजा को कों कर दो” (call_contact) → other
- “प्रजजए को पून कर दो” (call_contact) → other
- “मीरा को पून कर दो” (call_contact) → other
- “कर रंको पूंक अदूग्” (call_contact) → other
- “जिव्या कुप कुण कर दो” (call_contact) → other
- “तुरीश कुपूं कदो” (call_contact) → other
- “इशान को पूंड कर दो” (call_contact) → other
- “लग्ष्मी कुपन का दो” (call_contact) → other
- “पर्षान को पूंड कर दो” (call_contact) → other
- “दरत अंजे को को लगाओ?” (call_contact) → other
- “दरा मीरा को कोल लगाओ” (call_contact) → other
- “दरा करन को कॉल लगाओ” (call_contact) → other
- “दर दिव्याको को लगाउ?” (call_contact) → other
- “दरस वरेश को लगाव?” (call_contact) → other
- “दरा इशान को कॉल लगाओ” (call_contact) → other
- “दरा लप्ष्मीक अगोल लगाव” (call_contact) → other
- “दरख पर्धान को कॉल लगाओ” (call_contact) → other
- “वीपक से बात कराओ” (call_contact) → other
- “पूज़ा दिबात कराओ” (call_contact) → other
- “तंजे इवती बाग कर आउ” (call_contact) → other
- “नीरा दिबात कराओ” (call_contact) → other
- “करन दिबात कराओ” (call_contact) → other
- “दिवाज दिवाज कराउ” (call_contact) → other
- “तुरिष पिवाग कराउ” (call_contact) → other
- “इशान पर बात कराओ” (call_contact) → other
- “लबश्मीती बात कराओ” (call_contact) → other
- “पर्हान पिबात कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ.” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to Deepak.”
- “dial Deepak for me” → “Dial Deepak for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “इत तस विर लो”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “तुरिष पिवाग कराउ”

## Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, raw

### Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, raw, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 100.0% (5/5) | 50.0% (5/10) |
| call_contact | 100 | 96.3% (26/27) | 26.0% (26/100) |
| other | 24 | 21.8% (22/101) | 91.7% (22/24) |

Sensitive local decisions: 31/32 correct, 1 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 9/10 stayed off the phone. Leaked: Time flies..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 5 | 0 | 5 |
| call_contact | 0 | 0 | 26 | 74 |
| other | 1 | 0 | 1 | 22 |

### Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, raw, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 50.0% (2/4) | 20.0% (2/10) |
| take_photo | 10 | 100.0% (2/2) | 20.0% (2/10) |
| call_contact | 80 | 100.0% (19/19) | 23.8% (19/80) |
| other | 18 | 17.2% (16/93) | 88.9% (16/18) |

Sensitive local decisions: 21/21 correct, 0 wrong. With no failures in n=21, the 95% upper bound on the error rate is about 3/n = 14.3%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 4/5 stayed off the phone. Leaked: समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 2 | 0 | 0 | 8 |
| take_photo | 0 | 2 | 0 | 8 |
| call_contact | 0 | 0 | 19 | 61 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 95.5% | 42.5% |
| 0.60 | 96.3% | 39.0% |
| 0.70 | 96.2% | 37.5% |
| 0.80 | 95.7% | 33.5% |
| 0.90 | 96.7% | 29.5% |
| 0.95 | 98.1% | 26.0% |
| 0.98 | 100.0% | 18.0% |
| 0.99 | 100.0% | 15.5% |

Misrouted:

- “It's not a photo.” (take_photo) → other
- “Capture the food” (take_photo) → other
- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “I think I'll see you next time.” (take_photo) → other
- “Call up D-Buck.” (call_contact) → other
- “call off to Jack.” (call_contact) → other
- “Call up Sunday.” (call_contact) → other
- “So I'm at mila.” (call_contact) → other
- “Call up Cullen.” (call_contact) → other
- “call up the yard.” (call_contact) → other
- “Call up to race.” (call_contact) → other
- “Call up Yee Shan.” (call_contact) → other
- “Go and watch me.” (call_contact) → other
- “Call us, Garhan.” (call_contact) → other
- “Please call these tasks.” (call_contact) → other
- “Please call me God.” (call_contact) → other
- “The state is being sent to you.” (call_contact) → other
- “Please call Yishan.” (call_contact) → other
- “Please call Sarhan” (call_contact) → other
- “Connect me to the podcast.” (call_contact) → other
- “Connect me to Pooja.” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to me lah.” (call_contact) → other
- “Connect me to Karen.” (call_contact) → other
- “connect me to Divya” (call_contact) → other
- “Connect me to Suresh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Sarhan.” (call_contact) → other
- “I want to call the pastor.” (call_contact) → other
- “I want to call Puja.” (call_contact) → other
- “I want to call Miva.” (call_contact) → other
- “I want to call Salhan.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with me now.” (call_contact) → other
- “Start a call with current.” (call_contact) → other
- “start a call with India” (call_contact) → other
- “Start a call with Tarhan” (call_contact) → other
- “Ring odd debug.” (call_contact) → other
- “Ring of Fuja.” (call_contact) → other
- “Ring of Mira” (call_contact) → other
- “Ring art current” (call_contact) → other
- “Ring Octavia” (call_contact) → other
- “Ringatsu-ish” (call_contact) → other
- “Ring at Ishan.” (call_contact) → other
- “Ring at Farhan” (call_contact) → other
- “that you'll be part for me.” (call_contact) → other
- “Die Alkuja for me.” (call_contact) → other
- “Dylang Sanjay for me.” (call_contact) → other
- “Die Almira for me.” (call_contact) → other
- “Dial current for me” (call_contact) → other
- “Die all the gap for me.” (call_contact) → other
- “Die also raised for me.” (call_contact) → other
- “Dial each hand for me.” (call_contact) → other
- “Daryl Lachmi for me.” (call_contact) → other
- “Dying on some hand for me.” (call_contact) → other
- “Call Deepak now.” (call_contact) → other
- “Call to John now.” (call_contact) → other
- “Go Sanji now.” (call_contact) → other
- “Call me now now.” (call_contact) → other
- “all the VIA now” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Hold these on now.” (call_contact) → other
- “Call up to me now.” (call_contact) → other
- “Kool-Sarhan now.” (call_contact) → other
- “Could you phone me back?” (call_contact) → other
- “Could you phone me, La?” (call_contact) → other
- “Could you phone Shanghai?” (call_contact) → other
- “Put me through to the pub.” (call_contact) → other
- “Put me through to Kooja.” (call_contact) → other
- “with me too to Sanjay” (call_contact) → other
- “of me, too, to me, ah.” (call_contact) → other
- “put me through two current.” (call_contact) → other
- “took me through to the world” (call_contact) → other
- “took me through to Suresh.” (call_contact) → other
- “Look me too to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me to do something.” (call_contact) → other
- “Time flies.” (other) → time
- “Who is calling?” (other) → call_contact
- “कि अपना का इम हुआ?” (time) → other
- “ताइम क्या हो गाए” (time) → other
- “जरा ताइम बताना” (time) → other
- “इपनी बच्दी” (time) → other
- “यागा नगोगा” (time) → other
- “किपना बजा है।” (time) → other
- “ताइम बताना” (time) → other
- “अभी कितने बच रहे हैं।” (time) → other
- “पोटो क्लिक करो” (take_photo) → other
- “किसा की फो तो लो” (take_photo) → other
- “अबस्यूपिच चूँ” (take_photo) → other
- “पोई टिंच दो” (take_photo) → other
- “इस दो” (take_photo) → other
- “इसकी फो जो” (take_photo) → other
- “पोचो फ्रिक करो” (take_photo) → other
- “जल्वी पो तो लो” (take_photo) → other
- “पुरीं करो” (call_contact) → other
- “पिंजा को रिंकारो” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “मिला को रेंक रो” (call_contact) → other
- “कर दो रिंकारो” (call_contact) → other
- “बिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रेंकारो” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “लग्ष्मी को रेंकरोग।” (call_contact) → other
- “परहान को विंग करो” (call_contact) → other
- “जारसंदे को कौन कर दो” (call_contact) → other
- “जरा मीरा को कौन का दो” (call_contact) → other
- “जरा सुरेश को को जो” (call_contact) → other
- “जार इशान को कॉल कर दियो” (call_contact) → other
- “साल अफाल हान को को” (call_contact) → other
- “वीपको पॉण का दो” (call_contact) → other
- “पुजा को फोंका दो” (call_contact) → other
- “मिरा तो को अगा दो” (call_contact) → other
- “को पूंगा दो” (call_contact) → other
- “ते विवा को वों कादो” (call_contact) → other
- “सुरेश को पौन का दो” (call_contact) → other
- “इशान पुफंता दो” (call_contact) → other
- “लग्ष्मी को पॉन का लो” (call_contact) → other
- “पाहन पूँन का दो” (call_contact) → other
- “संजे को डियल करो” (call_contact) → other
- “मीना को डायल परो” (call_contact) → other
- “परहान को डियल करो” (call_contact) → other
- “दिपत भू कॉल का दो” (call_contact) → other
- “तो जा कोल कदो” (call_contact) → other
- “करन को कौल कर दो” (call_contact) → other
- “जिया कुछ का दूप” (call_contact) → other
- “वो जो जो जो जो जो” (call_contact) → other
- “इशान को कौन कर दो?” (call_contact) → other
- “नक्षमी को कॉल कर दो” (call_contact) → other
- “पठान को कॉन कर्दू?” (call_contact) → other
- “बीपत पोफों का दो” (call_contact) → other
- “पुजा कुपुं कड़ों” (call_contact) → other
- “जजए कुपून कर दूए” (call_contact) → other
- “मिरा को सो उनका दो” (call_contact) → other
- “करन को पूँव का दो” (call_contact) → other
- “इवा कुष नक दूटूँ” (call_contact) → other
- “वो दो जो जो जो” (call_contact) → other
- “इशान को फोन कर दूख” (call_contact) → other
- “नच्ष्मी को फोंका दो” (call_contact) → other
- “पर्खान को सून कर दो” (call_contact) → other
- “जरत संजय को कौन लगाओ?” (call_contact) → other
- “जड़ा मीरा को कोल लगाओ” (call_contact) → other
- “जर दिल्या को अगल नगाओ” (call_contact) → other
- “जरा सुरीश को प्कोर नगाओ” (call_contact) → other
- “जरा इशान को कोई लगाओ” (call_contact) → other
- “जरा लग्ष्मी को को लगाव” (call_contact) → other
- “इपक्ति बात कराओ” (call_contact) → other
- “पुजा इबाट कराओ” (call_contact) → other
- “संजे सी बाज कराओ” (call_contact) → other
- “मीरा सी बाइ कराओ” (call_contact) → other
- “करन्सी बात कराओ” (call_contact) → other
- “दिल्यास इबाज कराउ” (call_contact) → other
- “तुरिष पिवाग कराओ” (call_contact) → other
- “इशान सी वास कराओ” (call_contact) → other
- “लगश्मी सी बात कराओ” (call_contact) → other
- “फरहान सिवाद कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to the podcast.”
- “dial Deepak for me” → “that you'll be part for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “इस दो”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “तुरिष पिवाग कराओ”

## Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, RNNoise

### Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, RNNoise, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 83.3% (5/6) | 50.0% (5/10) |
| call_contact | 100 | 95.2% (20/21) | 20.0% (20/100) |
| other | 24 | 19.8% (21/106) | 87.5% (21/24) |

Sensitive local decisions: 25/27 correct, 2 wrong. The 3/n bound needs zero failures, so it does not apply here.

Near misses (cloud utterances that share a word with a local intent): 6/8 stayed off the phone. Leaked: Time flies., Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 5 | 0 | 5 |
| call_contact | 0 | 0 | 20 | 80 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, auto-rickshaw, pink noise at 5 dB SNR, RNNoise, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 100.0% (2/2) | 20.0% (2/10) |
| take_photo | 10 | none predicted | 0/10 |
| call_contact | 80 | 100.0% (7/7) | 8.8% (7/80) |
| other | 18 | 16.5% (18/109) | 100.0% (18/18) |

Sensitive local decisions: 7/7 correct, 0 wrong. With no failures in n=7, the 95% upper bound on the error rate is about 3/n = 42.9%, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 1/1 stayed off the phone.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 2 | 0 | 0 | 8 |
| take_photo | 0 | 0 | 0 | 10 |
| call_contact | 0 | 0 | 7 | 73 |
| other | 0 | 0 | 0 | 18 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 88.5% | 27.0% |
| 0.60 | 94.3% | 25.0% |
| 0.70 | 94.3% | 25.0% |
| 0.80 | 95.5% | 21.0% |
| 0.90 | 95.0% | 19.0% |
| 0.95 | 94.1% | 16.0% |
| 0.98 | 100.0% | 11.5% |
| 0.99 | 100.0% | 7.5% |

Misrouted:

- “You have a photo.” (take_photo) → other
- “That's the code.” (take_photo) → other
- “Click this.” (take_photo) → other
- “Take one picture.” (take_photo) → other
- “Take a seat.” (take_photo) → other
- “All of the past.” (call_contact) → other
- “Paul Appuja.” (call_contact) → other
- “Ball up Sunday.” (call_contact) → other
- “Oh, my God,” (call_contact) → other
- “All up, Dagen.” (call_contact) → other
- “All of them, yeah.” (call_contact) → other
- “All at soish.” (call_contact) → other
- “Polakishan.” (call_contact) → other
- “Toy at Lakshmiu.” (call_contact) → other
- “Paul Afzalhan” (call_contact) → other
- “Please call D-Path.” (call_contact) → other
- “Give Paul Mima.” (call_contact) → other
- “Leave Paul Taran.” (call_contact) → other
- “dr bauldemia” (call_contact) → other
- “Keep Paul Suresh.” (call_contact) → other
- “Leave Goyishan.” (call_contact) → other
- “Please call Tarhan.” (call_contact) → other
- “Connect me to be back.” (call_contact) → other
- “connect me to Pooja” (call_contact) → other
- “Connect me to Sanjay.” (call_contact) → other
- “Connect me to me lah.” (call_contact) → other
- “Connect me to current.” (call_contact) → other
- “Thank you to Divya.” (call_contact) → other
- “Connect me to Suresh.” (call_contact) → other
- “Connect me to Ishan.” (call_contact) → other
- “Connect me to Lakshmi.” (call_contact) → other
- “Connect me to Farhan.” (call_contact) → other
- “I want to call the path.” (call_contact) → other
- “I want to call me back.” (call_contact) → other
- “I want to call Tarhan.” (call_contact) → other
- “Tata call with Puja.” (call_contact) → other
- “Tata call with Sanjay” (call_contact) → other
- “Ta Ta Taul Wibli Raab” (call_contact) → other
- “Start a call with Dhymia.” (call_contact) → other
- “Tata call with Suresh.” (call_contact) → other
- “Data call with Ishan” (call_contact) → other
- “Tata call with Lakshmi.” (call_contact) → other
- “Tata call with Tarhan” (call_contact) → other
- “Ring.debug” (call_contact) → other
- “Ring a puja.” (call_contact) → other
- “Ring at me.” (call_contact) → other
- “Ring up Karen.” (call_contact) → other
- “Ring of Divya” (call_contact) → other
- “Ringgatsuresh” (call_contact) → other
- “Bring up Yee Shan.” (call_contact) → other
- “Bring out Lakshmi.” (call_contact) → other
- “Ring at Palhan.” (call_contact) → other
- “that will be part for me” (call_contact) → other
- “Dial to Japanese” (call_contact) → other
- “Daryl Sanjay Pornik” (call_contact) → other
- “Daewang Mira forming” (call_contact) → other
- “Die all current for me.” (call_contact) → other
- “Daival Divya Porny” (call_contact) → other
- “They also raised for me.” (call_contact) → other
- “Dayan Yishan for me.” (call_contact) → other
- “Dival Lakshmi Parmi.” (call_contact) → other
- “Dial Palhaan for me.” (call_contact) → other
- “All deep up now.” (call_contact) → other
- “All Pooja now.” (call_contact) → other
- “Both Sanji now.” (call_contact) → other
- “Call me now.” (call_contact) → other
- “Point again now.” (call_contact) → other
- “All the way out now.” (call_contact) → other
- “Also is now.” (call_contact) → other
- “For this one now.” (call_contact) → other
- “All luck me now.” (call_contact) → other
- “Call Tarhan now.” (call_contact) → other
- “Would you phone me back?” (call_contact) → other
- “Would you call me now?” (call_contact) → other
- “Would you phone the via?” (call_contact) → other
- “Put me clue to deep up.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me to do Sanjay.” (call_contact) → other
- “Put me through to me, ah.” (call_contact) → other
- “Put me through to current.” (call_contact) → other
- “Put me to to Divya.” (call_contact) → other
- “Put me through to Suresh.” (call_contact) → other
- “Put me through to Ishaan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “Put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “Picture this.” (other) → take_photo
- “Who is calling?” (other) → call_contact
- “ताइं क्या हो बाइग” (time) → other
- “अभी ताइम क्या है?” (time) → other
- “दरा ताइं बताना” (time) → other
- “तिपने बच्चें” (time) → other
- “या दाइन वोगा” (time) → other
- “किपना बजा है?” (time) → other
- “ताइन बताना” (time) → other
- “अब ही कितने बच रहे हैं?” (time) → other
- “एक फो दो प्रेंच दो” (take_photo) → other
- “पोड़ प्रिकारो” (take_photo) → other
- “जल्वी पोडोलो” (take_photo) → other
- “किसा की पो टो लो” (take_photo) → other
- “तास्वीर की चौू।” (take_photo) → other
- “पो तो प्योट प्योट” (take_photo) → other
- “एक तफ इनो” (take_photo) → other
- “इप इप पो तो डो” (take_photo) → other
- “पुट अप्रिक करो” (take_photo) → other
- “जर वो तो लो” (take_photo) → other
- “बुरीं करो” (call_contact) → other
- “तिंजा को रिंकारो” (call_contact) → other
- “तंडे को रिंकरो” (call_contact) → other
- “इरा को रेंगारो” (call_contact) → other
- “तरां को रिंकारो” (call_contact) → other
- “इव्याको रिंकरो” (call_contact) → other
- “तुरे इप सिको रेंग करो” (call_contact) → other
- “इतान पुर रिंकारो?” (call_contact) → other
- “लगष नीपो रिंकरो” (call_contact) → other
- “पहां पुरिंकरो!” (call_contact) → other
- “तरा भी पको पॉल कर दो” (call_contact) → other
- “जरा पूजा को पॉल कर दो” (call_contact) → other
- “गारसंगे को कॉन का दो” (call_contact) → other
- “जरा मीरा तो कौन कर दो” (call_contact) → other
- “लागा रांको कोल कर दो” (call_contact) → other
- “जरा दिज्या को कॉल कर दो” (call_contact) → other
- “जरा सुरेश को पॉल कर दो” (call_contact) → other
- “दार इशान को कॉल कर दियो” (call_contact) → other
- “जरा लच्छ नूपो कॉल कर दो” (call_contact) → other
- “दारब परहान को कर” (call_contact) → other
- “इपको पूँन का दो” (call_contact) → other
- “पुजा पुपों कर दो.” (call_contact) → other
- “तंजे को पूंका दो” (call_contact) → other
- “बीरा पुपोन करो” (call_contact) → other
- “पोपों कादो।” (call_contact) → other
- “इव्या पूँन कर दो” (call_contact) → other
- “दुरेश को पॉन कर दो” (call_contact) → other
- “कि शान पुपों तरो” (call_contact) → other
- “लच्छी को पूंकलो” (call_contact) → other
- “पहां पौन का दो” (call_contact) → other
- “हुंजा को डायल करो.” (call_contact) → other
- “तंजे को डियाल करो” (call_contact) → other
- “तुरेश को डायल दरो” (call_contact) → other
- “पहां को दियल करो” (call_contact) → other
- “इपत पुख कॉन का दो” (call_contact) → other
- “पुजा को कौन कर दो?” (call_contact) → other
- “प्रजय को ल कर दो” (call_contact) → other
- “नीडा पू कॉल कर दो” (call_contact) → other
- “तरन को को जड़ो” (call_contact) → other
- “दिया को ओन का दो” (call_contact) → other
- “बड़िश पुर ओूट दो” (call_contact) → other
- “तीशान पो कौन करदो?” (call_contact) → other
- “लच्ष्मी को कोल कर दो” (call_contact) → other
- “इपक पुप पुण का दो” (call_contact) → other
- “प्ञजब पूँब पूम कदो” (call_contact) → other
- “तंजय पुपोन कदड़ू” (call_contact) → other
- “याप पुप ओम का दो” (call_contact) → other
- “तरंगो पूंका दो” (call_contact) → other
- “जिल्या कुप पूंक दो” (call_contact) → other
- “तुरीश पुपूं का दुट” (call_contact) → other
- “इशान पूँ पूंका दो” (call_contact) → other
- “नच्मी को फंका दो” (call_contact) → other
- “परखान को फों कर दो” (call_contact) → other
- “दरा दीपत पू को नगाव?” (call_contact) → other
- “तेरा पूजा को कौन नगाओ?” (call_contact) → other
- “दरग रंजे पूद कोल लगाओ” (call_contact) → other
- “तरा मिरा पूर को लेगाओ” (call_contact) → other
- “दरा करन पूख को नगाओ” (call_contact) → other
- “दर दिल्या को झाल नगाओ” (call_contact) → other
- “बरत दुरेश को को लगाव” (call_contact) → other
- “बिरा एशान पो को लगाव?” (call_contact) → other
- “बड़ा नच्मी को ओन गाव” (call_contact) → other
- “दरत पठान पुकोर नगाओ” (call_contact) → other
- “इपत्विबात कराओ” (call_contact) → other
- “पुज़क दिबात कराओ” (call_contact) → other
- “पंजय पिवार कराओ” (call_contact) → other
- “नीरा तिवाद कराओ।” (call_contact) → other
- “तरं पिबाद कर आओ” (call_contact) → other
- “विवाज दिवाज कराव” (call_contact) → other
- “प्रीष पिवाद कराउ” (call_contact) → other
- “इतान पिवार कराओ” (call_contact) → other
- “लग्ष्मी दिवाद कराल” (call_contact) → other
- “परखाल पिवार कराओ” (call_contact) → other

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to be back.”
- “dial Deepak for me” → “that will be part for me”
- “how's the weather in delhi” → “How the weather in Delhi?”
- “एक तस्वीर लो” → “एक तफ इनो”
- “Suresh ko dial karo” → “तुरेश को डायल दरो”
- “सुरेश से बात कराओ” → “प्रीष पिवाद कराउ”
