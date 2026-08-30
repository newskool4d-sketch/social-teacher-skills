# SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
# SPDX-License-Identifier: Apache-2.0
"""역사·선택과목 실측 조사 스크립트 (v0.2.0 Task 1).

korean-secondary-learning-map-mcp 저장소를 `git clone --depth 1`로 받은 뒤, 그 안의
`data/kr/*.json`을 직접 읽어 역사 계열(중 역사·고 한국사1·2)과 사회과 선택과목
(일반사회·지리 계열의 일반/진로/융합선택) 관련 사실을 뽑아낸다. npx/node 실행은 전혀
하지 않는다 (실행 회피는 v1 controller ruling을 그대로 승계).

초등(elementary) 저장소는 이 조사 범위에 없다 — 초등 사회는 역사·지리·일반사회가
코드로 분리되지 않고 전부 `[4사..]`/`[6사..]`로 통합되어 있음이 v1 survey §6에서
이미 확인됐고, v0.2.0은 중·고 역사 계열과 고교 선택과목만 증분 추가하기 때문이다.

사용법 (저장소 루트에서):
    python docs/superpowers/survey_history_electives.py <secondary_clone_dir>

인자는 secondary 저장소를 클론한 디렉터리(그 아래 data/kr/*.json이 있는 경로) 하나뿐이다.
표준 라이브러리만 사용 — 외부 패키지 설치나 npm 스크립트 실행이 전혀 없다.

주의: 이 스크립트가 읽는 것은 저장소에 커밋된 데이터 파일이지, 실행 중인 MCP 서버의
실제 tools/call 응답이 아니다 (v1과 동일한 전제 — social-map-survey.md 서두 참조).
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ---------------------------------------------------------------------------
# 조사 대상 과목명 (실측 확인용 후보 목록 — 과목명·존재 여부·코드·건수는 아래에서
# 데이터로 검증된다. 단, ELECTIVE_INCLUDE_GENERAL/GEO의 "일반사회/지리 계열" 이분법
# 자체는 데이터 필드가 아니라 이 스크립트 작성자가 과목명으로 붙인 편집 구분이다 —
# [3z] 섹션이 이 이분법에 대응하는 데이터 신호가 없음을 직접 확인한다)
# ---------------------------------------------------------------------------

HISTORY_TRACK = ["역사", "한국사1", "한국사2"]

ELECTIVE_INCLUDE_GENERAL = ["경제", "국제 관계의 이해", "금융과 경제생활", "법과 사회",
                            "사회문제 탐구", "사회와 문화", "정치"]
ELECTIVE_INCLUDE_GEO = ["기후변화와 지속가능한 세계", "도시의 미래 탐구", "세계시민과 지리",
                        "여행지리", "한국지리 탐구"]
ELECTIVE_INCLUDE = ELECTIVE_INCLUDE_GENERAL + ELECTIVE_INCLUDE_GEO

HISTORY_ELECTIVE_EXCLUDE = ["세계사", "동아시아 역사 기행", "역사로 탐구하는 현대 세계"]
MORAL_EXCLUDE = ["현대사회와 윤리", "윤리문제 탐구", "윤리와 사상", "인문학과 윤리"]

ALL_NEW_INCLUDE = HISTORY_TRACK + ELECTIVE_INCLUDE
ALL_EXCLUDE = HISTORY_ELECTIVE_EXCLUDE + MORAL_EXCLUDE


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def section(title: str):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


def code_prefix(code: str) -> str:
    """코드 문자열에서 학년 숫자 + 한글 접두(구두점 전까지)를 뽑는다."""
    m = re.match(r"(\[\d+[가-힣]+)", code)
    return m.group(1) if m else code


# ---------------------------------------------------------------------------
# 1. 중학교 역사 — 커리큘럼 엔트리 구조·코드·영역·표준 수
# ---------------------------------------------------------------------------

def survey_middle_history(by_subj, topics):
    section("[1] 중학교 '역사' — 커리큘럼 엔트리 구조")
    c = by_subj["역사"]
    meta = {k: v for k, v in c.items() if k != "standards"}
    print(json.dumps(meta, ensure_ascii=False, indent=2))

    codes = [s["code"] for s in c["standards"]]
    print(f"\n표준(성취기준) 수: {len(codes)}")
    print("코드 예시(첫 3):", codes[:3])
    bracket_tags = sum(1 for code in codes if re.search(r"\(.+?\)", code))
    print(f"괄호 태그(예: 사회의 (일사)/(지리))를 포함한 코드 수: {bracket_tags}/{len(codes)} "
          f"— 역사는 사회와 달리 코드 내부에 세계사/한국사 태그가 없다")

    domains = OrderedDict()
    for s in c["standards"]:
        domains.setdefault(s["domainKorean"], 0)
        domains[s["domainKorean"]] += 1
    print(f"\n영역(도메인) 수: {len(domains)}개")
    for name, cnt in domains.items():
        print(f"  - {name} ({cnt}건)")

    print("\n필드 목록(표준 1건 기준):", sorted(c["standards"][0].keys()))

    n_topics = sum(1 for t in topics if t.get("subjectKorean") == "역사")
    ratio = n_topics / c["standardCount"]
    print(f"\n연결 topic 수: {n_topics} (표준 대비 배수: {ratio:.2f})")
    facet_keys = Counter(t.get("facetKey") for t in topics if t.get("subjectKorean") == "역사")
    print("facetKey 분포:", dict(facet_keys))

    section("[1z] 대조 — 중학교 '사회'도 같은 3배 패턴인지 재확인 (v1 문서 본문 미기재, 직접 재집계)")
    social = by_subj.get("사회")
    if social is not None:
        n_social_topics = sum(1 for t in topics if t.get("subjectKorean") == "사회")
        print(f"사회 표준 수: {social['standardCount']} | 연결 topic 수: {n_social_topics} "
              f"(표준 대비 배수: {n_social_topics / social['standardCount']:.2f})")
        print("facetKey 분포:", dict(Counter(t.get("facetKey") for t in topics if t.get("subjectKorean") == "사회")))


# ---------------------------------------------------------------------------
# 2. 고교 한국사1·한국사2 — 동일 항목 + 공통과목 여부
# ---------------------------------------------------------------------------

def survey_korean_history_1_2(by_subj, topics):
    for subj in ("한국사1", "한국사2"):
        section(f"[2] 고교 '{subj}' — 커리큘럼 엔트리 구조")
        c = by_subj[subj]
        meta = {k: v for k, v in c.items() if k != "standards"}
        print(json.dumps(meta, ensure_ascii=False, indent=2))
        print(f"\ncourseCategory == 'common' → 공통과목 여부: "
              f"{'예 (공통과목)' if c['courseCategory'] == 'common' else '아니오'}")

        codes = [s["code"] for s in c["standards"]]
        print(f"표준 수: {len(codes)}")
        print("코드 예시(첫 3):", codes[:3])

        domains = OrderedDict()
        for s in c["standards"]:
            domains.setdefault(s["domainKorean"], 0)
            domains[s["domainKorean"]] += 1
        print(f"영역 수: {len(domains)}개")
        for name, cnt in domains.items():
            print(f"  - {name} ({cnt}건)")

        print("필드 목록:", sorted(c["standards"][0].keys()))

        n_topics = sum(1 for t in topics if t.get("subjectKorean") == subj)
        facet_keys = Counter(t.get("facetKey") for t in topics if t.get("subjectKorean") == subj)
        print(f"연결 topic 수: {n_topics} (표준 대비 배수: {n_topics / c['standardCount']:.2f}) "
              f"| facetKey 분포: {dict(facet_keys)}")


# ---------------------------------------------------------------------------
# 3. 사회과 선택과목 전수 — 포함분(일반사회·지리) + 제외분(역사선택·도덕과)
# ---------------------------------------------------------------------------

CATEGORY_KO = {
    "general-elective": "일반선택",
    "career-elective": "진로선택",
    "convergence-elective": "융합선택",
}


def survey_electives(by_subj, topics):
    section("[3a] 사회과 선택과목 — 포함분 (일반사회 계열 — 편집 구분, [3z] 참조)")
    for subj in ELECTIVE_INCLUDE_GENERAL:
        _print_elective_row(by_subj, topics, subj)

    section("[3b] 사회과 선택과목 — 포함분 (지리 계열 — 편집 구분, [3z] 참조)")
    for subj in ELECTIVE_INCLUDE_GEO:
        _print_elective_row(by_subj, topics, subj)

    section("[3c] 제외 목록 — 역사 선택 (세계사·동아시아 계열, 범위 밖 유지)")
    for subj in HISTORY_ELECTIVE_EXCLUDE:
        _print_elective_row(by_subj, topics, subj, show_group=True)

    section("[3d] 제외 목록 — 도덕과 (윤리 계열, 범위 밖 유지)")
    for subj in MORAL_EXCLUDE:
        _print_elective_row(by_subj, topics, subj, show_group=True)


def survey_elective_track_signal(by_subj, course_relations):
    """[3a]/[3b]의 일반사회/지리 이분법이 데이터로 뒷받침되는지 직접 확인한다.

    확인 대상: (1) subjectGroupKorean이 12개 선택과목 전부 동일한지, (2) 39건짜리
    course-relations.json에 이 19과목(포함 12 + 제외 7) 관련 relation이 있는지,
    (3) sourceLocator.pdfPage 순서가 courseCategory(일반/진로/융합선택) 기준인지
    아니면 일반사회/지리/역사 계열 기준인지. 셋 다 "계열 신호 없음"으로 나오면
    [3a]/[3b]의 구분은 편집 판단이지 실측이 아니라는 뜻이다.
    """
    section("[3z] 검증 — 일반사회/지리 이분법에 대응하는 데이터 신호가 있는가")

    groups = {by_subj[s]["subjectGroupKorean"] for s in ELECTIVE_INCLUDE}
    print(f"(1) 12개 선택과목의 subjectGroupKorean 종류 수: {len(groups)} -> {groups}")
    print("    (1개뿐이면 이 필드로는 일반사회/지리를 구분할 수 없다는 뜻)")

    by_course_id = {c["deck6CourseId"]: subj for subj, c in by_subj.items()}
    all19 = ELECTIVE_INCLUDE + HISTORY_ELECTIVE_EXCLUDE + MORAL_EXCLUDE
    all19_set = set(all19)
    hits = [r for r in course_relations
            if by_course_id.get(r.get("fromCourseId")) in all19_set
            or by_course_id.get(r.get("toCourseId")) in all19_set]
    print(f"(2) course-relations.json 전체 {len(course_relations)}건 중 이 19과목 관련: {len(hits)}건")

    print("(3) pdfPage 순으로 정렬한 15과목(포함 12 + 역사선택 3, 도덕 제외) — "
          "courseCategory 띠와 편집 계열 라벨을 나란히 표시:")
    non_moral = [s for s in ELECTIVE_INCLUDE + HISTORY_ELECTIVE_EXCLUDE]
    label = {}
    for s in ELECTIVE_INCLUDE_GENERAL:
        label[s] = "일반사회(편집)"
    for s in ELECTIVE_INCLUDE_GEO:
        label[s] = "지리(편집)"
    for s in HISTORY_ELECTIVE_EXCLUDE:
        label[s] = "역사(제외)"
    rows = []
    for subj in non_moral:
        c = by_subj[subj]
        page = (c["standards"][0].get("sourceLocator") or {}).get("pdfPage")
        rows.append((page, subj, c["courseCategory"], label[subj]))
    rows.sort(key=lambda r: (r[0] is None, r[0]))
    for page, subj, cat, lab in rows:
        print(f"    p.{page!s:<4} {subj:16s} | {CATEGORY_KO.get(cat, cat):6s} | {lab}")
    print("    -> 계열 라벨이 courseCategory 띠 안에서 뒤섞여 있으면(일반사회/지리/역사가")
    print("       같은 띠 안에 교차 출현) 정렬 기준은 courseCategory뿐이고 계열 신호는 없다.")


def _print_elective_row(by_subj, topics, subj, show_group=False):
    c = by_subj[subj]
    codes = [s["code"] for s in c["standards"]]
    prefix = code_prefix(codes[0])
    domains = OrderedDict((s["domainKorean"], None) for s in c["standards"])
    n_topics = sum(1 for t in topics if t.get("subjectKorean") == subj)
    cat_ko = CATEGORY_KO.get(c["courseCategory"], c["courseCategory"])
    group_part = f" | group={c['subjectGroupKorean']}" if show_group else ""
    print(f"{subj:16s} | {cat_ko:6s} | n={c['standardCount']:3d} | prefix={prefix:10s} | "
          f"example={codes[0]:16s} | 영역 {len(domains)}개 | topic {n_topics}건{group_part}")


# ---------------------------------------------------------------------------
# 4. 원문 수록 상태 (officialText 커버리지) — 신규 과목 표본 + 전수 스캔
# ---------------------------------------------------------------------------

GOOD_ENDING_RE = re.compile(r"(한다|기른다|참여한다|탐구한다|이해한다|표현한다|설명한다|익힌다|갖는다|파악한다|분석한다)\s*[.\s]*$")
BAD_START_RE = re.compile(r"^(은|는|이|가|을|를|에|의|과|와)\s")


def survey_official_text(by_subj, texts):
    section("[4] officialText 수록 상태 — 신규 과목 표본(과목당 첫 표준)")
    for subj in ALL_NEW_INCLUDE:
        c = by_subj[subj]
        std = c["standards"][0]
        t = texts.get(std["key"], "MISSING")
        status = "MISSING" if t == "MISSING" else "OK"
        print(f"{subj:14s} {std['code']:16s} [{status}] -> {t[:50] if t != 'MISSING' else ''}")
    missing = [subj for subj in ALL_NEW_INCLUDE
               if texts.get(by_subj[subj]["standards"][0]["key"], "MISSING") == "MISSING"]
    print(f"\nMISSING 건수(표본): {len(missing)} {missing if missing else '(없음)'}")

    section("[4z] officialText 전수 스캔 — 신규 15과목의 모든 표준 (v1 §3-2 방식과 동일 휴리스틱)")
    total = 0
    missing_all = []
    candidates = []
    for subj in ALL_NEW_INCLUDE:
        for s in by_subj[subj]["standards"]:
            total += 1
            t = texts.get(s["key"])
            if t is None:
                missing_all.append((subj, s["code"]))
                continue
            if BAD_START_RE.match(t) or not GOOD_ENDING_RE.search(t):
                candidates.append((subj, s["code"], t[:50]))
    print(f"전수 {total}건(15과목 표준 합계) 중 MISSING: {len(missing_all)} {missing_all if missing_all else ''}")
    print(f"휴리스틱 후보(수동 검토 필요, 결함 확정 아님) {len(candidates)}건:")
    for subj, code, snip in candidates:
        print(f"  {subj} {code}: {snip}")


# ---------------------------------------------------------------------------
# 5. 선수관계(dependencies) — 신규 과목 관련 edge 전수
# ---------------------------------------------------------------------------

def survey_dependencies(by_subj, topics, deps):
    section("[5] 선수관계(dependencies) — 신규 과목별 edge 전수")
    topic_by_id = {t["id"]: t for t in topics}
    total_edges = 0
    for subj in ALL_NEW_INCLUDE:
        ids = {t["id"] for t in topics if t.get("subjectKorean") == subj}
        sdeps = [d for d in deps if d["topicId"] in ids or d["prerequisiteId"] in ids]
        total_edges += len(sdeps)
        print(f"{subj:14s} | topic={len(ids):3d} | edge={len(sdeps)}")

    print(f"\n신규 과목 관련 edge 합계: {total_edges} (전체 dependencies {len(deps)}건 중)")

    section("[5a] edge 실례 — 존재하는 것 중 대표 사례")
    new_ids = {t["id"] for t in topics if t.get("subjectKorean") in ALL_NEW_INCLUDE}
    new_deps = [d for d in deps if d["topicId"] in new_ids or d["prerequisiteId"] in new_ids]
    for d in new_deps:
        t1 = topic_by_id.get(d["topicId"])
        t2 = topic_by_id.get(d["prerequisiteId"])
        cross = (t1 or {}).get("subjectKorean") != (t2 or {}).get("subjectKorean")
        print(f"  {(t1 or {}).get('subjectKorean')}:{(t1 or {}).get('standards')} <- "
              f"{(t2 or {}).get('subjectKorean')}:{(t2 or {}).get('standards')} "
              f"| cross-subject={cross}")
        print(f"    reason: {d.get('reason')}")
        print(f"    basis:  {d.get('basis')}")

    cross_subject = sum(
        1 for d in new_deps
        if (topic_by_id.get(d["topicId"]) or {}).get("subjectKorean")
        != (topic_by_id.get(d["prerequisiteId"]) or {}).get("subjectKorean")
    )
    print(f"\n신규 과목 관련 edge 중 cross-subject(과목 간) edge 수: {cross_subject} "
          f"({'없음 — 전부 같은 과목 내부 edge' if cross_subject == 0 else '있음, 위 목록 참조'})")


# ---------------------------------------------------------------------------
# 6. 중→고 전이(transitions) — 역사 관련 재확인 (v1 survey §5의 2건)
# ---------------------------------------------------------------------------

def survey_transitions(topics, transitions):
    section("[6] 중→고 전이(transitions) — '역사' 관련 전건 재확인")
    topic_by_id = {t["id"]: t for t in topics}
    hits = []
    for tr in transitions:
        from_subj = {topic_by_id[tid]["subjectKorean"] for tid in tr.get("fromTopicIds", []) if tid in topic_by_id}
        to_subj = {topic_by_id[tid]["subjectKorean"] for tid in tr.get("toTopicIds", []) if tid in topic_by_id}
        if "역사" in (from_subj | to_subj):
            hits.append((tr, from_subj, to_subj))
    print(f"전체 transitions: {len(transitions)} / '역사' 관련: {len(hits)}")
    for tr, fs, ts in hits:
        print(f"  {fs} -> {ts} | {tr['transitionKind']} | {tr.get('reason')}")
        print(f"    fromTopicIds: {tr.get('fromTopicIds')}")
        print(f"    toTopicIds:   {tr.get('toTopicIds')}")

    to_subjects = {s for _, _, ts in hits for s in ts}
    print(f"\n'역사'에서 나가는 전이의 도착 과목: {sorted(to_subjects)}")
    print(f"'한국사2'로 가는 전이 존재 여부: "
          f"{'있음' if '한국사2' in to_subjects else '없음 — 데이터에 없음(생성 금지 대상)'}")


# ---------------------------------------------------------------------------
# 7. 대표 full record 부록 — 중 역사 1 · 한국사1 1 · 선택과목(정치) 1
# ---------------------------------------------------------------------------

def build_representative_records(by_subj, topics, texts):
    section("[7] 대표 레코드 — get_standard 응답 형태 재현 (중 역사 / 한국사1 / 정치)")

    samples = [
        ("역사", "[9역01-01]"),
        ("한국사1", "[10한사1-01-01]"),
        ("정치", "[12정치01-01]"),
    ]
    for subj, code in samples:
        c = by_subj[subj]
        std = next(s for s in c["standards"] if s["code"] == code)
        linked = [t for t in topics if std["key"] in t.get("standards", [])]
        record = dict(std)
        record["officialText"] = texts.get(std["key"])
        record["linkedTopics"] = [{"id": t["id"], "titleKorean": t["titleKorean"]} for t in linked]
        print(f"\n--- {subj} get_standard(\"{code}\") 재현 ---")
        print(json.dumps(record, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) != 2:
        print("usage: python survey_history_electives.py <secondary_clone_dir>", file=sys.stderr)
        sys.exit(1)
    base = Path(sys.argv[1]) / "data" / "kr"

    curricula = load_json(base / "curriculum-standards.json")["curricula"]
    texts = {t["key"]: t["text"] for t in load_json(base / "standard-texts.json")["texts"]}
    topics = load_json(base / "topics.json")["topics"]
    deps = load_json(base / "dependencies.json")["dependencies"]
    transitions = load_json(base / "transitions.json")["transitions"]
    course_relations = load_json(base / "course-relations.json")["courseRelations"]

    by_subj = {c["subjectKorean"]: c for c in curricula}

    missing = [s for s in ALL_NEW_INCLUDE + ALL_EXCLUDE if s not in by_subj]
    if missing:
        print(f"경고: 커리큘럼에서 찾지 못한 과목명: {missing}", file=sys.stderr)

    survey_middle_history(by_subj, topics)
    survey_korean_history_1_2(by_subj, topics)
    survey_electives(by_subj, topics)
    survey_elective_track_signal(by_subj, course_relations)
    survey_official_text(by_subj, texts)
    survey_dependencies(by_subj, topics, deps)
    survey_transitions(topics, transitions)
    build_representative_records(by_subj, topics, texts)


if __name__ == "__main__":
    main()
