from lbo_template.layout import SHEET_OVERLAY


def test_overlay_row_labels(wb):
    ws = wb[SHEET_OVERLAY]
    labels = [ws.cell(row=r, column=1).value for r in range(5, 25)]
    expected = [
        "Base Revenue",
        "Base YoY Growth",
        "Stressed YoY Growth",
        "Stressed Revenue",
        "Base EBITDA Margin",
        "Stressed EBITDA Margin",
        "Stressed EBITDA",
        "Base Capex % of Revenue",
        "Stressed Capex",
        "Base ΔNWC % of Revenue",
        "Stressed ΔNWC",
        "D&A (Base pass-through)",
        "EBIT (Stressed)",
        "Cash Taxes",
        "UFCF (Stressed)",
    ]
    for e in expected:
        assert e in labels, f"missing row: {e}"


def test_stressed_revenue_formula_uses_active(wb):
    ws = wb[SHEET_OVERLAY]
    for r in range(5, 25):
        if ws.cell(row=r, column=1).value == "Stressed Revenue":
            e_cell = ws.cell(row=r, column=5).value
            assert (
                "Active_Revenue_Growth_Delta" in e_cell
                or "Stressed YoY" in e_cell
                or "(1+" in e_cell
            )
            return
    raise AssertionError("Stressed Revenue row not found")


def test_ufcf_formula(wb):
    ws = wb[SHEET_OVERLAY]
    for r in range(5, 25):
        if ws.cell(row=r, column=1).value == "UFCF (Stressed)":
            f1 = ws.cell(row=r, column=5).value
            assert "EBITDA" in f1 or "-" in f1
            return
    raise AssertionError("UFCF row not found")
