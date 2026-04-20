"""Tests for 7_Returns_LTV sheet (Task 15)."""
from lbo_template.layout import SHEET_RETURNS


def test_three_method_rows(wb):
    ws = wb[SHEET_RETURNS]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 30)]
    assert "평가방식 1" in col_a
    assert "평가방식 2" in col_a
    assert "평가방식 3" in col_a


def test_method_type_dropdown(wb):
    ws = wb[SHEET_RETURNS]
    dvs = ws.data_validations.dataValidation
    found = False
    for dv in dvs:
        f = dv.formula1 or ""
        if "DCF_Stressed" in f and "Trading_EV_EBITDA" in f and "Trading_PBR" in f:
            found = True
    assert found


def test_named_ranges_method_abstraction(wb):
    for i in [1, 2, 3]:
        assert f"DASH_Valuation_Method{i}_Label" in wb.defined_names
        assert f"DASH_Valuation_Method{i}_Multiple" in wb.defined_names
        assert f"DASH_Valuation_Method{i}_EV" in wb.defined_names
        assert f"DASH_LTV_Method{i}_Opco" in wb.defined_names
        assert f"DASH_LTV_Method{i}_Cumulative" in wb.defined_names


def test_method_type_switch_formula(wb):
    ws = wb[SHEET_RETURNS]
    found_switch = False
    for r in range(5, 15):
        for col in "BCDEFGHI":
            v = ws[f"{col}{r}"].value
            if isinstance(v, str) and "SWITCH" in v and "DCF_Stressed" in v:
                found_switch = True
                break
    assert found_switch
