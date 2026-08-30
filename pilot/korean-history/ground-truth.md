<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 고등학교 1학년 한국사1 `[10한사1-03-01]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(v0.1 controller Ruling 1 승계: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[10한사1-03-01]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
조선의 개항을 국제 질서의 변동과 연관하여 분석한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "key": "kr-2022-high-한국사1:[10한사1-03-01]",
  "code": "[10한사1-03-01]",
  "schoolLevel": "high",
  "gradeBand": "10",
  "subjectKorean": "한국사1",
  "domainKorean": "근대 국가 수립의 노력",
  "summary": "조선의 개항을 국제 질서의 변동과 연관하여 분석하기",
  "summaryKind": "mechanical-derivative",
  "sourceRefs": ["kr-nec-2024-3-annex7"],
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[10한사1-03-01]",
    "pdfPage": 104,
    "printedPage": null,
    "section": "한국사1 > 근대 국가 수립의 노력",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "deck6Id": "kr.standard.2022.high.2cc7228f1762c868dad9",
  "officialText": "조선의 개항을 국제 질서의 변동과 연관하여 분석한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.high.608243ccfaaabefa7d3a",
      "titleKorean": "한국사1 — 조선의 개항을 국제 질서의 변동과 연관하여 분석하기",
      "facetKey": null,
      "types": ["meta"]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건. 한국사1 전체의 edge가 0건이다
  (survey-v2 §4). 수업안의 선수 학습 줄에 "추정"을 단다.
- **심화 연계 문장을 쓰지 않는다.** 한국사1에서 나가는 전이는 데이터에 없다(survey-v2 §5).
- 한국사1은 표준 1건당 topic 1건(`facetKey: null`)이 붙는 1.00배 패턴이다(survey-v2 §2-2).
- 한국사1은 통합사회1·2와 같은 **고교 공통과목**(`courseCategory: "common"`, `gradeBand: "10"`)
  이다 — 선택과목이 아니다. `shared.subject`는 과목명 그대로 **`한국사1`**, `shared.grade`는
  `Grade 10 · 고등학교 1학년`.
- 영역명(`domainKorean`)은 **근대 국가 수립의 노력** — 역사 서술 가드레일 ③(복수 해석 병기)의
  발동 영역 다섯 곳 중 하나다.

## 4. 수록 사료의 출처 (파일럿 저작 근거)

성취기준과 달리 사료는 학습맵 데이터에 없다. 이 파일럿이 학생 지면(사료 묶음)에 수록한
사료 2종의 출처는 아래와 같다.

| 사료 | 구분 | 출처 |
|---|---|---|
| 사료 가 — 조일 수호 조규 제1관·제10관 (1876) | 수록 (발췌) | 국사편찬위원회 우리역사넷 '사료로 본 한국사' 국문 번역문, 출전 『고종실록』권13, 13년 2월 3일(을축) |
| 사료 나 — 최익현 지부복궐척화의소 (1876) | 수록 (발췌) | 국사편찬위원회 우리역사넷 '사료로 본 한국사' 국문 번역문, 출전 『면암선생문집』 권3, 소, 지부복궐척화의소 |

수록 사료가 2종이므로 `id: "source_packet"` 문서를 함께 낸다(짝 파일 history.md 매핑 규칙).
학생 학습지는 "사료 가와 사료 나는 사료 묶음에 있습니다."로 시작하고 사료 카드를 다시 싣지 않는다.

두 사료의 날짜는 **성격이 다른 표기**다. 사료 나는 아카이브 페이지의 '작성 연도' 줄을 그대로
옮긴 `1876년 1월 22일 (병자년)`이고, 사료 가는 출전 『고종실록』의 기사 날짜 표기다 — 그래서
카드에도 `고종 13년(1876) 2월 3일 — 『고종실록』 기사 표기`로 적었다. **아카이브는 사료 가의
양력 날짜를 주지 않았으므로 만들어 넣지 않았다.** 두 표기가 같은 역법인지는 자료에서 확인되지
않으며(확인 필요), 수업안은 학생에게 어느 쪽이 먼저인지까지만 견주게 한다(두 해석 어느 쪽에서도
사료 나가 앞선다).

`lesson_plan`의 연표에서 `(확인 필요)`가 붙은 연도(1882)와 위 역법 주석은 두 사료와 성취기준
원문 밖에서 온 훈련 지식이다 — 가드레일 ④에 따라 그 자리에 표기했고 학생 지면에는 싣지 않았다.
