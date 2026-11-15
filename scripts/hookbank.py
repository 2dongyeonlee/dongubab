"""훅 모음(references/hookbank.csv) 조회·추가.

조회: python3 scripts/hookbank.py query 빵집 디저트 [--n 5]
  태그·세부·커버 문구에 키워드가 하나라도 들어간 행을 배수(조회÷계정 중앙값) 높은 순으로 출력.
  맞는 행이 없으면 그 사실을 먼저 알리고 전체 상위 행을 "형식 참고용"으로 출력.
추가: python3 scripts/hookbank.py add --top <상위.csv> --date YYYY-MM-DD [--views <조회.csv>] [--kind 캡처]
  동연 캡처 판독 결과나 aside 수집 결과를 붙인다. --views가 있으면 계정 중앙값·배수를 계산.
  게시물URL이 없으면(캡처) 계정+커버 문구로 중복을 판단한다.
"""
import argparse
import csv
import os
import statistics
import sys

BANK = os.path.join(os.path.dirname(__file__), "..", "references", "hookbank.csv")
COLS = ["수집일", "구분", "계정", "태그", "세부", "지역", "커버1", "커버2", "조회", "계정중앙값", "배수",
        "훅유형", "첫3초", "길이초", "캡션첫줄", "말투", "협찬", "URL"]


def num(s):
    s = str(s or "").strip().replace(",", "")
    if not s:
        return None
    if s.endswith("만"):
        return round(float(s[:-1]) * 10000)
    if s.endswith("천"):
        return round(float(s[:-1]) * 1000)
    try:
        return round(float(s))
    except ValueError:
        return None


def load():
    if not os.path.exists(BANK):
        return []
    return list(csv.DictReader(open(BANK, encoding="utf-8-sig")))


def save(rows):
    with open(BANK, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in COLS})


def mult(r):
    try:
        return float(r["배수"])
    except (TypeError, ValueError):
        return -1.0


def show(rows):
    for r in rows:
        m = f"{mult(r):.1f}배" if mult(r) >= 0 else "배수 없음"
        cover = " / ".join(x for x in [r["커버1"], r["커버2"]] if x)
        print(f"- [{r['구분']}] {r['계정']} | {r['태그']} | {m} | 조회 {r['조회'] or '-'} | 커버: {cover}"
              f" | 훅: {r['훅유형'] or '-'} | 첫3초: {r['첫3초'] or '-'} | {r['길이초'] or '-'}초 | {r['수집일']} | {r['URL']}")


def query(keys, n):
    rows = load()
    hit = [r for r in rows if any(k in (r["태그"] + r["세부"] + r["커버1"] + r["커버2"]) for k in keys)]
    hit.sort(key=mult, reverse=True)
    if hit:
        print(f"## 업종 일치 {len(hit)}개 중 상위 {min(n, len(hit))}개 ({', '.join(keys)})")
        show(hit[:n])
    else:
        print(f"## 업종 일치 레퍼런스 없음 ({', '.join(keys)}) → aside 수집 필요 업종")
    top = sorted([r for r in rows if r not in hit and r["구분"] in ("상위영상", "캡처")], key=mult, reverse=True)[:3]
    print("## 형식 참고용 전체 상위 3개")
    show(top)
    dates = sorted({r["수집일"] for r in rows})
    print(f"## 훅 모음 {len(rows)}개, 최신 수집일 {dates[-1] if dates else '-'}")


def key(r):
    return r.get("URL") or f"{r.get('계정')}|{r.get('커버1')}|{r.get('커버2')}"


def add(views, top, date, kind):
    vals = {}
    for r in (csv.DictReader(open(views, encoding="utf-8-sig")) if views else []):
        if (r.get("고정여부") or "").strip():
            continue
        v = num(r.get("공개조회수"))
        if v:
            vals.setdefault(r["계정"], []).append(v)
    med = {a: statistics.median(v) for a, v in vals.items() if len(v) >= 5}
    rows = load()
    seen = {key(r) for r in rows}
    added = 0
    for r in csv.DictReader(open(top, encoding="utf-8-sig")):
        url = (r.get("게시물URL") or "").strip()
        k = url or f"{r.get('계정')}|{r.get('커버 1줄', '')}|{r.get('커버 2줄', '')}"
        if k in seen or not (url or r.get("커버 1줄")):
            continue
        v, m = num(r.get("공개 조회수")), med.get(r["계정"])
        rows.append({
            "수집일": date, "구분": kind, "계정": r["계정"], "태그": r.get("태그", ""), "세부": r.get("세부", ""),
            "지역": r.get("지역", ""), "커버1": r.get("커버 1줄", ""), "커버2": r.get("커버 2줄", ""),
            "조회": v or "", "계정중앙값": m or "", "배수": round(v / m, 2) if v and m else "",
            "훅유형": r.get("훅유형", ""), "첫3초": r.get("첫 3초 화면", ""), "길이초": r.get("영상 길이(초)", ""),
            "캡션첫줄": r.get("캡션 첫 줄", ""), "말투": r.get("캡션 말투", ""), "협찬": r.get("협찬 표기", ""), "URL": url})
        seen.add(k)
        added += 1
    save(rows)
    print(f"추가 {added}개. 중앙값 계산 계정 {len(med)}개(최근 조회 5개 미만 계정은 배수 비움). 훅유형이 빈 행은 reference-analyze로 채운다.")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    q = sub.add_parser("query")
    q.add_argument("keys", nargs="+")
    q.add_argument("--n", type=int, default=5)
    a = sub.add_parser("add")
    a.add_argument("--views")
    a.add_argument("--kind", default="상위영상", help="상위영상 / 캡처 / 같은가게검색")
    a.add_argument("--top", required=True)
    a.add_argument("--date", required=True)
    args = ap.parse_args()
    if args.cmd == "query":
        query(args.keys, args.n)
    else:
        add(args.views, args.top, args.date, args.kind)


if __name__ == "__main__":
    sys.exit(main())
