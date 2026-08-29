# SPDX-FileCopyrightText: 2026 social-teacher-skills contributors
# SPDX-License-Identifier: Apache-2.0
"""사회과 학습맵 실측 조사 스크립트 (Task 1, Ruling 1).

korean-secondary-learning-map-mcp / korean-elementary-learning-map-mcp 두 저장소를
`git clone --depth 1`로 받은 뒤, 그 안의 `data/kr/*.json`을 직접 읽어 사회과 관련
사실을 뽑아낸다. npx/node 실행은 전혀 하지 않는다 (실행 회피는 controller ruling).

사용법 (저장소 루트에서):
    python docs/superpowers/survey_social_map.py <secondary_clone_dir> <elementary_clone_dir>

두 인자 모두 각 저장소를 클론한 디렉터리(그 아래 data/kr/*.json이 있는 경로)를 받는다.
표준 라이브러리만 사용 — 외부 패키지 설치나 npm 스크립트 실행이 전혀 없다.

주의: 이 스크립트가 읽는 것은 두 저장소에 커밋된 데이터 파일이지, 실행 중인 MCP
서버의 실제 tools/call 응답이 아니다. get_standard 등의 도구가 반환하는 필드는
각 저장소의 src/server.mjs를 읽어 확인했다(문자열 검색만, 실행 없음) — 그 대응 관계는
survey 문서에 소스 인용과 함께 기록했다. MCP를 처음 실제로 호출하는 시점(파일럿 단계)에
필드명이 이 조사와 다르면 그쪽이 우선한다.
"""
import hashlib
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")


def load_json(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def section(title: str):
    print()
    print("=" * 78)
    print(title)
    print("=" * 78)


# ---------------------------------------------------------------------------
# 0. manifest 무결성 점검 (실행 없이 파일만 해시)
# ---------------------------------------------------------------------------

def check_manifest(data_dir: Path, label: str):
    section(f"[0] manifest 무결성 점검 — {label}")
    manifest = load_json(data_dir / "manifest.json")
    files = manifest.get("files", {})
    mismatches = []
    missing = []
    for fname, meta in files.items():
        full = data_dir / fname
        if not full.exists():
            missing.append(fname)
            continue
        raw = full.read_bytes()
        actual_sha = hashlib.sha256(raw).hexdigest()
        if actual_sha != meta.get("sha256") or len(raw) != meta.get("bytes"):
            mismatches.append((fname, meta.get("bytes"), len(raw)))
    print(f"manifest.files 항목 수: {len(files)}")
    print(f"실제 파일 없음(missing): {len(missing)} {missing if missing else ''}")
    print(f"체크섬/바이트수 불일치: {len(mismatches)}")
    for fname, expect_b, actual_b in mismatches:
        print(f"  - {fname}: manifest bytes={expect_b} / 실제={actual_b}")
    return {"missing": missing, "mismatches": mismatches}


# ---------------------------------------------------------------------------
# 1. secondary (중·고) — curriculum-standards.json 로드 + 사회 관련 커리큘럼 추출
# ---------------------------------------------------------------------------

SECONDARY_EXCLUDED_NAMES = [
    "역사", "경제", "국제 관계의 이해", "금융과 경제생활", "기후변화와 지속가능한 세계",
    "도시의 미래 탐구", "동아시아 역사 기행", "법과 사회", "사회문제 탐구", "사회와 문화",
    "세계사", "세계시민과 지리", "여행지리", "역사로 탐구하는 현대 세계", "정치",
    "한국사1", "한국사2", "한국지리 탐구", "현대사회와 윤리",
]


def survey_secondary(base: Path):
    section("[1] secondary — 사회(역사 포함) 교과군 커리큘럼 목록")
    curricula = load_json(base / "curriculum-standards.json")["curricula"]
    texts = {t["key"]: t["text"] for t in load_json(base / "standard-texts.json")["texts"]}
    topics = load_json(base / "topics.json")["topics"]
    deps = load_json(base / "dependencies.json")["dependencies"]
    transitions = load_json(base / "transitions.json")["transitions"]

    for c in curricula:
        if "사회" in c.get("subjectGroupKorean", "") or c.get("subjectKorean") in ("사회", "통합사회1", "통합사회2"):
            print(f"{c['schoolLevel']:6s} | {c['subjectGroupKorean']:12s} | {c['subjectKorean']:14s} | "
                  f"{c['courseCategory']:20s} | {c['gradeBand']:6s} | n={c['standardCount']}")

    section("[1a] 중학교 '사회' 과목 — 영역·코드 접두 breakdown")
    for c in curricula:
        if c["schoolLevel"] == "middle" and c["subjectKorean"] == "사회":
            tag_domains = OrderedDict()
            tag_counts = Counter()
            for s in c["standards"]:
                m = re.match(r"\[9사\((일사|지리)\)", s["code"])
                tag = m.group(1)
                tag_counts[tag] += 1
                tag_domains.setdefault(tag, [])
                if s["domainKorean"] not in tag_domains[tag]:
                    tag_domains[tag].append(s["domainKorean"])
            print("표준 수:", c["standardCount"], "| tag counts:", dict(tag_counts))
            for tag, doms in tag_domains.items():
                print(f"  {tag} 영역({len(doms)}개):", doms)
            print("  일사 예시:", [s["code"] for s in c["standards"] if "(일사)" in s["code"]][:3])
            print("  지리 예시:", [s["code"] for s in c["standards"] if "(지리)" in s["code"]][:3])

    section("[1b] 통합사회1·2 — 영역·코드·표준 수")
    for c in curricula:
        if c["subjectKorean"] in ("통합사회1", "통합사회2"):
            domains = list(OrderedDict((s["domainKorean"], None) for s in c["standards"]).keys())
            print(f"{c['subjectKorean']} | gradeBand={c['gradeBand']} | n={c['standardCount']}")
            print("  영역:", domains)
            print("  예시 코드:", [s["code"] for s in c["standards"][:3]])

    section("[1c] 제외 대상 과목 — 코드 접두 (고교 선택과목·역사)")
    for c in curricula:
        if c["subjectKorean"] in SECONDARY_EXCLUDED_NAMES:
            code0 = c["standards"][0]["code"]
            m = re.match(r"\[\d+[가-힣0-9]+", code0)
            print(f"{c['subjectKorean']:16s} | schoolLevel={c['schoolLevel']:6s} | n={c['standardCount']:3d} | "
                  f"prefix~{m.group(0) if m else code0} | example={code0}")

    section("[1d] 성취기준 원문(officialText) 검증 — secondary는 항상 존재")
    sample_keys = []
    for c in curricula:
        if c["subjectKorean"] in ("사회", "통합사회1", "통합사회2"):
            for s in c["standards"][:2]:
                sample_keys.append(s["key"])
    for k in sample_keys:
        print(k, "->", texts.get(k, "MISSING")[:60])

    section("[1e] 필드 존재 여부 (사회 표준 레코드 1건)")
    for c in curricula:
        if c["schoolLevel"] == "middle" and c["subjectKorean"] == "사회":
            print("fields:", sorted(c["standards"][0].keys()))
            break

    section("[1f] 선수관계(dependencies) — 사회/통합사회 관련 edge")
    topic_by_id = {t["id"]: t for t in topics}
    social_topic_ids = {t["id"] for t in topics if t.get("subjectKorean") in ("사회", "통합사회1", "통합사회2")}
    social_deps = [d for d in deps if d["topicId"] in social_topic_ids or d["prerequisiteId"] in social_topic_ids]
    print(f"전체 dependencies: {len(deps)} / 사회·통합사회 관련 topic 수: {len(social_topic_ids)} / "
          f"관련 edge 수: {len(social_deps)}")
    for d in social_deps:
        t1 = topic_by_id.get(d["topicId"])
        t2 = topic_by_id.get(d["prerequisiteId"])
        print("  edge:", d["topicId"], "<-", d["prerequisiteId"])
        print("    topic std:", t1.get("standards") if t1 else None)
        print("    prereq std:", t2.get("standards") if t2 else None)
        print("    reason:", d["reason"], "| basis:", d["basis"])

    # empty-edges 예시: 사회 topic 중 dependencies의 topicId로 한 번도 등장하지 않는 것
    as_topic_id = {d["topicId"] for d in deps}
    empty_examples = [tid for tid in sorted(social_topic_ids) if tid not in as_topic_id]
    print(f"\n'edges: []'가 되는 사회 topic 수(직접 선수 없음): {len(empty_examples)}")
    if empty_examples:
        t = topic_by_id[empty_examples[0]]
        print("  예시 topicId:", empty_examples[0], "| standards:", t.get("standards"))

    section("[1g] 중→고 전이(transitions) — 사회/통합사회/역사 관련")
    social_related_kinds = {"사회", "통합사회1", "통합사회2", "역사"}
    hits = []
    for tr in transitions:
        from_subj = {topic_by_id[tid]["subjectKorean"] for tid in tr.get("fromTopicIds", []) if tid in topic_by_id}
        to_subj = {topic_by_id[tid]["subjectKorean"] for tid in tr.get("toTopicIds", []) if tid in topic_by_id}
        if (from_subj | to_subj) & social_related_kinds:
            hits.append((tr, from_subj, to_subj))
    print(f"전체 transitions: {len(transitions)} / 사회 계열 관련: {len(hits)}")
    strict_social_hits = [h for h in hits if (h[1] | h[2]) & {"사회", "통합사회1", "통합사회2"}]
    print(f"그중 순수 사회/통합사회(역사 제외) 관련: {len(strict_social_hits)}")
    for tr, fs, ts in hits:
        print(" ", fs, "->", ts, "|", tr["transitionKind"], "|", tr["reason"][:50])

    return {
        "curricula": curricula,
        "texts": texts,
        "topics": topics,
        "deps": deps,
        "topic_by_id": topic_by_id,
    }


# ---------------------------------------------------------------------------
# 2. elementary (초) — 사회 표준 22(3-4)+27(5-6)=49건, verbatim 여부 실측
# ---------------------------------------------------------------------------

def survey_elementary(base: Path):
    section("[2] elementary — 사회 커리큘럼 개요")
    doc = load_json(base / "curriculum-standards.json")
    print("top-level textPolicy:", json.dumps(doc.get("textPolicy"), ensure_ascii=False))
    print("top-level sourceBasis:", doc.get("sourceBasis"))
    curricula = doc["curricula"]
    social = next(c for c in curricula if c["subjectKorean"] == "사회")
    print(json.dumps({k: v for k, v in social.items() if k != "standards"}, ensure_ascii=False, indent=2))

    texts_doc = load_json(base / "standard-texts.json")
    texts_by_code = {t["code"]: t["text"] for t in texts_doc["texts"]}
    print("\nstandard-texts.json version:", texts_doc["version"], "| generatedAt:", texts_doc["generatedAt"])
    print("sourceNote:", texts_doc["sourceNote"])

    section("[2a] 3-4 / 5-6 학년군 개수 + 예시 코드")
    by_gb = OrderedDict([("3-4", []), ("5-6", [])])
    for s in social["standards"]:
        by_gb[s["gradeBand"]].append(s["code"])
    for gb, codes in by_gb.items():
        print(f"{gb}: {len(codes)}건 — 예시:", codes[:3])
        for code in codes[:3]:
            print("   ", code, "->", texts_by_code.get(code, "N/A")[:60])

    section("[2b] 영역(도메인) 전체 목록")
    domains = list(OrderedDict((s["domainKorean"], None) for s in social["standards"]).keys())
    print(f"{len(domains)}개:", domains)

    section("[2c] 필드 존재 여부 — 사회 표준 레코드 1건 전체")
    sample = social["standards"][0]
    print(json.dumps(sample, ensure_ascii=False, indent=2))

    section("[2d] standard-texts.json 품질 휴리스틱 스캔 (수동 검토 후보 — 최종 판정 아님)")
    social_codes = [s["code"] for s in social["standards"]]
    good_endings = re.compile(r"(한다|기른다|참여한다|탐구한다|이해한다|표현한다|설명한다|익힌다|갖는다)\s*[\.\s]*$")
    bad_start = re.compile(r"^(은|는|이|가|을|를|에|의|과|와)\s")
    candidates = []
    for code in social_codes:
        t = texts_by_code.get(code)
        if t is None:
            candidates.append((code, "MISSING"))
            continue
        if bad_start.match(t) or not good_endings.search(t):
            candidates.append((code, t[:50]))
    print(f"전체 {len(social_codes)}건 중 휴리스틱 후보 {len(candidates)}건 (수동 검토 필요, 아래는 원문 앞부분만):")
    for code, snip in candidates:
        print(f"  {code}: {snip}")

    section("[2e] 필드명 실측 — search_standards 요약 필드(focus vs summary), 사회 한정")
    has_focus = sum(1 for s in social["standards"] if "focus" in s)
    has_module = sum(1 for s in social["standards"] if "module" in s)
    has_summary = sum(1 for s in social["standards"] if "summary" in s)
    print(f"사회(49건) 중 focus 보유: {has_focus} / module 보유: {has_module} / summary 보유: {has_summary}")
    print("=> src/search.mjs의 compactStandard()는 focus/module을 노출하고 summary는 노출하지 않음")
    print("   (elementary/src/search.mjs:50, elementary/src/search.mjs:103 참조)")
    print("   사회는 focus가 전무하므로 search_standards 결과에 요약 텍스트가 전혀 없다 (JSON.stringify가 undefined 키 제거)")

    section("[2f] 선수관계(dependencies) — 사회 topic 관련 edge")
    topics = load_json(base / "topics.json")["topics"]
    deps = load_json(base / "dependencies.json")["dependencies"]
    social_topic_ids = {t["id"] for t in topics if t.get("subjectKorean") == "사회"}
    social_deps = [d for d in deps if d["topicId"] in social_topic_ids or d["prerequisiteId"] in social_topic_ids]
    cross_code = 0
    code_re = re.compile(r"\.(\d[a-z]{2}\d{4})\.")
    for d in social_deps:
        m1, m2 = code_re.search(d["topicId"]), code_re.search(d["prerequisiteId"])
        if m1 and m2 and m1.group(1) != m2.group(1):
            cross_code += 1
    print(f"전체 dependencies: {len(deps)} / 사회 topic 수: {len(social_topic_ids)} / 사회 관련 edge: {len(social_deps)} "
          f"/ 그중 코드 간(cross-standard) edge: {cross_code}")
    print("예시 edge:", json.dumps(social_deps[0], ensure_ascii=False))

    as_topic_id = {d["topicId"] for d in deps}
    empty_examples = sorted(tid for tid in social_topic_ids if tid not in as_topic_id)
    print(f"'edges: []' 사회 topic 수: {len(empty_examples)} — 예시: {empty_examples[0] if empty_examples else None}")

    return {"curricula": curricula, "texts_by_code": texts_by_code, "topics": topics}


# ---------------------------------------------------------------------------
# 3. 대표 레코드 appendix (get_standard/ get_topic 응답 모양 재현)
# ---------------------------------------------------------------------------

def build_representative_records(sec, elem):
    section("[3] 대표 레코드 — get_standard 응답 형태 재현 (초/중/통사)")

    # 초등: [4사01-02] — 텍스트가 정상적으로 추출된 사례를 고른다
    elem_curricula = elem["curricula"]
    social_elem = next(c for c in elem_curricula if c["subjectKorean"] == "사회")
    std = next(s for s in social_elem["standards"] if s["code"] == "[6사01-01]")
    linked = [t for t in elem["topics"] if std["key"] in t.get("standards", [])]
    record = dict(std)
    record["officialText"] = elem["texts_by_code"].get(std["code"])
    record["linkedTopics"] = [{"id": t["id"], "titleKorean": t["titleKorean"]} for t in linked]
    print("--- 초등 get_standard([6사01-01]) 재현 ---")
    print(json.dumps(record, ensure_ascii=False, indent=2))

    # 중학교: [9사(일사)01-01]
    sec_curricula = sec["curricula"]
    mid_social = next(c for c in sec_curricula if c["schoolLevel"] == "middle" and c["subjectKorean"] == "사회")
    std2 = next(s for s in mid_social["standards"] if s["code"] == "[9사(일사)01-01]")
    linked2_ids = [t["id"] for t in sec["topics"] if std2["key"] in t.get("standards", [])]
    record2 = dict(std2)
    record2["officialText"] = sec["texts"].get(std2["key"])
    record2["linkedTopics"] = [{"id": t["id"], "titleKorean": sec["topic_by_id"][t["id"]]["titleKorean"]}
                                for t in [{"id": i} for i in linked2_ids]]
    print("\n--- 중학교 get_standard([9사(일사)01-01]) 재현 ---")
    print(json.dumps(record2, ensure_ascii=False, indent=2))

    # 통합사회1: [10통사1-01-01]
    ts1 = next(c for c in sec_curricula if c["subjectKorean"] == "통합사회1")
    std3 = next(s for s in ts1["standards"] if s["code"] == "[10통사1-01-01]")
    record3 = dict(std3)
    record3["officialText"] = sec["texts"].get(std3["key"])
    print("\n--- 통합사회1 get_standard([10통사1-01-01]) 재현 ---")
    print(json.dumps(record3, ensure_ascii=False, indent=2))

    # topic 레코드 예시 (evidence/assessmentPrompts) — 중학교 사회, edges:[] 사례와 동일 topic
    topic_example = next(t for t in sec["topics"] if std2["key"] in t.get("standards", []))
    print("\n--- 중학교 사회 topic 레코드 예시 (evidence/assessmentPrompts) ---")
    print(json.dumps(topic_example, ensure_ascii=False, indent=2))


def main():
    if len(sys.argv) != 3:
        print("usage: python survey_social_map.py <secondary_clone_dir> <elementary_clone_dir>", file=sys.stderr)
        sys.exit(1)
    secondary_dir = Path(sys.argv[1]) / "data" / "kr"
    elementary_dir = Path(sys.argv[2]) / "data" / "kr"

    check_manifest(secondary_dir, "secondary")
    check_manifest(elementary_dir, "elementary")

    sec = survey_secondary(secondary_dir)
    elem = survey_elementary(elementary_dir)
    build_representative_records(sec, elem)


if __name__ == "__main__":
    main()
