from lbo_template.layout import SHEET_DCF


def test_dcf_rows(wb):
    ws = wb[SHEET_DCF]
    labels = [ws.cell(row=r, column=1).value for r in range(1, 25)]
    expected = [
        "Stressed EBITDA",
        "(-) Cash Taxes on EBIT",
        "(-) Capex",
        "(-) ΔNWC",
        "FCFF",
        "WACC",
        "Discount Period",
        "Discount Factor",
        "PV of FCFF",
        "Terminal Value (Gordon)",
        "PV of TV",
        "EV (PV 합계)",
        "(+) 비영업자산",
        "(-) Net Debt (Closing)",
        "담보기준 Equity Value",
    ]
    for e in expected:
        assert e in labels, f"missing: {e}"


def test_mid_year_discount_periods(wb):
    ws = wb[SHEET_DCF]
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "Discount Period":
            assert ws.cell(row=r, column=5).value == 0.5
            assert ws.cell(row=r, column=6).value == 1.5
            assert ws.cell(row=r, column=7).value == 2.5
            assert ws.cell(row=r, column=8).value == 3.5
            assert ws.cell(row=r, column=9).value == 4.5
            assert ws.cell(row=r, column=10).value == 5.0
            return
    raise AssertionError("Discount Period row missing")


def test_tv_and_pv_use_perm_growth_and_j11_exponent(wb):
    ws = wb[SHEET_DCF]
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "Terminal Value (Gordon)":
            assert "Perm_Growth" in ws.cell(row=r, column=10).value
            break
    else:
        raise AssertionError("TV row missing")
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "PV of TV":
            pv = ws.cell(row=r, column=10).value
            assert "J11" in pv and "^" in pv, f"expected PV(TV) to use ^J11, got {pv!r}"
            assert "5.0" not in pv, "PV(TV) should not hardcode 5.0 exponent (use J11)"
            return
    raise AssertionError("PV of TV row missing")


def test_wacc_uses_active_uplift(wb):
    ws = wb[SHEET_DCF]
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "WACC":
            wacc = ws.cell(row=r, column=5).value
            assert "Active_WACC_Uplift" in wacc
            assert "Base_WACC" in wacc
            return
    raise AssertionError("WACC row missing")
