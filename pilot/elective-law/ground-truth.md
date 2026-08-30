<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 고등학교 선택과목 법과 사회 `[12법사02-02]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 값은 전부 아래 클론의 데이터
파일에서 그대로 옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지
않았다(v0.1 controller Ruling 1 승계: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[12법사02-02]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/curriculum-standards.json` |
| 원문 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/standard-texts.json` |
| 학습 주제 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/topics.json` |
| 선수관계 파일 | `.superpowers/sdd/2026-08-29-social-port/external/secondary/data/kr/dependencies.json` |

## 1. 성취기준 원문 (byte-verbatim)

```
우리나라 헌법의 기본 원리와 기본권 내용을 이해하고, 기본권 제한의 요건과 한계를 탐구한다.
```

이 문자열이 `lesson.json`의 `shared.standard_text`와 바이트 단위로 같아야 한다.
어절 사이 공백까지 그대로 둔다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "key": "kr-2022-high-법과-사회:[12법사02-02]",
  "code": "[12법사02-02]",
  "schoolLevel": "high",
  "gradeBand": "10-12",
  "subjectKorean": "법과 사회",
  "domainKorean": "국가 생활과 법",
  "summary": "우리나라 헌법의 기본 원리와 기본권 내용을 이해하고, 기본권 제한의 요건과 한계를 탐구하기",
  "summaryKind": "mechanical-derivative",
  "sourceRefs": ["kr-nec-2024-3-annex7"],
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[12법사02-02]",
    "pdfPage": 230,
    "printedPage": null,
    "section": "법과 사회 > 국가 생활과 법",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "deck6Id": "kr.standard.2022.high.3025b98af80aab897a78",
  "officialText": "우리나라 헌법의 기본 원리와 기본권 내용을 이해하고, 기본권 제한의 요건과 한계를 탐구한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.high.b1d36c0386645ebd89f3",
      "titleKorean": "법과 사회 — 우리나라 헌법의 기본 원리와 기본권 내용을 이해하고, 기본권 제한의 요건과 한계를 탐구하기",
      "facetKey": null,
      "types": ["conceptual"]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건. 법과 사회 전체의 edge가 0건이다
  (survey-v2 §4). 수업안의 선수 학습 줄에 "추정"을 단다.
- **심화 연계 문장을 쓰지 않는다.** 사회과 선택과목은 전이 데이터가 없다(survey-v2 §5).
- 법과 사회는 표준 1건당 topic 1건(`facetKey: null`)이 붙는 1.00배 패턴이다(survey-v2 §2-3).
- 법과 사회는 `courseCategory: "career-elective"`(진로선택), `gradeBand: "10-12"`다. 이 파일럿의
  `shared.grade`는 `Grade 11 · 고등학교 2학년`이며 고교 세 학년의 답란 크기는 116pt로 같다.
- `shared.subject`는 실측 과목명 verbatim **`법과 사회`** — 띄어쓰기까지 그대로 둔다(커리큘럼
  엔트리 id는 `kr-2022-high-법과-사회`이지만 `subjectKorean`은 `법과 사회`다). 학생 문서
  `eyebrow`는 `"고등학교 2학년 법과 사회 · [12법사02-02]"`이다.
- ⚠ "일반사회 계열"은 데이터 필드가 아니라 **편집 구분**이다(survey-v2 §2-3·§6). 이 파일럿의
  자료·발문 강조(조문·판례 중심, 논쟁 가드레일 최고 강도)는 `social.md`의 과목군 표를 따른
  설계 판단이며, 데이터에 기록된 사실이 아니다.

## 4. 수록 자료의 출처 (파일럿 저작 근거)

성취기준과 달리 자료는 학습맵 데이터에 없다. 이 파일럿이 학생 지면(자료 묶음)에 수록한
자료 2종의 출처는 아래와 같다.

| 자료 | 구분 | 출처 |
|---|---|---|
| 자료 가 — 「대한민국헌법」 제37조 제1항·제2항 | 수록 (발췌) | 국가법령정보센터 법령 원문 (1988. 2. 25. 시행), korean-law-mcp `get_law_text(lawId="001444", jo="제37조")`로 조문 실검증 |
| 자료 나 — 「도로교통법」 제50조 제1항·제4항 | 수록 (발췌) | 국가법령정보센터 법령 원문 (2026. 7. 1. 시행), korean-law-mcp `get_law_text(lawId="001638", jo="제50조")`로 조문 실검증 |

수록 자료가 2종이므로 `id: "source_packet"` 문서를 함께 낸다(`social.md` 매핑 규칙).
학생 학습지는 "자료 가와 자료 나는 자료 묶음에 있습니다."로 시작하고 자료 카드를 다시 싣지 않는다.

**판례는 수록하지 않았다.** korean-law-mcp의 헌법재판소 결정 검색(`search_decisions`,
domain `constitutional`)이 '과잉금지원칙' 등 키워드에서 결과 0건을 반환해 조문처럼 실검증할
수 없었다. 검증되지 않은 결정문을 지면에 만들어 넣지 않고, 수업안에는 판례를 교사가 직접
검색해 조문과 견주게 하는 안내 한 줄만 두었다. 학생이 대는 심사 기준 세 칸(목적·형식·한계)은
자료 가 제2항의 문언에서 직접 뽑은 것이며, 조문 밖의 판단 기준을 정답처럼 제시하지 않는다.
