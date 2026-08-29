<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 사회과 이식 (social-teacher-skills) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 과학판 포크(`newskool4d-sketch/social-teacher-skills`)를 2022 개정 사회과(초3–6 사회 · 중학교 사회 · 고교 통합사회) 수업 설계·차별화 플러그인으로 전면 대체한다.

**Architecture:** 과학판의 이식 방법론(ADR-6: SKILL.md는 diff, 과목 레퍼런스는 재작성) 재적용. 렌더러·검사기·CI 골격은 무수정 계승, 과목 결합 지점(레퍼런스 2종·MCP 가이드 절·루브릭·파일럿·스모크·매니페스트)만 교체. 데이터는 기존 학습맵 MCP 2종이 이미 사회과를 수록하므로 신규 소스 없음.

**Tech Stack:** Python 3 표준 라이브러리(렌더러·검사기), bash(render_all.sh), GitHub Actions, 학습맵 MCP 2종(npx, stdio JSON-RPC), HWPX(OWPML 직접 생성).

**Spec:** `docs/superpowers/plans/2026-08-29-social-port-spec.md` — 범위·설계 결정 S-1~S-10·변경 대상 전수 목록·DoD는 전부 spec이 정본. 이 계획은 spec을 실행 순서로 푼 것.

## Global Constraints

- 작업 사본: `C:/Users/홍주형/projects/social-teacher-skills` (origin = newskool4d-sketch 포크). 모든 경로는 이 저장소 루트 기준.
- 브랜치 `feat/social-port`에서만 작업. main 직접 커밋 금지. **push는 Task 12의 사용자 승인 후에만.**
- 렌더러 6종(`check_hwpx_min.py`, `lesson_common.py`, `render_documents.py`, `render_lesson_html.py`, `render_lesson_hwpx.py`, `theme.css`) 로직 무수정. 예외는 Task 9의 메타 문자열 2곳뿐. 어떤 수정이든 **두 스킬 사본에 동일 적용** (CI `cmp` 게이트).
- 파일 쓰기는 UTF-8 명시(`encoding='utf-8'`). 한글 경로 조작은 Python으로. Python 실행 시 `PYTHONIOENCODING=utf-8`.
- 성취기준 코드·원문·과목 구조는 **Task 1 실측값만** 사용 — 훈련 지식 추정 금지(추정 시 "추정" 표기, 과학판 ADR-3 규율).
- 커밋 메시지는 기존 저장소 관례(한국어, `feat:`/`fix:`/`docs:` 접두) + `Co-Authored-By: Claude Fable 5 <noreply@anthropic.com>`.
- 새 의존성·패키지 추가 금지 (표준 라이브러리 전용 원칙 유지).
- SPDX 헤더: 기존 3줄(Anthropic·Learning Commons·science-teacher-skills contributors) 유지 + `social-teacher-skills contributors` 1줄 추가. 기존 줄 삭제 금지.

---

### Task 1: 브랜치·업스트림 자료·학습맵 실측 조사

**Files:**
- Create: `docs/upstream/README.md`, `docs/superpowers/social-map-survey.md`, `scripts/survey_social_map.py`(저장소 밖 스크래치 실행 후 결과만 커밋 — 스크립트 자체는 `docs/superpowers/`에 보존)
- Commit: `docs/upstream/social_studies-plan.md`, `docs/upstream/social_studies-differentiation.md` (이미 워킹트리에 복사됨)

**Interfaces:**
- Produces: `docs/superpowers/social-map-survey.md` — 이후 모든 태스크가 참조하는 사회과 실측 데이터(과목명·성취기준 코드 형식·영역 구조·통합사회 핵심 개념·초등 verbatim 여부). Task 2~8은 이 파일의 값만 인용한다.

- [ ] **Step 1: 브랜치 생성 + 업스트림 자료 커밋**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills"
git checkout -b feat/social-port
```

`docs/upstream/README.md` 내용:

```markdown
# 업스트림 원재료

Anthropic `anthropics/k12-teacher-skills`(main, 2026-08 시점)의 사회과 레퍼런스 2종 사본.
Apache-2.0 (각 파일 말미 저작권 표기 참조). 사회과 이식(social.md 재작성)의 원재료로만
사용하며, 플러그인 런타임은 이 폴더를 읽지 않는다.

- `social_studies-plan.md` — k12-lesson-plan-creation/references/social_studies.md
- `social_studies-differentiation.md` — k12-lesson-differentiation/references/social_studies.md
```

```bash
git add docs/upstream/ && git commit -m "docs: 업스트림 사회과 레퍼런스 2종 사본 — 이식 원재료"
```

- [ ] **Step 2: 학습맵 npm 패키지 2종 보안 심사**

`security-vet` 스킬(설치 심사)로 `korean-secondary-learning-map-mcp`·`korean-elementary-learning-map-mcp`를 심사한다 (npx 첫 실행 = 설치이므로 사용자 규칙상 선행 필수). 통과 못 하면 여기서 중단하고 사용자에게 보고.

- [ ] **Step 3: 실측 스크립트 작성**

`docs/superpowers/survey_social_map.py` (실행은 저장소 루트에서):

```python
# SPDX-License-Identifier: Apache-2.0
# 학습맵 MCP 2종에서 사회과 실측 데이터를 뽑는다. stdio JSON-RPC, 표준 라이브러리만.
import json, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")

def rpc(pkg, calls):
    msgs = [
        {"jsonrpc": "2.0", "id": 0, "method": "initialize",
         "params": {"protocolVersion": "2025-06-18", "capabilities": {},
                    "clientInfo": {"name": "survey", "version": "0"}}},
        {"jsonrpc": "2.0", "method": "notifications/initialized"},
    ]
    for i, (name, args) in enumerate(calls, 1):
        msgs.append({"jsonrpc": "2.0", "id": i, "method": "tools/call",
                     "params": {"name": name, "arguments": args}})
    inp = "\n".join(json.dumps(m) for m in msgs) + "\n"
    r = subprocess.run(["npx.cmd", "-y", pkg], input=inp.encode("utf-8"),
                       capture_output=True, timeout=300)
    return r.stdout.decode("utf-8", errors="replace")

print("=== secondary ===")
print(rpc("korean-secondary-learning-map-mcp", [
    ("list_curricula", {"schoolLevel": "middle"}),
    ("list_curricula", {"schoolLevel": "high", "subjectGroup": "사회"}),
    ("search_standards", {"query": "사회", "schoolLevel": "middle"}),
    ("search_standards", {"query": "통합사회"}),
]))
print("=== elementary ===")
print(rpc("korean-elementary-learning-map-mcp", [
    ("list_curricula", {}),
    ("search_standards", {"query": "사회", "gradeBand": "3-4"}),
    ("search_standards", {"query": "사회", "gradeBand": "5-6"}),
]))
```

도구명·파라미터가 실제 스키마와 다르면(오류 응답) 같은 방식으로 `tools/list`를 먼저 호출해 실제 스키마를 확인하고 스크립트를 고쳐 재실행한다.

- [ ] **Step 4: 실행 + 대표 성취기준 상세 조회**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && PYTHONIOENCODING=utf-8 python docs/superpowers/survey_social_map.py > /tmp/survey-raw.txt 2>&1; tail -5 /tmp/survey-raw.txt
```

결과에서 학교급별 대표 성취기준 코드를 1개씩 골라 `get_standard`로 전체 레코드(원문 verbatim 여부, `linkedTopics`, `sourceTextIncluded`)를 추가 조회한다 (같은 스크립트에 호출 추가). 초등 `get_prerequisites` 1건도 호출해 사회과 선수관계 edge 존재 여부를 확인한다.

- [ ] **Step 5: 실측 결과 문서화**

`docs/superpowers/social-map-survey.md`에 기록 (raw 출력이 아니라 추출 사실만):

```markdown
# 사회과 학습맵 실측 (2026-08-29)

## 코드 형식 (실측 verbatim)
- 초3–4: [실측값] / 초5–6: [실측값] / 중: [실측값] / 통합사회: [실측값]
## 과목·영역 구조
- 중학교 "사회" 과목 수: [실측] / 영역명: [실측]
- 통합사회1·2 핵심 개념(영역명): [실측 목록]
## 원문 수록 상태
- 중등·통사: officialText verbatim [실측 확인] / 초등: sourceTextIncluded=[실측]
  → 초등 재구성 푸터 규칙 유지 여부: [판정]
## 선수관계
- 사회과 edge 존재 사례: [실측] / 빈 배열 사례: [실측]
## 스킬이 쓸 코드 신호 (Step 0 과목 판별용)
- [최종 확정 목록]
```

⚠ 초등 학습맵 README(npm 최신판)는 "공식 원문 620건 수록"을 주장하는데, 과학판 `curriculum-kr-mcp.md`는 "초등 verbatim 아님"을 전제한다 — **어느 쪽이 현재 설치 버전의 실태인지 이 실측에서 판정**하고, 판정 결과를 Task 4·8(P1 루브릭)에 반영한다.

- [ ] **Step 6: 커밋**

```bash
git add docs/superpowers/ && git commit -m "feat: 사회과 학습맵 실측 조사 — 코드 형식·영역 구조·원문 수록 상태 확정"
```

---

### Task 2: `references/social.md` — 수업 설계 pedagogy 재작성

**Files:**
- Create: `plugin/skills/ko12-lesson-planning/references/social.md`
- Delete: `plugin/skills/ko12-lesson-planning/references/science.md`
- 원재료(읽기): 과학판 `science.md`(구조·한국화 장치), `docs/upstream/social_studies-plan.md`(사회과 pedagogy), `docs/superpowers/social-map-survey.md`(실측값)

**Interfaces:**
- Produces: `references/social.md` — SKILL.md Step 0이 로드하는 유일한 과목 레퍼런스. 섹션 구성은 과학판 science.md와 동형(확인 → 성취기준 근거 → 수업 설계/학년군 분기 → 섹션 구조 → 정리 문항 → lesson.json 매핑)이어야 Task 5의 SKILL.md diff가 최소화된다.

- [ ] **Step 1: 작성** — 다음 골격·설계값을 그대로 반영해 한국어 산문으로 완성한다 (과학판 science.md의 문체·밀도 준수, 분량 목표 250~300줄):

**확인(Clarify) 절:**
- 학년군 밴드: 초3–4 / 초5–6 / 중1–3 / 고(통합사회1·2). 침묵 기본값: 초 40분 / 중 45분 / 고 50분, 과정중심평가 연계, 보편적 학습 설계.
- ⚠ 초1–2는 사회 교과 없음(통합교과 '바른 생활'·'슬기로운 생활') — 과학판 특례 문구 구조 재사용.
- 고교에서 통합사회 외 과목(정치와 법 등) 요청 → 범위 밖 안내.
- 교과서 중립·출판사 가드레일: 과학판 문단 그대로 이월.
- 확인 우선순위: (1) 학년 (2) 주제 또는 성취기준 (3) 단원 내 위치 (4) 차시 분량.

**단원 탐구 질문(upstream compelling question의 한국화):**
- 차시는 단원 탐구 질문(논쟁 가능·삶과 연결·자료로 답할 수 있는) 아래 차시 탐구 질문 1개를 갖는다. 교사가 안 줬으면 초안하고 [제안] 표시.
- 학년군별 예시 각 2개를 실제로 작성해 넣는다 (예: 초3–4 "우리 고장의 모습은 왜 서로 다를까?", 중 "법은 왜 바뀌는가?", 통사 "정의로운 사회란 무엇인가?" 수준의 한국 맥락 질문 — 실측 영역명에 맞춰 조정).

**학년군 분기(각 밴드: 단계 + 분 배분 + 협상 불가 원칙):**
- **초3–4 (40분)**: 질문 만나기(5–8) → 자료 살펴보기(12–15: 사진·그림·쉬운 지도, 구술 중심) → 이야기 나누기(8–10) → 표현하기(5–8: 그림+짧은 문장) → 정리 문항(3–5). 협상 불가: 자료는 학생이 직접 보는 것이어야 한다(교사 설명 대체 금지) / 고장·지역 등 학생 생활 맥락 우선 / 텍스트 밀도 최소.
- **초5–6 (40분)**: 탐구 질문 확인(5) → 자료 조사·분석(15: 짧은 글·통계·지도) → 의견 나누기(8–10) → 주장-근거 쓰기(7–8) → 정리 문항(3–5). 협상 불가: 주장에는 제시 자료에서 나온 근거가 붙는다 / 자료에는 출처가 붙는다.
- **중1–3 (45분)**: 쟁점·사례 제시(5–7) → 자료 분석(15: 자료 2종 내외 — 사료·통계·지도·법령) → 토의·논증(8–10) → 주장-근거 글쓰기(8–10: 중3은 반론 인식까지) → 정리 문항(3–5). ⚠ 과학판과 동일한 "권장 분 최대치 합 > 45분" 경고 문단을 넣고 실배분 예시(합 45)를 명시. 협상 불가: 근거는 이번 차시 자료에서 / 자료 2종은 관점·형식이 달라 긴장을 만들 것 / 논쟁 쟁점은 균형 재현(아래 가드레일).
- **고 통합사회 (50분)**: 쟁점 던지기(5–8: 핵심 개념 연계, 초기 입장 쓰기) → 자료 탐구(15–20: 복합 자료, 통계 해석 포함) → 논증·토론(10–12: 반론 검토 필수) → 통합적 관점 쓰기(8–10: 둘 이상 관점 통합, 사회 참여 연결) → 형성 확인(5). 협상 불가: 통합적 접근(영역 분과로 쪼개지 않는다 — 실측 핵심 개념 인용) / 반론 없는 논증은 미완성 / 사회 참여 연결은 실질적으로.

**논쟁 문제 가드레일 절(신설 — spec §3-3):** 논쟁적 쟁점은 교실에서도 논쟁적으로 다루되 특정 입장을 정답화하지 않는다. 실재 정당·정치인 명명 금지. 가치 문항은 "근거를 들어 자신의 입장을 서술" 형식. 산출물 어디에도 모델의 입장 표명 금지.

**자료(source) 규칙 절(신설 — upstream Source set 한국화):** 자료 2종 내외, 실재·구체 출처(제목·생산자·연도·소장처). 발췌 수록 가능: 법령·정부 간행물·공공데이터·저작권 만료 사료(`source_card`). 지목만: 신문 기사·방송·교과서 지문·저작권 있는 사진/도표(Materials에 제목·출처·접근 경로). 재구성 발췌는 origin에 "…에서 재구성" 표기.

**섹션 구조(7개 — 과학판 동형):** 한눈에 보기(성취기준 verbatim 콜아웃 + 수업 흐름 한 줄 + 단원/차시 탐구 질문 + 준비물) / 범주별 학습 목표(3범주 분리 — 과정·기능 동사는 사회과형: 조사하다·분석하다·비교하다·토의하다·평가하다) / 단원 맥락 / 어휘 / 예상되는 학생 생각·오개념(최대 3) / 수업 전개(관찰 포인트 3개+, 토의 발문 구체) / 설계 노트.

**정리 문항 지침:** 차시 탐구 질문에 자료 근거를 들어 답하기. 초3–4 그림+한 문장, 초5–6 주장+근거 1, 중 주장+근거 2, 통사 주장+근거+반론 고려. 분류 3칸(이해함/거의/재지도 필요) 유지.

**lesson.json 매핑:** 과학판 매핑 절을 기반으로: `shared.subject: "사회"` / `shared.grade` 영문 학년 선행 규칙 그대로(`"Grade 10 · 고등학교 1학년"`) / `shared.anchor_task` → 쟁점·사례 제시 / `shared.source_a`·`source_b`(source_card, 교사용 근거는 별도 키) / `shared.q1..q3`(자료 분석 발문 — 각 발문은 대상 자료를 명명) / `shared.exit_ticket` / student_materials는 항상 포함 + 자료 수록 시 `source_packet` 문서 추가(upstream 학생 페이지 레이아웃 이월).

- [ ] **Step 2: 잔존 검사**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && grep -n "과학\|현상\|탐구 실험\|NGSS" plugin/skills/ko12-lesson-planning/references/social.md
```

기대: "과학" 0건(비교 문맥 포함 금지), "현상"은 사회 현상 문맥만 허용(직접 확인). SPDX 헤더 4줄 + 원본 경로 주석(upstream social_studies.md + 과학판 science.md 이중 표기) 존재 확인.

- [ ] **Step 3: science.md 삭제 + 커밋**

```bash
git rm plugin/skills/ko12-lesson-planning/references/science.md
git add plugin/skills/ko12-lesson-planning/references/social.md
git commit -m "feat: 수업 설계 사회과 레퍼런스 — C3 탐구 아크를 2022 사회과 자료 기반 탐구로 치환"
```

---

### Task 3: `references/social.md` — 차별화 pedagogy 재작성

**Files:**
- Create: `plugin/skills/ko12-lesson-differentiation/references/social.md`
- Delete: `plugin/skills/ko12-lesson-differentiation/references/science.md`
- 원재료: 과학판 차별화 `science.md`(R1–R8 골격·한국화 장치), `docs/upstream/social_studies-differentiation.md`

**Interfaces:**
- Produces: R1–R8 규칙 체계 유지(SKILL.md Step 3이 "여덟 규칙 R1–R8"을 명명 호출하므로 번호·개수 불변). 문서 내용 템플릿(teacher_plan 5쪽 상한·worksheet 구조)도 과학판 동형.

- [ ] **Step 1: 작성** — 과학판 R1–R8 구조에 다음 치환을 적용 (upstream 차별화 social_studies.md의 대응 절 참조):

- R1(산출 구조)·R5(필수 장치 5종)·R8(범위와 기본값): 구조 그대로, 예시 문구만 사회과로.
- R2(3범주 범위 보존): "탐구를 읽기 자료로 바꾸기 금지" → "자료 분석을 요약문 읽기로 바꾸기 금지". 모든 수준이 **같은 자료, 같은 핵심 질문**을 다룬다.
- R3(진입점): 과학의 관찰→표현→설명 → 사회과의 **자료 읽기 → 정보 추출 → 해석·주장**. 기초(가): 구조화된 자료 읽기 지원과 함께 정보 추출 → 문장 지원 있는 주장으로 / 보통(나): 추출 → 해석(주장-근거) / 심화(다): 해석 → 확장(반론 검토, 다른 자료와 대조, 현재 쟁점 적용, 통합적 관점).
- R4(기초 스캐폴드): 금지 — 자료를 요약본으로 대체, 결론 미리 제시, 자료 단순화(모든 수준 같은 자료), 답이 드러나는 안내. 허용 — 자료 읽기 안내 발문("누가 만들었나요? 무엇이 보이나요? 왜 만들었을까요?"), 어휘 뜻풀이(자료 속 옛말·한자어·전문어), 일부 채워진 정보 추출 표, 주장-근거 문장 지원. 밀도 상한(과제당 1–2) 유지.
- R6(보이지 않는 조정): 같은 자료·같은 발문·같은 핵심 과제, 지원만 다름. 스캐폴드 부재는 조용히.
- R7(점진 제거 + 심화 품질 검사): 심화 확장 유효 요건을 사회과형으로 — 반론 구성 / 추가 자료와 교차 검증 / 현재 사례 적용 / 다른 영역 관점 통합(통사) / 대안 제안과 근거. 거절: 같은 자료 더 읽기, 더 긴 학습지.
- 사고 충돌 문장 지원: *"나는 ____라고 생각했는데 자료에서 ____를 보았다. 이제 나는 ____라고 생각한다."* (그대로 이월 — 사회과에도 유효).
- differentiation.json 매핑: `shared.subject: "사회"`, 나머지 과학판 규칙 이월. 저작권 문단에 검정 교과서 + **신문·방송 자료** 추가.

- [ ] **Step 2: 잔존 검사 + R 규칙 무결성**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && grep -c "^### R" plugin/skills/ko12-lesson-differentiation/references/social.md && grep -n "과학\|현상 던지기\|변인" plugin/skills/ko12-lesson-differentiation/references/social.md
```

기대: R 절 정확히 8개, 과학 잔존 0건.

- [ ] **Step 3: 삭제 + 커밋**

```bash
git rm plugin/skills/ko12-lesson-differentiation/references/science.md
git add plugin/skills/ko12-lesson-differentiation/references/social.md
git commit -m "feat: 차별화 사회과 레퍼런스 — R1~R8을 자료 기반 탐구 체계로 치환"
```

---

### Task 4: `curriculum-kr-mcp.md` ×2 — 사회 절 교체

**Files:**
- Modify: `plugin/skills/ko12-lesson-planning/references/curriculum-kr-mcp.md`
- Modify: `plugin/skills/ko12-lesson-differentiation/references/curriculum-kr-mcp.md`

**Interfaces:**
- Consumes: Task 1 실측(코드 형식·subject 파라미터 값·초등 verbatim 판정)
- Produces: "## 사회 (Social Studies)" 절 — 호출 시퀀스 6단계 구조는 과학 절과 동형 유지 (SKILL.md가 "사회 절을 따른다"로 참조).

- [ ] **Step 1: 두 파일 수정** — 서버 라우팅·성취기준 확정 절(과목 공통)은 유지하고:
  - "## 과학 (Science)" → "## 사회 (Social Studies)"로 교체. 6단계 구조(성취기준 → 선수관계 → 세부 주제 → 심화 연계 → 오개념 → 커리큘럼 자료 생략) 유지하되: `search_standards` 예시 쿼리·`subject` 파라미터 값·코드 예시를 실측값으로. 5단계 오개념 → "예상되는 학생 생각"(사회과는 오개념보다 선개념·고정관념 — 예: "법은 처벌을 위한 것", "지도의 위가 항상 북쪽" 유형)으로 명명 조정.
  - 초등 원문 주의 문단: Task 1 판정 결과로 갱신 (verbatim 확인 시 주의 문단을 "초등도 verbatim(실측 확인 2026-08-29)"로 교체, 아니면 유지).
  - 통합사회 라우팅 한 줄 추가: 코드 형식(실측)과 `schoolLevel: "high"` 지정.
- [ ] **Step 2: 두 사본 diff 확인** — 두 파일은 스킬별 문구 차이(planning/differentiation 절)만 남기고 사회 절은 동일해야 한다. `diff`로 의도된 차이만 있는지 확인.
- [ ] **Step 3: 커밋**

```bash
git add plugin/skills/*/references/curriculum-kr-mcp.md
git commit -m "feat: 학습맵 호출 시퀀스 사회 절 — 실측 코드 형식·통합사회 라우팅 반영"
```

---

### Task 5: SKILL.md ×2 — 과목 판별·전용 문구 diff

**Files:**
- Modify: `plugin/skills/ko12-lesson-planning/SKILL.md`
- Modify: `plugin/skills/ko12-lesson-differentiation/SKILL.md`

**Interfaces:**
- Consumes: Task 1 코드 신호, Task 2·3 레퍼런스 파일명(`social.md`)
- Produces: 발동 조건(description)·Step 0 라우팅이 사회과 신호로 동작. 이후 태스크(파일럿 생성)가 이 SKILL.md를 따른다.

- [ ] **Step 1: planning SKILL.md diff** — 변경 지점만 (그 외 무수정):
  - frontmatter description: 과학 신호("광합성" 등) → 사회 신호(예: "다음 주에 인권 단원 가르쳐야 해요", "중2 시장 경제 수업 준비") / "※ 이 스킬은 과학 전용" → "※ 이 스킬은 사회 전용이다(초3–6 사회·중학교 사회·고교 통합사회) — 다른 과목·고교 선택과목은 다루지 않는다."
  - Step 0-1: subject 판별 목록 → "**social** — 사회 현상·쟁점, 지리·일반사회·경제·정치·법·문화, 통합사회, 코드 [실측 코드 신호]" / 레퍼런스 경로 `references/social.md` / 범위 밖 안내 문구의 "과학" → "사회".
  - 본문 인라인 예시 2곳(Keeping the teacher posted의 예문, 5c 반복 옵션 예시)을 사회과 예문으로.
- [ ] **Step 2: differentiation SKILL.md diff** — 같은 요령: description 신호·"과학 전용" 문구·Step 0 판별·`references/social.md` 경로·학생 문서 eyebrow 규칙 `"[학년] 사회 · [성취기준 코드]"`(2곳)·학생 대면 언어 절의 과학 예시("CER" 문단은 유지하되 예문을 사회과로).
- [ ] **Step 3: 잔존 검사**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && grep -n "과학\|science.md\|광합성" plugin/skills/*/SKILL.md
```

기대: 0건 (SPDX 주석의 원본 경로 표기만 예외 — 해당 줄은 `원본:` 접두 확인).

- [ ] **Step 4: 커밋**

```bash
git add plugin/skills/*/SKILL.md && git commit -m "feat: SKILL.md 사회과 라우팅 — 발동 신호·과목 판별·전용 범위 교체"
```

---

### Task 6: 예시·스모크 교체 (red → green)

**Files:**
- Modify: `plugin/skills/ko12-lesson-planning/references/example_lesson.json` (사회과 소재로 교체)
- Modify: `tests/smoke/korean_lesson.json`, `tests/smoke/check_hwpx.py`

**Interfaces:**
- Consumes: Task 2 lesson.json 매핑 규칙
- Produces: `example_lesson.json` — SKILL.md가 "완전한 스키마·워크드 예시"로 지목하는 파일. 이후 파일럿 작성(Task 7)의 준거.

- [ ] **Step 1: check_hwpx.py 기대값을 먼저 사회과로 수정 (failing test)** — 파일을 읽고, 스모크 lesson JSON의 내용 문자열을 검사하는 지점(제목·과목명·특정 한글 문자열 assert)을 새 사회과 스모크 내용 기준으로 바꾼다. 이 시점에는 korean_lesson.json이 아직 과학 내용이므로 실패해야 정상.
- [ ] **Step 2: 실패 확인**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && bash plugin/skills/ko12-lesson-planning/scripts/render_all.sh tests/smoke/korean_lesson.json /tmp/smoke-red && PYTHONIOENCODING=utf-8 python tests/smoke/check_hwpx.py /tmp/smoke-red
```

기대: check_hwpx.py FAIL (기대 문자열 불일치).

- [ ] **Step 3: korean_lesson.json을 사회과 스모크로 교체** — 소재: 중학교 사회 1개 성취기준(Task 1 실측에서 선택), 문서 3종(lesson_plan·student_materials·observation_template) + `source_card` 1개 포함(사회과 고유 블록의 스모크 커버리지 확보). `shared.grade`는 `"Grade 8 · 중학교 2학년"` 형식.
- [ ] **Step 4: 통과 확인**

```bash
bash plugin/skills/ko12-lesson-planning/scripts/render_all.sh tests/smoke/korean_lesson.json /tmp/smoke-green && PYTHONIOENCODING=utf-8 python tests/smoke/check_hwpx.py /tmp/smoke-green
```

기대: PASS.

- [ ] **Step 5: example_lesson.json 교체** — 같은 소재를 확장한 완전판(SKILL.md 스키마의 블록 타입 커버: from_shared·faceted 키·source_card·fill_table·cards·group·answer_box 포함). 렌더로 자가 검증:

```bash
bash plugin/skills/ko12-lesson-planning/scripts/render_all.sh plugin/skills/ko12-lesson-planning/references/example_lesson.json /tmp/example-check && PYTHONIOENCODING=utf-8 python tests/check_hwpx_quality.py /tmp/example-check
```

- [ ] **Step 6: 커밋**

```bash
git add tests/smoke/ plugin/skills/ko12-lesson-planning/references/example_lesson.json
git commit -m "feat: 스모크·워크드 예시를 사회과로 교체 — source_card 커버리지 포함"
```

---

### Task 7: 파일럿 4종 재생성 + CI 갱신

**Files:**
- Create: `pilot/elementary/lesson.json`+`differentiation.json`(초4), `pilot/random-elementary/`(초5–6 무작위 추첨 단원), `pilot/middle-school/`(중), `pilot/high-integrated/lesson.json`(고1 통합사회 — 신설)
- Delete: `pilot/urgent-middle-school/` (과학판 시나리오 종속 — spec S-10의 4종 구성으로 대체)
- Modify: `.github/workflows/ci.yml` (파일럿 루프 목록)

**Interfaces:**
- Consumes: Task 2·3 pedagogy, Task 6 example, Task 1 실측 성취기준
- Produces: CI가 매번 새로 렌더·검사하는 사회과 파일럿 세트. Task 8 실채점의 대상.

- [ ] **Step 1: 소재 확정** — 학습맵 실측 호출로 성취기준 4건 선정: 초4 지역 관련 1건 / 초5–6은 실측 성취기준 목록에서 **무작위 추첨**(과학판 random-elementary 방법론: `python -c "import random; ..."` 절차를 `pilot/random-elementary/`에 ground-truth로 기록) / 중학교 일반사회 영역 1건 / 통합사회1 1건. 각 건의 officialText·linkedTopics·prerequisites를 조회해 파일럿 폴더에 `ground-truth.md`로 저장.
- [ ] **Step 2: lesson.json 4종 작성** — social.md의 해당 학년군 구조·섹션 7종·밀도 규칙 준수. 성취기준 원문은 실측값 문자 그대로(초등은 Task 1 판정에 따라 푸터 처리).
- [ ] **Step 3: differentiation.json 3종 작성** (elementary·middle-school·random-elementary) — R1~R8 준수, 학습지 3종 + teacher_plan.
- [ ] **Step 4: 전수 렌더 + DoD + 품질 검사**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills"
for p in elementary middle-school random-elementary high-integrated; do
  bash plugin/skills/ko12-lesson-planning/scripts/render_all.sh "pilot/$p/lesson.json" "/tmp/out-$p" && PYTHONIOENCODING=utf-8 python tests/check_lesson.py "pilot/$p/lesson.json" "/tmp/out-$p" || echo "FAIL $p"
done
for p in elementary middle-school random-elementary; do
  bash plugin/skills/ko12-lesson-differentiation/scripts/render_all.sh "pilot/$p/differentiation.json" "/tmp/diff-$p" || echo "FAIL diff $p"
done
PYTHONIOENCODING=utf-8 python tests/check_hwpx_quality.py /tmp/out-elementary /tmp/out-middle-school /tmp/out-random-elementary /tmp/out-high-integrated /tmp/diff-elementary /tmp/diff-middle-school /tmp/diff-random-elementary
```

기대: 전부 PASS. 실패 시 JSON을 고쳐 재렌더 (렌더러 수정 금지).

- [ ] **Step 5: ci.yml 파일럿 목록 교체** — 수업 4종 루프를 `elementary middle-school random-elementary high-integrated`로, 차별화 3종 루프는 유지. 주석의 과학판 문구 갱신.
- [ ] **Step 6: 한컴 실열림 확인 (로컬)** — 대표 2종(`/tmp/out-middle-school/lesson_plan.hwpx`, `/tmp/diff-elementary/worksheet_group_a.hwpx`)을 한글(HWP) COM으로 열어 오류 없음 확인 (과학판 품질 루프의 실열림 절차). CI로는 불가한 층이므로 결과를 커밋 메시지에 명기.
- [ ] **Step 7: 커밋**

```bash
git add pilot/ .github/workflows/ci.yml && git rm -r pilot/urgent-middle-school
git commit -m "feat: 사회과 파일럿 4종(통합사회 포함) — 전 검사 층 통과, 한컴 실열림 확인"
```

---

### Task 8: 루브릭 이식 + 1차 실채점

**Files:**
- Create: `evals/ko12-lesson-planning/rubrics/social.csv`
- Delete: `evals/ko12-lesson-planning/rubrics/science.csv`
- Modify: `evals/ko12-lesson-planning/rubrics/shared.csv`, `evals/ko12-lesson-differentiation/rubrics/differentiation.csv` (과학 전제 항목만), `evals/live-conversation/README.md` (보류 1줄), `evals/README.md`
- Create: `evals/runs/2026-08-29/` (실채점 결과)

**Interfaces:**
- Consumes: Task 7 렌더 산출물, social.md의 협상 불가 원칙(루브릭 기준의 출처)
- Produces: 사회과 루브릭 세트 + 첫 실채점 기록 (CHANGELOG 수치 주장의 근거).

- [ ] **Step 1: social.csv 작성** — science.csv의 P-S 계열을 사회과 기준으로 재작성. 최소 포함 (각각 What-pass-requires를 social.md 해당 절에서 도출, Notes에 출처 절 명기):
  - P-C1 3범주 분리 진술 (P-S1 이월 — 과정·기능 동사만 사회과형)
  - P-C2 차시 탐구 질문이 논쟁 가능하고 자료로 답할 수 있는가 (P-S2 앵커 현상의 치환)
  - P-C3 자료 실재성 — 출처(제목·생산자·연도) 명기, 미확인 자료 발췌 수록 금지
  - P-C4 주장-근거 결합 — 학생 산출 과제가 제시 자료의 근거 인용을 요구하는가
  - P-C5 논쟁 균형 — 입장 정답화·실재 정당/정치인 명명 없음
  - P-C6 (통사 한정, Conditional) 통합적 관점 — 둘 이상 영역 관점이 실제 과제에 나타나는가
- [ ] **Step 2: shared.csv·differentiation.csv 검토** — 전 항목을 훑어 과학 전제(현상·변인·실험) 문구가 있는 항목만 사회과 표현으로 수정, 항목 ID·구조 보존. P1(초등 verbatim 분기)은 Task 1 판정 반영.
- [ ] **Step 3: 실채점** — 과학판 방법론(`evals/runs/2026-08-08-diff/summary.md` 형식) 재사용: 파일럿 렌더 산출물을 루브릭 전 항목에 대해 판정하고 verdict JSON + summary.md 기록. 항목별 pass/fail/skip과 근거 인용. **fail은 고치고 재채점하거나 알려진 한계로 CHANGELOG에 명시** — 무기록 fail 금지.
- [ ] **Step 4: 커밋**

```bash
git add evals/ && git rm evals/ko12-lesson-planning/rubrics/science.csv
git commit -m "feat: 사회과 루브릭 이식 + 1차 실채점 — 결과는 evals/runs/2026-08-29"
```

---

### Task 9: 리네이밍·매니페스트·문서 전면 교체

**Files:**
- Modify: `README.md`, `DESIGN.md`, `CHANGELOG.md`, `NOTICE`, `.claude-plugin/marketplace.json`, `plugin/.claude-plugin/plugin.json`, 렌더러 메타 문자열(`render_lesson_hwpx.py` 2곳 ×2 사본), 전 파일 SPDX 추가줄, `plugin/skills/*/references/NOTICE`

**Interfaces:**
- Consumes: 전 태스크 완료 상태 (문서가 실태를 서술해야 하므로 마지막에서 두 번째)
- Produces: 설치 좌표 `newskool4d-sketch/social-teacher-skills`, 플러그인명 `social-teacher-skills` v0.1.0-preview.1.

- [ ] **Step 1: marketplace.json / plugin.json** — name·description·owner·homepage를 social판으로: name `social-teacher-skills`, homepage `https://github.com/newskool4d-sketch/social-teacher-skills`, version `0.1.0-preview.1`, description "한국 2022 개정 교육과정 기반 사회 수업 설계·수준별 차별화 스킬. …(과학판의 사회과 이식)".
- [ ] **Step 2: 렌더러 메타 문자열** — `render_lesson_hwpx.py`의 `content="science-teacher-skills render_lesson_hwpx"` → `social-teacher-skills`, `application="science-teacher-skills"` → `social-teacher-skills`. **두 스킬 사본 모두 동일 수정** 후:

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && for f in check_hwpx_min.py lesson_common.py render_documents.py render_lesson_html.py render_lesson_hwpx.py theme.css; do cmp "plugin/skills/ko12-lesson-planning/scripts/$f" "plugin/skills/ko12-lesson-differentiation/scripts/$f" && echo "OK $f"; done
```

- [ ] **Step 3: NOTICE 이중 계보** — 기존 Anthropic 표기 유지 + "이 저장소는 raphysicst-create/science-teacher-skills v0.3.0-preview.1 (Apache-2.0)의 사회과 이식판" 추가. references/NOTICE ×2 동일.
- [ ] **Step 4: README 재작성** — 과학판 README 구조 이월: 정의(사회 전용 — 초3–6·중 사회·통합사회) / 무엇을 만드나 / 설치(`/plugin marketplace add newskool4d-sketch/social-teacher-skills`) / 사용 예("중2 사회, 인권 보장과 헌법 45분 수업 만들어 줘") / 데이터 출처 / 원저작 표기(이중 계보 — 바꾼 지점: 과목 pedagogy 사회과 치환·범위) / 로드맵(live-conversation 보류 명시).
- [ ] **Step 5: DESIGN.md 개정** — 제목·1장 범위를 사회판으로, ADR에 "ADR-7 사회과 이식: 범위·자료 규칙·논쟁 가드레일 (spec 참조)" 추가, 기존 ADR-1~6은 계보 기록으로 유지.
- [ ] **Step 6: CHANGELOG** — `## [0.1.0-preview.1] — 2026-08-29` 신설: 사회과 이식 초판, 파일럿 4종, 실채점 결과 요약(Task 8 수치 인용), 알려진 한계(live-conversation 미실측, 고교 선택과목 미지원, 초1–2 특례). 과학판 이력은 "계보 — science-teacher-skills 시절" 절로 하단 보존.
- [ ] **Step 7: SPDX 추가줄 일괄** — 변경 파일들에 `SPDX-FileCopyrightText: 2026 social-teacher-skills contributors` 추가 (Python 스크립트로 일괄, 기존 줄 보존 검증 포함).
- [ ] **Step 8: 커밋**

```bash
git add -A && git commit -m "feat: social-teacher-skills 리네이밍 — 매니페스트·문서·계보 표기 v0.1.0-preview.1"
```

---

### Task 10: 전체 검증 (CI 로컬 재현 + 잔존 스윕)

**Files:** 없음 (검증 전용 — 발견 시 해당 태스크 파일로 돌아가 수정)

- [ ] **Step 1: CI 전 단계 로컬 재현** — ci.yml의 5개 스텝을 순서대로 로컬 실행 (사본 동일 cmp / 스모크+무결성 / 파일럿 수업 4종 DoD / 차별화 3종 / 품질 검사기 전체). 전부 PASS까지 수정 반복.
- [ ] **Step 2: 잔존 스윕**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && grep -rn "science-teacher-skills\|과학 전용\|raphysicst" --include="*.md" --include="*.json" --include="*.py" --include="*.yml" . | grep -v "docs/upstream\|docs/superpowers\|NOTICE\|원본:\|계보\|evals/runs/2026-08-0"
```

기대: 0건 (허용 예외: 업스트림 사본, 계획·조사 문서, NOTICE·SPDX 원본 표기, 과학판 시절 run 기록).

- [ ] **Step 3: 결과 보고** — 사용자에게 검증 결과 요약 (spec §5 DoD 6항 대조표).

---

### Task 11: push 게이트 (사용자 승인)

- [ ] **Step 1: 파일 목록 제시** — `git diff main --stat` 전체와 커밋 목록을 사용자에게 제시하고 push 승인을 청한다 (사용자 규칙 §8). **승인 전 push 금지.**
- [ ] **Step 2: 승인 시**

```bash
cd "C:/Users/홍주형/projects/social-teacher-skills" && git push -u origin feat/social-port
```

main 병합 방식(직접 push vs PR)도 이때 함께 확인한다.

---

## Self-Review 기록

- **Spec 커버리지**: S-1~S-10 → Task 9(S-1·S-7), 전 태스크(S-2), Task 1(S-3), Task 2·3(S-4), Task 9-2(S-5), Task 2~5(S-6), Task 8(S-8·S-9), Task 7(S-10). spec §4 전수 목록의 각 행이 Task 2~9 중 하나에 대응함을 확인. spec §5 DoD → Task 10 대조표.
- **과학판 함정 이월 확인**: 학년 문자열 첫 숫자 파싱(Task 2 매핑·Task 6 스모크에 명시), 중학교 분 합계 함정(Task 2 중1–3 경고 문단), 초등 verbatim(Task 1 실측 판정으로 상향 해소 경로 확보).
- **타입/이름 일관성**: 레퍼런스 파일명 `social.md`(Task 2·3 생성 = Task 5 참조), 파일럿 폴더명(Task 7 생성 = ci.yml 루프 = Task 8 실채점 대상), 루브릭 ID P-C1~P-C6(Task 8 내 폐쇄).
