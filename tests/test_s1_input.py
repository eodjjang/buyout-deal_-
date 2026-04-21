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
    labels = [ws.cell(row=r, column=1).value for r in range(40, 45)]
    assert "EBITDA Margin" in labels
    assert "Capex as % of Revenue" in labels
    assert "Revenue YoY Growth" in labels


def test_dual_check_rows(wb):
    """v0.4 이중 check: (1) Sources=Uses (표시용), (2) Target Leverage 상한 (실질 검증)"""
    ws = wb[SHEET_INPUT]
    labels = [ws.cell(row=r, column=1).value for r in range(5, 25)]
    assert any("Sources − Uses" in (v or "") for v in labels)
    assert any("Target Leverage Check" in (v or "") for v in labels)


def test_check_formulas(wb):
    """Dual check row formulas — locks the Sources−Uses display formula and
    the Target Leverage check (downstream T8 Debt Schedule reads B19)."""
    ws = wb[SHEET_INPUT]
    assert ws["B18"].value == "=(B10+B11+B12+B13)-B9"
    assert ws["B19"].value == '=IFERROR((B10+B11+B12)/D27,"")'


def test_section_c_formula_shape(wb):
    """Section C IFERROR templates — locks row references EBITDA=27, Revenue=24,
    Capex=29, ΔNWC=30 used by Sections B and C contract."""
    ws = wb[SHEET_INPUT]
    # EBITDA Margin (row 40) — col F = FY2
    assert ws["F40"].value == '=IFERROR(F27/F24, "")'
    # Revenue YoY (row 43) — FY-2 (col B) intentionally blank
    assert ws["B43"].value is None
    assert ws["C43"].value == '=IFERROR(C24/B24-1, "")'


def test_named_ranges(wb):
    """Cross-sheet contract — Tasks 6-13 will reference these names."""
    expected = {
        "LTM_EBITDA": "'1_Input_BaseCase'!$D$27",
        "Target_Leverage": "'1_Input_BaseCase'!$B$14",
        "Closing_Date": "'1_Input_BaseCase'!$B$15",
        "Exit_Date": "'1_Input_BaseCase'!$B$16",
        "Opco_Senior_Principal": "'1_Input_BaseCase'!$B$10",
        "Opco_2L_Principal": "'1_Input_BaseCase'!$B$11",
        "Holdco_Sub_Principal": "'1_Input_BaseCase'!$B$12",
    }
    for name, attr in expected.items():
        assert name in wb.defined_names, f"missing named range: {name}"
        assert wb.defined_names[name].attr_text == attr, \
            f"{name} attr_text mismatch: {wb.defined_names[name].attr_text!r} != {attr!r}"
