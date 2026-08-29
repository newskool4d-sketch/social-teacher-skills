"""렌더된 hwpx의 한글 무결성 검사: U+FFFD 없음 + 핵심 한글 문자열 존재.

표준 라이브러리만 사용한다 (렌더러와 동일한 의존성 원칙).
"""
import glob
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from check_lesson import hwpx_text  # noqa: E402


def main(outdir):
    paths = sorted(glob.glob(f"{outdir}/*.hwpx"))
    assert paths, f"no hwpx in {outdir}"
    combined = ""
    for p in paths:
        text = hwpx_text(p)
        assert "�" not in text, f"replacement character in {p}"
        combined += text
        print(f"ok: {p} ({len(text)} chars)")
    # 문서 3종을 각각 짚는다 — 하나라도 렌더에서 빠지면 걸린다.
    needles = [
        "자아 정체성에 대해 성찰한다",   # 수업안 · 성취기준 원문
        "결론을 밝히지 않는다",          # 수업안 · 단계 표의 셀
        "내가 그리는 나",                # 학생 자료 · 문서 제목
        "에서 재구성",                   # 학생 자료 · 자료 카드(source_card) 출처
        "학생의 결론이 아니라 근거",      # 관찰 템플릿 · 분류 기준
    ]
    for needle in needles:
        assert needle in combined, f"missing: {needle}"
    print("korean smoke test passed")


if __name__ == "__main__":
    main(sys.argv[1])
