#!/usr/bin/env bash
# Copyright 2026 Anthropic, PBC
# Copyright 2026 Learning Commons
# SPDX-License-Identifier: Apache-2.0

# Render all four artifacts (teacher plan + three tier worksheets) from one
# differentiation.json in a single invocation. Writes .html, .txt and .md by default; an
# editable .hwpx (opens in 한글) is written only when FORMATS includes hwpx, and is saved by
# the 한글 installed on this computer when available (Python-rendered fallback otherwise).
# Standard library only — no third-party packages, nothing to install.
# Fail-fast: any renderer error stops the run.
#
# Usage: bash scripts/render_all.sh differentiation.json "$OUTPUT_DIR" [html,txt,md,hwpx]
set -euo pipefail

json="${1:?usage: render_all.sh DIFFERENTIATION_JSON OUTPUT_DIR [FORMATS]}"
outdir="${2:?usage: render_all.sh DIFFERENTIATION_JSON OUTPUT_DIR [FORMATS]}"
# 출력 형식: 쉼표 목록. 기본은 html·txt·md, hwpx는 요청할 때만 (예: html,txt,md,hwpx).
formats="${3:-html,txt,md}"
here="$(cd "$(dirname "$0")" && pwd)"

text_formats=""
want_hwpx=0
IFS=',' read -r -a requested <<< "$formats"
for f in "${requested[@]}"; do
  f="$(echo "$f" | tr -d '[:space:]')"
  case "$f" in
    html|txt|md) text_formats="${text_formats:+$text_formats,}$f" ;;
    hwpx) want_hwpx=1 ;;
    "") ;;
    *) echo "error: unknown format '$f' — use html, txt, md, hwpx" >&2; exit 2 ;;
  esac
done
if [ -z "$text_formats" ] && [ "$want_hwpx" -eq 0 ]; then
  echo "error: no output format requested" >&2; exit 2
fi

mkdir -p "$outdir"
if [ -n "$text_formats" ]; then
  python3 "$here/render_documents.py" "$json" --outdir "$outdir" --formats "$text_formats"
fi
if [ "$want_hwpx" -eq 1 ]; then
  python3 "$here/render_lesson_hwpx.py" "$json" --outdir "$outdir"
  # 최소 품질 게이트: 구조·인코딩·영어 크롬·마크다운 리터럴. 실패하면 여기서 멈춘다 —
  # 게이트에 걸린 산출물은 교사에게 전달하지 않는다. (전체 검사는 저장소의
  # tests/check_hwpx_quality.py — hwpx-quality-loop 참고.)
  python3 "$here/check_hwpx_min.py" "$outdir"
  # 출력 엔진: 설치된 한글이 기본(HWPX_ENGINE=auto) — 한글로 열어 다시 저장한다.
  # 한글이 없거나 실패하면 위에서 게이트를 통과한 Python 산출물을 그대로 쓴다.
  python3 "$here/hancom_engine.py" "$outdir" --engine "${HWPX_ENGINE:-auto}"
fi

# Persist the source JSON alongside the rendered artifacts so later revision
# turns can re-render from it (same guarantee the lesson-planning renderer
# makes with lesson.json).
cp "$json" "$outdir/differentiation.json" 2>/dev/null || true

# Delivery guarantee: when $OUTPUT_DIR is set and the render went elsewhere
# (a staging dir like /tmp/out), mirror EVERYTHING into $OUTPUT_DIR too.
# Revision turns re-render from the differentiation.json that lands there;
# hand-copying a subset there is the failure this removes.
if [ -n "${OUTPUT_DIR:-}" ] && [ "$(cd "$outdir" && pwd)" != "$(mkdir -p "$OUTPUT_DIR" && cd "$OUTPUT_DIR" && pwd)" ]; then
  cp -R "$outdir"/. "$OUTPUT_DIR"/
fi
