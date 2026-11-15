"""성과기록 xlsx 생성. 사용: python3 scripts/make_perf_sheet.py <출력경로> [seed.csv]
seed.csv(log/*_정규화.csv 형식)를 주면 그 행으로 채우고, 없으면 log/001·002 기본값을 쓴다.
기존 파일이 있으면 중단한다(덮어쓰기 금지)."""
import csv
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.worksheet.datavalidation import DataValidation

INPUT = ["No", "게시일", "가게", "카테고리", "협찬", "커버 문구", "커버 유형", "톤",
         "조회", "도달", "좋아요", "댓글", "공유", "저장", "팔로우", "평균시청(초)", "건너뛰기율", "비팔로워비율", "메모"]
CALC = ["공유율", "저장율", "팔로우율", "공유/저장", "유형", "공유/조회", "저장/조회", "팔로우/조회"]
CATS = ["노포", "숨은맛집", "대중맛집", "바·술집", "브랜드·팝업", "카페·디저트", "기타"]
COVERS = ["가격·룰", "궁금증(정체숨김)", "구성놀람", "공간반전", "신상·소식", "권위차용", "비유·최상급", "혜택·이벤트", "일반워딩", "기타"]
TONES = ["반말혼잣말", "존댓말구어체", "기타"]
MAX_ROW = 200

# /log/001, /log/002 실데이터
SEED = [
    [1, None, "미동식당", "노포", "N", "서대문 만원 안주 오마카세 / 53년된 아파트에 위치한 가성비 좋은 술집",
     "가격·룰", "반말혼잣말", 142723, 120644, 989, 136, 3900, 2800, 36, 7, None, None, "출처 log/001, 게시일 확인 필요"],
    [2, None, "올디스타코", "바·술집", "N", "을지로 추천 샴페인 바 / 힙한 분위기에 샴페인 페어링 안주 다 성공",
     "일반워딩", "반말혼잣말", 65297, 58171, 441, 112, 610, 643, 10, 4, 0.589, None, "출처 log/002, 게시일 확인 필요"],
]


def col(name):
    from openpyxl.utils import get_column_letter
    return get_column_letter((INPUT + CALC).index(name) + 1)


def load_seed(path):
    """정규화 CSV → INPUT 순서 행 목록. 숫자는 int, 빈칸은 None."""
    num = {"조회", "도달", "좋아요", "댓글", "공유", "저장", "팔로우", "평균시청"}
    rows = []
    for r in csv.DictReader(open(path, encoding="utf-8-sig")):
        row = []
        for k in ["No", "게시일", "가게", "카테고리", "협찬", "커버문구", "커버유형", "톤", "조회", "도달",
                  "좋아요", "댓글", "공유", "저장", "팔로우", "평균시청", "건너뛰기율", "비팔로워비율", "메모"]:
            v = (r.get(k) or "").strip()
            if v == "":
                row.append(None)
            elif k in num or k == "No":
                row.append(int(v))
            elif k in ("건너뛰기율", "비팔로워비율"):
                row.append(float(v))
            else:
                row.append(v)
        rows.append(row)
    return rows


def main(out, seed=None):
    if os.path.exists(out):
        sys.exit(f"이미 존재: {out} (덮어쓰지 않음, _v2로 저장할 것)")
    seed = seed if seed is not None else SEED
    wb = Workbook()
    ws = wb.active
    ws.title = "게시물"
    head = Font(bold=True)
    calc_fill = PatternFill("solid", fgColor="EEEEEE")
    ws.append(INPUT + CALC)
    for c in ws[1]:
        c.font = head
        c.alignment = Alignment(horizontal="center")
    for c in ws[1][len(INPUT):]:
        c.fill = calc_fill

    R, S, V, F = col("도달"), col("저장"), col("공유"), col("팔로우")
    for r in range(2, MAX_ROW + 1):
        if r - 2 < len(seed):
            for i, v in enumerate(seed[r - 2]):
                ws.cell(r, i + 1, v)
        base = len(INPUT)
        ws.cell(r, base + 1, f'=IF(OR({R}{r}="",{V}{r}=""),"",{V}{r}/{R}{r})')
        ws.cell(r, base + 2, f'=IF(OR({R}{r}="",{S}{r}=""),"",{S}{r}/{R}{r})')
        ws.cell(r, base + 3, f'=IF(OR({R}{r}="",{F}{r}=""),"",{F}{r}/{R}{r})')
        ws.cell(r, base + 4, f'=IF(OR({S}{r}="",{S}{r}=0,{V}{r}=""),"",{V}{r}/{S}{r})')
        ws.cell(r, base + 5, f'=IF({col("공유/저장")}{r}="","",IF({col("공유/저장")}{r}>=1,"소환형","위시리스트형"))')
        Lk = col("조회")
        for k, src in [(6, V), (7, S), (8, F)]:
            ws.cell(r, base + k, f'=IF(OR({Lk}{r}="",{Lk}{r}=0,{src}{r}=""),"",{src}{r}/{Lk}{r})')
        ws.cell(r, base + 6).number_format = "0.00%"
        ws.cell(r, base + 7).number_format = "0.00%"
        ws.cell(r, base + 8).number_format = "0.000%"
        ws.cell(r, col_idx("비팔로워비율")).number_format = "0.0%"
        for k in range(1, 4):
            ws.cell(r, base + k).number_format = "0.00%"
        ws.cell(r, base + 4).number_format = "0.00"
        ws.cell(r, col_idx("건너뛰기율")).number_format = "0.0%"

    for name, items in [("카테고리", CATS), ("커버 유형", COVERS), ("톤", TONES), ("협찬", ["Y", "N"])]:
        dv = DataValidation(type="list", formula1='"' + ",".join(items) + '"', allow_blank=True)
        ws.add_data_validation(dv)
        dv.add(f"{col(name)}2:{col(name)}{MAX_ROW}")
    ws.freeze_panes = "D2"
    ws.column_dimensions[col("커버 문구")].width = 50
    ws.column_dimensions[col("메모")].width = 30

    sm = wb.create_sheet("요약")
    rng = lambda n: f"게시물!${col(n)}$2:${col(n)}${MAX_ROW}"
    metrics = ["조회", "비팔로워비율", "공유/조회", "팔로우/조회", "공유율", "평균시청(초)"]
    row = 1
    for group, items in [("카테고리", CATS), ("커버 유형", COVERS), ("협찬", ["Y", "N"]), ("톤", TONES)]:
        sm.cell(row, 1, group).font = head
        sm.cell(row, 2, "게시물 수").font = head
        for j, m in enumerate(metrics):
            sm.cell(row, 3 + j, m if m.startswith("평균") else f"평균 {m}").font = head
        row += 1
        for it in items:
            sm.cell(row, 1, it)
            sm.cell(row, 2, f'=COUNTIFS({rng(group)},$A{row})')
            for j, m in enumerate(metrics):
                c = sm.cell(row, 3 + j, f'=IFERROR(AVERAGEIFS({rng(m)},{rng(group)},$A{row}),"")')
                c.number_format = {"평균시청(초)": "0.0", "조회": "#,##0", "비팔로워비율": "0.0%", "팔로우/조회": "0.000%"}.get(m, "0.00%")
            row += 1
        row += 1
    sm.cell(row, 1, "표본 3개 미만 그룹은 결론에 쓰지 않는다(표본 부족). 도달이 비거나 판독 의심이면 x/조회로 비교한다.")
    sm.column_dimensions["A"].width = 18
    for L in "BCDEFGH":
        sm.column_dimensions[L].width = 14
    wb.save(out)
    print("생성:", out)


def col_idx(name):
    return (INPUT + CALC).index(name) + 1


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "log/2026-11-14_dongubab_성과기록.xlsx"
    main(out, load_seed(sys.argv[2]) if len(sys.argv) > 2 else None)
