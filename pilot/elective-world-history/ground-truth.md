<!--
SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
SPDX-License-Identifier: Apache-2.0
-->

# 파일럿 ground truth — 고등학교 선택과목 세계사 `[12세사03-03]`

이 문서는 이 파일럿의 **판정 근거 자료(ground truth)** 다. 성취기준 값은 아래 두 곳에서 그대로
옮겼다 — 재타이핑·재구성·훈련 지식 추정 없음. MCP 서버 코드는 실행하지 않았다(v0.1 controller
Ruling 1 승계: 데이터 파일 직접 판독).

| 항목 | 값 |
|---|---|
| 성취기준 | `[12세사03-03]` |
| 데이터 저장소 | `raphysicst-create/korean-secondary-learning-map-mcp` |
| 클론 HEAD | `964bfaef6e02781359288a6c1f55240bfb9c439d` |
| 표준 레코드 | `data/kr/curriculum-standards.json` (클론 루트 기준) |
| 원문 파일 | `data/kr/standard-texts.json` |
| 학습 주제 파일 | `data/kr/topics.json` |
| 선수관계 파일 | `data/kr/dependencies.json` |
| 선택과목 실측 추출본 | `electives-latest.json` (manifest `2026-08-21T05:14:58.671Z`) — 과목 `세계사`, `course: "세계사 2022 개정 고등학교 교육과정"`, `category: "general-elective"`, `count: 13`, `transitions: []`, `courseRelations: []`, `dependencies: 0` |

> ⚠ **locator 불일치 기록.** 실측 추출본 `electives-latest.json`의 이 성취기준 `locator`는 `null`이다.
> 같은 HEAD의 클론 `curriculum-standards.json`에는 아래 §2의 `sourceLocator`(pdfPage 151)가 들어 있어,
> 레코드 전문은 기존 파일럿과 같은 방식으로 클론 값에서 병합 재현했다. officialText·영역·summary는 두
> 출처가 문자 단위로 같다. (기존 파일럿 ground-truth의 `.superpowers/sdd/…/external/secondary/` 경로는 이
> 작업 트리에 없어, 실제로 판독한 클론 상대 경로를 적었다.)

## 1. 성취기준 원문 (byte-verbatim)

```
제1⋅2차 산업 혁명이 가져온 사회, 경제, 생태환경의 변화를 분석한다.
```

이 문자열이 `lesson.json`·`differentiation.json`의 `shared.standard_text`와 바이트 단위로
같아야 한다. `제1⋅2차`의 가운뎃점은 **U+22C5**(⋅)이며, 3범주 라벨(`지식·이해`)의 U+00B7(·)과
다른 문자다 — 정규화하지 않는다.

## 2. 레코드 전문 (`get_standard` + `get_topic` + `get_prerequisites` 병합 재현)

```json
{
  "key": "kr-2022-high-세계사:[12세사03-03]",
  "code": "[12세사03-03]",
  "schoolLevel": "high",
  "gradeBand": "10-12",
  "subjectKorean": "세계사",
  "domainKorean": "국민 국가의 형성",
  "summary": "제1⋅2차 산업 혁명이 가져온 사회, 경제, 생태환경의 변화를 분석하기",
  "summaryKind": "mechanical-derivative",
  "sourceRefs": ["kr-nec-2024-3-annex7"],
  "sourceLocator": {
    "attachmentNo": "10003993",
    "code": "[12세사03-03]",
    "pdfPage": 151,
    "printedPage": null,
    "section": "세계사 > 국민 국가의 형성",
    "sha256": "7383ec75add6dae0d1c2138ecfe36dc2c762ab980a96db4aafccface33979e06",
    "sourceId": "kr-nec-2024-3-annex7"
  },
  "deck6Id": "kr.standard.2022.high.6b288370023eacba0a84",
  "officialText": "제1⋅2차 산업 혁명이 가져온 사회, 경제, 생태환경의 변화를 분석한다.",
  "officialTextLocator": "pattern-match",
  "linkedTopics": [
    {
      "id": "kr.topic.2022.high.e0844b37480ff6b60a86",
      "titleKorean": "세계사 — 제1⋅2차 산업 혁명이 가져온 사회, 경제, 생태환경의 변화를 분석하기",
      "facetKey": null,
      "types": ["meta"]
    }
  ],
  "prerequisiteEdges": []
}
```

## 3. 성취기준 선택 근거

세계사 13건 가운데 이 차시를 고른 기준은 과업이 정한 세 가지다.

| 기준 | `[12세사03-03]`에서 |
|---|---|
| 사료 2종으로 탐구 가능 | 서술어가 '분석한다'(사료 분석형). 공장 아동 체벌에 대해 크게 다른 모습을 그리는(늘 맞았다 / 드물고 본 적이 없다) 1차 사료 2종 — 노동자 증언(1832)과 공장제 옹호 저술(1835) — 이 작성 주체·기록 형태·장소·시점 모두 달라 교차 검증거리가 선다 |
| 사실 확인 가능 | 두 사료 모두 저작권이 만료된 영어 원문을 직접 판독했다(§5). 사료 나는 1835년 책의 디지털 스캔 본문에서 쪽(pp. 300–301)까지 확인 |
| 논쟁 위험 관리 가능 | 산업 혁명의 사회적 영향은 평가가 갈리지만 현대 정당·정치 쟁점과 직접 닿지 않는다. 해석 A(비용 강조)·B(이전 삶과 비교)를 각각 다른 사료에 기대어 같은 분량으로 병기할 수 있다 |

견주어 본 후보와 배제 이유:
- `[12세사03-02]`(미국·프랑스 혁명 — '파악한다'): 두 선언문은 모두 의회 단위의 선언이라 작성 주체의 긴장이
  약하고, 서술어가 사실·흐름형에 가까워 사료 1종 구조로 기운다.
- `[12세사04-01]`·`[12세사04-02]`(세계 대전·냉전): 사료 다수가 현대 저작권 대상이거나 현존 국가·정치 쟁점과
  직접 닿아 가드레일 부담이 크다.

**범위 한정(과대 주장 금지).** 성취기준은 제1·2차 산업 혁명과 사회·경제·생태환경 세 측면을 함께 묶는다.
두 사료는 모두 제1차 산업 혁명기 섬유 공장의 아동 노동에 관한 것이므로, 이 차시는 **사회 변화 측면만** 다룬다.
수업안 '단원 맥락'에 경제·생태환경 측면과 제2차 산업 혁명은 다른 차시에서 다룬다고 적었고, 순서는 가정하지
않았다.

## 4. 이 파일럿에서의 사용 규칙

- **선수 관계 기록이 없다** — `prerequisiteEdges` 0건, 세계사 전체 `dependencies: 0`. 수업안의 선수 학습 줄에
  "추정"을 단다.
- **심화 연계 문장을 쓰지 않는다.** 세계사의 `transitions`·`courseRelations`가 모두 비어 있다. 실측 전이
  '중학교 역사 → 세계사(문명 형성 주제)'는 세계사로 **들어오는** 1건이며 이 성취기준과 무관하다.
- 세계사는 이 성취기준에 topic 1건(`facetKey: null`, `types: ["meta"]`)이 붙는다.
- `category: "general-elective"`(일반선택), `gradeBand: "10-12"`. 이 파일럿의 `shared.grade`는
  `Grade 11 · 고등학교 2학년`(선택과목 고2 가정)이며 차시는 고교 기본값 50분이다.
- `shared.subject`와 문서 `eyebrow`는 실측 과목명 verbatim **`세계사`**. 학생 문서 `eyebrow`는
  `"고등학교 2학년 세계사 · [12세사03-03]"`이다.
- 세계사는 현행 두 스킬의 `references/history.md` 지원 범위다. 이 파일럿은 그 파일의 **고등학교
  (한국사1·2·역사 선택과목) 분기(복수 해석 검토, 7/15/10/13/5 = 50분)**를 적용했고, 가드레일 ③(복수 해석
  병기)을 켰다 — ③ 발동은 history.md '역사 선택과목별 조정' 절의 세계사 규정('국민 국가의 형성'·'현대
  세계의 과제')을 따른다. 이 두 영역 발동은 학습맵 데이터 사실이 아니라 파일럿 작성자의 설계 제안을 채택한
  것이다.

## 5. 수록 사료의 출처 (파일럿 저작 근거)

성취기준과 달리 사료는 학습맵 데이터에 없다. 두 사료 모두 학생 지면(사료 묶음·차별화 학습지 3종)에 발췌를
수록했다. **두 사료의 한국어 문장은 출판된 번역본을 쓰지 않고 영어 원문에서 이 파일럿 작성자가 직접 옮긴 것이다**(기존 한국어 번역본의 유무는 조사하지 않았다) —
주어·시제·판단의 강도는 원문대로 두었고 원문에 없는 평가를 넣지 않았다.

| 사료 | 구분 | 원문 출처(판독 경로) | 번역 |
|---|---|---|---|
| 사료 가 — 엘리자베스 벤틀리의 하원 특별위원회 증언(문·답 12쌍 발췌, 생략 자리는 "…" 줄로 표시) | 수록 (발췌) | Parliamentary Papers 1831–32, vol. XV, p. 195. 판독본: Jonathan F. Scott·Alexander Baltzly 편 *Readings in European History Since 1814*(New York: F. S. Crofts & Co., 1930) 재수록본을 옮긴 Victorian Web 사본 — https://victorianweb.org/history/workers1.html (2026-10-29 열람). 출판지·출판사는 Open Library 목록(New York, F. S. Crofts & Co., 1930)과 인터넷 아카이브 메타데이터(`readingineuropia0000jona`, F. S. Crofts & Co., 1930)로 확인했다. Victorian Web 쪽은 출판사를 Appleton-Century-Crofts로 적어 어긋난다(인터넷 아카이브에는 같은 제목의 Appleton-Century-Crofts판 사본도 따로 있다). 재수록 쪽 번호는 확인하지 못했다 — Victorian Web 사본에 쪽 표기가 없고 인터넷 아카이브 1930년판은 대출 제한이라 본문 검색이 되지 않는다. | 이 파일럿 작성자 |
| 사료 나 — Andrew Ure, *The Philosophy of Manufactures*, pp. 300–301 발췌 | 수록 (발췌) | 2nd ed., corrected (London: Charles Knight, 1835), Book III ch. I, pp. 300–301. 판독본: 웰컴 컬렉션 디지털 사본, 인터넷 아카이브 식별자 `b29288824`(OCR 본문 `b29288824_djvu.txt`에서 쪽 번호 300·301 확인) | 이 파일럿 작성자 |

- 사료 가의 질문 줄("Suppose you flagged a little, or were too late, what would they do?", "Are they in the habit of
  strapping those who are last in doffing?" 등)은 유도성 질문을 지면에 남겨 생산 조건을 묻게 하려고 일부러 함께
  실었다. 공장 이름·작업 종류·아침 식사 등 사이의 문답은 생략하고 그 자리에 "…" 줄을 두었다. 1930년 독본의 머리말도 이 질문들이 자주 유도적이었다고
  적는다.
- 사료 나의 첫 문장("Hence, ill-usage of any kind is a very rare occurrence.")은 p. 300 끝에서 시작해 p. 301로 넘어가며,
  앞에 "…"를 두고 실었다. 이 문장을 빼면 Ure가 체벌을 전면 부정한 것처럼 읽혀 판단의 강도가 원문보다 세지기
  때문이다. "그러므로"가 받는 바로 앞 내용 — 공장주는 조수를 학대하는 방적공을 벌금 처분하거나 내보낸다는 서술,
  그리고 그 앞(p. 300)에 Ure가 인용한 선서 증언("Who is it that beats the children? — The spinner.",
  "Are the children ever beaten? — Sometimes they get beat, but not severely …", 각주 Supplementary Factory
  Commission Report, p. 193) — 은 학생 지면에 싣지 않았다. 즉 Ure는 체벌을 전면 부정하지 않고 '드물고, 방적공이
  했으며, 자신은 보지 못했다'고 쓴다. 그래서 두 사료의 관계를 '정면으로 어긋난다'고 쓰지 않고 '크게 다르게
  그린다'로 적었다(2026-10-29 원문 재대조).
- 사료 나의 "lively elves"는 "활발한 꼬마 요정들"로 옮겼고 반어나 평가어를 덧붙이지 않았다.
- 증언 일자(1832년 6월 4일)는 2차 교육 사이트에만 있어 쓰지 않았다. 사료 가의 날짜 줄은 위원회가 열린 해인
  1832년까지만 적었다.

**교사용 문서에만 둔 배경(확인 필요 표기).** 위원회가 선서 없이 증언을 받았고 유도 질문·증인 선정이 당시에도
비판받았다는 점, 1833년 정부 조사가 긴 노동 시간은 확인했으나 체벌은 줄었다고 보았고 그 조사가 반대쪽으로
치우쳤다는 1836년 맨체스터 의사의 비판이 있었다는 점(문서는 공장주 편향을 직접 단정하지 않음), 1833년 공장법은 영어판 위키백과 'Sadler report' 문서로만 대조했다. 그래서
수업안 해당 위치에 `(확인 필요)`를 달았고 학생 지면에는 싣지 않았다. 현대 역사가의 이름은 쓰지 않았다.
