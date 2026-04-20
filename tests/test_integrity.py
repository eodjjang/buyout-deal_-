"""End-to-end integrity checks."""
from __future__ import annotations

import re

from lbo_template.layout import ALL_SHEETS


def test_all_sheets_exist(wb):
    assert wb.sheetnames == ALL_SHEETS


def test_no_iterative_calc_marker(wb):
    """어떤 셀도 iterative calc를 가정한 수식을 쓰지 않아야 함"""
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    # Heuristic: same-cell self-reference
                    assert f"'{ws.title}'!{cell.coordinate}" not in cell.value, (
                        f"self-ref in {ws.title}!{cell.coordinate}"
                    )


# Scalars use single-token names (e.g. DASH_Case); tables use DASH_*_*_* …
DASH_NAME_PATTERN = re.compile(r"^DASH_[A-Za-z0-9]+(?:_[A-Za-z0-9]+)*$")


def test_dash_names_follow_convention(wb):
    for name in wb.defined_names:
        if name.startswith("DASH_"):
            assert DASH_NAME_PATTERN.match(name), f"bad DASH name: {name}"


def test_named_range_count_threshold(wb):
    """v0.5 설계상 최소 예상 named range 수"""
    dash_names = [n for n in wb.defined_names if n.startswith("DASH_")]
    # CFTable 40 + CFTable_Label 8 + LTV Method 6 + Valuation Method 9 + Coverage 3 + Div 5 + Lev 5 + Case + Version + IRR = ~80+
    assert len(dash_names) >= 70, f"only {len(dash_names)} DASH names; expected ≥70"


def test_active_named_ranges_cover_all_params(wb):
    for n in [
        "Active_Revenue_Growth_Delta",
        "Active_EBITDA_Margin_Delta",
        "Active_Capex_Pct_Delta",
        "Active_NWC_Pct_Delta",
        "Active_WACC_Uplift",
        "Active_Exit_Multiple_Delta",
        "Perm_Growth",
    ]:
        assert n in wb.defined_names


def test_sources_equals_uses_check_formula_exists(wb):
    ws = wb["1_Input_BaseCase"]
    # Check row referenced in Task 5 test — label "Check: Sources − Uses"
    found = False
    for r in range(1, 30):
        label = ws.cell(row=r, column=1).value
        if label and "Sources − Uses" in label:
            formula = ws.cell(row=r, column=2).value
            assert formula.startswith("=")
            found = True
    assert found


def test_debt_ending_balances_use_max_zero(wb):
    ws = wb["4_Debt_Schedule"]
    max_zero_count = 0
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "MAX(0" in cell.value:
                max_zero_count += 1
    assert max_zero_count >= 10, "Ending Balance rows must use MAX(0,...) throughout tranches"
