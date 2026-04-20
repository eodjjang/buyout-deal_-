from lbo_template.layout import SHEET_INPUT


def test_section_a_labels(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A3"].value == "Section A — 인수 조건 (Transaction Terms)"
    labels_col_a = [ws.cell(row=r, column=1).value for r in range(5, 20)]
    expected = [
        "인수금액 (Purchase EV)",
        "Less: Net Debt Assumed",
        "= 지분 인수가액 (Equity Purchase Price)",
        "+ Transaction Fee (M&A 자문·실사·세무)",
        "= Uses of Funds 합계",
        "Sources: Opco Senior TL",
        "Sources: Opco 2nd Lien",
        "Sources: Holdco Sub Loan",
        "Sources: Sponsor Equity (plug)",
        "Target Net Debt / LTM EBITDA (본부 승인치)",
        "Closing Date",
        "Exit Date (Assumed)",
    ]
    for i, e in enumerate(expected):
        assert labels_col_a[i] == e, f"row {5+i}: {labels_col_a[i]!r} != {e!r}"


def test_section_a_formulas(wb):
    ws = wb[SHEET_INPUT]
    assert ws["B7"].value == "=B5-B6"
    assert ws["B9"].value == "=B7+B8"
    assert ws["B13"].value == "=B9-B10-B11-B12"


def test_section_b_fy_axis(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A22"].value == "Section B — Base Case 4대 드라이버"
    expected = ["FY-2 Actual", "FY-1 Actual", "LTM", "FY1", "FY2", "FY3", "FY4", "FY5"]
    for i, col in enumerate(["B", "C", "D", "E", "F", "G", "H", "I"]):
        assert ws[f"{col}23"].value == expected[i]


def test_section_b_ebitda_is_reported(wb):
    """Precondition 1 반영: Reported EBITDA 단일 행"""
    ws = wb[SHEET_INPUT]
    rows_col_a = [ws.cell(row=r, column=1).value for r in range(24, 35)]
    assert "EBITDA (Reported)" in rows_col_a
    assert not any("Adjusted" in (v or "") for v in rows_col_a), \
        "Adjusted EBITDA row should NOT exist per Precondition 1"


def test_section_c_implied_ratios(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A38"].value == "Section C — Implied 역산 지표 (검증용)"
    labels = [ws.cell(row=r, column=1).value for r in range(39, 48)]
    assert "EBITDA Margin" in labels
    assert "Capex as % of Revenue" in labels
    assert "Revenue YoY Growth" in labels


def test_dual_check_rows(wb):
    """v0.4 이중 check: (1) Sources=Uses (표시용), (2) Target Leverage 상한 (실질 검증)"""
    ws = wb[SHEET_INPUT]
    labels = [ws.cell(row=r, column=1).value for r in range(5, 25)]
    assert any("Sources − Uses" in (v or "") for v in labels)
    assert any("Target Leverage Check" in (v or "") for v in labels)
