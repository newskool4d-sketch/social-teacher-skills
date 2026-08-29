<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 사회과 이식 명세 (social-teacher-skills)

> 2026-08-29 확정. 과학판(`raphysicst-create/science-teacher-skills` v0.3.0-preview.1) 포크를
> 2022 개정 **사회과** 교육과정용으로 전면 대체하는 작업의 설계 명세.
> 구현 계획: [2026-08-29-social-port.md](./2026-08-29-social-port.md)

## 1. 범위 (사용자 확정)

| 학교급 | 포함 | 제외 |
|---|---|---|
| 초등 | 3–6학년 사회 | 초1–2 (통합교과 특례 안내 — 과학판 ADR-2 방식 계승) |
| 중학교 | 사회 (일반사회·지리 통합 과목) | 역사 (별도 과목 체계) |
| 고등학교 | **통합사회1·2** | 한국사, 일반·진로선택 (정치와 법, 사회와 문화, 세계시민과 지리 등) |

범위 밖 과목 요청 시: 과학판과 동일하게 "범위 밖" 안내 후 스킬 밖 일반 지식으로 지원
(미확인 성취기준 코드 인용 금지).

## 2. 핵심 설계 결정

| # | 결정 | 근거 |
|---|---|---|
| S-1 | **전면 대체** — 과학+사회 동거 아님 | 원본 ADR-5(다과목 포팅 폐기) 선례. 과학판은 upstream으로 계속 존재 |
| S-2 | 목표 프레임 **3범주 무수정 이월** (지식·이해/과정·기능/가치·태도) | 2022 개정 내용 체계는 전 교과 공통 — ADR-1 그대로 유효 |
| S-3 | 데이터 소스 **학습맵 MCP 2종 그대로** | 중등맵은 보통교과 전체 3,838건, 초등맵은 전 교과 11종 620건 수록 — 사회과 이미 포함 |
| S-4 | pedagogy 원재료 = upstream `social_studies.md` 2종 (`docs/upstream/`) + 과학판 한국화 방법론(ADR-6) | C3 탐구 아크 → 2022 사회과 탐구 흐름으로 치환, 관할(state) 분기 제거 |
| S-5 | **렌더러 6종 무수정** (메타데이터 앱명 문자열 2곳만 리네이밍, 두 스킬 사본 동일 유지) | 과학판 불변 원칙 §5 계승. `source_card`·`fill_table` 등 사회과 필요 블록 이미 존재 |
| S-6 | 스킬 이름 유지 (`ko12-lesson-planning` / `ko12-lesson-differentiation`), 레퍼런스는 `science.md` → `social.md` | 스킬명은 과목 중립. 플러그인명·매니페스트만 social로 |
| S-7 | 버전 **0.1.0-preview.1**로 새 출발, CHANGELOG에 계보 명시 | 과목 전면 교체 = 새 산출물. NOTICE에 Anthropic + 과학판 이중 표기 |
| S-8 | 과학판 evals/runs 이력은 **보존** (계보 기록), 루브릭 파일만 교체 | "측정 없이 수정 없다" — 새 실채점은 새 run 폴더로 |
| S-9 | live-conversation 평가 체계는 이번 범위에서 **보류** (시나리오가 과학 전제) | 과학판도 실측 전 상태였음. 로드맵에 후속 명시 |
| S-10 | 파일럿 4종: 초4 · 초5–6(무작위 추첨) · 중 · **고1 통합사회** | 통합사회가 범위에 들어왔으므로 과학판의 "고교 미검증" 한계를 해소 |

## 3. 사회과 고유 요구사항 (과학판에 없던 것)

1. **앵커 치환**: 과학의 "관찰 가능한 현상" → 사회과의 **쟁점·사례·자료(사료·통계·지도)**.
   upstream의 compelling question(단원 탐구 질문) + supporting question(차시 탐구 질문) 구조 이월.
2. **자료 기반 탐구**: `source_card`(사료 카드) 적극 사용. 저작권 규칙 — 공공저작물·저작권
   만료 자료만 발췌 수록, 그 외는 출처 명기 후 지목만 (upstream 규칙 한국화: 법령·정부
   간행물·공공데이터는 수록 가능, 신문 기사·교과서 지문은 지목만).
3. **논쟁 문제 수업 가드레일**: 논쟁적 쟁점(정치·이념 관련)은 **교실에서도 논쟁적으로 재현**
   하되 특정 입장을 정답으로 제시하지 않는다. 실재 정당·정치인 명명 금지, 가치 판단 문항은
   "근거를 들어 자신의 입장을" 형식으로. (교육기본법 제6조 교육의 중립성)
4. **성취기준 코드 신호**: `[4사…]` `[6사…]` `[9사…]` `[10통사…]` 계열 — 정확한 형식은
   구현 Task 1에서 학습맵 실측으로 확정 (추정 금지).
5. **통합사회 특성**: 9개 핵심 개념(행복, 자연환경, 생활공간, 인권, 시장, 정의, 문화, 세계화,
   지속가능한 삶) 중심 통합적 접근 — 영역 분과(지리/일사/윤리/역사)로 쪼개지 않는다.
   ※ 개념 목록은 Task 1 실측으로 재확인.

## 4. 변경 대상 목록 (전수)

| 파일 | 처분 |
|---|---|
| `references/science.md` ×2 | → `references/social.md` ×2 **재작성** |
| `references/curriculum-kr-mcp.md` ×2 | "과학" 절 → "사회" 절 교체 (서버 라우팅·성취기준 확정 절은 유지) |
| `SKILL.md` ×2 | description·Step 0 과목 판별·"과학 전용" 문구 diff |
| `references/example_lesson.json` | 사회과 소재 한국어 예시로 교체 |
| `tests/smoke/korean_lesson.json` + `tests/smoke/check_hwpx.py` | 사회과 스모크로 교체 + 기대값 수정 |
| `pilot/` 전체 | 사회과 파일럿 4종으로 교체, `ci.yml` 파일럿 목록 갱신 |
| `evals/ko12-lesson-planning/rubrics/science.csv` | → `social.csv` 재작성 (P-S 계열) |
| `evals/*/rubrics/` 나머지 | 과학 전제 항목만 수정 (shared.csv·differentiation.csv 검토) |
| `evals/hwpx-format/` V1–V10 | **무수정** (과목 무관) |
| `evals/live-conversation/` | 보류 표기 (README에 한 줄) |
| README·DESIGN.md·CHANGELOG·NOTICE·marketplace.json·plugin.json | social 전면 리네이밍 + 계보 표기 |
| 렌더러 6종 ×2 | 메타 문자열(`science-teacher-skills`) 2곳만 수정, 그 외 무수정 |
| `tests/check_lesson.py`·`tests/check_hwpx_quality.py` | 로직 무수정 (저작권 헤더만 갱신) |

## 5. 완료 기준 (Definition of Done)

1. CI 전 게이트 로컬 재현 통과: 렌더러 사본 동일 / 스모크 렌더 + 한글 무결성 / 파일럿 4종
   DoD / HWPX 품질 검사기 전 산출물.
2. 파일럿 4종 모두: 성취기준 원문이 학습맵 실측값과 문자 단위 일치(중등·통사) 또는 초등
   재구성 주의 푸터 부착 / 3범주 목표 분리 진술 / 단계 분 합계 = 차시 분.
3. 루브릭 1차 실채점 완료, 결과가 `evals/runs/`에 기록됨 (과학판 규율: 측정 없이 수치 주장 없음).
4. `grep -ri "과학 전용\|과학과\|anchor phenomenon" plugin/` 잔존 0건 (렌더러 주석 제외 규칙은
   계획서 Task 9에 명시).
5. 한컴 실열림 확인 (로컬, 파일럿 대표 2종 이상).
6. push는 파일 목록 제시 → 사용자 승인 후에만.
