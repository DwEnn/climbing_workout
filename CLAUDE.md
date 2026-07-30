# CLAUDE.md — 클라이머 훈련 가이드 웹페이지 제작 지침

## 프로젝트 개요

볼더러를 위한 훈련 가이드 웹페이지를 제작한다. 페이지는 **주력/보조 2계층**으로 나뉜다.
용어 정의는 [CONTEXT.md](./CONTEXT.md)를 따른다.

**주력 훈련** — 등반 수행력을 직접 결정하는 능력. 지배 제약은 조직 회복(간격이 프로토콜의 일부)
- **행보드 세션 (손가락 굴곡근 최대근력)** — Abrahangs + Max Hangs

**보조 훈련** — 등반만 해서는 훈련되지 않는 부위를 채운다. 지배 제약은 볼륨 상한(전체의 25% 이하)
- **푸쉬 세션 (대항근 훈련)** — 가슴·삼두·어깨 중심
- **코어 세션 (근지구력 훈련)** — 전면·후면 코어 포함
- **파워 세션 (플라이오메트릭)** — 폭발적 전신 파워 (다이노·데드포인트·컴프레션)
- **손가락 신전근 (사무실 프리햅)** — 굴곡근 과사용 대항

모든 페이지는 같은 **디자인 시스템**을 공유한다. **출처 체계(증거 집적)는 보조 훈련 페이지에만 적용**된다 — 아래 "증거 집적의 적용 범위" 참고.

### ⚠️ 이 문서의 우선순위

`validation/spec.yaml`이 **단일 진실**이며, 이 문서는 그보다 아래다:

```
validation/spec.yaml > latest_intentional_git_commits > guide_html > CLAUDE.md
```

운동 구성·검증 판정·대상 프로필(`athlete_profile`)이 `spec.yaml`과 어긋나면 **`spec.yaml`이 맞다.** 이 문서를 고쳐서 spec을 이기려 하지 말 것. 가이드를 수정하면 `scripts/validate_guides.py`가 `FINAL_AUDIT_GUIDE_CHANGED`로 해시 불일치를 잡으므로 **재채점이 필요**하다.

## 사용 장비

케틀벨 8kg × 1, 푸쉬업 바, 풀업바, 손가락 행보드, **짐링(gymnastic rings)**, 저항 밴드, 고무밴드(손가락용)

---

## 출처 기준 — 이 프로젝트의 핵심 원칙

**근거 없는 추천은 싣지 않는다.** 다만 근거를 *표기하는 단위*는 문서 유형에 따라 다르다.

### 증거 집적의 적용 범위 ⚠️ 검증 시 반드시 확인

"증거 집적"이란 아래 4개 장치의 묶음을 말한다 — ① 운동별 Tier 뱃지(✅/🔶) ② 인라인 번호 레퍼런스 `[n]` + 하단 목록 ③ "출처 기준" 아코디언 섹션 ④ 운동 카드 8요소 구조.

| 문서 유형 | 해당 페이지 | 표기 단위 | 증거 집적 |
|---|---|---|---|
| **카탈로그형** — 운동마다 출처가 다름 | 보조 훈련 4개 (푸쉬·코어·파워·손가락 신전근) | 운동별 | **적용** |
| **프로토콜형** — 페이지 전원이 한 출처 | 주력 훈련 (행보드 세션) | 페이지 수준 | **적용하지 않음** |

프로토콜형 페이지는 대신 다음을 지킨다:
- 1차 출처를 페이지 상단에 명시 (저자·연도·저널·링크)
- 연구 설계의 **한계를 명시** (예: 후향적 관찰연구 → 인과 주장 금지)
- 운동별 Tier 뱃지를 달지 않는 **이유를 독자에게 설명** (뱃지를 달 단위가 없기 때문임을 밝힌다)

> **행보드 세션은 근거가 약해서 면제되는 게 아니다.** Gilmore et al. (2024)는 peer-reviewed(Tier 1)로, 이 사이트에서 가장 강한 출처에 속한다. 페이지 전체가 그 한 논문의 프로토콜이라 운동별로 쪼갤 출처가 없는 것이다.
>
> **검증·코드리뷰 시:** 행보드 페이지에 Tier 뱃지·번호 레퍼런스·출처 기준 아코디언이 없는 것은 **위반이 아니다.** 반대로 위 3개 항목(1차 출처·한계·이유 설명)이 빠졌다면 그것이 위반이다.

### Tier 체계

| Tier | 정의 | 예시 |
|------|------|------|
| **Tier 1** | Peer-reviewed 학술 연구 | Wong & Ng (2009) — J. Athletic Training; Stien et al. (2023) — 저항 훈련 메타분석 |
| **Tier 1.5** | 대규모 실무 데이터셋 (peer-reviewed 아님) | Lattice Training 독점 데이터베이스 — 세계 최대 클라이머 퍼포먼스 메트릭. 등급별 벤치마크 (예: 사이드 플랭크 홀드 시간과 등급 상관관계) |
| **Tier 2** | 공인 자격 클라이밍 전문 코치/저자 | Steve Bechtel (CSCS, Climb Strong), Lattice Training (Torr, Randall, Procter), Eric Hörst (Training for Climbing) |
| **Tier 3** | 클라이밍 전문 의료 전문가 | Dr. Jared Vagy DPT (The Climbing Doctor), Dr. Esther Smith DPT (Grassroots PT), Hooper's Beta (DPT) |
| **Tier 4** | 클라이밍 전문 미디어 | Climbing Magazine, Gripped Magazine, Power Company Climbing Podcast, TrainingBeta, UKClimbing, improve-climbing.com |
| **Tier A** | 인접 학문 (일반 운동과학) | NSCA/ACSM 확립 원리를 클라이밍에 적용. 클라이밍 특화 RCT보다 근거가 강한 경우 있음. 🔶 표기하되 근거 강도를 별도 명시 |

### 검증 수준 표기

각 운동 카드에 반드시 아래 중 하나를 뱃지로 표시:

- **✅ 직접 검증** — 위 Tier 1~4 소스에서 해당 운동을 클라이머에게 **명시적으로 추천**한 기록이 확인됨
- **🔶 원칙 적용** — 출처에서 **훈련 원칙**은 확인되었으나, 해당 **특정 운동**의 직접 추천은 미확인. 일반 운동과학에서는 검증됨. 어떤 원칙에서 도출되었는지 반드시 명시

### 출처 귀속 규칙

- 발언/주장은 실제로 말한 사람에게 귀속. 같은 기사에 나온 다른 사람의 발언을 혼동하지 않는다
- 인라인 레퍼런스 번호 `[1]`, `[2]` 등을 사용하고, 페이지 하단에 전체 레퍼런스 목록을 배치
- 레퍼런스 번호는 클릭 시 해당 항목으로 스크롤

### 면책 고지

공통 면책 고지는 `index.html`에 둔다. 개별 운동 카드에서는 직접 근거와
원칙 적용을 구분하고, 통증·부상·복귀 판단이 필요한 경우 전문가 평가를
우선하도록 안내한다. 근거가 없는 포괄적 효과나 부상 예방 보장은 사용하지 않는다.

프로토콜형 페이지(행보드)는 사이트 고지를 반복하지 않되, **자기 1차 출처의
연구 설계상 한계**를 Hero에 명시한다 (예: 후향적 관찰연구 → 인과 주장 금지).

---

## 운동 카드 구조

**적용 대상: 보조 훈련 페이지.** 주력 훈련(프로토콜형) 페이지는 이 구조를 따르지 않는다 — "증거 집적의 적용 범위" 참고.

각 운동은 아래 구조를 따른다:

1. **제목 + 서브타이틀** (영문 운동명 + 한줄 설명)
2. **근거 Tier 뱃지** (✅ 또는 🔶 + Tier 번호 + 출처명)
3. **참고 영상** (YouTube 썸네일 링크)
4. **원문 근거** — 어떤 출처에서 뭐라고 했는지. 인라인 레퍼런스 번호 포함
5. **클라이밍 연관성** — 이 운동이 벽에서 어떤 상황에 도움되는지
6. **세트/렙/휴식 카드**
7. **프로그레션 테이블** (Lv.1 ~ Lv.4)
8. **검증 수준 callout** — Tier 뱃지 + 한줄 요약

🔶 원칙 적용 운동의 경우, "원문 근거" 블록에 **적용된 원칙**과 **해당 원칙의 출처**를 명시해야 한다. "클라이밍 연관성"은 "(원칙 기반 추론)"으로 표기.

---

## 페이지별 운동 목록

### 행보드 세션 (주력) — `guides/fingerboard-training-guide.html`

**설계 원칙: 단일 1차 출처의 프로토콜을 그대로 옮긴다.** 출처는 Gilmore, Klimek, Abrahamsson & Baar (2024) [F-1] 하나이며, Tier 1(peer-reviewed)이지만 후향적 관찰연구이므로 인과를 주장하지 않는다. 운동별 Tier 뱃지·번호 레퍼런스·운동 카드 8요소는 적용하지 않는다.

| 운동 | 역할 | 처방 | 근거 |
|------|------|------|------|
| Abrahangs | 저강도 등척성 · 빈번한 자극 | 18~22mm, 발 바닥, 전완에 작은 긴장(표 기준 40~60% BW), 10초/20초, 주 3회 | [F-1] |
| Max Hangs | 고강도 최대근력 | 20mm strict half crimp, 총부하의 85~95%, 10초 × 6회, 2분 휴식, 2주 1회부터 | [F-1] |

**논문에서 벗어난 부분(반드시 구분 표기):**
- 논문 프로토콜은 85/90/95%를 모두 포함하지만, 페이지는 **85% 시작**을 권한다 — 등반 볼륨을 함께 감당해야 하므로 보수적으로 잡은 것
- A주/B주 2주 사이클의 **요일 배치는 예시**다. 등반 주 2회를 가정했으며, 지켜야 하는 것은 요일이 아니라 간격(고강도 사이 48~72h)
- 8주 난이도 조절 표는 논문에 없는 진행 계획이다

**측정 vs 훈련 초 수:** 1RM 측정은 **7초** 기준(Finger Strength Assessment), 훈련 세트는 **10초** 홀드. "10초 1RM"이라는 값은 존재하지 않는다.

**장비 제약:** 보유 중량물은 케틀벨 8kg 하나 → 추가무게 상한 약 **+8kg**. 그 이상이 필요하면 ① 배낭 보충 또는 ② 엣지 축소로 대체하되, ②는 **1RM 재측정 필요**(엣지가 바뀌면 기존 1RM이 무효).

### 푸쉬 세션

| 운동 | 검증 | 핵심 출처 | 비고 |
|------|------|----------|------|
| 푸쉬업 플러스 | ✅ | McClure / The Climbing Doctor | 견갑 전인 활성화 |
| KB 오버헤드 프레스 | ✅ + 🔶 | Bechtel + 일반 프로그래밍 원칙 | 8kg 단일 케틀벨에 맞춘 단팔 진행 |
| 플로어 푸쉬업 프로그레션 | ✅ + 🔶 | Climbing Magazine + 용량 조정 | 링 없이 안정된 바닥부터 진행 |
| 밴드 편심 삼두 신전 | ✅ + 🔶 | Vagy + 장비·용량 조정 | 3~4초 편심 |
| 스탠딩 로우-투-캑터스 | ✅ | Climbing Magazine | 후인·외회전 결합 |
| 손목 익스텐서-업 | ✅ | Climbing Magazine | 저부하 고반복 |

### 코어 세션

**설계 원칙: 주 1회, 30~40분 코어 전용 통합 세션.**
데드버그 2세트로 준비한 뒤 턱 프론트 레버를 첫 주운동으로 수행한다.
링 롤아웃과 사용자가 선택한 행잉 니/레그레이즈를 거쳐 밴드
안티로테이션 할로우와 밴드 사이드 플랭크로 마무리한다.

| 운동 | 패턴 | 검증 | 핵심 출처 |
|------|------|------|----------|
| 데드버그 | 운동 제어 | ✅ + 🔶 | Mike Hwang / The Climbing Doctor + 세션 용량 조정 |
| 링 롤아웃 | 항신전 | ✅ | Hörst / TrainingBeta |
| 밴드 안티로테이션 할로우 홀드 | 항회전 | ✅ | The Climbing Doctor |
| 행잉 니/레그레이즈 | 고관절 굴곡 | ✅ | Power Company Climbing |
| 밴드 사이드 플랭크 | 항측굴 | ✅ | The Climbing Doctor |
| 턱 프론트 레버 프로그레션 | 당김+코어 통합 | ✅ | Hörst / Gripped / Power Company |

> **중복 제어:** 동적 행잉 코어는 행잉 니/레그레이즈 하나만 사용한다.
> 윈드쉴드 와이퍼는 활성 세션에서 제거해 그립·어깨 매달림 피로를 제한한다.

### 파워 세션 (플라이오메트릭)

**설계 원칙: 최대 파워 품질을 위한 4운동 세션.**
낮은 싱글레그 홉으로 착지 제어를 확인한 뒤 파워 풀업과 파워 푸쉬업을
수행한다. 하체 파워는 스쿼트 점프와 점프 런지 중 하나만 선택한다.
박스가 필요한 박스 점프는 장비 게이트에서 탈락했고, 마운틴 클라이머는
최대 파워 세션 통합 게이트를 통과하지 못해 별도 컨디셔닝 옵션으로 이동했다.

| 운동 | 패턴 | 검증 | 핵심 출처 |
|------|------|------|----------|
| 파워 풀업 | 폭발적 당김 | ✅ | Hanes [P-1], Hörst 별도 글 |
| 파워 푸쉬업 | 폭발적 밀기 | ✅ | Hanes [P-1] |
| 스쿼트 점프 + 스틱 랜딩 | 양측성 하체 파워 | ✅ + 🔶 | White-Graff 착지 단계 + ACE 스쿼트 점프 |
| 점프 런지 | 단측성 하체 파워 | ✅ + 🔶 | Hanes [P-1] + 접촉 수 조정 |
| 낮은 싱글레그 홉-앤-스틱 | 착지 제동·발목 제어 | ✅ + 🔶 | White-Graff/Hedges + hop-stabilization RCT |

> **타이밍 주의 (다른 세션과 반대):** 푸쉬·코어는 클라이밍 직후에 붙이지만, 파워 훈련은 **신선할 때만** 제대로 된다. Hörst: "피로한 상태에서는 파워를 제대로 훈련할 수 없다." → 워밍업 후 본격 등반 전, 또는 등반 볼륨이 가벼운 날에 배치. 주 1~2회.
>
> **장비 주의:** 보유 장비에 박스가 없으므로 가구나 불안정한 벤치를
> 대체 박스로 사용하지 않는다. 파워 풀업은 당김 계열이라 주간 당김
> 볼륨(클라이밍 + 프론트 레버)에 합산한다.
>
> **발목 모듈(EX05 래터럴 홉-앤-스틱) 근거 구분:** Hörst 플라이오 글에는 발목 특화 내용이 없고, hop-stabilization의 클라이밍 퍼포먼스 전이는 🔶 Tier A로 표기. hop-stabilization RCT [P-6]는 peer-reviewed지만 **대상이 농구선수(클라이머 아님)**라 전이는 원칙 기반 추론. 반면 **착지 메커닉스·측면 홉·발목 반응 훈련**은 볼더링 발목 염좌(클라이머 하체 부상 1위) 예방으로 Vagy [P-4]·Hooper's Beta [P-5]·Hedges/Climbing Doctor [P-8](Tier 3)가 직접 추천 → 이 부분은 ✅. 한 카드에 ✅/🔶를 함께 달되 어느 부분이 어느 근거인지 명시. 주 가치는 파워가 아니라 부상예방·풋워크 지지 (고관절 가동성이 더 높은 우선순위).
>
> **주의 (검증에서 확인된 사항):** ① hop-stabilization 연구의 구체적 홉 거리(예: 30cm/40cm)는 접근 가능한 논문에 명시돼 있지 않음 → 페이지에는 "연구 수치가 아닌 실전 시작값"으로만 표기. ② The Climbing Doctor의 발목 재활 홉 진행 콘텐츠 저자는 **Nicholas Hedges(게스트 DPT)**이며 Vagy가 아님 → 귀속 구분.

---

## 레퍼런스 목록

### 공통 (두 페이지에서 공유)

```
[1]  Wong & Ng (2009). J. Athletic Training, 44(5), 527–530.
     https://pmc.ncbi.nlm.nih.gov/articles/PMC2742463/
[2]  Bechtel, S. PCC Podcast Ep.2 — Resistance Training.
     https://www.powercompanyclimbing.com/blog/2016/01/episode-2-resistance-training-with.html
[3]  Bechtel, S. TrainingBeta Podcast Ep.80.
     https://www.trainingbeta.com/media/steve-bechtel-3/
[4]  Torr, O. (2023). Lattice Training — Antagonist Training During Performance Phase.
     https://latticetraining.com/blog/training-tips-for-climbers-the-importance-of-antagonist-training-during-performance-phase/
[5]  Procter, J. (2025). Lattice Training — How to Structure Your Training.
     https://latticetraining.com/blog/how-to-structure-your-training/
[6]  Randall, T. UKClimbing — Lattice Series Part 4: Conditioning & Mobility.
     https://www.ukclimbing.com/articles/skills/series/lattice_training_series_with_tom_randall/part_4_conditioning+mobility-11396
[7]  Vagy, J. (2015). The Climbing Doctor — Antagonist Muscle Strength.
     https://theclimbingdoctor.com/how-to-train-antagonist-muscle-strength-for-climbing/
[8]  Vagy, J. The Climbing Doctor — Antagonist Strength Exercises.
     https://theclimbingdoctor.com/rock-climbing-injury-tips-antagonist-strength-exercises/
[9]  Slavsky, B. (2019). Climbing Magazine — Antagonist Workouts for Climbers.
     https://www.climbing.com/skills/antagonist-workouts-for-climbers-improve-performance-and-prevent-injury/
[10] Vagy, J. Climb Injury-Free. (서적)
[11] Bechtel, S. & Manganiello, C. Unstoppable Force. (서적)
[12] REI Expert Advice — How to Prevent Climbing Injuries.
     https://www.rei.com/blog/climb/how-to-climb-injury-free
```

### 푸쉬 세션 추가

```
[13] Hooper's Beta — Top 12 WORST Exercises for Climbers.
     https://www.hoopersbeta.com/library/top-12-worst-exercises-for-climbers-that-everyone-does
[14] improve-climbing.com — Antagonist Training Climbing: 20 Best Exercises.
     https://www.improve-climbing.com/antagonist-training-climbing/
[15] UKClimbing — The Importance of Antagonistic Training for Climbers.
     https://www.ukclimbing.com/articles/skills/the_importance_of_antagonistic_training_for_climbers-7364
[16] McClure, G. — Optimal Training and Injury Prevention.
     https://theclimbingdoctor.com/optimal-training-and-injury-prevention-techniques-for-climbers-with-a-full-time-schedule/
[17] Hanes, L. (2024). Training for Climbing — 6 Plyometric Exercises.
     https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/
[18] Sciolino, C. "Train Like A Guide." Climbing Magazine. — TGU 5회 × 3세트 처방.
     https://www.climbing.com/skills/freaky-fit/
[19] Corsaro, P. "Kettlebells for Climbers." Power Company Climbing Podcast.
     https://www.powercompanyclimbing.com/blog/2016/3/21/episode
```

### 코어 세션 추가

```
[C-1] Hörst, E. EpicTV — Complete Core Training Ep.4. / TrainingBeta 정리.
      https://trainingforclimbing.com/video-complete-core-training-epic-tv-ep-4/
      https://www.trainingbeta.com/complete-core-training-eric-horst/
[C-2] Hörst, E. Training for Climbing 3판. (서적) — 코어 훈련 전용 챕터.
[C-3] Hörst, E. Conditioning for Climbers. (서적)
[C-4] Lattice (Hadley, J.) UKClimbing — Training the Upper Body at Home.
      https://www.ukclimbing.com/articles/skills/series/lattice_home_training/
[C-5] Randall, T. Lattice — Front Lever Goals.
      https://latticetraining.com/blog/front-lever-goals-tom-randall/
[C-6] Gripped Magazine — Learning How to Front Lever for Climbing.
      https://gripped.com/indoor-climbing/learning-how-to-front-lever-for-climbing/
[C-7] Vagy & Hörst — Optimal Training and Injury Prevention. (= [16]과 동일)
[C-8] Vagy, J. "Low Back Injuries in Boulderers." The Climbing Doctor. — 데드버그 직접 처방.
     https://theclimbingdoctor.com/low-back-injuries-in-boulderers-preventative-measures-for-chronic-low-back-pain/
```

### 파워 세션 추가

```
[P-1] Hanes, L. (2024). "6 Plyometric Exercises to Boost Climbing Power." Training for Climbing.
      https://trainingforclimbing.com/6-plyometric-exercises-to-boost-climbing-power/
      — 6개 운동 전부를 직접 추천 + 수행법/클라이밍 적용/시연 영상 제공 (1차 출처).
[P-2] Hörst, E. Training for Climbing 3판. (서적) — 파워/파워 지구력 훈련 챕터.
[P-3] Haff, G.G. & Triplett, N.T. (eds.) Essentials of Strength Training and Conditioning
      (4th ed.). NSCA / Human Kinetics. — 플라이오메트릭 원리 (Tier A: SSC, 근력 기반, 회복).
[P-4] White-Graff, A.J. "The Gym Boulder's Guide to Preventing Lower Body Injuries While
      Jumping/Landing/Falling." The Climbing Doctor. (Tier 3) — 착지 메커닉스, 발목 부상 예방.
      https://theclimbingdoctor.com/the-gym-boulders-guide-to-preventing-lower-body-injuries-while-jumping-landing-falling/
[P-5] Hooper, J. "How to Fix Ankle Pain for Climbers." Hooper's Beta. (Tier 3) — 염좌 후
      고유수용성 저하, 점진적 플라이오 진행의 재발 예방.
      https://www.hoopersbeta.com/library/how-to-heal-ankle-injury-back-to-100-climbing
[P-6] Ardakani, M.K., Wikstrom, E.A., et al. (2019). "Hop-Stabilization Training and Landing
      Biomechanics in Athletes With Chronic Ankle Instability: A RCT." J. Athletic Training.
      (Tier A) — 좌우·앞뒤·지그재그·4방향 홉(최종 2Hz)로 착지 역학 개선. 대상: 남자 대학
      농구선수(클라이머 아님) → 전이는 원칙 기반 추론. https://pubmed.ncbi.nlm.nih.gov/31618073/
[P-7] Massachusetts General Brigham Sports Medicine. "Rehabilitation Protocol for Lateral
      Ankle Sprain: non-operative management." — 진행 기준 싱글레그 힐레이즈 25회 + Y/Star
      balance 80%; 복귀 기준 Y-balance·홉 대칭 90% + 통증·붓기 증가 없음.
      https://www.massgeneral.org/assets/MGH/pdf/orthopaedics/sports-medicine/physical-therapy/rehabilitation-protocol-for-ankle-sprain.pdf
[P-8] Hedges, N. (DPT). "Rock Climbing Injury: Ankle Sprain Rehab." The Climbing Doctor.
      (Tier 3) — 클라이머용 발목 재활: 정적 균형 → 앞뒤 홉 → 좌우 홉 → 한발 진행, 스텝오프
      착지 드릴. ⚠️ The Climbing Doctor 게스트 저자(Vagy 아님).
      https://theclimbingdoctor.com/ankle-sprain-assessment-and-rehab/
```

### 행보드 세션 (주력)

행보드 페이지는 프로토콜형이라 인라인 번호 레퍼런스를 쓰지 않는다. 아래는 기록용 등록이며, 페이지에는 "출처" 섹션에 서술형으로 실린다.

```
[F-1] Gilmore, S.L., Klimek, A., Abrahamsson, R. & Baar, K. (2024). "Effects of Different
      Loading Programs on Finger Strength in Rock Climbers." Sports Medicine – Open.
      (Tier 1 — peer-reviewed, 단 후향적 관찰연구)
      https://link.springer.com/article/10.1186/s40798-024-00793-7
      — Crimpd 앱 훈련 로그의 후향적 분석. Max Hangs / Abrahangs / Both 세 그룹 비교.
        Both 그룹 분류 기준: Abrahangs 주 3회 이상 + Max Hangs 주 0.5회 이상.
        Finger Strength Assessment: 약 20mm 엣지, strict half crimp, 7초 성공 기준,
        세트 사이 2분, 최대 5kg씩 증량.
      ⚠️ 한계: 무작위 배정 없음, 전체 클라이밍 볼륨 미통제, Abrahangs 실제 부하 미통제
        → 연관성만 보여주며 인과를 주장할 수 없다. 페이지에 이 한계를 명시해야 한다.
```

---

## 디자인 시스템

### 공통 규칙
- 다크 테마 (`#0a0a0c` 계열 배경)
- 한국어 본문, 운동명은 영문 병기
- Noto Sans KR + JetBrains Mono (수치/코드용)
- 페이지 전체 단일 HTML 파일 (외부 JS 프레임워크 없음)
- Intersection Observer 기반 fade-in 애니메이션
- Sticky TOC 네비게이션
- 반응형 (640px 브레이크포인트)

### 페이지별 악센트 색상
- **행보드 세션**: `--accent: #22c55e` (그린 계열)
- **푸쉬 세션**: `--accent: #e94560` (레드 계열)
- **코어 세션**: `--accent: #ff6b35` (오렌지 계열)
- **파워 세션**: `--accent: #6366f1` (인디고 계열)
- **손가락 신전근**: `--accent: #4ecdc4` (틸 계열)

새 악센트를 고를 때는 아래 뱃지 색상 및 위 목록과 충돌하지 않는 색조를 쓴다.
**이미 점유된 색조:** 로즈(`#e94560` 푸쉬 / `#ef476f` --red) · 오렌지(`#ff6b35` 코어 / `#f4a261` Tier A) · 인디고(`#6366f1` 파워) · 퍼플(`#a855f7` Tier 3) · 틸(`#4ecdc4` 신전근 = Tier 1) · 블루(`#118ab2` Tier 2) · 옐로(`#ffd166` 🔶 원칙 적용) · 그린(`#22c55e` 행보드).

> ⚠️ 틸(`#4ecdc4`)은 손가락 신전근 악센트와 Tier 1 뱃지가 **같은 값을 공유**한다. 기존 상태이며 의도된 것은 아니다. 새 페이지에서 이 패턴을 따라하지 말 것 — 악센트와 뱃지 색은 분리한다.
>
> 페이지 CSS에서 **뱃지·의미 토큰(`--tier1`~`--tierA`, `--green`, `--yellow`, `--red`, `--blue`)은 모든 페이지에서 같은 값**이어야 한다. 페이지마다 달라지는 것은 `--accent` / `--accent-glow` 둘뿐이다. 같은 토큰 이름에 다른 값을 넣지 말 것.

### 뱃지 색상
- ✅ 직접 검증 Tier 1: `#4ecdc4` 배경 (`var(--tier1)`)
- ✅ 직접 검증 Tier 2: `var(--blue)` 배경 (`#118ab2`)
- ✅ 직접 검증 Tier 3: `#a855f7` 배경
- ✅ 직접 검증 Tier 4: `var(--text-dim)` 배경 (`#8a8a95`)
- 🔶 직접 검증 Tier A (일반 운동과학): `#f4a261` 배경 — 클라이밍 특화 아님을 별도 명시
- 🔶 원칙 적용: `var(--yellow)` 배경 (`#ffd166`) — 직접 검증과 시각적으로 명확히 구분

### 핵심 컴포넌트

**보조 훈련 페이지 전용** (프로토콜형 페이지에는 요구되지 않음 — "증거 집적의 적용 범위" 참고):
- **운동 카드**: section.fade-in 단위, 내부에 뱃지 → 영상 → 원문 근거 → 클라이밍 연관 → 세트/렙 카드 → 프로그레션 테이블 → 검증 수준 callout
- **세트/렙 카드**: 3컬럼 그리드 (세트, 반복, 휴식)
- **프로그레션 테이블**: Lv.1~4 색상 구분 뱃지
- **세션 순서**: order-flow (가로 화살표, 모바일에서 세로 전환)
- **출처 기준 섹션**: 아코디언 UI로 Tier 1~4 설명
- **레퍼런스 섹션**: 번호 리스트, 외부 링크 포함

**모든 페이지 공통:**
- **sticky 네비**: 페이지 내 모든 섹션을 빠짐없이 링크할 것 (섹션에 `id`가 있으면 네비 항목도 있어야 함)
- **fade-in**: 모든 `<section>`에 `.fade-in` + Intersection Observer
- **맨 위로 버튼**: `.back-to-top`, 400px 스크롤 후 노출

**행보드 세션(프로토콜형) 고유 컴포넌트:**
- **2주 사이클 타임라인**: `.timeline` / `.day` — 요일 라벨 + 내용 박스, 640px에서 세로 전환
- **무게 계산기**: 총부하 입력 3개 → 85/90/95% 결과 카드. **장비 상한 초과 시 `.over` 클래스로 시각 경고** (정적 안내로는 어느 강도가 걸리는지 알 수 없으므로 계산 결과에 직접 표시할 것)
- **세션 전 체크리스트**: `.check` 체크박스 리스트
- **접이식 상세**: `details` / `summary`

---

## 주간 스케줄 및 볼륨 관리

> **범위: 보조 훈련 전용.** 주력 훈련(행보드)은 **배치 규칙이 다르므로 이 표에 합치지 않는다.** 두 계층을 하나의 마스터 주간으로 묶으려 하지 말 것.
>
> | | 주력 (행보드) | 보조 (푸쉬·코어·파워·신전근) |
> |---|---|---|
> | 지배 제약 | 조직 회복 — 고강도 사이 48~72h | 볼륨 상한 — 전체의 25% 이하 |
> | 간격의 성격 | **프로토콜의 일부** (지켜야 함) | 유연 (붙일 자리만 있으면 됨) |
> | 실패 비용 | 부상 = 수 주~수 개월 이탈 | 피로 = 며칠 |
> | 배치 문서 | 행보드 페이지의 2주 A/B 사이클 | 아래 표 |
>
> 아래 표와 행보드 페이지의 사이클은 **둘 다 예시**다. 실제 등반 빈도는 주 2~4회로 유동적이므로, 요일이 아니라 각자의 제약(간격 / 볼륨 상한)을 지키면 된다.

**핵심 원칙:** 푸쉬 등 짧은 보충 세션은 클라이밍 후에 통합하되, 코어는
사용자의 최신 선택에 따라 주 1회 30~40분 단독 세션으로 수행한다.
Bechtel의 비등반 훈련 25% 이하 원칙을 고려해 나머지 보충 볼륨은 제한한다.

| 요일 | 내용 | 상세 |
|------|------|------|
| 월 | 코어 단독 (30~40분) | 통합 6운동 세션 |
| 화 | **휴식** | |
| 수 | 클라이밍 + 푸쉬 (15~20분) | |
| 목 | **휴식** 또는 가벼운 모빌리티 | 고관절 CARs, 스트레칭 |
| 금 | 클라이밍 | 코어 추가 없음 |
| 토 | 클라이밍 또는 푸쉬 단독 | |
| 일 | **휴식** | |

**주기화:** 3~4주마다 볼륨 40~60% 감량 (디로드 주)

### 병행 시 주의사항

- 코어의 프론트 레버는 광배근을 강하게 동원하는 **당김 계열** (~70%). 클라이밍 3~4회 + 프론트 레버 2회 = 당김 5~6회. 푸쉬 볼륨을 확실히 챙길 것
- 밴드 안티로테이션 할로우 + 사이드 플랭크가 항회전·항측굴 패턴을 커버. 오버행에서 한 손 뻗을 때 몸이 회전/옆으로 무너지지 않게 잡아주는 능력

### 빠진 영역 (향후 추가 고려)

| 영역 | 현재 상태 | 중요도 | 권장 |
|------|----------|--------|------|
| 고관절 가동성 | 없음 | **매우 높음** | 매일 10~15분. 90/90 스위치, 코사크 스쿼트, 고관절 CARs |
| 하체 파워 | 없음 | 중간 | 피스톨 스쿼트 또는 스플릿 스쿼트 주 1~2회 |
| 주기화/디로드 | 없음 | 높음 | 3~4주마다 볼륨 40~60% 감량 |
| ~~손가락 굴곡근 최대근력~~ | **행보드 세션으로 채워짐** | — | — |

---

## 절대 하지 않을 것

- 출처 없이 운동을 추천하지 않는다
- ✅와 🔶를 구분 없이 섞지 않는다
- 한 사람의 발언을 다른 사람에게 귀속시키지 않는다
- "이 운동이 V등급을 올린다"는 식의 직접적 효과 주장을 하지 않는다
- 검증되지 않은 주장 (Alex Megos "대항근 x3", Nina Tappin 렙 범위 등)을 포함하지 않는다
- **주력 훈련 스케줄과 보조 훈련 스케줄을 하나의 표로 합치지 않는다** — 지배 제약이 다르다
- **관찰연구(후향적)를 근거로 인과관계를 주장하지 않는다** — 연관성까지만 말한다
- **`validation/spec.yaml`을 거치지 않고 세션 가이드의 운동 구성을 바꾸지 않는다** — 감사 해시가 깨진다
