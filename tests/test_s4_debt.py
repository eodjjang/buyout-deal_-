from lbo_template.layout import SHEET_DEBT


def test_three_tranches_present(wb):
    ws = wb[SHEET_DEBT]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 60)]
    assert any("Opco Senior TL" in (v or "") for v in col_a)
    assert any("Opco 2nd Lien" in (v or "") for v in col_a)
    assert any("Holdco Sub" in (v or "") for v in col_a)


def test_interest_uses_opening_balance(wb):
    """순환참조 방지: Interest = Opening × Rate (not Ending or Average)"""
    ws = wb[SHEET_DEBT]
    for r in range(1, 60):
        label = ws.cell(row=r, column=1).value
        if label and "Interest Expense" in label:
            fy1 = ws.cell(row=r, column=5).value
            assert "E" in fy1 or "Opening" in fy1
            return


def test_holdco_pik_dropdown(wb):
    ws = wb[SHEET_DEBT]
    dvs = ws.data_validations.dataValidation
    assert any(
        "PIK" in (dv.formula1 or "") or "Cash" in (dv.formula1 or "")
        for dv in dvs
    ), "Holdco needs PIK/Cash dropdown"


def test_ending_balance_never_negative(wb):
    """Ending = MAX(0, Opening − Mand − Sweep)"""
    ws = wb[SHEET_DEBT]
    for r in range(1, 60):
        label = ws.cell(row=r, column=1).value
        if label and "Ending Balance" in label:
            fy1 = ws.cell(row=r, column=5).value
            assert "MAX(0" in fy1, f"Ending Balance row {r} must use MAX(0,..."
