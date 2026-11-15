"""콘텐츠 문구 검사(account-identity/references/rules.md 기준).

사용:
  python3 scripts/lint_copy.py <문구 파일> [--sponsor] [--facts <사실 파일>]

- 문구 파일: 커버·자막·캡션 텍스트만 담은 파일(표·설명 제외)
- --sponsor: 협찬 금지어(할인, 최저가, 효능)도 검사
- --facts: 입력 자료 텍스트. 문구 속 숫자가 이 파일에 없으면 "미확인 수치"
위반이 1건 이상이면 종료 코드 1.
"""
import argparse
import re
import sys

BANNED = ["유명", "3대", "프리미엄", "핫한", "고급", "미친", "명품", "최고급"]
METAPHOR_ONLY = ["끝판왕", "에르메스"]          # "○○계 끝판왕"처럼 비유일 때만 허용
SOURCED_ONLY = ["1위", "1등", "최고"]           # "~라는" 출처 표기 또는 [확인 필요]일 때만 허용
NEEDS_VENDOR = ["공짜", "무료", "서비스"]        # [업체 확인] 표시가 있어야 허용
SPONSOR_BANNED = ["할인", "최저가", "효능"]
CHECK_MARK = "[확인 필요"


def numbers(text):
    return {n.replace(",", "") for n in re.findall(r"\d[\d,]*", text)}


def lint(lines, sponsor=False, facts=None):
    out = []  # (줄 번호, 등급, 내용)
    fact_nums = numbers(facts) if facts is not None else None
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if not s:
            continue
        marked = CHECK_MARK in s
        for w in BANNED:
            if w in s:
                if ("소개" in s or "래요" in s) and marked:
                    out.append((i, "확인", f"업체 설명 전언형 '{w}' — 필수 문구인지 확인"))
                else:
                    out.append((i, "위반", f"근거 없는 평가어 '{w}'"))
        for w in METAPHOR_ONLY:
            for m in re.finditer(w, s):
                if "계" not in s[max(0, m.start() - 6):m.start()]:
                    out.append((i, "위반", f"'{w}'는 '○○계 {w}' 비유형만 허용"))
        prize = (re.search(r"1등.*[23]등", s) or re.search(r"\(\d+명\)", s)
                 or re.search(r"1등\S*\s*\S*\s*(쿠폰|상품권|경품|당첨)", s))  # 경품 순위는 최상급 아님
        hearsay = re.search(r"라는|래요|[가-힣]래(?=[\s,.!~]|$)", s)  # 전언형(~라는, ~래요, ~이래)
        for w in SOURCED_ONLY:
            if w in s and not (hearsay or marked or prize):
                out.append((i, "위반", f"'{w}'는 출처 표기('~라는') 또는 [확인 필요] 필요"))
        for w in NEEDS_VENDOR:
            if w in s and "[업체 확인]" not in s:
                out.append((i, "위반", f"'{w}'는 업체 확인 전 금지"))
        if sponsor:
            for w in SPONSOR_BANNED:
                if w in s:
                    out.append((i, "위반", f"협찬 금지어 '{w}'"))
        if fact_nums is not None:
            for n in numbers(s) - fact_nums:
                out.append((i, "위반", f"미확인 수치 '{n}'(입력 자료에 없음)"))
        if marked:
            out.append((i, "확인", "확인 필요 표시"))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--sponsor", action="store_true")
    ap.add_argument("--facts")
    a = ap.parse_args()
    lines = open(a.file, encoding="utf-8").read().splitlines()
    facts = open(a.facts, encoding="utf-8").read() if a.facts else None
    res = lint(lines, a.sponsor, facts)
    v = [r for r in res if r[1] == "위반"]
    c = [r for r in res if r[1] == "확인"]
    for i, kind, msg in res:
        print(f"{a.file}:{i}: [{kind}] {msg}")
    print(f"위반 {len(v)}건 / 확인 필요 {len(c)}건")
    sys.exit(1 if v else 0)


if __name__ == "__main__":
    main()
