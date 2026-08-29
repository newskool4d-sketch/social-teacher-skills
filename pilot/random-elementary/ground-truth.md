<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 초등학교 5학년 사회 `[6사01-02]` (무작위 추첨)

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(controller Ruling 1: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[6사01-02]` |
| 데이터 저장소 | `taehyeonglim/korean-elementary-learning-map-mcp` |
| 클론 HEAD | `e5c2c6b40081ce5c27ddd125a77e3a00574976a1` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/elementary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
독도의 지리적 특성과 독도에 대한 역사 기록을 바탕으로 영토로서 독도의 중요성을 이해 한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
PDF 절취 과정의 어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "code": "[6사01-02]",
  "key": "kr-2022-elem-social-studies:[6사01-02]",
  "gradeBand": "5-6",
  "subjectKorean": "사회",
  "domainKorean": "우리나라 국토 여행",
  "summary": "독도의 지리·역사 자료로 영토적 중요성 이해하기",
  "sourceTextIncluded": false,
  "sourceLocator": {
    "sourceId": "kr-ncic-2022-social-pdf",
    "attachmentNo": "10003800",
    "sha256": "a852e8da3e6aea7d1c95690dcae140be02e014b779ac2e5cc0801200cfb16923",
    "pdfPage": 34,
    "pageLabel": "PDF p.34",
    "section": "우리나라 국토 여행",
    "standardCode": "[6사01-02]"
  },
  "officialText": "독도의 지리적 특성과 독도에 대한 역사 기록을 바탕으로 영토로서 독도의 중요성을 이해 한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.mt.social.5-6.6sa0102.concept",
      "titleKorean": "독도의 지리·역사 자료로 영토적 중요성 이해하기 — 핵심 개념 이해",
      "type": "CONCEPTUAL",
      "facetKey": null,
      "evidence": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기의 핵심 대상과 관계를 두 가지 이상 찾아 자신의 말로 설명한다.",
        "우리나라 국토 여행 사례에서 배운 개념이 드러나는 장면을 선택하고 판단 근거를 제시한다."
      ],
      "assessmentPrompts": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기의 핵심 개념을 한국의 지역·역사·시민 생활 사례와 연결해 설명하고, 선택한 사례가 알맞은지 근거로 판단하게 한다."
      ]
    },
    {
      "id": "kr.mt.social.5-6.6sa0102.evidence",
      "titleKorean": "독도의 지리·역사 자료로 영토적 중요성 이해하기 — 자료 탐구와 해석",
      "type": "REPRESENTATIONAL",
      "facetKey": null,
      "evidence": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기에 관련된 서로 다른 자료 두 가지를 비교하여 공통점과 차이점을 설명한다.",
        "자료가 만들어진 시기와 목적을 구분하고, 자료에서 확인한 내용을 근거와 함께 제시한다."
      ],
      "assessmentPrompts": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기에 관련된 자료 두 가지를 비교·분석하고, 자료가 보여 주는 사실과 자신의 해석을 구분해 설명하게 한다."
      ]
    },
    {
      "id": "kr.mt.social.5-6.6sa0102.inquiry",
      "titleKorean": "독도의 지리·역사 자료로 영토적 중요성 이해하기 — 탐구와 참여",
      "type": "PROCEDURAL",
      "facetKey": null,
      "evidence": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기에 대한 조사 질문을 만들고 알맞은 자료를 찾아 조사 과정을 기록한다.",
        "조사 결과를 근거와 함께 설명하고 학교나 지역사회에서 실행할 제안을 한 가지 제시한다."
      ],
      "assessmentPrompts": [
        "독도의 지리·역사 자료로 영토적 중요성 이해하기에 대한 질문을 세우고 자료를 조사한 뒤, 한국 사회 맥락에 맞는 설명이나 참여 제안을 근거와 함께 제시하게 한다."
      ]
    }
  ],
  "prerequisiteEdges": [
    {
      "topicId": "kr.mt.social.5-6.6sa0102.evidence",
      "prerequisiteId": "kr.mt.social.5-6.6sa0102.concept",
      "strength": "hard",
      "reason": "[6사01-02]의 적용 주제는 같은 기준의 핵심 이해를 먼저 다루는 흐름이 자연스럽다.",
      "basis": "workstream-authored",
      "source": "workstream:social.json"
    },
    {
      "topicId": "kr.mt.social.5-6.6sa0102.inquiry",
      "prerequisiteId": "kr.mt.social.5-6.6sa0102.evidence",
      "strength": "soft",
      "reason": "[6사01-02]의 성찰 주제는 같은 기준의 자료 탐구 또는 수행 경험 뒤에 점검하는 흐름이다.",
      "basis": "workstream-authored",
      "source": "workstream:social.json"
    }
  ]
}
```

## 3. 무작위 추첨 절차 (재현 가능)

```python
import json, random, re
# 1) 풀 구성 — elementary 클론의 curriculum-standards.json에서 초5-6 사회 코드를 전부 모아
#    코드 문자열 오름차순으로 정렬한다.
pool_all = sorted(c for c in codes if re.match(r"^\[6사\d{2}-\d{2}\]$", c))   # 27건
# 2) 사전 등록 제외 — social-map-survey.md §3-2가 원문 추출 결함으로 판정한 항목만 뺀다.
EXCLUDE = ["[6사10-02]"]                                                      # 1건
pool = [c for c in pool_all if c not in EXCLUDE]                              # 26건
# 3) 추첨 — 씨앗 고정.
random.Random(20260830).choice(pool)                                          # → [6사01-02]
```

- **정렬 기준**: 코드 문자열 오름차순(`sorted()` 기본, 유니코드 코드포인트 순).
  풀 전체: `[6사01-01] … [6사12-02]`, `[6사10-02]` 제외.
- **씨앗**: `20260830` (추첨 실행일).
- **제외 규칙은 추첨 전에 등록했다** — 결과를 보고 다시 뽑지 않았다. 제외 사유는 오직
  "원문 추출 결함"이며 소재 선호가 아니다.
- 추첨 결과 `[6사01-02]`는 대한민국 국가 교육과정이 내용으로 확정한 성취기준이다
  (사회적 미합의 쟁점이 아니므로 논쟁 가드레일의 "정답화 금지" 대상이 아니다).
  수업은 자료에서 근거를 찾아 쓰는 구조로 설계하고, 외국 정부·정당·정치인을 대립 축으로
  세우지 않는다.

## 4. 이 파일럿에서의 사용 규칙

- **원문의 어절 공백**: `이해 한다` — PDF 줄바꿈에서 온 공백이다. **정규화하지 않고 그대로**
  `shared.standard_text`에 넣는다(byte-verbatim).
- **선수 학습은 "추정"**: 위 `prerequisiteEdges`는 같은 코드 내부의 자체 저작 연결이라
  공식 선수 근거로 인용하지 않는다.
- 전이 데이터 0건 — "이후 ___로 심화된다"를 쓰지 않는다.
