<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 사회과 학습맵 실측 (2026-08-29)

Task 2~8은 이 문서의 값만 인용한다. 모든 항목은 아래 두 클론의 데이터 파일을 직접 읽어
확인했다 — **npx/node 실행은 전혀 하지 않았다** (controller Ruling 1). MCP 서버 코드(`src/*.mjs`)는
필드명 확인을 위해 문자열만 읽었고 실행하지 않았다.

## 0. 조사 방법 및 재현

| 항목 | secondary | elementary |
|---|---|---|
| repo | `raphysicst-create/korean-secondary-learning-map-mcp` | `taehyeonglim/korean-elementary-learning-map-mcp` |
| clone 방식 | `git clone --depth 1` | `git clone --depth 1` |
| HEAD commit | `964bfaef6e02781359288a6c1f55240bfb9c439d` (2026-08-25) | `e5c2c6b40081ce5c27ddd125a77e3a00574976a1` (2026-08-27) |
| package.json version | 0.3.0 | 0.5.2 |
| 클론 위치 | `.superpowers/sdd/2026-08-29-social-port/external/secondary` (git-ignored) | `.superpowers/sdd/2026-08-29-social-port/external/elementary` (git-ignored) |

- 추출 스크립트: `docs/superpowers/survey_social_map.py` (표준 라이브러리만, 커밋됨).
  재현: `python docs/superpowers/survey_social_map.py <secondary_clone_dir> <elementary_clone_dir>`
  (두 인자 모두 클론 루트 — 스크립트가 내부에서 `data/kr/`을 붙인다). 2026-08-29 클린 셸에서
  재실행해 exit code 0, 동일 출력 확인함 (아래 "검증" 절 참고).
- **주의 (모든 표에 적용)**: 이 조사는 두 저장소에 **커밋된 데이터 파일**을 읽은 것이며, 실행 중인
  MCP 서버가 `tools/call`로 실제 반환하는 JSON과 100% 동일하다는 보장은 없다. 도구별 응답 필드명은
  각 저장소의 `src/server.mjs`/`src/search.mjs`/`src/graph.mjs`를 읽어 대조했지만(실행 없이 grep/Read만),
  **파일럿 단계에서 MCP를 처음 실제로 호출할 때 이 문서와 실제 응답이 다르면 실제 응답이 우선한다**
  — 특히 아래 §7 "필드명 실측 차이"에 정리한 항목은 재검증 우선순위가 높다.

## 1. 코드 형식 (실측 verbatim)

| 학교급 | 코드 형식 | 실측 예시 (원문 verbatim) | 출처 |
|---|---|---|---|
| 초3–4 | `[4사NN-NN]` | `[4사01-01]`, `[4사01-02]`, `[4사02-01]` | elementary `data/kr/curriculum-standards.json` (사회 커리큘럼) |
| 초5–6 | `[6사NN-NN]` | `[6사01-01]`, `[6사01-02]`, `[6사02-01]` | 〃 |
| 중학교 사회 | `[9사(일사)NN-NN]` / `[9사(지리)NN-NN]` | `[9사(일사)01-01]`, `[9사(일사)01-02]`, `[9사(지리)01-01]` | secondary `data/kr/curriculum-standards.json` (subjectKorean="사회") |
| 통합사회1 | `[10통사1-NN-NN]` | `[10통사1-01-01]`, `[10통사1-01-02]`, `[10통사1-02-01]` | secondary 〃 (subjectKorean="통합사회1") |
| 통합사회2 | `[10통사2-NN-NN]` | `[10통사2-01-01]`, `[10통사2-01-02]`, `[10통사2-01-03]` | secondary 〃 (subjectKorean="통합사회2") |

중학교 사회는 **괄호 안에 세부 과목 태그(일사/지리)가 들어간다** — 코드만 보고 "사회"라고
정규식을 짜면 `(일사)`/`(지리)` 괄호를 놓치기 쉬우므로 §6 정규식에 명시했다. 역사는 `사회` 커리큘럼과
분리된 별도 커리큘럼(`[9역NN-NN]`)이다 — §6 제외 목록 참조.

## 2. 과목·영역 구조

### 2-1. 중학교 "사회" 과목

- **커리큘럼 엔트리 수**: 1개 (`id: kr-2022-middle-사회`, `subjectKorean: "사회"`, `subjectGroupKorean: "사회(역사 포함)"`,
  `courseCategory: "common"`, `gradeBand: "7-9"`, `standardCount: 74`). 역사는 별도 엔트리(`subjectKorean: "역사"`, 40건).
- 74건 = 일사 36건 + 지리 38건 (코드 접두로 구분, 같은 커리큘럼 엔트리 안에 공존).
- **영역명(도메인, 실측 24개)**:

| 계열 | 영역명 (실측, 12개씩) |
|---|---|
| 일사 | 인간과 사회생활 · 다양한 문화의 이해 · 민주주의와 시민 · 정치과정과 시민 참여 · 일상생활과 법 · 인권과 기본권 · 헌법과 국가기관 · 경제생활과 선택 · 시장과 가격 · 우리나라 경제와 세계화 · 국제 사회와 한반도 · 사회 변동과 사회문제 |
| 지리 | 세계화 시대, 지리의 힘 · 아시아 · 유럽 · 아프리카 · 아메리카 · 오세아니아와 극지방 · 대한민국, 우리가 살아가는 곳 · 우리나라의 자연환경과 인간 생활 · 중부 지역 · 남부 지역 · 북부 지역 · 지속가능한 세계와 글로컬 시민 |

출처: secondary `data/kr/curriculum-standards.json`.

### 2-2. 통합사회1·2

| 과목명(실측 subjectKorean) | gradeBand | 표준 수 | 영역명(실측 domainKorean) |
|---|---|---|---|
| 통합사회1 | 10 | 14 | 통합적 관점 · 인간, 사회, 환경과 행복 · 자연환경과 인간 · 문화와 다양성 · 생활공간과 사회 |
| 통합사회2 | 10 | 16 | 인권보장과 헌법 · 사회정의와 불평등 · 시장경제와 지속가능발전 · 세계화와 평화 · 미래와 지속가능한 삶 |

출처: secondary `data/kr/curriculum-standards.json`.

**spec §3.5의 "9개 핵심 개념" 재확인 결과**: 데이터에 별도 "핵심개념" 필드는 없다 —
`domainKorean`(영역명) 10개가 실측값이며, spec이 나열한 9개 개념은 이 영역명 안에 **복합**되어 있다.
대응표:

| spec의 핵심 개념 | 실측 영역명(domainKorean) |
|---|---|
| 행복 | 인간, 사회, 환경과 행복 |
| 자연환경 | 자연환경과 인간 |
| 생활공간 | 생활공간과 사회 |
| 문화 | 문화와 다양성 |
| 인권 | 인권보장과 헌법 |
| 정의 | 사회정의와 불평등 |
| 시장 | 시장경제와 지속가능발전 |
| 세계화 | 세계화와 평화 |
| 지속가능한 삶 | 미래와 지속가능한 삶 |
| (대응 없음) | **통합적 관점** — 9개 개념과 별도로 통합사회1의 도입 영역(방법론 프레이밍), 개념이 아니라 관점 |

→ Task 2·3에서 "9개 핵심 개념"을 언급할 때는 반드시 위 오른쪽 열(실측 영역명)을 verbatim으로
쓸 것. "통합적 관점"은 10번째 영역으로 함께 언급하되 "핵심 개념"이 아니라 "통합적 접근의 방법론적
관점"으로 구분해서 쓴다.

### 2-3. 제외 대상 (범위 밖) 과목명 — spec §1 표현과 실측 차이

spec은 "정치와 법"을 제외 예시로 들었으나, **2022 개정 실제 데이터에는 "정치와 법"이라는
과목이 없다** — 대신 "정치"(`[12정치`, 16건)와 "법과 사회"(`[12법사`, 13건) **두 개의 별도 과목**으로
분리되어 있다 (2015 개정의 "정치와 법"이 개편된 것으로 보임). 후속 태스크에서 "정치와 법"을
인용하지 말고 아래 §6 표의 실제 과목명을 쓸 것.

## 3. 원문 수록 상태 (verbatim 판정)

### 3-1. 중등·통합사회 — officialText는 항상 verbatim (실측 확인)

secondary는 `standard-texts.json`(3,838건, PDF 페이지·sha256 pinning)에서 `get_standard`가
`officialText`를 채운다 (`src/server.mjs:202`: `officialText: store.textsByKey.get(standard.key) ?? null`).
사회·통합사회1·2 샘플 전수 스팟체크 결과 전부 정상적인 성취기준 문장("~한다"로 종결, 해설·평가
방법 안내 등 잡음 없음)이었다. `sourceTextIncluded`/`sourceBasis` 필드 자체가 secondary에는
**없다** (verbatim이 당연하므로 별도 플래그가 불필요한 설계) — `summaryKind: "mechanical-derivative"`
필드로 "summary는 기계 생성, officialText만 원문"임을 표시한다. 이 부분은 과학판 참조 문서
(`curriculum-kr-mcp.md`)의 서술과 일치한다.

### 3-2. 초등 — 3단 판정 (⚠ 표 브리프의 핵심 질문에 대한 답)

**브리프의 질문("초등 README의 '원문 620건 수록' 주장 vs 과학판의 'verbatim 아님' 전제, 어느 쪽이
현재 설치 버전의 실태인가")에 대한 실측 답변은 "양쪽 다 부분적으로 맞고, 과학판 참조 문서는
갱신이 필요하다"** — 아래 3가지가 동시에 참이다.

1. **officialText는 실제 공식 원문이다 (재구성 아님).** v0.5.0(devlog: "성취기준 원문 620건 수록",
   `CHANGELOG.md`)에서 `standard-texts.json`(버전 `kr-standard-texts-v1`, `generatedAt:
   2026-07-28T09:17:36.960Z`, `sourceNote: "교육부 공표 공공저작물(NCIC 공개 PDF)에서 추출한 성취기준
   본문"`)이 신규 추가됐다. `get_standard`는 이 파일에서 코드로 조회해 `officialText`를 채운다
   (`src/server.mjs:123`: `officialText: store.textsByCode.get(standard.code) ?? null`) — **`focus`나
   `summary`를 조립한 값이 아니다.** 과학판 참조 문서의 "`officialText` 필드는 존재하지만
   `focus + "할 수 있다"`로 조립된 값이다"라는 문장은 **이 버전(v0.5.2) 기준으로는 사실이 아니다** —
   그 문서는 `standard-texts.json`이 없던 구버전(v0.4 이하) 기준으로 쓰인 것으로 보인다.
2. **레코드 자체의 메타 플래그는 여전히 "false"다 (갱신 안 됨, 모순).** `curriculum-standards.json`의
   사회 표준 49건 전부 `sourceTextIncluded: false`, `sourceBasis: "...the summary is repository-authored
   and does not quote the official standard text."`, 최상위 `textPolicy.standardTextIncluded: false`.
   이 필드들은 `standard-texts.json`이 추가되기 전(v0.4) 시점 그대로 남아 있는 **낡은/모순된 메타데이터**다
   — `get_standard`는 이 필드를 무시하고 `standard-texts.json`을 직접 조회하므로 실제 동작에는
   영향이 없지만, 이 필드만 보고 "verbatim 아님"이라 판단하면 틀린다.
3. **레코드별 추출 품질이 균일하지 않다 (스팟체크 결과).** 사회 49건 전수를 휴리스틱으로 스캔한 뒤
   수동으로 원문을 읽어 판정했다:

   | 판정 | 건수 | 코드 |
   |---|---|---|
   | 정상 (성취기준 원문으로 보임, 줄바꿈 공백 등 경미한 PDF 추출 잡음만 있음) | 44/49 | 나머지 전부 |
   | **결함 — 해설/평가방법 문단이 섞여 있거나 문장 중간부터 시작·다음 단원 제목까지 침범** | 4/49 | `[4사01-01]`, `[4사01-02]`, `[4사07-02]`, `[6사10-02]` |
   | 경미한 잡음만 (성취기준 문장 자체는 온전, 끝에 페이지 꼬리말 "25 사회과 교육과정"이 붙음) | 1/49 | `[4사08-02]` |

   예: `[6사10-02]`의 `text` 값은 "에서 본격적으로 학습하고, ... (10) 세계의 자연환경"로 끝나
   **다음 단원 제목까지 포함**돼 있다 — `locator: "pattern-match"`(정규식 기반 자동 절취)의
   경계 오류로 보인다. 출처: elementary `data/kr/standard-texts.json`.

**초등 재구성 푸터 규칙 유지 여부 — 판정**: 완전 유지도, 완전 폐기도 아니다. **문구를 다음과 같이
교체할 것을 권고**한다 (Task 4가 그대로 복사해서 쓸 수 있도록 여기 확정):

> 기존 문구(폐기): "초등 성취기준 문장은 학습맵의 요약 필드에서 재구성된 것입니다. 공식 고시문과
> 대조해 확인하세요."
>
> **신규 권고 문구**: "초등 성취기준 원문은 NCIC 고시 PDF에서 자동 추출한 것입니다(재구성 아님).
> 다만 일부 항목(약 8%)은 절취 과정에서 해설 문단이 섞이거나 문장이 잘렸을 수 있으니, 인용 전
> 공식 고시문과 대조해 확인하세요."

### 3-3. 필드 존재 여부 비교표 (사회 표준 레코드 1건 기준)

| 필드 | secondary(사회) | elementary(사회) | 비고 |
|---|---|---|---|
| `summary` | 있음 (`mechanical-derivative`) | 있음 (`sourceBasis`: repository-authored) | 둘 다 인용 금지 대상, 의미는 다름 |
| `summaryKind` | 있음 (`"mechanical-derivative"`) | **없음** | 초등은 이 라벨이 없다 — summary가 원문이 아님을 알리는 수단은 `sourceBasis` 문장뿐 |
| `sourceLocator` | 있음 (PDF쪽·sha256) | 있음 (PDF쪽·sha256) | 양쪽 다 출처 추적 가능 |
| `sourceTextIncluded` | **없음** (필드 자체가 없음 — verbatim이 기본값) | 있음, 값은 `false` (§3-2 참고 — 낡은 값) | 초등에만 존재하는 필드, 신뢰도 낮음 |
| `sourceBasis` | **없음** | 있음 | 초등에만 존재 |
| `focus` | **없음** (secondary는애초 이 필드 개념이 없음) | **없음** (사회 49건 전부 0/49) | §7 참조 — 과학판 문서의 "focus" 주장은 사회에는 적용 안 됨 |

출처: secondary/elementary 각 `data/kr/curriculum-standards.json` 표준 레코드 1건씩 key 비교.

## 4. 선수관계 (prerequisites)

| 항목 | secondary | elementary |
|---|---|---|
| 전체 dependencies 건수 | 266 | 1,894 |
| 사회/통합사회 관련 topic 수 | 252 (전체 topic 5,284건 중) | 147 (전체 1,956건 중, 사회만) |
| 사회/통합사회 관련 edge 수 | **1건** | **98건** |
| edge의 성격 | 공식 근거 기반, **교차 성취기준**(cross-standard) | 전부 **동일 코드 내부** 하위주제 연결(concept→evidence→inquiry), cross-standard 0건 |
| edge `basis` 예시 | `"국가교육위원회 고시 제2024-3호 별책7 사회·역사과 교육과정 성취기준 해설 p.54"` (공식 문서 근거) | `"workstream-authored"` (자체 저작, 공식 근거 아님) |

**edge 존재 사례** (secondary, `data/kr/dependencies.json`):
```
topicId(선수 필요) = [9사(지리)12-03] "...지역 문제를 해결 방안 모색과 실천으로 확장한다."
prerequisiteId(선수) = [9사(지리)07-03]
reason: "앞서 발견한 지역 문제를 해결 방안 모색과 실천으로 확장한다."
```

**edges: [] 사례** (secondary, topicId `kr.topic.2022.middle.3004ad3c1125f03f7bce`,
표준 `[9사(일사)01-01]`) — 이 topic은 `dependencies.json`에 `topicId`로 한 번도 등장하지 않으므로
`get_prerequisites(topicId, direction:"prerequisites")` 호출 시 `edges: []`가 반환된다.
secondary는 사회 관련 topic 252건 중 **251건**이 이 상태다(직접 선수 없음). elementary도
`edges: []` 사례가 있다 — 사회 topic 49건(각 성취기준의 "concept" 유형 하위주제)은 그 자체가
선수가 없는 뿌리 노드다 (예: `kr.mt.social.3-4.4sa0101.concept`).

**결론**: 사회과에서 "학습맵에 공식 근거가 있는 선수관계"는 secondary 기준 극히 드물다(266건 중
1건만 사회) — Task 4/skill 작성 시 "edge가 없는 성취기준이 많다"는 과학판의 경고가 사회과에는
**더 강하게** 적용된다고 서술할 것. 반면 elementary는 edge가 조밀하지만 전부 같은 성취기준의
하위 주제를 순서대로 이은 것(workstream 자체 저작)이라 "공식 선수관계 근거"로 인용해서는 안 된다.

## 5. 통합사회 전이 (중→고 transitions)

**0건.** secondary `data/kr/transitions.json`(전체 175건)에는 순수 사회/통합사회(1·2) 관련
전이가 **없다**. 사회 계열과 걸치는 전이는 2건뿐이며 둘 다 **역사**(범위 밖) 관련이다:

| from | to | transitionKind | reason(발췌) |
|---|---|---|---|
| 역사 | 세계사 | deepens | "중학교 역사 학습을 기반으로 문명 형성 주제를 심층적으로 탐구한다." |
| 역사 | 한국사1 | deepens | "중학교 한국사 학습에 이어 근대 국가 수립 주제를 근현대사 중심으로 심화한다." |

→ 통합사회1·2, 중학교 사회(일사/지리)는 `get_transitions` 호출 시 항상 빈 배열이 반환될 것으로
예상된다. Task 4의 curriculum-kr-mcp.md "심화 연계" 절에서 사회과는 이 문장을 써야 한다: "이 내용은
이후 ___로 심화된다"는 **생성하지 않는다** (전이 데이터가 아예 없음, 훈련 지식으로 대체 서술 금지).

## 6. 스킬이 쓸 코드 신호 목록 (Step 0 과목 판별용)

### 포함 (사회과 이식 범위)

| 학교급 | 정규식(문자 그대로 사용 가능) | 실측 건수 |
|---|---|---|
| 초3–4 사회 | `^\[4사\d{2}-\d{2}\]$` | 22건 |
| 초5–6 사회 | `^\[6사\d{2}-\d{2}\]$` | 27건 |
| 중학교 사회 | `^\[9사\((일사\|지리)\)\d{2}-\d{2}\]$` | 74건 (일사 36 + 지리 38) |
| 통합사회1 | `^\[10통사1-\d{2}-\d{2}\]$` | 14건 |
| 통합사회2 | `^\[10통사2-\d{2}-\d{2}\]$` | 16건 |

**⚠ 초등 예외**: 초등 사회(`[4사…]`/`[6사…]`)는 지리·일반사회·역사가 코드로 분리되지 않는다 —
"일상에서 만나는 과거", "유적과 유물로 살펴본 옛 사람들의 생활", "식민 통치와 저항, 전쟁이 바꾼
사회와 생활" 같은 **역사 성격의 영역도 전부 `[4사…]`/`[6사…]` 코드를 그대로 쓴다**. spec §1은
초3–6 사회 전체를 범위에 포함하므로 문제는 없지만, "역사는 제외"라는 규칙을 초등에도 그대로
적용해 정규식으로 필터링하려 하면 안 된다 — 초등은 과목 자체가 통합돼 있어 코드로 역사 콘텐츠만
솎아낼 수 없다.

### 제외 (범위 밖 — 실제 과목명·코드접두 실측)

| 학교급 | 과목명(실측) | 코드 접두 | 건수 |
|---|---|---|---|
| 중 | 역사 | `[9역` | 40 |
| 고(공통) | 한국사1 | `[10한사1-` | 13 |
| 고(공통) | 한국사2 | `[10한사2-` | 13 |
| 고(일반선택) | 세계사 | `[12세사` | 13 |
| 고(일반선택) | 사회와 문화 | `[12사문` | 15 |
| 고(일반선택) | 세계시민과 지리 | `[12세지` | 13 |
| 고(진로선택) | 정치 | `[12정치` | 16 |
| 고(진로선택) | 법과 사회 | `[12법사` | 13 |
| 고(진로선택) | 경제 | `[12경제` | 12 |
| 고(진로선택) | 국제 관계의 이해 | `[12국관` | 12 |
| 고(진로선택) | 동아시아 역사 기행 | `[12동역` | 12 |
| 고(진로선택) | 한국지리 탐구 | `[12한탐` | 15 |
| 고(융합선택) | 금융과 경제생활 | `[12금융` | 12 |
| 고(융합선택) | 기후변화와 지속가능한 세계 | `[12기지` | 12 |
| 고(융합선택) | 도시의 미래 탐구 | `[12도탐` | 12 |
| 고(융합선택) | 여행지리 | `[12여지` | 12 |
| 고(융합선택) | 역사로 탐구하는 현대 세계 | `[12역현` | 14 |
| 고(융합선택) | 사회문제 탐구 | `[12사탐` | 12 |
| 고(도덕 교과군, 일반선택) | 현대사회와 윤리 | `[12현윤` | 17 |

(spec §1의 "정치와 법"은 실제 데이터에 없음 — §2-3 참고. "정치"·"법과 사회" 두 과목으로 대체해서 쓸 것.)

## 7. 필드명 실측 vs 과학판 참조 문서(`curriculum-kr-mcp.md`) — 차이점

과학판 두 스킬(`ko12-lesson-planning`/`ko12-lesson-differentiation`)의
`references/curriculum-kr-mcp.md`를 실제 서버 소스와 대조한 결과, 아래 항목은 **문서와 실측이
다르다** — Task 4가 이 파일을 사회과용으로 다시 쓸 때 고쳐야 한다.

| 항목 | 과학판 문서의 서술 | 실측 결과 | 근거(파일) |
|---|---|---|---|
| `get_prerequisites` depth=1 응답 필드명 | `directEdges: []`라고 서술 | 실제 필드명은 **`edges`** (`{topicId, direction, edges: [...]}`) | secondary/elementary `src/server.mjs` (`get_prerequisites` 핸들러) — `directEdges`는 내부 함수 이름일 뿐, 응답 키는 `edges` |
| 초등 `search_standards` 요약 필드 | "`summary`가 아니라 `focus`"라고 서술 | **사회는 focus가 0/49건** — search_standards 결과에 사회는 요약 텍스트가 아예 없음(코드/영역명만). focus는 수학·과학·도덕·실과에만 있음 | elementary `data/kr/curriculum-standards.json`(사회 표준 전수), `src/search.mjs`(`compactStandard()`가 `focus`만 노출, `summary` 미노출) |
| 초등 verbatim 여부 | "verbatim이 아니다"(`sourceTextIncluded: false` 근거) | §3-2 참조 — **officialText 자체는 진짜 원문**(v0.5.0부터), 단 레코드 메타플래그가 낡음 + 8%가 추출 결함 | elementary `data/kr/standard-texts.json` |
| 초등·중등 성취기준 subject 공유 | "코드 공유 과목 11개, subject로 구분 필요" | 사회/통합사회 코드는 **공유 과목에 포함되지 않음** — 사회과는 code만으로 유일하게 정해짐 (`get_standard`에 `subject` 불필요) | secondary `data/kr/curriculum-standards.json` 전수 스캔 |

## 8. 부록 — 대표 레코드 (get_standard/get_topic 응답 형태 재현)

아래 JSON은 `docs/superpowers/survey_social_map.py` §3 섹션이 각 저장소의 `curriculum-standards.json`
+ `standard-texts.json`(+elementary는 `topics.json`)을 병합해 재구성한 것으로, 실제 MCP
`get_standard`/`get_topic` 도구가 반환할 값과 같은 모양이다 (필드 구성 로직은 `src/server.mjs`를
그대로 따라했다). **주의**: 실행 결과가 아니라 정적 병합이므로, 필드 순서·부가 필드(`hint` 등)는
실제 MCP 응답과 다를 수 있다.

### 8-1. 초등 — `get_standard("[6사01-01]")` 재현

```json
{
  "key": "kr-2022-elem-social-studies:[6사01-01]",
  "code": "[6사01-01]",
  "gradeBand": "5-6",
  "subjectKorean": "사회",
  "domainKorean": "우리나라 국토 여행",
  "summary": "우리나라 산지·하천·해안 지형의 분포 탐구하기",
  "sourceTextIncluded": false,
  "sourceLocator": { "sourceId": "kr-ncic-2022-social-pdf", "pdfPage": 34, "section": "우리나라 국토 여행" },
  "sourceBasis": "Achievement-standard code and PDF page placement were checked against [별책7] 사회과 교육과정.pdf ...; the summary is repository-authored and does not quote the official standard text.",
  "officialText": "우리나라 산지, 하천, 해안 지형의 위치를 확인하고 지형의 분포 특징을 탐구한다.",
  "linkedTopics": [
    { "id": "kr.mt.social.5-6.6sa0101.concept", "titleKorean": "우리나라 산지·하천·해안 지형의 분포 탐구하기 — 핵심 개념 이해" },
    { "id": "kr.mt.social.5-6.6sa0101.evidence", "titleKorean": "우리나라 산지·하천·해안 지형의 분포 탐구하기 — 자료 탐구와 해석" },
    { "id": "kr.mt.social.5-6.6sa0101.inquiry", "titleKorean": "우리나라 산지·하천·해안 지형의 분포 탐구하기 — 탐구와 참여" }
  ]
}
```

(주: `sourceTextIncluded: false`인데 `officialText`는 실제로 채워진다 — §3-2 판정 참조. 필드 전체
목록은 스크립트 raw 출력 §[2c] 참조.)

### 8-2. 중학교 — `get_standard("[9사(일사)01-01]")` 재현

```json
{
  "key": "kr-2022-middle-사회:[9사(일사)01-01]",
  "code": "[9사(일사)01-01]",
  "schoolLevel": "middle",
  "gradeBand": "7-9",
  "subjectKorean": "사회",
  "domainKorean": "인간과 사회생활",
  "summary": "사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰하기",
  "summaryKind": "mechanical-derivative",
  "sourceLocator": { "pdfPage": 61, "section": "사회 > 인간과 사회생활", "sourceId": "kr-nec-2024-3-annex7" },
  "officialText": "사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰한다.",
  "linkedTopics": [
    { "id": "kr.topic.2022.middle.3004ad3c1125f03f7bce", "titleKorean": "사회 — ... — 자료·맥락 해석과 관점 비교" },
    { "id": "kr.topic.2022.middle.44a62aa07dbf9d80b41a", "titleKorean": "사회 — ... — 근거 기반 판단과 사회적 적용" },
    { "id": "kr.topic.2022.middle.d2fcd0f6be6ee37f6d38", "titleKorean": "사회 — ..." }
  ]
}
```

### 8-3. 통합사회1 — `get_standard("[10통사1-01-01]")` 재현

```json
{
  "key": "kr-2022-high-통합사회1:[10통사1-01-01]",
  "code": "[10통사1-01-01]",
  "schoolLevel": "high",
  "gradeBand": "10",
  "subjectKorean": "통합사회1",
  "domainKorean": "통합적 관점",
  "summary": "인간, 사회, 환경을 바라보는 시간적, 공간적, 사회적, 윤리적 관점의 의미와 특징을 사례를 통해 파악하기",
  "summaryKind": "mechanical-derivative",
  "sourceLocator": { "pdfPage": 115, "section": "통합사회1 > 통합적 관점", "sourceId": "kr-nec-2024-3-annex7" },
  "officialText": "인간, 사회, 환경을 바라보는 시간적, 공간적, 사회적, 윤리적 관점의 의미와 특징을 사례를 통해 파악한다."
}
```

### 8-4. 학습 주제(topic) 레코드 — evidence/assessmentPrompts 필드 예시

중학교 사회 [9사(일사)01-01]의 연결 주제 중 하나 (`get_topic` 재현, secondary `data/kr/topics.json`
원본 그대로):

```json
{
  "id": "kr.topic.2022.middle.3004ad3c1125f03f7bce",
  "titleKorean": "사회 — 사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰하기 — 자료·맥락 해석과 관점 비교",
  "schoolLevel": "middle",
  "subjectKorean": "사회",
  "gradeBand": "7-9",
  "domainKorean": "인간과 사회생활",
  "facetKey": "source-context",
  "types": ["representational"],
  "description": "사회의 인간과 사회생활 영역에서 사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰하기를 '자료·맥락 해석과 관점 비교' 관점으로 분해한 세부 학습 주제 후보다.",
  "evidence": [
    "학습자가 사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰하기와 관련된 자료·표현·사례를 비교하거나 변환하고 그 의미와 관계를 설명한다. 이 증거는 '자료·맥락 해석과 관점 비교' 후보 단위에 한정한다."
  ],
  "assessmentPrompts": [
    "사회화의 의미를 일상생활의 사례를 들어 설명하고, 사회화 과정에서 형성되는 자아 정체성에 대해 성찰하기와 관련된 새로운 자료나 상황을 제시하고, '자료·맥락 해석과 관점 비교' 관점에서 해석·수행·판단한 과정과 근거를 설명하게 한다."
  ],
  "standards": ["kr-2022-middle-사회:[9사(일사)01-01]"],
  "sourceRefs": ["kr-nec-2024-3-annex7"]
}
```

(참고: `edges: []`가 되는 예시로도 이 topic을 쓸 수 있다 — `dependencies.json`에 `topicId`로
한 번도 등장하지 않는다. §4 참조.)

## 9. 참고 — elementary 클론의 manifest.json 무결성 관찰 (파일럿 리스크, Task 1 차단 아님)

이 git 스냅샷(HEAD `e5c2c6b4`) 한정으로, `data/kr/manifest.json`이 **같은 클론 안의 실제 데이터
파일과 전부 어긋나 있다** (5개 파일 전부 바이트 수·sha256 불일치, `manifest.json`이 참조하는
`*.seed.json` 8개·`workstreams/*.json` 9개는 아예 존재하지 않음 — v0.4 모노레포 시절의 낡은
manifest로 보인다). `src/data-store.mjs`의 `readVerified()`는 체크섬이 안 맞으면 `throw`하므로,
**이 git 클론을 그대로 실행하면(`node src/cli.mjs`) 서버가 기동을 거부한다.**

- 이 관찰은 **이 git 클론에만 한정**된다 — npm에 배포된 `korean-elementary-learning-map-mcp` 타볼이
  같은 문제를 갖는지는 확인하지 않았다(타볼을 받아 확인하는 것은 이번 조사 범위 밖).
  release 절차(`CLAUDE.md` "배포 절차")상 `npm publish` 전에 `pipeline:verify`가 manifest 해시를
  다시 기록하므로, 배포본은 정상일 가능성이 있다 — **확인되지 않은 가정이다.**
  Task 1을 막지는 않는다(데이터 내용 판독에는 영향 없음 — JSON 파싱은 체크섬과 무관) — **파일럿
  단계(Task 7)에서 실제 npx 설치본으로 스모크 실행할 때 이 문제가 재현되는지 먼저 확인할 것.**
  재현되면 security-vet 심사 전에 "설치본이 기동을 거부한다"는 그 자체가 별도 이슈가 된다.

## 검증 (재현성)

2026-08-29, 클린 셸에서 재실행:
```
python docs/superpowers/survey_social_map.py \
  .superpowers/sdd/2026-08-29-social-port/external/secondary \
  .superpowers/sdd/2026-08-29-social-port/external/elementary
```
exit code 0, 402줄 출력. 이 문서의 모든 수치·예시 코드·JSON은 위 실행 출력에서 그대로 옮겨 적었다
(재구성·훈련 지식 추정 없음). 원본 raw 출력은 커밋하지 않는다(브리프 지시 — 추출 사실만 문서화).
