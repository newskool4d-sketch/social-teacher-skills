<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 중학교 3학년 사회(일반사회) `[9사(일사)04-03]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(controller Ruling 1: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[9사(일사)04-03]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
PDF 절취 과정의 어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "code": "[9사(일사)04-03]",
  "key": "kr-2022-middle-사회:[9사(일사)04-03]",
  "schoolLevel": "middle",
  "gradeBand": "7-9",
  "subjectKorean": "사회",
  "domainKorean": "정치과정과 시민 참여",
  "summary": "민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기",
  "summaryKind": "mechanical-derivative",
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[9사(일사)04-03]",
    "pdfPage": 64,
    "printedPage": null,
    "section": "사회 > 정치과정과 시민 참여",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "officialText": "민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.middle.04ffc06e7f400f60313b",
      "titleKorean": "사회 — 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기 — 자료·맥락 해석과 관점 비교",
      "type": "representational",
      "facetKey": "source-context",
      "evidence": [
        "학습자가 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기와 관련된 자료·표현·사례를 비교하거나 변환하고 그 의미와 관계를 설명한다. 이 증거는 ‘자료·맥락 해석과 관점 비교’ 후보 단위에 한정한다."
      ],
      "assessmentPrompts": [
        "민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기와 관련된 새로운 자료나 상황을 제시하고, ‘자료·맥락 해석과 관점 비교’ 관점에서 해석·수행·판단한 과정과 근거를 설명하게 한다."
      ]
    },
    {
      "id": "kr.topic.2022.middle.efee2185ac3806253e40",
      "titleKorean": "사회 — 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기 — 근거 기반 판단과 사회적 적용",
      "type": "meta",
      "facetKey": "evidence-judgment",
      "evidence": [
        "학습자가 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기에 대한 판단이나 수행을 근거와 함께 돌아보고 다음 적용에서 바꿀 점을 제안한다. 이 증거는 ‘근거 기반 판단과 사회적 적용’ 후보 단위에 한정한다."
      ],
      "assessmentPrompts": [
        "민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기와 관련된 새로운 자료나 상황을 제시하고, ‘근거 기반 판단과 사회적 적용’ 관점에서 해석·수행·판단한 과정과 근거를 설명하게 한다."
      ]
    },
    {
      "id": "kr.topic.2022.middle.fd8d44c96123f342c564",
      "titleKorean": "사회 — 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기",
      "type": "procedural",
      "facetKey": "core",
      "evidence": [
        "학습자가 민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기와 관련된 개념, 판단 근거 또는 수행 과정을 자신의 말이나 결과물로 보여 준다."
      ],
      "assessmentPrompts": [
        "민주주의의 발전을 위한 지방 자치의 중요성을 설명하고, 지역사회의 문제를 해결 하기 위한 시민 참여 활동을 계획하기와 관련된 과제나 사례를 제시하고, 학습자가 해결 과정과 근거를 설명하거나 수행하게 한다."
      ]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **원문의 어절 공백**: `해결 하기` — PDF 줄바꿈에서 온 공백이다. 중등 `officialText`는
  verbatim이 기본이지만 이런 절취 잡음이 섞인다. **정규화하지 않고 그대로** 넣는다.
- **선수 관계 기록이 없다.** 위 `prerequisiteEdges`가 **0건**이다 — 이 성취기준의 연결
  주제 3건은 `dependencies.json`에 `topicId`로도 `prerequisiteId`로도 등장하지 않는다.
  수업안에는 "학습맵에 이 성취기준의 선수 관계 기록이 없습니다"로 적는다.
- 전이 데이터 0건 — "이후 ___로 심화된다"를 쓰지 않는다.
- **example_lesson.json과 다른 성취기준**이다(예시는 `[9사(일사)01-01]`).
