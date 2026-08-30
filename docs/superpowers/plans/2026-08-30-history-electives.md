<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# v0.2.0 역사·선택과목 확장 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** v0.1.0-preview.1(사회판) 위에 역사 계열(중 역사·고 한국사1·2)과 고교 사회 선택과목을 증분 추가해 v0.2.0-preview.1을 만든다.

**Architecture:** v0.1 이식 방법론 재적용 — 실측 우선(Task 1 delta 조사), 과목 레퍼런스 신설(history.md ×2)과 기존 레퍼런스 증분(social.md 선택과목 분기), SKILL.md 2-way 판별, 파일럿 증분+실채점, 기존 범위 무회귀. 렌더러·검사기·기존 파일럿·기존 레퍼런스 절은 무수정 원칙.

**Tech Stack:** v0.1과 동일 (Python 3 stdlib, bash, GitHub Actions, HWPX/OWPML, 학습맵 데이터 파일 직접 읽기).

**Spec:** `docs/superpowers/plans/2026-08-30-history-electives-spec.md` — E-1~E-10·§3 전수 목록·§4 DoD가 정본. v0.1 spec의 규율(S-2·S-5·논쟁 가드레일·자료 규칙)은 상속.

## Global Constraints

- 브랜치 `feat/history-electives` (base = main aa48b18). main 직접 커밋 금지, **push는 Task 11 사용자 승인 후만**.
- 렌더러 6종·검사기 로직 무수정. 수정은 실측 증명 결함 + 컨트롤러 승인 시에만(v0.1 S-5 예외 절차). 두 사본 동일(CI cmp).
- 기존 산출물 무회귀: v0.1 레퍼런스의 기존 절·기존 파일럿 7패키지·기존 루브릭 판정을 바꾸는 수정 금지(증분·Conditional 추가만).
- 사실 원천: 모든 코드·과목명·영역명·officialText는 Task 1 실측 문서만. 훈련 지식 추정 금지("확인 필요" 표기). npx 실행 금지(elementary MCP 미심사 — v0.1 Ruling 1).
- 역사 서술 가드레일(E-10): 연도·사건·인물은 학습맵 실측 우선, 훈련 지식 단독이면 "확인 필요" / 근현대사 쟁점 복수 해석 병기 / 역사 교과서 출판사 명명 금지.
- UTF-8 명시, 한글 경로 Python, 인라인 원라이너 금지. Commit 한국어 `feat:`/`fix:`/`docs:`/`chore:` + `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- SPDX: 변경·신설 파일에 `social-teacher-skills contributors` 줄(기존 줄 보존).
- 미연결 푸터·byte-exact 문자열(reflect_prompt·사고 충돌 문장)·가/나/다 모둠 관례는 v0.1 값 그대로.

---

### Task 1: 브랜치 + 백로그 정리 + 실측 delta 조사

**Files:**
- Modify(백로그 6건): `plugin/skills/ko12-lesson-planning/references/social.md`(:236 한정어), `DESIGN.md`(§6.1 주제 수 4,333→5,284), planning social.md(:136 중 경고 워딩·지목 전용 자료 2종 조합 규정), `evals/README.md`(judge 프롬프트 M2 예외 주석), differentiation social.md(E-3 역참조 반 줄)
- Create: `docs/superpowers/social-map-survey-v2.md`, `docs/superpowers/survey_history_electives.py`

**Interfaces:**
- Produces: `social-map-survey-v2.md` — 역사·한국사·선택과목의 실측 사실(과목명 verbatim·코드 형식·영역 구조·성취기준 수·원문 수록·선수관계·전이). Task 2~8은 이 문서 값만 인용.

- [ ] **Step 1: 브랜치 생성**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && git checkout main && git pull && git checkout -b feat/history-electives
```

- [ ] **Step 2: post-merge 백로그 6건 일괄 정리** — v0.1 최종 리뷰에서 park된 항목(위 Modify 목록, 처분은 v0.1 ledger `.superpowers/sdd/2026-08-29-social-port/progress.md`의 해당 줄 참조). 전부 한 줄급: ① :236에 "(수록 자료가 2종 이상일 때)" ② 4,333→5,284(+실측 근거 표기) ③ 중 경고 첫 문장을 괄호 계산과 일치하게 ④ 지목 전용 2종 조합 시 학생 자료 섹션 처리 한 문장(자료 이름·출처만 표에 싣고 실물은 교사가 제시) ⑤ judge 프롬프트에 "(M2는 문서 판정 예외)" 괄호 ⑥ R5 앵커 행에 가드레일 역참조 반 줄. 수정 후 스모크 1회 렌더+체크.

```bash
git add -A && git commit -m "chore: v0.1 post-merge 백로그 6건 정리 — 참조 문서 정합"
```

- [ ] **Step 3: 클론 확인·delta 조사 스크립트** — 기존 클론 `.superpowers/sdd/2026-08-29-social-port/external/secondary`(HEAD 964bfaef) 존재 확인, 없으면 v0.1 절차로 재클론(`git clone --depth 1 https://github.com/raphysicst-create/korean-secondary-learning-map-mcp <path>`; 코드 실행 금지, 데이터 읽기만). `docs/superpowers/survey_history_electives.py`(stdlib, 클론 경로 argv)로 추출:
  - 중학교 역사: 과목 엔트리 수·정확 과목명·코드 형식(예시 3)·영역명·성취기준 수
  - 고교 한국사1·2: 동일 항목 + 공통과목 여부
  - 사회과 선택과목 전수 목록: 일반사회·지리 계열의 일반/진로/융합선택 — 과목명 verbatim·코드 접두·성취기준 수 (도덕과·역사 선택은 제외 목록으로 별도 기재)
  - 원문 수록 상태(officialText·sourceLocator)·선수관계 edge 실례·중→고 전이(역사 2건 재확인: survey v1 §5)
  - 대표 full record 부록: 중 역사 1·한국사1 1·선택과목 1

- [ ] **Step 4: survey-v2 문서화** — v1 형식(표 우선·전 주장 파일 경로 인용·"데이터에 없음" 관례). 코드 신호 최종 목록(포함/제외)에 **v0.1 포함분과의 합집합 표**를 넣어 Task 5의 SKILL.md 갱신이 한 표로 끝나게 한다.

- [ ] **Step 5: 재현 검증 + 커밋**

```bash
PYTHONIOENCODING=utf-8 python docs/superpowers/survey_history_electives.py <secondary_clone> > /tmp/sv2-a.txt && PYTHONIOENCODING=utf-8 python docs/superpowers/survey_history_electives.py <secondary_clone> > /tmp/sv2-b.txt && cmp /tmp/sv2-a.txt /tmp/sv2-b.txt && echo REPRODUCIBLE
git add docs/superpowers/ && git commit -m "feat: 역사·선택과목 실측 delta 조사 — 과목명·코드·영역·원문 수록 확정"
```

---

### Task 2: `references/history.md` — 수업 설계 (신설)

**Files:**
- Create: `plugin/skills/ko12-lesson-planning/references/history.md`
- 원재료: `docs/upstream/social_studies-plan.md`(sourcing pedagogy), `plugin/skills/ko12-lesson-planning/references/social.md`(구조 동형·한국화 장치), `docs/superpowers/social-map-survey-v2.md`

**Interfaces:**
- Produces: SKILL.md Step 0의 history 경로가 로드하는 레퍼런스. **social.md와 절 구조 동형**(확인 → 단원 탐구 질문 → 학년군/과목 분기 → 가드레일 → 자료 규칙 → 섹션 구조 7종 → 정리 문항 → lesson.json 매핑) — SKILL.md의 6가지 지시 대상(clarify priorities/curriculum branching/grade-band structures/section structure/non-negotiables/mapping)이 전부 성립해야 한다.

- [ ] **Step 1: 작성** — 분량 250~330줄, 다음 설계값 반영:
  - **분기**: 중 역사(45분) / 고 한국사1·2(50분). 단계(사료 탐구 아크): 시대 질문 만나기(5–7) → 사료 읽기(15: 출처 확인 — 누가·언제·왜 만들었나) → 교차 검증·맥락화(8–10: 사료 2종 대조, 시대 배경 연결) → 해석 구성(10–12: 주장-근거-사료 인용, 고: 복수 해석 검토) → 정리 문항(3–5). 분 합계 45/50 산술 명시.
  - **성취기준 유형 분기**(social.md 관례 계승): 사실·흐름형(변천·전개 서술어 — 연표·인과 사슬 중심) / 사료 분석형(분석·해석 — 기본 구조) / 평가·논쟁형(평가·토의 — 복수 해석 병기 필수).
  - **역사 가드레일 절**(E-10 그대로): 사실/해석 구분 명문화, 시대착오 금지(당대 맥락으로 판단 지시), 근현대사 쟁점 복수 해석 병기 + 논쟁 가드레일 상속, 연도·사건·인물 "확인 필요" 관례(학습맵 원문 밖 서술), 역사 교과서 출판사 명명 금지.
  - **사료 규칙**: 발췌 수록=저작권 만료 사료(고문헌·근대 문서)·정부 간행물·공공 아카이브 공개 자료 / 지목만=현대 저작 사료집·교과서 지문·박물관 소장 이미지. 번역·현대어 재구성은 origin "…을 현대어로 재구성" 표기. `source_card` 필드 활용(author=작성 주체, date=연대, origin=소장처/출전).
  - 섹션 구조 7종·정리 문항(사료 근거로 답하기, 분류 3칸)·lesson.json 매핑(`shared.subject` "역사"/"한국사1"/"한국사2", grade 영문 선행 규칙 재사용, 연표는 `table`·`number_line` 활용 명시) — social.md 해당 절과 같은 밀도.
- [ ] **Step 2: 검사** — `grep -c "^## "` 절 수가 social.md와 동형인지, 협상 불가에 부정 예시 동반, 코드·과목명 survey-v2 일치, 분 합계 산술. 잔존 검사(사회 전용 표현·과학 어휘 0).
- [ ] **Step 3: 커밋** `feat: 역사 수업 설계 레퍼런스 — 사료 탐구 아크·사실/해석 구분·복수 해석 가드레일`

---

### Task 3: `references/history.md` — 차별화 (신설)

**Files:**
- Create: `plugin/skills/ko12-lesson-differentiation/references/history.md`
- 원재료: `docs/upstream/social_studies-differentiation.md`, differentiation `references/social.md`(R1~R8 골격), survey-v2, Task 2 산출물(용어 정합)

**Interfaces:**
- Produces: R1~R8 정확히 8개(역할명 SKILL.md 일치), byte-exact 문자열 3종(reflect_prompt·사고 충돌 문장·eyebrow 규칙) 유지. eyebrow: `"[학년] 역사 · [코드]"`(중) / `"[학년] 한국사1 · [코드]"` 형(고 — 과목명 verbatim).

- [ ] **Step 1: 작성** — 350~430줄. 치환 요점: R3 진입점 = 사료 읽기→정보 추출→해석·주장(social판과 동일 축, 예문만 사료로) / R4 허용 스캐폴드에 출처 확인 안내 발문·연표 틀·일부 채워진 사료 대조표, 금지에 "사료를 현대문 요약으로 대체"(같은 사료 원칙) / R6 같은 사료·같은 질문 + 사료 난도 조정 금지 명시 / R7 심화 확장 유효 요건 = 반론 해석 구성·추가 사료 교차 검증·현재와의 연결·역사가 관점 비교 / 사고 충돌 문장 byte-exact 이월. 문서 템플릿·매핑은 social판 동형.
- [ ] **Step 2: 검사** — `grep -c "^### R"` = 8, byte-exact 3종, Task 2와 용어 대조, survey-v2 일치.
- [ ] **Step 3: 커밋** `feat: 역사 차별화 레퍼런스 — R1~R8 사료 탐구 체계`

---

### Task 4: social.md ×2 — 선택과목 분기 증분

**Files:**
- Modify: `plugin/skills/ko12-lesson-planning/references/social.md` (고 밴드 뒤 "선택과목 분기" 절 신설 + 확인 절·매핑에 선택과목 한 줄씩)
- Modify: `plugin/skills/ko12-lesson-differentiation/references/social.md` (범위 서술·매핑 subject 목록 증분)

**Interfaces:**
- Consumes: survey-v2 선택과목 목록(과목명 verbatim)
- Produces: 고 밴드 구조를 재사용하되 영역별 조정 delta 표 — 경제(통계·모형 해석 강조, 정량 근거 필수), 정치·법과 사회(쟁점·판례·법령 자료 중심, 논쟁 가드레일 최고 강도 명시), 사회와 문화(연구 방법·개념 적용), 지리 계열(공간 자료·지도 중심). `shared.subject` = 실측 과목명 verbatim.

- [ ] **Step 1: 증분 작성** — **기존 절 무수정** 원칙: 고 밴드 통합사회 서술은 그대로 두고, 그 뒤에 "선택과목 분기(고)" 절 추가(과목군별 조정 표, 셀당 25어절 규칙 준수). 확인(Clarify) 절의 범위 서술과 lesson.json 매핑 subject 값 목록에 각 한 줄. 범위 밖 안내에서 선택과목 제외 문구 삭제·조정.
- [ ] **Step 2: 검사** — 기존 절 diff 0(신설 절·지정 한 줄들 외), 과목명 전부 survey-v2 verbatim, 두 사본의 서로 참조 정합.
- [ ] **Step 3: 커밋** `feat: 고교 사회 선택과목 분기 — 영역별 조정 delta (social.md 증분)`

---

### Task 5: curriculum-kr-mcp.md ×2 + SKILL.md ×2 — 라우팅 확대

**Files:**
- Modify: `references/curriculum-kr-mcp.md` ×2 (역사·한국사·선택과목 라우팅: 코드 신호·subject 파라미터 필요 여부 실측 반영·전이 2건 예외)
- Modify: SKILL.md ×2 (frontmatter description 신호 증분, Step 0 판별 2-way: social→`references/social.md` / history→`references/history.md`, 범위 문구 "사회·역사 전용(초3–6 사회·중 사회·중 역사·고 통합사회·한국사·사회 선택과목)"형, 범위 밖 안내 갱신)

- [ ] **Step 1: curriculum-kr-mcp.md 증분** — 서버 라우팅 표에 역사·한국사·선택과목 행, 전이 절의 "사회 0건" 서술을 "역사 계열 전이 2건 존재(실측) — 해당 시 사용"으로 정정(survey v1 §5·v2 재확인 값), 코드 공유 과목(subject 파라미터) 실측 반영.
- [ ] **Step 2: SKILL.md diff** — 판별 목록: social(기존) / **history**(역사·한국사 신호: 사료·시대·인물·사건, 코드 [실측]) 분기 추가, references/history.md 로드 지시, description에 역사 예문 1("다음 주 3·1 운동 수업 준비해야 해요" 류 — 실측 단원명 기반) 추가. 미연결 푸터·draft offer 등 무수정.
- [ ] **Step 3: 검사** — 두 사본 공통 절 diff, SKILL.md의 신호·경로가 Task 2·3 파일명과 일치, 잔존 grep.
- [ ] **Step 4: 커밋** `feat: 역사·선택과목 라우팅 — Step 0 2-way 판별·학습맵 라우팅 증분`

---

### Task 6: 파일럿 증분 4+1종 + CI

**Files:**
- Create: `pilot/middle-history/`(lesson+differentiation+ground-truth), `pilot/korean-history/`(lesson, 한국사1), `pilot/elective-econ/`(lesson, 경제 — 정량 자료), `pilot/elective-law/`(lesson, 법과 사회 또는 정치 — 논쟁 밀도 확보; 과목·성취기준은 실측 후 확정)
- Modify: `.github/workflows/ci.yml` (수업 루프 4→8, 차별화 루프 3→4)

- [ ] **Step 1: 소재 확정** — 클론 데이터에서 성취기준 선정·ground-truth.md(v0.1 형식: full record·클론 sha·데이터 경로). 근현대사 성취기준 1건 포함(복수 해석 관례 실증 목적).
- [ ] **Step 2: 저작** — history.md·social.md 선택과목 분기 준수. 역사 파일럿: 사료 2종(발췌 1 이상), "확인 필요" 관례 시연 1곳 이상(훈련 지식 보완 서술이 있다면), 복수 해석 병기. 경제 파일럿: 정량 자료 해석+수치 인용 근거. 법·정치 파일럿: 법령·판례 자료, 가드레일 최고 강도.
- [ ] **Step 3: 전수 렌더+DoD+품질** — 신규 4+1과 **기존 7패키지 회귀** 모두:

```bash
for p in elementary middle-school random-elementary high-integrated middle-history korean-history elective-econ elective-law; do bash plugin/skills/ko12-lesson-planning/scripts/render_all.sh "pilot/$p/lesson.json" "/tmp/v2-out-$p" && PYTHONIOENCODING=utf-8 python tests/check_lesson.py "pilot/$p/lesson.json" "/tmp/v2-out-$p" || echo "FAIL $p"; done
for p in elementary middle-school random-elementary middle-history; do bash plugin/skills/ko12-lesson-differentiation/scripts/render_all.sh "pilot/$p/differentiation.json" "/tmp/v2-diff-$p" || echo "FAIL diff $p"; done
PYTHONIOENCODING=utf-8 python tests/check_hwpx_quality.py /tmp/v2-out-* /tmp/v2-diff-*
```

- [ ] **Step 4: ci.yml 루프 갱신 + 한컴 실열림**(신규 대표: middle-history lesson_plan·korean-history lesson_plan·elective-law worksheet 중 2종 이상, COM 불가 시 사실대로 보고).
- [ ] **Step 5: byte 대조 스크립트 검증(신규 전건) + 커밋** `feat: 역사·선택과목 파일럿 4+1종 — 전 검사 층·기존 회귀 통과`

---

### Task 7: 루브릭 확장 + 실채점

**Files:**
- Create: `evals/ko12-lesson-planning/rubrics/history.csv` (P-H 계열: 사료 실재성·출처 확인 발문 존재·사실/해석 구분·시대착오 금지·복수 해석(Conditional 근현대사)·연도 확인 필요 관례)
- Modify: `social.csv`(선택과목 Conditional 1~2항목: 경제 정량 근거·선택과목 subject 정합), `shared.csv`·`differentiation.csv`(역사 문구 수용 — 기존 판정 무효화 금지)
- Create: `evals/runs/2026-08-3X/` 실채점 기록

- [ ] **Step 1: 루브릭 작성** — 각 항목 Notes에 history.md/social.md 출처 절, 판정 가능 형식(부정 예시 동반). 금지: 쪽수 기준·이연 항목 fail화·어절 공백 감점(v0.1 ruling 계승).
- [ ] **Step 2: 실채점** — 신규 파일럿 전체(수업 4·차별화 1) × 해당 루브릭 + HWPX V1~V10, 기존 파일럿 회귀 표본 2패키지. verdicts+summary(v0.1 형식, 천장 병기, skip 정직 표기). fail 처분 3경로·무기록 fail 금지.
- [ ] **Step 3: 커밋** `feat: 역사 루브릭(P-H) 신설 + v0.2 실채점 — 기록 evals/runs/…`

---

### Task 8: 문서·버전 v0.2.0-preview.1

**Files:**
- Modify: README(범위·사용 예에 역사 1건·데이터 출처 무변경·로드맵), CHANGELOG(`## [0.2.0-preview.1]` — 실채점 정본 수치 인용·알려진 한계 갱신: 역사 선택과목 미지원 등), DESIGN.md(ADR-8: E-1~E-10 요약·spec 참조, §1 범위, §9 경로), `plugin/.claude-plugin/plugin.json`(version), marketplace.json(description 범위)

- [ ] **Step 1: 갱신** — 수치는 Task 7 summary.md 정본만. 범위 문구는 SKILL.md와 문자 정합.
- [ ] **Step 2: 커밋** `feat: v0.2.0-preview.1 — 역사·선택과목 범위 반영 (README·CHANGELOG·ADR-8)`

---

### Task 9: 전체 검증

- [ ] CI 전 단계 로컬 재현(확장 루프) / 잔존 스윕(범위 문구 구버전 "사회 전용" 잔존 0 — 계보 기록 제외) / spec §4 DoD 6항 대조표 보고.

### Task 10: 최종 whole-branch 리뷰

- [ ] `git merge-base main HEAD`부터 리뷰 패키지 생성, 최상위 모델 디스패치(요구: 교차 파일 정합·역사 가드레일 실증·기존 범위 무회귀·이연 triage). 발견 시 단일 fix wave + 단일 재리뷰(SDD 규정).

### Task 11: push 게이트

- [ ] 커밋·파일 목록 제시 → **사용자 승인** → push + 병합 방식 확인 (v0.1과 동일 절차).

---

## Self-Review 기록

- Spec 커버리지: E-1→T5(2-way), E-2→T4, E-3→T2, E-4→T3, E-5→T2/3/4 매핑, E-6→T6, E-7→T7, E-8→T8, E-9→T1, E-10→T2(가드레일 절)+T6(파일럿 실증)+T7(P-H 루브릭). §3 전수 목록 각 행 → T1~T8 대응. 백로그 6건 → T1 Step 2.
- 함정 이월: grade 영문 선행(T2 매핑), 분 합계 경고(T2), byte-exact 3종(T3), 기존 무회귀(GC+T6 Step 3+T7 회귀 표본), npx 금지(T1).
- 이름 일관성: `history.md`(T2/3 생성=T5 참조), 파일럿 폴더명(T6 생성=ci.yml=T7 대상), P-H 계열(T7 내 폐쇄), subject 값(T2·T3·T4 매핑 = survey-v2 verbatim).
