<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 중학교 3학년 역사 `[9역13-03]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(v0.1 controller Ruling 1 승계: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[9역13-03]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
한국의 민주화 과정에서 나타난 성과와 과제를 탐구한다.
```

이 문자열이 `lesson.json`·`differentiation.json`의 `shared.standard_text`와 바이트 단위로
같아야 한다. 어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "key": "kr-2022-middle-역사:[9역13-03]",
  "code": "[9역13-03]",
  "schoolLevel": "middle",
  "gradeBand": "7-9",
  "subjectKorean": "역사",
  "domainKorean": "근⋅현대 사회로의 전환",
  "summary": "한국의 민주화 과정에서 나타난 성과와 과제를 탐구하기",
  "summaryKind": "mechanical-derivative",
  "sourceRefs": ["kr-nec-2024-3-annex7"],
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[9역13-03]",
    "pdfPage": 91,
    "printedPage": null,
    "section": "역사 > 근⋅현대 사회로의 전환",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "deck6Id": "kr.standard.2022.middle.aba8da7f7f776df15358",
  "officialText": "한국의 민주화 과정에서 나타난 성과와 과제를 탐구한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.middle.551fd86ed6a29228e1bf",
      "titleKorean": "역사 — 한국의 민주화 과정에서 나타난 성과와 과제를 탐구하기",
      "facetKey": "core",
      "types": ["conceptual"]
    },
    {
      "id": "kr.topic.2022.middle.5d3cb75848d0a484aa98",
      "titleKorean": "역사 — 한국의 민주화 과정에서 나타난 성과와 과제를 탐구하기 — 자료·맥락 해석과 관점 비교",
      "facetKey": "source-context",
      "types": ["representational"]
    },
    {
      "id": "kr.topic.2022.middle.1d7de09b8b02b5eff97d",
      "titleKorean": "역사 — 한국의 민주화 과정에서 나타난 성과와 과제를 탐구하기 — 근거 기반 판단과 사회적 적용",
      "facetKey": "evidence-judgment",
      "types": ["meta"]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건. 중학교 역사 전체에서 edge는 1건뿐이며
  그것은 `[9역09-03]`이다(survey-v2 §4). 수업안·차별화 수업안의 선수 학습 줄에 "추정"을 단다.
- **심화 연계 문장을 쓰지 않는다.** 역사에서 나가는 실측 전이 2건은 세계사·한국사1이며 그 근거는
  '근대 국가 수립' 주제다(survey-v2 §5) — 민주화를 다루는 이 차시에 그 edge를 끌어다 쓰지 않는다.
- 중학교 역사는 표준 1건당 topic 3건(`core` / `source-context` / `evidence-judgment`)이 붙는
  3.00배 패턴이다(survey-v2 §2-1).
- `shared.subject`는 과목명 그대로 **`역사`**, `shared.grade`는 `Grade 9 · 중학교 3학년`.
- 영역명(`domainKorean`)은 **근⋅현대 사회로의 전환** — 가운뎃점은 U+22C5이며 원문 표기 그대로
  옮긴다. 이 영역은 역사 서술 가드레일 ③(복수 해석 병기)의 발동 영역 다섯 곳 중 하나다.

## 4. 수록 사료의 출처 (파일럿 저작 근거)

성취기준과 달리 사료는 학습맵 데이터에 없다. 이 파일럿이 학생 지면에 수록한 사료 1종의
출처는 아래와 같으며, 나머지 1종은 지목만 한다.

| 사료 | 구분 | 출처 |
|---|---|---|
| 사료 가 — 대한민국 임시 헌장 제1조~제3조 (1919) | 수록 (발췌) | 국사편찬위원회 우리역사넷 '사료로 본 한국사' 국문 번역문, 출전 「대한민국임시헌장선포문」 |
| 사료 나 — 역대 선거 투표율 통계 | 지목 | 중앙선거관리위원회 선거통계시스템(info.nec.go.kr) 화면 |

`lesson_plan`의 연표에서 `(확인 필요)`가 붙은 연도(1948·1960·1987)는 위 두 사료와 성취기준
원문 밖에서 온 훈련 지식이다 — 가드레일 ④에 따라 그 자리에 표기했고 학생 지면에는 싣지 않았다.
