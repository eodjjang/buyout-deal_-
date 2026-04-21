from lbo_template.layout import SHEET_STRESS, CASE_SWITCH_CELL


def test_case_switch_cell(wb):
    ws = wb[SHEET_STRESS]
    assert ws[CASE_SWITCH_CELL].value == "Base"
    assert "Case_Switch" in wb.defined_names


def test_case_switch_validation(wb):
    ws = wb[SHEET_STRESS]
    dvs = ws.data_validations.dataValidation
    assert any(
        CASE_SWITCH_CELL in [c.coord for c in dv.sqref.ranges] or CASE_SWITCH_CELL in str(dv.sqref)
        for dv in dvs
    ), "Case_Switch cell must have data validation (Base/Upside/Downside dropdown)"


def test_param_table_structure(wb):
    ws = wb[SHEET_STRESS]
    assert ws["A7"].value == "파라미터"
    assert ws["B7"].value == "Base"
    assert ws["C7"].value == "Upside"
    assert ws["D7"].value == "Downside"
    assert ws["E7"].value == "단위"
    assert ws["F7"].value == "Active"
    params = [ws.cell(row=r, column=1).value for r in range(8, 16)]
    assert params[0] == "Revenue Growth Δ"
    assert params[1] == "EBITDA Margin Δ"
    assert params[2] == "Capex % of Revenue Δ"
    assert params[3] == "ΔNWC % of Revenue Δ"
    assert params[4] == "WACC Uplift"
    assert params[5] == "Exit Multiple Δ"
    assert params[6] == "Permanent Growth (고정)"


def test_default_values(wb):
    ws = wb[SHEET_STRESS]
    assert ws["B8"].value == 0.0
    assert ws["C8"].value == 0.02
    assert ws["D8"].value == -0.05
    assert ws["B14"].value == 0.01
    assert ws["C14"].value == 0.01
    assert ws["D14"].value == 0.01


def test_active_formula_uses_case_branch(wb):
    ws = wb[SHEET_STRESS]
    f8 = ws["F8"].value
    assert "Case_Switch" in f8
    assert "IF(" in f8 and "Base" in f8 and "Upside" in f8 and "Downside" in f8


def test_named_ranges_for_active_values(wb):
    expected = [
        "Active_Revenue_Growth_Delta",
        "Active_EBITDA_Margin_Delta",
        "Active_Capex_Pct_Delta",
        "Active_NWC_Pct_Delta",
        "Active_WACC_Uplift",
        "Active_Exit_Multiple_Delta",
        "Perm_Growth",
    ]
    for name in expected:
        assert name in wb.defined_names, f"missing named range: {name}"


def test_active_named_ranges_attr_text(wb):
    expected = {
        "Active_Revenue_Growth_Delta": f"'{SHEET_STRESS}'!$F$8",
        "Active_EBITDA_Margin_Delta": f"'{SHEET_STRESS}'!$F$9",
        "Active_Capex_Pct_Delta": f"'{SHEET_STRESS}'!$F$10",
        "Active_NWC_Pct_Delta": f"'{SHEET_STRESS}'!$F$11",
        "Active_WACC_Uplift": f"'{SHEET_STRESS}'!$F$12",
        "Active_Exit_Multiple_Delta": f"'{SHEET_STRESS}'!$F$13",
        "Perm_Growth": f"'{SHEET_STRESS}'!$F$14",
    }
    for name, attr in expected.items():
        assert name in wb.defined_names, f"missing named range: {name}"
        assert wb.defined_names[name].attr_text == attr, (
            f"{name} attr_text mismatch: {wb.defined_names[name].attr_text!r} != {attr!r}"
        )
