<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 고등학교 선택과목 경제 `[12경제03-03]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(v0.1 controller Ruling 1 승계: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[12경제03-03]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
경기 변동의 의미와 요인을 이해하고, 경기 안정화 방안으로 재정 정책과 통화 정책을 분석한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "key": "kr-2022-high-경제:[12경제03-03]",
  "code": "[12경제03-03]",
  "schoolLevel": "high",
  "gradeBand": "10-12",
  "subjectKorean": "경제",
  "domainKorean": "거시 경제",
  "summary": "경기 변동의 의미와 요인을 이해하고, 경기 안정화 방안으로 재정 정책과 통화 정책을 분석하기",
  "summaryKind": "mechanical-derivative",
  "sourceRefs": ["kr-nec-2024-3-annex7"],
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[12경제03-03]",
    "pdfPage": 242,
    "printedPage": null,
    "section": "경제 > 거시 경제",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "deck6Id": "kr.standard.2022.high.9aff96c304995afa0159",
  "officialText": "경기 변동의 의미와 요인을 이해하고, 경기 안정화 방안으로 재정 정책과 통화 정책을 분석한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.high.dc4fa0e49d67d46bf0a4",
      "titleKorean": "경제 — 경기 변동의 의미와 요인을 이해하고, 경기 안정화 방안으로 재정 정책과 통화 정책을 분석하기",
      "facetKey": null,
      "types": ["meta"]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건. 경제 전체의 edge가 0건이다
  (survey-v2 §4). 수업안의 선수 학습 줄에 "추정"을 단다.
- **심화 연계 문장을 쓰지 않는다.** 사회과 선택과목은 전이 데이터가 없다(survey-v2 §5).
- 경제는 표준 1건당 topic 1건(`facetKey: null`)이 붙는 1.00배 패턴이다(survey-v2 §2-3).
- 경제는 `courseCategory: "career-elective"`(진로선택), `gradeBand: "10-12"`다. 선택과목은
  2·3학년도 이수하므로 `shared.grade`의 영문 학년을 실제 이수 학년으로 쓴다 — 이 파일럿은
  `Grade 11 · 고등학교 2학년`이며 고교 세 학년의 답란 크기는 116pt로 같다.
- `shared.subject`는 실측 과목명 verbatim **`경제`** — 계열명("일반사회")이나 축약형으로
  바꾸지 않는다. 학생 문서 `eyebrow`는 `"고등학교 2학년 경제 · [12경제03-03]"`이다.
- ⚠ "일반사회 계열"은 데이터 필드가 아니라 **편집 구분**이다(survey-v2 §2-3·§6). 이 파일럿의
  자료·발문 강조(정량 근거 필수)는 `social.md`의 과목군 표를 따른 설계 판단이며, 데이터에
  기록된 사실이 아니다.

## 4. 수록 자료의 출처 (파일럿 저작 근거)

성취기준과 달리 자료는 학습맵 데이터에 없다. 이 파일럿이 학생 지면에 수록한 자료 1종의
출처는 아래와 같으며, 정량 자료 1종은 지목만 한다.

| 자료 | 구분 | 출처 |
|---|---|---|
| 자료 가 — 「한국은행법」 제1조·제6조 | 수록 (발췌) | 국가법령정보센터 법령 원문 (2026. 1. 2. 시행), korean-law-mcp `get_law_text(lawId="001550")`로 조문 실검증 |
| 자료 나 — 기준금리·소비자물가상승률 시계열 | 지목 | 한국은행 경제통계시스템(ECOS, ecos.bok.or.kr) 화면 |

정량 자료를 **지목으로 둔 것은 의도된 설계**다. 확인할 수 없는 정확 수치를 지면에 만들어
넣지 않고, 학생이 화면에서 값을 직접 찾아 인용하게 한다 — 발문 2·3과 형성 확인이 수치 인용을
요구하므로 경제 계열의 "정량 근거 필수"는 과제 구조로 강제된다.
