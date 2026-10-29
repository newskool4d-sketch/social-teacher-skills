#!/usr/bin/env python3
# Copyright 2026 social-teacher-skills contributors
# SPDX-License-Identifier: Apache-2.0

"""HWPX 출력 엔진: 사용자 컴퓨터의 한글(한컴오피스)을 기본 엔진으로 쓴다.

render_lesson_hwpx.py가 만든 HWPX를 설치된 한글로 열어 HWPX로 다시 저장한다 — 최종 파일을
한글이 직접 쓰므로 교사 컴퓨터의 한글과 완전히 같은 구조가 된다. 한글을 쓸 수 없으면
(Windows 아님·한글 미설치·자동화 실패·시간 초과) Python 산출물을 그대로 둔다(폴백).
한글이 쓴 파일도 최소 게이트(check_hwpx_min)를 통과해야 교체한다.

표준 라이브러리 전용 — 한글 COM은 pywin32 없이 Windows 기본 PowerShell로 호출한다.
한글 보안 승인 창 없이 돌리려면 한컴 '자동화 보안 모듈'(FilePathCheckerModule)을
등록해 두면 된다. 다른 이름으로 등록했으면 HANCOM_SECURITY_MODULE 환경변수로 지정한다.

  --engine auto    (기본) 한글이 있으면 한글, 없거나 실패하면 Python 산출물 유지
  --engine hancom  한글 필수 — 쓸 수 없거나 실패하면 exit 1
  --engine python  한글을 쓰지 않음

Usage: python hancom_engine.py OUTDIR [STEM ...] [--engine auto|hancom|python]
  stem을 주면 그 문서들의 hwpx만 다시 저장한다(이번 실행에서 쓴 파일).
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_hwpx_min import check  # noqa: E402

PROG_ID = "HWPFrame.HwpObject"

# 경로·옵션은 작업 파일(UTF-8 JSON)로 넘긴다 — 한글 경로를 명령줄 인용에 싣지 않기 위해.
_PS_SCRIPT = r"""
$ErrorActionPreference = 'Stop'
$job = Get-Content -LiteralPath $env:HANCOM_JOB -Raw -Encoding UTF8 | ConvertFrom-Json
$results = @()
$h = $null
try {
  $h = New-Object -ComObject HWPFrame.HwpObject
  try { [void]$h.RegisterModule('FilePathCheckDLL', $job.module) } catch {}
  try { $h.XHwpWindows.Item(0).Visible = $false } catch {}
  foreach ($j in $job.jobs) {
    $ok = $false; $msg = ''
    try {
      if ($h.Open($j.src, 'HWPX', '')) {
        $ok = [bool]$h.SaveAs($j.dst, 'HWPX', '')
        $msg = 'pages=' + $h.PageCount
      } else { $msg = 'open failed' }
      [void]$h.Clear(1)
    } catch { $msg = $_.Exception.Message }
    $results += [pscustomobject]@{ src = $j.src; ok = $ok; msg = $msg }
  }
} catch {
  $results += [pscustomobject]@{ src = ''; ok = $false; msg = $_.Exception.Message }
} finally {
  if ($h) { try { $h.Quit() } catch {} }
}
$json = ConvertTo-Json -InputObject @($results) -Depth 3
[System.IO.File]::WriteAllText($env:HANCOM_RESULT, $json, (New-Object System.Text.UTF8Encoding $false))
"""


def available() -> tuple[bool, str]:
    """한글 자동화 객체가 등록돼 있는지 (Windows 레지스트리 확인만 — 한글을 띄우지 않는다)."""
    if sys.platform != "win32":
        return False, "Windows가 아님"
    import winreg
    try:
        winreg.CloseKey(winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, PROG_ID))
    except OSError:
        return False, "한글(HWPFrame.HwpObject) 미설치"
    return True, ""


def resave(files: list[Path]) -> dict[Path, str]:
    """한글로 각 파일을 열어 HWPX로 다시 저장한다. 반환: 파일 -> '' (성공) 또는 실패 사유."""
    status: dict[Path, str] = {f: "한글 결과 없음" for f in files}
    with tempfile.TemporaryDirectory(prefix="hancom_") as tmp:
        tmpdir = Path(tmp)
        jobs = [{"src": str(f.resolve()), "dst": str(tmpdir / f"{i}.hwpx")}
                for i, f in enumerate(files)]
        job_path, result_path = tmpdir / "job.json", tmpdir / "result.json"
        job_path.write_text(json.dumps({
            "module": os.environ.get("HANCOM_SECURITY_MODULE", "FilePathCheckerModule"),
            "jobs": jobs}, ensure_ascii=False), encoding="utf-8")
        env = dict(os.environ, HANCOM_JOB=str(job_path), HANCOM_RESULT=str(result_path))
        try:
            # -EncodedCommand: 여러 줄 스크립트를 파일 없이 한 번에 넘긴다(-Command -는 줄 단위로
            # 읽어 try/foreach 블록이 깨진다). 실행 정책 대상도 아니다.
            encoded = base64.b64encode(_PS_SCRIPT.encode("utf-16-le")).decode("ascii")
            proc = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-EncodedCommand", encoded],
                text=True, env=env, capture_output=True,
                encoding="utf-8", errors="replace", timeout=60 + 30 * len(files))
        except subprocess.TimeoutExpired:
            return {f: "한글 응답 시간 초과(보안 승인 창이 떠 있을 수 있음)" for f in files}
        except OSError as e:
            return {f: f"PowerShell 실행 실패: {e}" for f in files}
        if not result_path.exists():
            tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-3:]
            return {f: "한글 결과 없음" + (f" ({' / '.join(tail)})" if tail else "")
                    for f in files}
        results = json.loads(result_path.read_text(encoding="utf-8-sig"))
        by_src = {r.get("src"): r for r in results if isinstance(r, dict)}
        fatal = by_src.get("")
        for f, j in zip(files, jobs):
            r = by_src.get(j["src"]) or fatal
            if not r or not r.get("ok"):
                status[f] = f"한글 저장 실패: {(r or {}).get('msg') or '원인 불명'}"
                continue
            out = Path(j["dst"])
            errs = check(out) if out.exists() else ["한글이 파일을 쓰지 않음"]
            if errs:
                status[f] = "한글 산출물 게이트 실패: " + "; ".join(errs)
                continue
            os.replace(out, f)
            status[f] = ""
    return status


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("outdir")
    ap.add_argument("stems", nargs="*")
    ap.add_argument("--engine", choices=("auto", "hancom", "python"), default="auto")
    args = ap.parse_args()
    outdir = Path(args.outdir)
    files = ([outdir / f"{s}.hwpx" for s in args.stems if (outdir / f"{s}.hwpx").exists()]
             if args.stems else sorted(outdir.glob("*.hwpx")))
    if args.engine == "python" or not files:
        return 0
    ok, why = available()
    if not ok:
        print(f"hwpx engine: python (한글 사용 불가 — {why})")
        return 1 if args.engine == "hancom" else 0
    failed = 0
    for f, err in resave(files).items():
        if err:
            failed += 1
            print(f"hwpx engine: python (폴백) {f.name} — {err}")
        else:
            print(f"hwpx engine: 한글 {f.name}")
    return 1 if failed and args.engine == "hancom" else 0


if __name__ == "__main__":
    sys.exit(main())
