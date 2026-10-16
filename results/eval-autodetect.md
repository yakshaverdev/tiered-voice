# Router eval

Train 214 rows, calibration 54 rows, temperature 0.72. Test 262 rows with templates and contact names the router never saw. Thresholds: {'take_photo': 0.95, 'call_contact': 0.95, 'time': 0.8}, floor 0.5. Online mode, so the gray zone goes to the cloud.

## Typed text

### Typed text, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 88.9% (8/9) | 80.0% (8/10) |
| call_contact | 100 | 98.6% (70/71) | 70.0% (70/100) |
| other | 24 | 39.6% (21/53) | 87.5% (21/24) |

Sensitive local decisions: 78/80 correct. With n=80, the 95% upper bound on the error rate is about 3/n = 3.8% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: time flies, picture this.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 8 | 0 | 2 |
| call_contact | 0 | 0 | 70 | 30 |
| other | 1 | 1 | 1 | 21 |

### Typed text, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 77.8% (7/9) | 70.0% (7/10) |
| take_photo | 10 | 100.0% (6/6) | 60.0% (6/10) |
| call_contact | 80 | 100.0% (70/70) | 87.5% (70/80) |
| other | 18 | 48.5% (16/33) | 88.9% (16/18) |

Sensitive local decisions: 76/76 correct. With n=76, the 95% upper bound on the error rate is about 3/n = 3.9% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

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
| 0.50 | 97.9% | 95.0% |
| 0.60 | 97.9% | 95.0% |
| 0.70 | 97.9% | 94.5% |
| 0.80 | 97.8% | 88.5% |
| 0.90 | 98.9% | 87.0% |
| 0.95 | 98.7% | 77.0% |
| 0.98 | 100.0% | 69.0% |
| 0.99 | 100.0% | 47.0% |

Misrouted:

- “click this” (take_photo) → other
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
| take_photo | 10 | 88.9% (8/9) | 80.0% (8/10) |
| call_contact | 100 | 97.7% (42/43) | 42.0% (42/100) |
| other | 24 | 25.9% (21/81) | 87.5% (21/24) |

Sensitive local decisions: 50/52 correct. With n=52, the 95% upper bound on the error rate is about 3/n = 5.8% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 9/11 stayed off the phone. Leaked: Time flies, Picture this..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 8 | 0 | 2 |
| call_contact | 0 | 0 | 42 | 58 |
| other | 1 | 1 | 1 | 21 |

### Synthetic speech through Whisper, clean, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 75.0% (6/8) | 60.0% (6/10) |
| take_photo | 10 | 100.0% (3/3) | 30.0% (3/10) |
| call_contact | 80 | 100.0% (30/30) | 37.5% (30/80) |
| other | 18 | 20.8% (16/77) | 88.9% (16/18) |

Sensitive local decisions: 33/33 correct. With n=33, the 95% upper bound on the error rate is about 3/n = 9.1% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 7/8 stayed off the phone. Leaked: समय बहुत कम है..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 6 | 0 | 0 | 4 |
| take_photo | 0 | 3 | 0 | 7 |
| call_contact | 0 | 0 | 30 | 50 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 95.2% | 69.5% |
| 0.60 | 96.4% | 66.0% |
| 0.70 | 96.2% | 64.0% |
| 0.80 | 95.8% | 57.0% |
| 0.90 | 98.0% | 49.5% |
| 0.95 | 97.6% | 41.5% |
| 0.98 | 100.0% | 39.5% |
| 0.99 | 100.0% | 33.5% |

Misrouted:

- “Click this.” (take_photo) → other
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
- “I want to call Mira.” (call_contact) → other
- “I want to call Ishan.” (call_contact) → other
- “Start a call with the puck.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with Ishan.” (call_contact) → other
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
- “Could you phone Ishan?” (call_contact) → other
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
- “야가임호개야.” (time) → other
- “कितना बजा है।” (time) → other
- “Zără să mai bătau.” (time) → other
- “Foto klickar och.” (take_photo) → other
- “पेसा की फोटो लो.” (take_photo) → other
- “Das will Kichol.” (take_photo) → other
- “Forto KIC do...” (take_photo) → other
- “Ít tất cả sếp lúc.” (take_photo) → other
- “فورتو کلک کرو” (take_photo) → other
- “जल्दी फोतो लो” (take_photo) → other
- “不倫かろう?” (call_contact) → other
- “पूजा को रिंग करो” (call_contact) → other
- “संजे को रिंग करो.” (call_contact) → other
- “Mira co ring karo.” (call_contact) → other
- “Karanko Ring Karo.” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “すれしくおれんかろう?” (call_contact) → other
- “इशान को रिंग करो.” (call_contact) → other
- “लक्ष्मी को रिंग करो.” (call_contact) → other
- “فرحان کو رنگ کرو” (call_contact) → other
- “जारा संजे को कॉल कर दो” (call_contact) → other
- “ذرا میرا کو کال کر دو” (call_contact) → other
- “जरा करन को कॉल कर दो” (call_contact) → other
- “जारा इशान को कॉल कर डियो” (call_contact) → other
- “زارہ فرحان کو کہا” (call_contact) → other
- “संजे को फोन कर दो” (call_contact) → other
- “Cofone cadeau.” (call_contact) → other
- “عشان کو فون کر دو” (call_contact) → other
- “فرحان کو فون کر دو” (call_contact) → other
- “संजे को DL करो.” (call_contact) → other
- “करन को डायल करो” (call_contact) → other
- “عشان کو ڈائل کرو” (call_contact) → other
- “लक्षमी को डायल करो.” (call_contact) → other
- “فرحان کو ڈیل کرو” (call_contact) → other
- “मेरा को कॉल कर दो” (call_contact) → other
- “इशान को कॉल कर दो.” (call_contact) → other
- “लक्षमी को कॉल कर दो.” (call_contact) → other
- “فرحان کو کال کر دو” (call_contact) → other
- “Să ne jăi cu funcărdu.” (call_contact) → other
- “करन को फोन कर दो.” (call_contact) → other
- “Sua responde o cardôo.” (call_contact) → other
- “इशान को फोन कर दो.” (call_contact) → other
- “लक्षमी को फोन कर दो” (call_contact) → other
- “فرحان کو فون کر دو” (call_contact) → other
- “जरा संजे को कॉल लगाओ” (call_contact) → other
- “जरा मेरा को कॉल लगाओ.” (call_contact) → other
- “Zara devjako kol legav?” (call_contact) → other
- “Zara sureško kol legav.” (call_contact) → other
- “जरा एशान को कॉल लगाओ.” (call_contact) → other
- “जरा फर्हान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ.” (call_contact) → other
- “پوجہ سے بات کراؤ” (call_contact) → other
- “Să înceam zi bat cărau.” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करंसी बात कराओ” (call_contact) → other
- “Divya se bat cărau.” (call_contact) → other
- “Suriș si bat carau.” (call_contact) → other
- “इशान से बात कराओ.” (call_contact) → other
- “लक्षमी से बात कराओ.” (call_contact) → other
- “فرحان سے بات کراؤ” (call_contact) → other
- “टाइम पास कर रहा हूँ.” (other) → time
- “समय बहुत कम है.” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to Deepak.”
- “dial Deepak for me” → “Dial Deepak for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “Ít tất cả sếp lúc.”
- “Suresh ko dial karo” → “सुरेश को डायल करो.”
- “सुरेश से बात कराओ” → “Suriș si bat carau.”

## Synthetic speech through Whisper, pink noise at 10 dB SNR

### Synthetic speech through Whisper, pink noise at 10 dB SNR, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.9% (10/11) | 100.0% (10/10) |
| take_photo | 10 | 100.0% (7/7) | 70.0% (7/10) |
| call_contact | 100 | 97.1% (33/34) | 33.0% (33/100) |
| other | 24 | 23.9% (22/92) | 91.7% (22/24) |

Sensitive local decisions: 40/41 correct. With n=41, the 95% upper bound on the error rate is about 3/n = 7.3% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 8/9 stayed off the phone. Leaked: Time flies..

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 10 | 0 | 0 | 0 |
| take_photo | 0 | 7 | 0 | 3 |
| call_contact | 0 | 0 | 33 | 67 |
| other | 1 | 0 | 1 | 22 |

### Synthetic speech through Whisper, pink noise at 10 dB SNR, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 66.7% (4/6) | 40.0% (4/10) |
| take_photo | 10 | 100.0% (1/1) | 10.0% (1/10) |
| call_contact | 80 | 100.0% (17/17) | 21.2% (17/80) |
| other | 18 | 17.0% (16/94) | 88.9% (16/18) |

Sensitive local decisions: 18/18 correct. With n=18, the 95% upper bound on the error rate is about 3/n = 16.7% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 4/5 stayed off the phone. Leaked: समय बहुत कम है.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 4 | 0 | 0 | 6 |
| take_photo | 0 | 1 | 0 | 9 |
| call_contact | 0 | 0 | 17 | 63 |
| other | 2 | 0 | 0 | 16 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 94.2% | 57.0% |
| 0.60 | 96.4% | 54.0% |
| 0.70 | 96.3% | 52.0% |
| 0.80 | 95.8% | 45.5% |
| 0.90 | 95.8% | 34.5% |
| 0.95 | 98.3% | 29.0% |
| 0.98 | 100.0% | 25.0% |
| 0.99 | 100.0% | 20.5% |

Misrouted:

- “Super picture.” (take_photo) → other
- “Click this.” (take_photo) → other
- “take a snap.” (take_photo) → other
- “Call up D-Pack.” (call_contact) → other
- “Call up to Jack.” (call_contact) → other
- “Call at Mira.” (call_contact) → other
- “call up Surish.” (call_contact) → other
- “Call up Yishan.” (call_contact) → other
- “Please call me now.” (call_contact) → other
- “प्लीज कॉल देविया.” (call_contact) → other
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
- “I want to call Ishan.” (call_contact) → other
- “I want to call Sarhan.” (call_contact) → other
- “Start a call with Puja.” (call_contact) → other
- “Start a call with Mira.” (call_contact) → other
- “Start a call with Ishan.” (call_contact) → other
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
- “All life is cool and hot now.” (call_contact) → other
- “Call Divya now.” (call_contact) → other
- “Call Suresh now.” (call_contact) → other
- “Call me Sean now.” (call_contact) → other
- “Call up me now.” (call_contact) → other
- “Call Sarhan now.” (call_contact) → other
- “Could you phone me back?” (call_contact) → other
- “Could you phone me lah?” (call_contact) → other
- “Could you found the via?” (call_contact) → other
- “Could you phone Ishan?” (call_contact) → other
- “Could you found Lakshmi?” (call_contact) → other
- “Put me through too deep up.” (call_contact) → other
- “Put me through to Pooja.” (call_contact) → other
- “Put me through to Sanjay.” (call_contact) → other
- “Tooth me too to me last.” (call_contact) → other
- “put me through to current” (call_contact) → other
- “put me through two divya.” (call_contact) → other
- “put me through to Suresh.” (call_contact) → other
- “Put me through to Ishan.” (call_contact) → other
- “Put me through to Lakshmi.” (call_contact) → other
- “put me through to Farhan.” (call_contact) → other
- “Time flies.” (other) → time
- “Who is calling?” (other) → call_contact
- “Time to go back.” (time) → other
- “Keep me butt gay.” (time) → other
- “자, 제인 후계야.” (time) → other
- “किपना बजा है।” (time) → other
- “Зараз самай батал.” (time) → other
- “अभी कितने बच रहे हैं।” (time) → other
- “project install” (take_photo) → other
- “पोडो क्लिका रो” (take_photo) → other
- “Es aquí Photolog.” (take_photo) → other
- “だすみゆきちょう。” (take_photo) → other
- “ポイントキーチド?” (take_photo) → other
- “Ít tập trí lục.” (take_photo) → other
- “Esquipotolo.” (take_photo) → other
- “フォートフリックカロー” (take_photo) → other
- “Jalbi Fotolo” (take_photo) → other
- “¿Pulín, caro?” (call_contact) → other
- “संजे को रिंग करो” (call_contact) → other
- “Mira corring caro.” (call_contact) → other
- “Caranco Rincarón.” (call_contact) → other
- “दिव्या को रिंग करो” (call_contact) → other
- “सुरेश को रिंग करो” (call_contact) → other
- “इशान को रिंग करो” (call_contact) → other
- “Lakshmi Korenkarova.” (call_contact) → other
- “फर्हान को विंग करो” (call_contact) → other
- “ذرا دیپاک کو کال کر دو” (call_contact) → other
- “जारसंजे को कॉल कर दो” (call_contact) → other
- “ذرا میرا کو کال کر دو” (call_contact) → other
- “जरा करन को कॉल कर दो” (call_contact) → other
- “जरा दिविया को कॉल कर दो” (call_contact) → other
- “जार इशान को कॉल कर दियो” (call_contact) → other
- “जरा लक्षमी को कॉल कर दो” (call_contact) → other
- “While all that stuff's done to work” (call_contact) → other
- “Deepak Coppon Cardo” (call_contact) → other
- “Look at the phone call.” (call_contact) → other
- “Go phone cardo.” (call_contact) → other
- “Di via Accopeung cards” (call_contact) → other
- “Ishaan Kofon Caldo.” (call_contact) → other
- “परहान को फोन का दो” (call_contact) → other
- “संजे को डियल करो” (call_contact) → other
- “करन को डायल करो” (call_contact) → other
- “पिशान को डायल करो,” (call_contact) → other
- “فرحان کو ڈیل کرو” (call_contact) → other
- “दीपट को कॉल कर दो.” (call_contact) → other
- “पुजा को कॉल कर दो” (call_contact) → other
- “سنجا کو کول کردو” (call_contact) → other
- “Cảm ơn các bạn đã theo dõi và hẹn gặp lại.” (call_contact) → other
- “Девяку сколько двух.” (call_contact) → other
- “Судишь по конкурсу.” (call_contact) → other
- “इशान को कॉल कर दो.” (call_contact) → other
- “नक्षमी को कॉल कर दो” (call_contact) → other
- “पर्षान को कॉल कर दो” (call_contact) → other
- “Bipat po phone ka do” (call_contact) → other
- “Uja kupon kaduk.” (call_contact) → other
- “Senjay Kukun kedua” (call_contact) → other
- “Miracaston Cadu” (call_contact) → other
- “currentstar” (call_contact) → other
- “Девяку фон каду.” (call_contact) → other
- “Sous les scoffres comme cadeau.” (call_contact) → other
- “इशान को फोन कर दो” (call_contact) → other
- “На пшми кухон кадок.” (call_contact) → other
- “पर्षान को सून कर दो” (call_contact) → other
- “जरा दीपत को कॉल लगाओ” (call_contact) → other
- “जरा करन को कॉल लगाओ” (call_contact) → other
- “Zdrażdzi w jakość kolegów.” (call_contact) → other
- “When you put the” (call_contact) → other
- “जरा इशान को कॉल लगाओ” (call_contact) → other
- “Zara lakšniko kol negal.” (call_contact) → other
- “जरब पर्षान को कॉल लगाओ” (call_contact) → other
- “दीपक से बात कराओ” (call_contact) → other
- “पुजास दिबात कराओ।” (call_contact) → other
- “Săncei și bătărău” (call_contact) → other
- “मीरा से बात कराओ” (call_contact) → other
- “करन्सी बात कराओ” (call_contact) → other
- “Diviați de bască rau.” (call_contact) → other
- “Зурис при Баскарау.” (call_contact) → other
- “И шансы баска рау.” (call_contact) → other
- “Лапшми сибат карао.” (call_contact) → other
- “फरहान सी बात कराओ” (call_contact) → other
- “टाइम पास कर रहा हूँ” (other) → time
- “समय बहुत कम है” (other) → time

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “Connect me to the button.”
- “dial Deepak for me” → “Die all the path for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “Ít tập trí lục.”
- “Suresh ko dial karo” → “सुरेश को डायल करो”
- “सुरेश से बात कराओ” → “Зурис при Баскарау.”

## Synthetic speech through Whisper, pink noise at 0 dB SNR

### Synthetic speech through Whisper, pink noise at 0 dB SNR, en (n=144)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 90.0% (9/10) | 90.0% (9/10) |
| take_photo | 10 | 100.0% (4/4) | 40.0% (4/10) |
| call_contact | 100 | 100.0% (7/7) | 7.0% (7/100) |
| other | 24 | 19.5% (24/123) | 100.0% (24/24) |

Sensitive local decisions: 11/11 correct. With n=11, the 95% upper bound on the error rate is about 3/n = 27.3% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 8/8 stayed off the phone.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 9 | 0 | 0 | 1 |
| take_photo | 0 | 4 | 0 | 6 |
| call_contact | 1 | 0 | 7 | 92 |
| other | 0 | 0 | 0 | 24 |

### Synthetic speech through Whisper, pink noise at 0 dB SNR, hi (n=118)

| Intent | n | Precision | Recall |
|:--|--:|--:|--:|
| time | 10 | 100.0% (3/3) | 30.0% (3/10) |
| take_photo | 10 | 0.0% (0/1) | 0.0% (0/10) |
| call_contact | 80 | 100.0% (2/2) | 2.5% (2/80) |
| other | 18 | 15.2% (17/112) | 94.4% (17/18) |

Sensitive local decisions: 2/3 correct. With n=3, the 95% upper bound on the error rate is about 3/n = 100.0% when none fail, so this set cannot show the 99.5% target (that needs about 600 clean decisions). The bound is optimistic: each call template appears once per contact name, so decisions are not independent.

Near misses (cloud utterances that share a word with a local intent): 2/3 stayed off the phone. Leaked: take a photo from camera.

| true \ routed | time | take_photo | call_contact | other |
|:--|--:|--:|--:|--:|
| time | 3 | 0 | 0 | 7 |
| take_photo | 0 | 0 | 0 | 10 |
| call_contact | 0 | 0 | 2 | 78 |
| other | 0 | 1 | 0 | 17 |

### Threshold sweep for sensitive intents (photo, call)

| Threshold | Precision | Recall |
|--:|--:|--:|
| 0.50 | 91.5% | 21.5% |
| 0.60 | 95.2% | 20.0% |
| 0.70 | 94.1% | 16.0% |
| 0.80 | 92.3% | 12.0% |
| 0.90 | 95.0% | 9.5% |
| 0.95 | 92.9% | 6.5% |
| 0.98 | 90.9% | 5.0% |
| 0.99 | 100.0% | 4.0% |

Misrouted:

- “Any idea what sign it is?” (time) → other
- “这个错都没有啊” (take_photo) → other
- “Not a fool” (take_photo) → other
- “卡通了步驟” (take_photo) → other
- “like this.” (take_photo) → other
- “dapat gambar ini” (take_photo) → other
- “Thank you.” (take_photo) → other
- “So you have to eat up.” (call_contact) → other
- “Пол ахуя.” (call_contact) → other
- “Call up Sunday.” (call_contact) → other
- “所以他吃了” (call_contact) → other
- “Call up seven.” (call_contact) → other
- “call after this year.” (call_contact) → other
- “Hold up to it.” (call_contact) → other
- “For your features.” (call_contact) → other
- “like machine” (call_contact) → other
- “So I have to go home.” (call_contact) → other
- “Please call these artists.” (call_contact) → other
- “Please call to John.” (call_contact) → other
- “Please follow Sanjay.” (call_contact) → other
- “He's so young.” (call_contact) → other
- “people” (call_contact) → other
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
- “I want to call Kagem” (call_contact) → other
- “I want to call Vivian” (call_contact) → other
- “I want to phone Yishan” (call_contact) → other
- “I want to call Sarhan.” (call_contact) → other
- “start a call with two jobs” (call_contact) → other
- “start a call with me now.” (call_contact) → other
- “Start a call with Kevin” (call_contact) → other
- “start a call with India” (call_contact) → other
- “start at all with Suresh” (call_contact) → other
- “Start the call with Ishan” (call_contact) → other
- “Start the call with Zanhan” (call_contact) → other
- “Spring indignably fun.” (call_contact) → other
- “Ring of Suja.” (call_contact) → other
- “Ring of Sanjay.” (call_contact) → other
- “뱅맞습니다.” (call_contact) → other
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
- “多三天啊” (call_contact) → other
- “Oh, you mean I know.” (call_contact) → other
- “I've only got a minute now.” (call_contact) → time
- “I'll give you an hour.” (call_contact) → other
- “Call police now.” (call_contact) → other
- “I'm going to be chan now.” (call_contact) → other
- “Call you up to me now.” (call_contact) → other
- “可以上下以後” (call_contact) → other
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
- “name at YouTube 7” (call_contact) → other
- “with me to be here.” (call_contact) → other
- “It took me to the stage.” (call_contact) → other
- “It took me through to Ishan.” (call_contact) → other
- “Put me through to luxury.” (call_contact) → other
- “It took me to do something hard.” (call_contact) → other
- “Get not time to work.” (time) → other
- “感谢后感” (time) → other
- “Типни ботинь.” (time) → other
- “야, 가인 포개야.” (time) → other
- “कितना बजा है।” (time) → other
- “Зараз самая бачалка.” (time) → other
- “अब ही ठिपने बच रहे हैं.” (time) → other
- “nic 땅에서” (take_photo) → other
- “フォートをクリックしております” (take_photo) → other
- “Chelsea photo note” (take_photo) → other
- “qu'est-ce qu'il faut donner ?” (take_photo) → other
- “だすゆうけちょう” (take_photo) → other
- “포토킹으로” (take_photo) → other
- “Y, está aquí, no.” (take_photo) → other
- “It's equal to no.” (take_photo) → other
- “소소 플릭터로” (take_photo) → other
- “जल्वी पोचो लो” (take_photo) → other
- “por rincaros” (call_contact) → other
- “其實 Winzer碰原 insan” (call_contact) → other
- “سندے کو رین کرو” (call_contact) → other
- “Mira tu venta, ¿no?” (call_contact) → other
- “estarán por 20 años.” (call_contact) → other
- “This one can take your excited” (call_contact) → other
- “すれしく連下の” (call_contact) → other
- “निशान को रिल करो” (call_contact) → other
- “Начну ковынь к роботу.” (call_contact) → other
- “for hand to wincaro” (call_contact) → other
- “J'ai là du pas de copain le cadeau.” (call_contact) → other
- “There are food for culture” (call_contact) → other
- “دارہ صندوق کو کون کا دو ہوگا” (call_contact) → other
- “Zara mirato contador” (call_contact) → other
- “The Ratarangku call the door.” (call_contact) → other
- “ज़रा दिखिया तो कॉल कर दो” (call_contact) → other
- “Don't tell your face” (call_contact) → other
- “जाय इशान को कॉल कर दियो” (call_contact) → other
- “there are Lakshmi to call the door” (call_contact) → other
- “nono falhan cooker” (call_contact) → other
- “비팟 통통 다�然” (call_contact) → other
- “先打開” (call_contact) → other
- “산 Diego 공카도” (call_contact) → other
- “Mira tu contador.” (call_contact) → other
- “Go conternutado.” (call_contact) → other
- “Tiveiado o contador.” (call_contact) → other
- “嬉しく本家像” (call_contact) → other
- “Ishan to font a door.” (call_contact) → other
- “Начни к фонтазон.” (call_contact) → other
- “by handbook phone cardo” (call_contact) → other
- “Dibat ko dialkan” (call_contact) → other
- “Sanjay to be answer” (call_contact) → other
- “लीना को डायल परो” (call_contact) → other
- “करन को डायल करो” (call_contact) → other
- “y vi a con la heltero.” (call_contact) → other
- “पिशान को डायल करो,” (call_contact) → other
- “लक्ष्णी को डायल करो” (call_contact) → other
- “for Hanko DL Terro” (call_contact) → other
- “Đi phát của Khoi Kha Đô” (call_contact) → other
- “미자 두천까지log” (call_contact) → other
- “संजे को कॉल कर दो” (call_contact) → other
- “Mira tu call the door.” (call_contact) → other
- “Current hook calls are due.” (call_contact) → other
- “Яphone конца дуриленоварка.” (call_contact) → other
- “turismo contra do” (call_contact) → other
- “इशान को कॉल का दूख” (call_contact) → other
- “Nạc gì cũng có lần cơ đụng.” (call_contact) → other
- “would take my food constantly” (call_contact) → other
- “Дипа кухонка 2.” (call_contact) → other
- “이제 누군가입니다.” (call_contact) → other
- “sans제 funds” (call_contact) → other
- “みらこそんかよ” (call_contact) → other
- “Karen kukuh kaduk” (call_contact) → other
- “Dia berkongsi kedua” (call_contact) → other
- “putting” (call_contact) → other
- “Ishan Pukung Kaduk.” (call_contact) → other
- “Начни по фонкаду.” (call_contact) → other
- “Водхан Кустун Каджук.” (call_contact) → other
- “जरा दीपत को सौन नगाओ करें” (call_contact) → other
- “जरा पूचा कुछ को लगाओ” (call_contact) → other
- “जनक संजय को को लगाओ” (call_contact) → other
- “Let me get the popcorn now.” (call_contact) → other
- “ज़रा करन को कॉल नगाओ” (call_contact) → other
- “Заразили я кухон не гау.” (call_contact) → other
- “Зараз пришлось коль над аудиторией.” (call_contact) → other
- “All right, so we're going to take the TV again.” (call_contact) → other
- “Look at this girl's eye to see what they look like.” (call_contact) → other
- “जरख बहान को को नगाओ” (call_contact) → other
- “Дипа-Стиват-Карау.” (call_contact) → other
- “ham que você vai ter algo..” (call_contact) → other
- “선제시 바스러우” (call_contact) → other
- “Mira que vas, Kraut.” (call_contact) → other
- “currency bars cut out.” (call_contact) → other
- “Двигаясь и баска рау.” (call_contact) → other
- “to reach the water out.” (call_contact) → other
- “Ich halte die Wasser auf.” (call_contact) → other
- “Nachschmied die Waske raus.” (call_contact) → other
- “Verhandt die Wackverrauch.” (call_contact) → other
- “take a photo from camera” (other) → take_photo

Sample transcripts:

- “what is the time” → “What is the time?”
- “connect me to Deepak” → “to make me too big up.”
- “dial Deepak for me” → “Die will be past for me.”
- “how's the weather in delhi” → “How's the weather in Delhi?”
- “एक तस्वीर लो” → “Y, está aquí, no.”
- “Suresh ko dial karo” → “सुरेश को टायल करो”
- “सुरेश से बात कराओ” → “to reach the water out.”
