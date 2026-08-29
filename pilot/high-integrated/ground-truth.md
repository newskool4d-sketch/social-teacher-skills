<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 고등학교 1학년 통합사회1 `[10통사1-02-01]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(controller Ruling 1: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[10통사1-02-01]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
PDF 절취 과정의 어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "code": "[10통사1-02-01]",
  "key": "kr-2022-high-통합사회1:[10통사1-02-01]",
  "schoolLevel": "high",
  "gradeBand": "10",
  "subjectKorean": "통합사회1",
  "domainKorean": "인간, 사회, 환경과 행복",
  "summary": "시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰하기",
  "summaryKind": "mechanical-derivative",
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[10통사1-02-01]",
    "pdfPage": 116,
    "printedPage": null,
    "section": "통합사회1 > 인간, 사회, 환경과 행복",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "officialText": "시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.high.b5f90addaf1c0606280a",
      "titleKorean": "통합사회1 — 시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰하기",
      "type": "meta",
      "facetKey": null,
      "evidence": [
        "학습자가 시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰하기와 관련된 개념, 판단 근거 또는 수행 과정을 자신의 말이나 결과물로 보여 준다."
      ],
      "assessmentPrompts": [
        "시대와 지역에 따라 다르게 나타나는 행복의 기준을 사례를 통해 비교하여 평가하고, 삶의 목적으로서 행복의 의미를 성찰하기와 관련된 과제나 사례를 제시하고, 학습자가 해결 과정과 근거를 설명하거나 수행하게 한다."
      ]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건.
- 통합사회는 중→고 전이 데이터가 0건이다 — "이후 ___로 심화된다"를 쓰지 않는다.
- `shared.subject`는 과목명 그대로 **`통합사회1`**, `shared.grade`는
  `Grade 10 · 고등학교 1학년`.
- 영역명(`domainKorean`)은 **인간, 사회, 환경과 행복** — 통합사회1의 아홉 개념 영역 중
  하나이며, 열 번째 영역 '통합적 관점'은 별도 차시 소재가 아니라 이 영역을 보는 방법이다.
