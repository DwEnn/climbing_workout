# 운동 세션 전수 감사

감사 기준: `validation/spec.yaml`, `validation/source-audit.yaml`
범위: 푸쉬 6개, 코어 8개, 파워 6개, 손가락 신전근 1개
원본 가이드 수정: 없음

## 결론

현재 운동 목록은 구조적으로 완결되지 않았고, 근거 귀속과 세션 통합에도 수정이
필요하다. 21개 중 `유지`는 KB 오버헤드 프레스 1개, `수정`은 9개,
`교체`는 11개다. 운동 자체가 모두 부적절한 것은 아니다. 가장 큰 문제는
직접 근거로 표시한 카드의 저자·대상·운동·용량이 원문과 다르거나, 개별 운동을
한 세션에 모두 쌓았을 때 프레스·행잉·플라이오메트릭 피로가 중복되는 점이다.

세션 평균은 푸쉬 78.3점, 코어 74.8점, 파워 76.5점, 손가락 신전근
60.0점이다. 현재 상태의 세션 판정은 푸쉬 `수정`, 코어·파워 `재설계`,
손가락 신전근 `프로토콜 교체`다.

## 1. 구조 검사

`python3 scripts/validate_guides.py --no-fail`의 재현 결과는 다음과 같다.

- 검사 범위: 4세션, 21개 운동, 내부 레퍼런스 링크 153개
- 상태: `fail`
- 오류: **1개**
- 경고: **22개**
- 끊어진 내부 레퍼런스: 0개

오류 1개는 `guides/finger-extensor-office.html`의 운동 카드 내부에 필수
`sets_reps_rest` 블록이 없는 문제다. 페이지 앞부분의 루틴 요약은 카드 필수
필드를 대신하지 않는다.

경고 22개는 다음처럼 나뉜다.

- 근거 마커 누락 20개: 푸쉬 6개, 코어 8개, 파워 5개
  (홉-앤-스틱 제외), 손가락 신전근 1개 카드의 badge row가 명세의
  `✅/🔶` 요구를 충족하지 않는다.
- 문서 드리프트 2개: `CLAUDE.md` 코어 목록에 앱 롤아웃·팔로프 프레스가
  남고 L-Sit·윈드쉴드 와이퍼가 빠져 있으며, 인덱스 전용 면책 정책과 달리
  “각 페이지 상단”이라고 적혀 있다.

이 1개 오류와 22개 경고는 DOM·명세 정합성 문제다. 아래의 출처 오귀속,
직접성, 세션 중복 판정과는 별도 축이다.

## 2. 21개 운동 근거 감사

하드 실패는 현재 카드의 발행을 막는 문제를 뜻한다. 출처 표기를 바로잡을 수
있고 운동 자체가 타당한 경우에는 하드 실패가 있어도 운동 판정은 `수정`일 수
있다. 반면 미보유 장비나 중요한 안전 문제는 운동 선택에 직접 적용된다.

| 세션 | 운동 / 슬롯 | 확인 근거·Tier | 점수·판정 | 핵심 문제와 하드 실패 | 같은 슬롯 대안 2개 |
|---|---|---|---|---|---|
| 푸쉬 | 견갑골 푸쉬업 / scapular activation | principle · T3 · [근거](https://theclimbingdoctor.com/optimal-training-and-injury-prevention-techniques-for-climbers-with-a-full-time-schedule/) | 79 · 수정 | Vagy가 이 동작을 직접 처방하지 않는다. McClure의 push-up plus로 근거를 바꾸고 치킨윙 예방 단정을 완화해야 한다. HF: 직접 주장 오귀속 | Serratus punch 84; Band reach 82 |
| 푸쉬 | KB 오버헤드 프레스 / vertical press | mixed · T2 · [근거](https://www.powercompanyclimbing.com/blog/2016/01/episode-2-resistance-training-with.html) | 87 · 유지 | Bechtel은 OHP를 직접 추천하지만 정확한 3세트 처방과 항회전 전이는 원칙 적용이다. HF 없음 | Pike push-up 85; Band shoulder press 78 |
| 푸쉬 | 링/다이아몬드 푸쉬업 / horizontal press | mixed · T2·T4·A · [근거](https://latticetraining.com/blog/how-to-structure-your-training/) | 77 · 교체 | 바닥 푸쉬업은 직접 근거가 있으나 링·다이아몬드는 원칙 적용이며 딥스 슬롯과 중복된다. HF 없음 | Floor push-up 85; Single-arm KB floor press 78 |
| 푸쉬 | 링 딥스 / high-intensity press | mixed · T2·T3 · [근거](https://latticetraining.com/blog/training-tips-for-climbers-the-importance-of-antagonist-training-during-performance-phase/) | 71 · 교체 | Hooper의 선호를 일반 처방처럼 쓰고, 인용한 Climbing 글에는 딥스가 없으며 어깨 불안정 시 깊이 제한이 빠졌다. HF: 직접 주장 오귀속 | Band eccentric triceps extension 84; Close-grip floor push-up 79 |
| 푸쉬 | 페이스 풀/밴드 풀어파트 / scapular retraction·ER | principle · T1·T3·T4 · [근거](https://www.climbing.com/skills/antagonist-workouts-for-climbers-improve-performance-and-prevent-injury/) | 83 · 수정 | 현재 출처는 face pull을 직접 처방하지 않고 Wong–Ng 자료는 관찰 연구다. HF: 직접 주장 오귀속 | Standing row-to-cactus 88; Bent-over letter T 83 |
| 푸쉬 | 손목 신전근 훈련 / wrist extensor prehab | mixed · T2·T3·T4·A · [근거](https://www.climbing.com/skills/antagonist-workouts-for-climbers-improve-performance-and-prevent-injury/) | 73 · 교체 | 운동 자체는 직접 추천되지만 그립 향상·부상 예방 효과를 과장했고 저항 설정이 불명확하다. HF 없음 | Wrist extensor-up 84; Light reverse wrist curl 82 |
| 코어 | 데드버그 / motor control·anti-rotation | direct · T3 · [근거](https://theclimbingdoctor.com/low-back-injuries-in-boulderers-preventative-measures-for-chronic-low-back-pain/) | 81 · 수정 | 직접 글의 저자는 Jared Vagy가 아니라 Mike Hwang이며 원문 용량은 측당 4×12, 주 4회다. HF: 직접 주장 오귀속 | Bird dog 79; Pallof press 77 |
| 코어 | L-Sit / static compression | principle · T2 · [근거](https://trainingforclimbing.com/video-complete-core-training-epic-tv-ep-4/) | 61 · 교체 | Hörst가 공개한 5개 코어 루틴에 L-Sit이 없다. 현재 직접 귀속은 검증되지 않았다. HF: 직접 주장 오귀속 | Ring rollout 87; Tuck L-hang 73 |
| 코어 | 할로우 바디 홀드 / anti-extension | mixed · T3 · [근거](https://theclimbingdoctor.com/360-core-power-unlock-full-body-strength-for-climbing/) | 78 · 교체 | 현재 Hörst/Lattice 귀속은 틀렸고 다른 Climbing Doctor 자료로만 직접성을 보완할 수 있다. HF: 직접 주장 오귀속 | Ring rollout 86; Body saw plank 78 |
| 코어 | 행잉 니레이즈/레그레이즈 / hanging hip flexion | direct · T2·T4 · [근거](https://www.powercompanyclimbing.com/blog/2011/06/hardcore.html) | 78 · 수정 | 운동은 직접 지지되지만 현재 Lattice/Metolius 귀속은 맞지 않고 프론트 레버 전 행잉 피로를 늘린다. HF: 직접 주장 오귀속 | Supine reverse crunch 81; Seated compression lift 79 |
| 코어 | 행잉 윈드쉴드 와이퍼 / dynamic rotation | direct · T2 · [근거](https://trainingforclimbing.com/my-favorite-core-exercise-windshield-wipers/) | 77 · 수정 | Hörst가 직접 추천하지만 원문은 6–12회, 2–3세트, 약 3분 휴식이며 현재 60초와 다르다. HF 없음 | Bent-knee windshield wiper 82; Slow cross-body mountain climber 72 |
| 코어 | 사이드 플랭크 프로그레션 / anti-lateral flexion | mixed · T3 · [근거](https://theclimbingdoctor.com/360-core-power-unlock-full-body-strength-for-climbing/) | 73 · 교체 | 주장한 Lattice 상관 데이터가 공개 확인되지 않는다. Tier 1.5를 제거해야 한다. HF: 직접 주장 오귀속 | Banded side plank 83; Suitcase carry in place 72 |
| 코어 | 글루트 브릿지 / posterior chain | principle · T3 · [근거](https://theclimbingdoctor.com/optimal-training-and-injury-prevention-techniques-for-climbers-with-a-full-time-schedule/) | 77 · 수정 | Vagy의 직접 처방을 확인할 수 없다. 직접 논의된 hip-extension 운동의 회귀형으로 표시해야 한다. HF: 직접 주장 오귀속 | Single-leg hip thrust 82; KB Romanian deadlift 80 |
| 코어 | 프론트 레버 프로그레션 / integrated pull-core | direct · T2 · [근거](https://trainingforclimbing.com/video-complete-core-training-epic-tv-ep-4/) | 73 · 교체 | Hörst의 직접 근거는 있으나 여러 행잉 운동 뒤 마지막 배치와 60–90초 휴식이 품질을 해친다. HF 없음 | 세션 첫 Tuck front lever 84; Ring rollout 83 |
| 파워 | 파워 풀업 / explosive pull | direct · T2 · [근거 1](https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/) · [근거 2](https://trainingforclimbing.com/power-training-chest-bump-pull-up/) | 82 · 수정 | 6개 플라이오메트릭 글은 Eric Hörst가 아니라 Lucie Hanes의 글이다. Hörst의 직접 글은 별도다. HF: 직접 주장 오귀속 | Chest-bump pull-up 86; Band-assisted power pull-up 78 |
| 파워 | 파워 푸쉬업 / explosive push | direct · T2 · [근거](https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/) | 84 · 수정 | 동작은 직접 추천되지만 저자를 Hörst로 잘못 적고, 글에 없는 전체 세션 설계를 원문 처방처럼 썼다. HF: 직접 주장 오귀속 | Incline power push-up 82; Kneeling clap push-up 78 |
| 파워 | 박스 점프 / bilateral lower power | direct · T2 · [근거](https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/) | 74 · 교체 | 보유 장비에 박스가 없다. 벤치나 계단은 안전한 임시 착지대로 인정할 수 없다. HF: 미보유 필수 장비 | Squat jump + stick landing 85; Broad jump + stick landing 80 |
| 파워 | 점프 런지 / unilateral lower power | direct · T2 · [근거](https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/) | 77 · 수정 | 직접 목록에는 있으나 현재 올인원 세션의 하체 플라이오메트릭 총량이 과하다. HF 없음 | Split-squat jump 79; Step-up knee drive 73 |
| 파워 | 싱글레그 래터럴·사선 홉-앤-스틱 / landing control | principle · A·T3 · [근거](https://pmc.ncbi.nlm.nih.gov/articles/PMC6922560/) | 74 · 교체 | RCT 대상은 클라이머가 아닌 만성 발목 불안정 남자 대학 농구선수다. 복합 진행은 원칙 적용이다. HF: 직접 주장 오귀속 | Low single-leg hop-and-stick 82; Star-excursion reach 78 |
| 파워 | 마운틴 클라이머 / fast knee-drive core | direct · T2 · [근거](https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/) | 68 · 교체 | 출처 목록에는 있지만 15개 파워 세트 뒤에는 최대 파워가 아닌 컨디셔닝이 된다. HF 없음 | Band-resisted high-knee drive 74; High-knee run in place 72 |
| 손가락 | 고무밴드 손가락 스프레드 / finger extensor prehab | mixed · T1·T2·T3·T4 · [근거](https://www.frontiersin.org/journals/sports-and-active-living/articles/10.3389/fspor.2023.1243354/full) | 60 · 교체 | 동작 추천은 있으나 매일 저강도 4–6세트와 부상 예방 약속은 인용 용량·결과와 맞지 않는다. HF: 직접 주장 오귀속 | High-resistance isometric extension 89; Carabiner-band 10-second expansion 81 |

`direct`는 확인 가능한 출처가 해당 운동을 클라이머에게 명시적으로 추천한다는
뜻이고, `principle`은 타 집단 연구나 일반 원칙의 적용이다. `mixed`는 같은
카드에 두 성격의 주장이 함께 있다는 뜻이다.

## 3. 세션 통합 판정

### 푸쉬 — 수정

OHP는 유지하되 세 개의 강한 프레스 슬롯을 모두 누적하지 않는다.
`견갑 활성화 2세트 → OHP 3세트 → 푸쉬업 또는 딥스 계열 3세트 →
row-to-cactus 3세트 → 손목 신전 2~3세트`로 줄이고 푸쉬업·딥스는 A/B로
교대한다. 근거 오류와 별개로 현재 구성은 수평 프레스와 고강도 프레스가
중복되어 30–40분 조건과 회복 품질을 해친다.

### 코어 — 재설계

현재 24세트와 다수의 행잉·당기기 운동은 주 2회 35–45분 세션으로 과하다.
A/B 15–20분 모듈로 나눈다.

- A: 데드버그, ring rollout 또는 hollow, side plank, glute bridge
- B: front lever를 첫 운동으로 수행하고 hanging raise와 windshield wiper
  중 하나만 선택

윈드쉴드 와이퍼를 유지하면 원문에 가깝게 2–3세트와 약 3분 휴식을 확보한다.

### 파워 — 재설계

6운동 18세트 대신 상체 pull/push 두 슬롯과 하체 파워 또는 착지 제어 한
슬롯을 합친 3–4운동 회전 모듈로 줄인다. 홉-앤-스틱은 피로 전에 수행하고,
마운틴 클라이머는 별도 컨디셔닝으로 이동한다. 박스가 없으므로 불안정한
벤치·계단이 아니라 squat jump + stick landing을 쓴다.

### 손가락 신전근 — 프로토콜 교체

사무실 밴드 스프레드는 저강도 움직임 옵션으로만 남기고 부상 예방을 약속하지
않는다. 근력 프로토콜은 현재 직접 연구가 시험한 주 2회 고저항 등척성
4세트와 분리한다. 통증·최근 손가락 부상이 있으면 운동 처방보다 개별 평가가
우선이다.

## 4. 문서 드리프트와 검증 한계

- `CLAUDE.md`의 코어 운동 목록과 면책 위치 설명을 최신 명세에 맞춰야 한다.
- 이 eval은 웹을 다시 탐색하지 않고 `validation/source-audit.yaml`에 이미
  기록된 검증 결과와 URL을 사용했다. 접근 불가·페이월 세부는 새로 추정하지
  않았다.
- 점수는 프로그램 선택을 위한 비교 도구이며 임상 진단이 아니다.
- 감사 결과만으로 네 HTML 가이드에는 어떤 수정도 하지 않았다.
