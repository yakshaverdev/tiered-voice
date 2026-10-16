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
