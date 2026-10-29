#!/usr/bin/env python3
# Copyright 2026 social-teacher-skills contributors
# SPDX-License-Identifier: Apache-2.0

"""블록 문서 JSON -> Markdown(.md) / 일반 텍스트(.txt).

render_lesson_html.py와 같은 블록 문서(eyebrow / title / meta / sections / audience)를 받아
같은 텍스트를 서식 없는 형식으로 낸다. 확장(expand_document)·머리부(build_header)·
성취기준 머리말(preamble_blocks)·인라인 마크다운 해석(md_tokens)은 lesson_common을 그대로
써서 세 형식(html·md·txt)이 같은 내용을 담는다. 블록 타입을 추가하면 여기에도 추가할 것.

Usage:
    python render_text.py lesson_doc.json --format md -o lesson_plan.md
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lesson_common import (  # noqa: E402
    Theme, CALLOUT_KINDS,
    btype as _btype, resolve_callout_kind as _resolve_callout_kind,
    answer_profile, expand_document, build_header, preamble_blocks, coerce_marks,
    workspace_height, label_text, label_sep, coerce_headers, coerce_rows, md_tokens,
    FILL_IN_CHARS,
)

FORMATS = ("md", "txt")


def inline(text, fmt: str) -> str:
    """인라인 마크다운(**굵게**·*기울임*·줄바꿈)을 형식에 맞게 다시 쓴다."""
    out = []
    for part, attrs in md_tokens(text):
        if attrs.get("break"):
            out.append("  \n" if fmt == "md" else "\n")
        elif fmt == "md" and attrs.get("bold"):
            out.append(f"**{part}**")
        elif fmt == "md" and attrs.get("italic"):
            out.append(f"*{part}*")
        else:
            out.append(part)
    return "".join(out).strip()


def _cell(c, fmt: str) -> str:
    s = inline(c, fmt).replace("  \n", " ").replace("\n", " ")
    if str(c).strip().strip("_") == "" and "_" in str(c):
        s = ""  # 밑줄 연속은 "빈칸에 쓰기" — 다른 렌더러와 같은 규칙
    return s.replace("|", "\\|") if fmt == "md" else s


def _table(headers: list, rows: list, fmt: str) -> str:
    ncol = max([len(headers)] + [len(r) for r in rows] + [1])
    rows = [list(r) + [""] * (ncol - len(r)) for r in rows]
    if fmt == "md":
        head = [_cell(h, fmt) for h in headers] + [""] * (ncol - len(headers))
        lines = ["| " + " | ".join(head) + " |", "|" + "---|" * ncol]
        lines += ["| " + " | ".join(_cell(c, fmt) or " " for c in r) + " |" for r in rows]
        return "\n".join(lines)
    lines = []
    if headers:
        lines.append(" | ".join(_cell(h, fmt) for h in headers))
        lines.append("-" * 40)
    lines += [" | ".join(_cell(c, fmt) or "____" for c in r) for r in rows]
    return "\n".join(lines)


def _answer_lines(blk: dict, theme: Theme, fmt: str) -> str:
    """쓰기 공간 — 높이를 줄 수로 환산해 밑줄 줄로 낸다(md는 전각 밑줄: 가로줄 오인 방지)."""
    h = workspace_height(blk, theme)
    n = min(12, max(2, int(round(h / float(theme.answer_gap or 22.0)))))
    line = "＿" * 24 if fmt == "md" else "_" * 48
    return "\n\n".join([line] * n) if fmt == "md" else "\n".join([line] * n)


def _quote(text: str, fmt: str) -> str:
    if fmt == "md":
        return "\n".join("> " + ln if ln else ">" for ln in text.split("\n"))
    return "\n".join("    " + ln for ln in text.split("\n"))


def render_block(blk: dict, theme: Theme, fmt: str) -> str:
    t = _btype(blk)
    md = fmt == "md"
    if t == "paragraph":
        return inline(blk.get("text", ""), fmt)
    if t == "labeled":
        lbl = label_text(blk)
        head = f"{inline(lbl, fmt)}{label_sep(lbl)}"
        return f"{'**' + head + '**' if md else head} {inline(blk.get('text', ''), fmt)}"
    if t in ("h1", "h2", "h3"):
        text = inline(blk.get("text", ""), fmt)
        if md:
            return {"h1": "## ", "h2": "### ", "h3": "#### "}[t] + text
        return {"h1": "■ ", "h2": "▶ ", "h3": "· "}[t] + text
    if t == "instructions":
        return _quote(inline(blk.get("text", ""), fmt), fmt)
    if t in ("list", "checklist"):
        items = []
        for i, it in enumerate(blk.get("items", []), 1):
            mark = "- [ ] " if t == "checklist" and md else "□ " if t == "checklist" \
                else f"{i}. " if blk.get("ordered") else "- "
            items.append(mark + inline(it, fmt).replace("\n", "\n   "))
        head = ""
        if blk.get("label"):
            lbl = inline(label_text(blk), fmt)
            head = f"**{lbl}**\n\n" if md else f"{lbl}\n"
        return head + "\n".join(items)
    if t == "callout":
        text = blk.get("text") or blk.get("body") or blk.get("content") or ""
        icon, _ = CALLOUT_KINDS[_resolve_callout_kind(blk)]
        lbl = inline(label_text(blk), fmt)
        head = f"{icon} " + (f"**{lbl}**" if md and lbl else lbl)
        body = inline(text, fmt)
        return _quote(head.rstrip() + ("\n" + body if body else ""), fmt)
    if t == "cards":
        out = []
        for c in blk.get("items", []):
            c = c if isinstance(c, dict) else {"title": str(c), "text": ""}
            title = inline(c.get("title", ""), fmt)
            body = inline(c.get("text", ""), fmt)
            out.append(f"- {'**' + title + '**' if md else '[' + title + ']'}"
                       + (f" — {body}" if body else ""))
        return "\n".join(out)
    if t == "fill_in":
        n = FILL_IN_CHARS.get(str(blk.get("size", "med")).lower(), FILL_IN_CHARS["med"])
        blank = ("＿" * max(4, n // 2)) if md else "_" * n
        if blk.get("label"):
            lbl = inline(label_text(blk), fmt)
            return f"{'**' + lbl + ':**' if md else lbl + ':'} {blank}"
        return blank
    if t == "phase_header":
        mins = blk.get("minutes")
        name = inline(blk.get("name", ""), fmt) + (f" ({mins}분)" if mins is not None else "")
        return ("### " if md else "▶ ") + name
    if t == "group":
        return "\n\n".join(s for s in (render_block(b, theme, fmt)
                                       for b in blk.get("blocks", [])) if s)
    if t == "workspace":
        return _answer_lines(blk, theme, fmt)
    if t == "labeled_box":
        lbl = inline(label_text(blk), fmt)
        head = (f"**{lbl}**\n\n" if md else f"{lbl}\n") if lbl else ""
        return head + _answer_lines(blk, theme, fmt)
    if t == "page_break":
        return "---" if md else "-" * 48
    if t == "table":
        return _table(coerce_headers(blk.get("headers")), coerce_rows(blk.get("rows")), fmt)
    if t == "columns":
        return "\n\n".join(s for s in (render_block(b, theme, fmt)
                                       for b in list(blk.get("left", []))
                                       + list(blk.get("right", []))) if s)
    if t == "source_card":
        bits = " · ".join(inline(str(blk.get(k)), fmt) for k in ("author", "date", "origin")
                          if blk.get(k))
        title = inline(blk.get("title", ""), fmt)
        head = (f"**{title}**" if md else f"[{title}]") + (f" · {bits}" if bits else "")
        excerpt = inline(blk.get("excerpt") or blk.get("text") or "", fmt)
        return _quote(head + ("\n" + excerpt if excerpt else ""), fmt)
    if t == "fill_table":
        headers = coerce_headers(blk.get("headers"))
        rows_val = blk.get("rows")
        if isinstance(rows_val, list):
            rows = coerce_rows(rows_val[:50])
        else:
            try:
                n = int(blk.get("blank_rows") or rows_val or 3)
            except (TypeError, ValueError):
                n = 3
            rows = [[] for _ in range(min(max(1, n), 50))]
        if not headers:
            try:
                ncol = min(max(1, int(blk.get("cols") or 2)), 12)
            except (TypeError, ValueError):
                ncol = 2
            rows = [list(r) + [""] * (ncol - len(r)) for r in rows]
        return _table(headers, rows, fmt)
    if t == "number_line":
        lo, hi = blk.get("min", 0), blk.get("max", 10)
        marks = coerce_marks(blk.get("marks"))
        pts = ", ".join(f"{v:g}" + (f"({inline(lab, fmt)})" if lab else "") for v, lab in marks)
        line = f"{'**수직선**' if md else '[수직선]'} {lo} ~ {hi}"
        return line + (f" — 표시: {pts}" if pts else "")
    # 알 수 없는 타입 — 원시 JSON은 절대 내보내지 않는다(HTML 렌더러와 같은 규칙).
    if blk.get("text"):
        return inline(blk.get("text"), fmt)
    if blk.get("items"):
        return "\n".join("- " + inline(i, fmt) for i in blk.get("items", []))
    return ""


def render(data: dict, fmt: str) -> str:
    if fmt not in FORMATS:
        raise ValueError(f"unknown text format: {fmt}")
    md = fmt == "md"
    data = expand_document(data, data.get("audience", "teacher"))
    theme = Theme(data.get("theme"))
    (theme.answer_height, theme.answer_gap,
     theme.answer_row, theme.ruled_default) = answer_profile(data)
    theme.student_doc = data.get("audience") == "student"
    hdr = build_header(data)
    out = []
    if hdr["eyebrow"]:
        out.append(inline(hdr["eyebrow"], fmt))
    title = inline(hdr["title"], fmt)
    out.append(f"# {title}" if md else f"{title}\n{'=' * 40}")
    if hdr["meta"]:
        out.append(inline(hdr["meta"], fmt))
    if hdr["name_line"]:
        out.append(inline(hdr["name_line"], fmt))
    for blk in preamble_blocks(data):
        out.append(render_block(blk, theme, fmt))
    for section in data.get("sections", []):
        heading = inline(str(section.get("heading", "")).rstrip(": "), fmt)
        if heading:
            out.append(f"## {heading}" if md else f"\n■ {heading}\n{'-' * 40}")
        for blk in section.get("blocks", []):
            out.append(render_block(blk, theme, fmt))
    if data.get("footer_note"):
        out.append(("---\n\n" if md else "-" * 40 + "\n") + inline(data["footer_note"], fmt))
    return "\n\n".join(s for s in out if s) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("input", help="block-document JSON file")
    ap.add_argument("--format", choices=FORMATS, default="md")
    ap.add_argument("-o", "--output", default=None)
    args = ap.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    out = args.output or f"lesson_preview.{args.format}"
    Path(out).write_text(render(data, args.format), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
