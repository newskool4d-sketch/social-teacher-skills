#!/usr/bin/env bash
# Copyright 2026 Anthropic, PBC
# Copyright 2026 Learning Commons
# SPDX-License-Identifier: Apache-2.0

# Render every document in lesson.json (lesson plan, student materials, observation, and any
# others the model authored) from one material-source JSON. It holds a `documents[]` array;
# each entry's `id` becomes the output filename. Writes .html, .txt and .md by default; an
# editable .hwpx (opens in 한글) is written only when FORMATS includes hwpx, and is saved by
# the 한글 installed on this computer when available (Python-rendered fallback otherwise).
# Standard library only — no third-party packages, nothing to install.
# Fail-fast: any renderer error stops the run.
#
# Usage: bash scripts/render_all.sh lesson.json "$OUTPUT_DIR" [html,txt,md,hwpx]
set -euo pipefail

json="${1:?usage: render_all.sh LESSON_JSON OUTPUT_DIR [FORMATS]}"
outdir="${2:?usage: render_all.sh LESSON_JSON OUTPUT_DIR [FORMATS]}"
# 출력 형식: 쉼표 목록. 기본은 html·txt·md, hwpx는 요청할 때만 (예: html,txt,md,hwpx).
formats="${3:-html,txt,md}"
here="$(cd "$(dirname "$0")" && pwd)"

text_formats=""
want_hwpx=0
parsed=""
IFS=',' read -r -a requested <<< "$formats"
for f in "${requested[@]}"; do
  f="$(echo "$f" | tr -d '[:space:]')"
  case "$f" in
    html|txt|md) text_formats="${text_formats:+$text_formats,}$f"; parsed="$parsed,$f" ;;
    hwpx) want_hwpx=1; parsed="$parsed,hwpx" ;;
    "") ;;
    *) echo "error: unknown format '$f' — use html, txt, md, hwpx" >&2; exit 2 ;;
  esac
done
if [ -z "$text_formats" ] && [ "$want_hwpx" -eq 0 ]; then
  echo "error: no output format requested" >&2; exit 2
fi

mkdir -p "$outdir"
# 문서별 출력 파일명(정제된 id) — 게이트·한글 엔진은 이번 실행에서 쓴 파일만 다룬다.
# documents[]가 없는 단일 문서 JSON이면 비어 있다 — 그때는 outdir 전체를 다룬다(예전 동작).
stems="$( (python3 "$here/render_documents.py" "$json" --list-ids 2>/dev/null || true) | tr -d '\r')"
if [ -n "$text_formats" ]; then
  python3 "$here/render_documents.py" "$json" --outdir "$outdir" --formats "$text_formats"
fi
if [ "$want_hwpx" -eq 1 ]; then
  python3 "$here/render_lesson_hwpx.py" "$json" --outdir "$outdir"
  # 최소 품질 게이트: 구조·인코딩·영어 크롬·마크다운 리터럴. 실패하면 여기서 멈춘다 —
  # 게이트에 걸린 산출물은 교사에게 전달하지 않는다. (전체 검사는 저장소의
  # tests/check_hwpx_quality.py — hwpx-quality-loop 참고.)
  # shellcheck disable=SC2086  # stems는 [A-Za-z0-9_-]만 — 단어 분리가 안전하다
  python3 "$here/check_hwpx_min.py" "$outdir" $stems
  # 출력 엔진: 설치된 한글이 기본(HWPX_ENGINE=auto) — 한글로 열어 다시 저장한다.
  # 한글이 없거나 실패하면 위에서 게이트를 통과한 Python 산출물을 그대로 쓴다.
  # shellcheck disable=SC2086
  python3 "$here/hancom_engine.py" "$outdir" $stems --engine "${HWPX_ENGINE:-auto}"
fi

# 이전 실행의 잔여물(문서를 빼거나 이름을 바꾼 뒤, 또는 이번에 요청하지 않은 형식)은
# 지우지 않고 알린다 — 이번 산출물로 착각해 교사에게 제시하는 일을 막는다.
for f in "$outdir"/*.html "$outdir"/*.txt "$outdir"/*.md "$outdir"/*.hwpx; do
  [ -n "$stems" ] && [ -e "$f" ] || continue
  name="$(basename "$f")"
  ext="${name##*.}"
  stem="${name%.*}"
  case "$parsed," in *",$ext,"*) ;; *) stem="" ;; esac
  case " $(echo $stems) " in
    *" $stem "*) ;;
    *) echo "warning: 이번 실행에서 만들지 않은 이전 파일: $name — 교사에게 제시하지 말 것" >&2 ;;
  esac
done

# Persist the source JSON alongside the rendered artifacts so later revision
# turns can re-render from it.
cp "$json" "$outdir/lesson.json" 2>/dev/null || true

# Delivery guarantee: when $OUTPUT_DIR is set and the render went elsewhere
# (a staging dir like /tmp/out), mirror EVERYTHING into $OUTPUT_DIR too.
# Revision turns re-render from the lesson.json that lands there;
# hand-copying a subset there is the failure this removes.
if [ -n "${OUTPUT_DIR:-}" ] && [ "$(cd "$outdir" && pwd)" != "$(mkdir -p "$OUTPUT_DIR" && cd "$OUTPUT_DIR" && pwd)" ]; then
  cp -R "$outdir"/. "$OUTPUT_DIR"/
fi
