from lbo_template.layout import SHEET_WATERFALL


def test_waterfall_key_rows(wb):
    ws = wb[SHEET_WATERFALL]
    labels = [ws.cell(row=r, column=1).value for r in range(1, 40)]
    expected = [
        "Opco UFCF",
        "Less: Opco Interest (Senior + 2nd Lien)",
        "Less: Opco Mandatory Amort",
        "= Opco CFADS",
        "Less: Minimum Cash Retention",
        "Less: Legal Reserve",
        "= Distributable to Holdco",
        "× Payout Ratio",
        "= Dividend Paid to Holdco",
        "Opco Sweep Available",
        "Holdco Dividend Received",
        "Holdco Interest (if Cash-Pay)",
        "Holdco Net Cash Flow",
        "Holdco ICR (Div / Holdco Interest)",
    ]
    for e in expected:
        assert e in labels, f"missing row: {e}"


def test_kpi_named_ranges(wb):
    for name in ["Opco_DSCR_Row", "Opco_ICR_Row", "Holdco_ICR_Row", "Net_Leverage_Row"]:
        assert name in wb.defined_names, f"missing named range: {name}"


def test_sweep_avail_named_ranges_per_col(wb):
    """4_Debt_Schedule이 참조하는 Opco_Sweep_Avail_E..I"""
    for col in ["E", "F", "G", "H", "I"]:
        name = f"Opco_Sweep_Avail_{col}"
        assert name in wb.defined_names, f"missing: {name}"
