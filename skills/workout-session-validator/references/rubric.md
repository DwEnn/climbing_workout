# Validation rubric

## Hard failures

- 직접 검증으로 표시했지만 원문이 해당 운동을 클라이머에게 추천하지 않는다.
- 필요한 장비가 없고 안전한 대체안도 없다.
- 현재 카드의 실행 지침에 중요한 안전 문제가 있다.

하드 실패의 범위를 함께 기록한다. 출처 오표기는 현재 카드의 발행을 막지만,
다른 직접 출처로 교체하거나 `principle`로 낮출 수 있고 운동 선택 자체가
타당하면 운동 판정은 `revise`일 수 있다. 장비 불가나 중요한 실행 안전 문제는
운동 선택에 직접 적용하므로 `replace` 또는 `remove`가 된다.

## Weighted score

| Dimension | Points | What to check |
|---|---:|---|
| Evidence accuracy | 30 | source existence, attribution, population, directness, dose |
| Goal and pattern fit | 25 | session purpose and distinct functional slot |
| Session integration | 20 | ordering, redundancy, fatigue and weekly interference |
| Equipment and time fit | 15 | owned equipment, substitute, claimed duration |
| Usability and progression | 10 | executable cues, regression, progression, stopping rule |

## Disposition

- `retain`: 80-100 and no hard failure
- `revise`: 70-79 and no hard failure
- `conditional`: 80+ but needs an explicit readiness or safety condition
- `replace`: below 70 or a better candidate wins by more than 5 points
- `remove`: hard failure without a viable correction

## Replacement approval gate

`5점 초과`는 교체 검토를 여는 규칙이지 자동 승인 규칙이 아니다. 대체 후보는
현재 운동과 독립적으로 다음을 모두 통과해야 한다.

- 총점 80점 이상
- 식별 가능한 원문에서 저자·대상·운동·목적 확인
- 하드 실패 없음
- 보유 장비·시간 조건 충족
- 새 세션 구성에서 중복·피로·순서·시간 검사 통과

통과 후보가 없으면 낮은 점수의 대안을 억지로 넣지 않는다. 현재 운동을
고쳐 유지할 수 있으면 `revise_current`, 슬롯 자체가 불필요하면
`remove_slot`, 둘 다 아니면 `unresolved`로 남긴다.

## Evidence rules

- A publisher or author does not receive one permanent Tier. Classify each evidence item.
- A study on non-climbers supports only a principle-based climbing claim.
- Correlation does not establish exercise efficacy.
- A source that names a broad category does not directly validate every exercise in it.
- Books and paywalled sources without inspectable pages are unverified for exact claims.
- Separate injury-prevention, performance, progression and dosage claims when their support differs.

## Demonstration video rules

- Every active exercise card has exactly one public, clickable YouTube video.
- The video demonstrates the named movement and its defining variation, not merely the same body part.
- A source article, thumbnail without a video link, unavailable video, generic progression, or adjacent movement fails.
- The HTML link ID, thumbnail ID and `validation/video-audit.yaml` ID must match.
- Record the verified title, channel, availability, match decision and replacement history.
- A demonstration video improves usability but does not prove a climbing-specific training claim.
