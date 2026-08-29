<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 초등학교 4학년 사회 `[4사09-01]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(controller Ruling 1: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[4사09-01]` |
| 데이터 저장소 | `taehyeonglim/korean-elementary-learning-map-mcp` |
| 클론 HEAD | `e5c2c6b40081ce5c27ddd125a77e3a00574976a1` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
생활 주변에서 찾을 수 있는 여러 가지 문제를 파악하고, 그 문제를 합리적으로 해결하는 능력을 기른다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
PDF 절취 과정의 어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "code": "[4사09-01]",
  "key": "kr-2022-elem-social-studies:[4사09-01]",
  "gradeBand": "3-4",
  "subjectKorean": "사회",
  "domainKorean": "지역문제를 해결하고 지역을 알리는 노력",
  "summary": "생활 주변 문제를 합리적 절차로 해결하기",
  "sourceTextIncluded": false,
  "sourceLocator": {
    "sourceId": "kr-ncic-2022-social-pdf",
    "attachmentNo": "10003800",
    "sha256": "a852e8da3e6aea7d1c95690dcae140be02e014b779ac2e5cc0801200cfb16923",
    "pdfPage": 32,
    "pageLabel": "PDF p.32",
    "section": "지역문제를 해결하고 지역을 알리는 노력",
    "standardCode": "[4사09-01]"
  },
  "officialText": "생활 주변에서 찾을 수 있는 여러 가지 문제를 파악하고, 그 문제를 합리적으로 해결하는 능력을 기른다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.mt.social.3-4.4sa0901.concept",
      "titleKorean": "생활 주변 문제를 합리적 절차로 해결하기 — 핵심 개념 이해",
      "type": "CONCEPTUAL",
      "facetKey": null,
      "evidence": [
        "생활 주변 문제를 합리적 절차로 해결하기의 핵심 대상과 관계를 두 가지 이상 찾아 자신의 말로 설명한다.",
        "지역문제를 해결하고 지역을 알리는 노력 사례에서 배운 개념이 드러나는 장면을 선택하고 판단 근거를 제시한다."
      ],
      "assessmentPrompts": [
        "생활 주변 문제를 합리적 절차로 해결하기의 핵심 개념을 한국의 지역·역사·시민 생활 사례와 연결해 설명하고, 선택한 사례가 알맞은지 근거로 판단하게 한다."
      ]
    },
    {
      "id": "kr.mt.social.3-4.4sa0901.evidence",
      "titleKorean": "생활 주변 문제를 합리적 절차로 해결하기 — 자료 탐구와 해석",
      "type": "REPRESENTATIONAL",
      "facetKey": null,
      "evidence": [
        "생활 주변 문제를 합리적 절차로 해결하기에 관련된 서로 다른 자료 두 가지를 비교하여 공통점과 차이점을 설명한다.",
        "자료가 만들어진 시기와 목적을 구분하고, 자료에서 확인한 내용을 근거와 함께 제시한다."
      ],
      "assessmentPrompts": [
        "생활 주변 문제를 합리적 절차로 해결하기에 관련된 자료 두 가지를 비교·분석하고, 자료가 보여 주는 사실과 자신의 해석을 구분해 설명하게 한다."
      ]
    },
    {
      "id": "kr.mt.social.3-4.4sa0901.inquiry",
      "titleKorean": "생활 주변 문제를 합리적 절차로 해결하기 — 탐구와 참여",
      "type": "PROCEDURAL",
      "facetKey": null,
      "evidence": [
        "생활 주변 문제를 합리적 절차로 해결하기에 대한 조사 질문을 만들고 알맞은 자료를 찾아 조사 과정을 기록한다.",
        "조사 결과를 근거와 함께 설명하고 학교나 지역사회에서 실행할 제안을 한 가지 제시한다."
      ],
      "assessmentPrompts": [
        "생활 주변 문제를 합리적 절차로 해결하기에 대한 질문을 세우고 자료를 조사한 뒤, 한국 사회 맥락에 맞는 설명이나 참여 제안을 근거와 함께 제시하게 한다."
      ]
    }
  ],
  "prerequisiteEdges": [
    {
      "topicId": "kr.mt.social.3-4.4sa0901.evidence",
      "prerequisiteId": "kr.mt.social.3-4.4sa0901.concept",
      "strength": "hard",
      "reason": "[4사09-01]의 적용 주제는 같은 기준의 핵심 이해를 먼저 다루는 흐름이 자연스럽다.",
      "basis": "workstream-authored",
      "source": "workstream:social.json"
    },
    {
      "topicId": "kr.mt.social.3-4.4sa0901.inquiry",
      "prerequisiteId": "kr.mt.social.3-4.4sa0901.evidence",
      "strength": "soft",
      "reason": "[4사09-01]의 성찰 주제는 같은 기준의 자료 탐구 또는 수행 경험 뒤에 점검하는 흐름이다.",
      "basis": "workstream-authored",
      "source": "workstream:social.json"
    }
  ]
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선정 근거.** 브리프의 "초4 지역 관련 성취기준"은 성취기준 문장이 아니라 `domainKorean`
  (**지역문제를 해결하고 지역을 알리는 노력**)으로 충족된다. 문장 자체는 "생활 주변"으로
  적혀 있으나 이 영역 전체가 지역사회 문제 해결을 다룬다.
- **선수 학습은 "추정"으로 표시한다.** 위 `prerequisiteEdges` 2건은 **같은 성취기준
  `[4사09-01]` 내부의 하위 주제(concept → evidence → inquiry)를 이은 자체 저작 연결**이며
  (`basis: "workstream-authored"`), 공식 선수 근거가 아니다 — 학습맵 edge를 선수 근거로
  인용하지 않는다(social-map-survey.md §4). 수업안의 선수 학습은 차별화 R3의 기본 관문
  (자료 어휘 / 출처 확인 관례)을 "추정"으로 적는다.
- **심화 연계 문장을 만들지 않는다.** 사회과는 전이 데이터가 0건이다 —
  "이후 ___로 심화된다"를 쓰지 않는다(같은 문서 §5).
- **초등 원문 푸터.** `sourceTextIncluded: false`는 v0.4 시절의 낡은 메타플래그이고
  `officialText`는 NCIC 고시 PDF에서 자동 추출한 실제 원문이다(§3-2). 푸터는 "재구성"이
  아니라 "자동 추출 + 약 8% 절취 결함 가능"으로 쓴다.
