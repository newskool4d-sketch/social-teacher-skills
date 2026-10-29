#!/usr/bin/env python3
# Copyright 2026 Anthropic, PBC
# Copyright 2026 Learning Commons
# SPDX-License-Identifier: Apache-2.0

"""Render every document in a multi-document source JSON to HTML (and/or md, txt).

Used by skills whose output is a set of documents that must stay consistent with each other
(e.g. the differentiation skills: 1 teacher plan + 3 tiered worksheets). The source JSON holds
ONE `shared` block (content that appears in more than one document) plus a `documents` array.
Each document is a full block-document — same schema as render_lesson_html.py /
render_lesson_hwpx.py (eyebrow / title / meta / sections / theme / audience) — and pulls shared
content with {"type": "from_shared", "key": ...} blocks, so shared content is written once and
cannot drift between documents. The HWPX twin of each document is rendered separately by
render_lesson_hwpx.py (which reuses build_doc below).

Material source shape:
  {
    "shared": {"standard_code": ..., "standard_text": ...,
               <any model-chosen keys: a block, a list of blocks, or a faceted
                {teacher, student, stimulus} value>, ...},
    "theme": {...},                              // default theme for every document
    "documents": [
      {"id": "teacher_plan",      "audience": "teacher", "title": ..., "sections": [...]},
      {"id": "worksheet_group_a", "audience": "student", "title": ..., "sections": [...]},
      {"id": "worksheet_group_b", "audience": "student", "title": ..., "sections": [...]},
      {"id": "worksheet_group_c", "audience": "student", "title": ..., "sections": [...]}
    ]
  }

`id` becomes the output filename; a document's own `theme` overrides the top-level one.

Usage:
    python render_documents.py differentiation.json                           # all docs -> HTML
    python render_documents.py differentiation.json --only worksheet_group_a worksheet_group_b
    python render_documents.py lesson.json --formats html,md,txt               # + md, txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))


AUDIENCES = ("teacher", "student")


def doc_audience(doc: dict) -> str:
    """Document audience. A missing value is inferred from the id (worksheet_*/student_* →
    student) — defaulting a worksheet to "teacher" would print teacher script on the
    student page. Any other value is a typo and stops the render."""
    aud = doc.get("audience")
    if aud is None:
        doc_id = str(doc.get("id") or "")
        student = ("worksheet", "student", "source_packet")
        return "student" if doc_id.startswith(student) else "teacher"
    if aud not in AUDIENCES:
        raise ValueError(f"document {doc.get('id')!r}: audience는 teacher 또는 student "
                         f"(받은 값: {aud!r})")
    return aud


def _task_keys(blocks) -> set[str]:
    """from_shared로 끌어 쓴 과제 키(t1, t2, …) — group·columns 안까지."""
    keys: set[str] = set()
    for b in blocks or []:
        if not isinstance(b, dict):
            continue
        if b.get("type") == "from_shared" and re.fullmatch(r"t\d+", str(b.get("key", ""))):
            keys.add(str(b["key"]))
        for k in ("blocks", "left", "right"):
            keys |= _task_keys(b.get(k))
    return keys


def check_tier_tasks(docs: list[dict]) -> None:
    """수준별 학습지(worksheet_group_*)와 teacher_plan이 같은 과제 키 집합을 참조하는지.
    한 학습지가 과제를 빠뜨리거나 문서 고유 블록으로 다시 타이핑하면 세 수준이 어긋난다."""
    tiers = {str(d.get("id")): set().union(*[_task_keys(s.get("blocks"))
                                             for s in d.get("sections", [])] or [set()])
             for d in docs if str(d.get("id", "")).startswith(("worksheet_group", "teacher_plan"))}
    sheets = {k: v for k, v in tiers.items() if k.startswith("worksheet_group")}
    if len(sheets) < 2:
        return
    ref = set().union(*sheets.values())
    bad = {k: sorted(ref - v) for k, v in tiers.items() if ref - v}
    if bad:
        detail = "; ".join(f"{k}에 없음: {', '.join(v)}" for k, v in sorted(bad.items()))
        raise ValueError(f"수준별 문서의 공유 과제가 어긋남 — {detail} "
                         "(모든 학습지와 teacher_plan이 같은 tN을 from_shared로 참조해야 함)")


def doc_filenames(docs: list[dict]) -> list[str]:
    """Output file stem per document. The id comes from generated JSON, so strip path
    separators and anything outside [A-Za-z0-9_-]; a missing id becomes document_N.
    Every renderer uses this, so twins share a name; duplicate stems stop the render
    (the second document would silently overwrite the first)."""
    stems = []
    for i, doc in enumerate(docs):
        raw = str(doc.get("id") or f"document_{i + 1}")
        stem = re.sub(r"[^A-Za-z0-9_\-]", "_", Path(raw).name) or f"document_{i + 1}"
        if stem in stems:
            raise ValueError(f"문서 파일명 중복: {stem!r} — documents[]의 id를 서로 다르게, "
                             "영문·숫자·밑줄로 쓸 것")
        stems.append(stem)
    return stems


def build_doc(source: dict, doc: dict) -> dict:
    """Merge a document entry with the source's shared block and default theme."""
    out = dict(doc)
    out["audience"] = doc_audience(doc)
    out.setdefault("shared", source.get("shared", {}))
    theme = dict(source.get("theme") or {})
    theme.update(doc.get("theme") or {})
    if theme:
        out["theme"] = theme
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="source JSON with a `documents` array")
    ap.add_argument("--only", nargs="*", default=None,
                    help="document ids to render (default: all)")
    ap.add_argument("--outdir", default=".")
    ap.add_argument("--formats", default="html",
                    help="comma list of html, md, txt (default: html)")
    ap.add_argument("--list-ids", action="store_true",
                    help="print each document's output file stem and exit")
    args = ap.parse_args()
    formats = [f.strip() for f in args.formats.split(",") if f.strip()]
    unknown = [f for f in formats if f not in ("html", "md", "txt")]
    if unknown or not formats:
        print(f"error: unknown format(s) {unknown} — use html, md, txt", file=sys.stderr)
        return 1

    source = json.loads(Path(args.input).read_text(encoding="utf-8"))
    docs = source.get("documents", [])
    if not docs:
        print("error: no `documents` array in input", file=sys.stderr)
        return 1
    try:
        stems = doc_filenames(docs)
        check_tier_tasks(docs)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if args.list_ids:
        print("\n".join(stems))
        return 0
    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    written = []
    for doc, doc_id in zip(docs, stems):
        if args.only and str(doc.get("id")) not in args.only and doc_id not in args.only:
            continue
        full = build_doc(source, doc)
        from render_lesson_html import render as render_html
        from render_text import render as render_text
        for fmt in formats:
            text = render_html(full) if fmt == "html" else render_text(full, fmt)
            path = outdir / f"{doc_id}.{fmt}"
            path.write_text(text, encoding="utf-8")
            written.append(str(path))

    if not written:
        print("nothing rendered — check --only ids against the documents' `id` fields",
              file=sys.stderr)
        return 1
    print("wrote " + ", ".join(written))
    return 0


if __name__ == "__main__":
    sys.exit(main())
