"""Tests for 9a / 9b / 9c CIQ raw sheets and (later) 9_Peer_Summary."""
from __future__ import annotations

from lbo_template.layout import SHEET_9A, SHEET_9B, SHEET_9C, SHEET_PEER


def test_9a_fixed_headers(wb):
    ws = wb[SHEET_9A]
    expected = [
        "Company Name",
        "CIQ ID / Ticker",
        "Country",
        "Currency",
        "Market Cap",
        "Enterprise Value",
        "LTM Revenue",
        "LTM EBITDA",
        "LTM EBITDA Margin %",
        "EV / LTM EBITDA",
        "EV / FY-1 EBITDA",
        "EV / FY-2 EBITDA",
        "EV / NTM EBITDA",
        "Net Debt / LTM EBITDA",
        "LTM Period End Date",
    ]
    for i, h in enumerate(expected):
        col = chr(ord("A") + i)
        assert ws[f"{col}2"].value == h, f"header col {col}: {ws[f'{col}2'].value!r} != {h!r}"


def test_9a_mode_cell(wb):
    ws = wb[SHEET_9A]
    assert ws["A1"].value == "Mode"
    mode_formula = ws["B1"].value
    assert "ISFORMULA" in mode_formula
    assert "Plug-in" in mode_formula
    assert "Paste Fallback" in mode_formula


def test_9a_ciq_primary_formula_row3(wb):
    """Row 3 = row 1 peer. E3 = =IFERROR(CIQ($B3,...IQ_MARKETCAP...)."""
    ws = wb[SHEET_9A]
    e3 = ws["E3"].value
    assert "CIQ" in e3 and "IQ_MARKETCAP" in e3 and "$B3" in e3


def test_9b_max_500_rows_warning(wb):
    ws = wb[SHEET_9B]
    c1 = ws["C1"].value
    assert "500" in c1
    assert "COUNTA" in c1 or "Export" in c1


def test_9b_headers(wb):
    ws = wb[SHEET_9B]
    expected_first_6 = [
        "Transaction ID",
        "Announced Date",
        "Closed Date",
        "Target Company Name",
        "Target Country",
        "Target Primary Industry",
    ]
    for i, h in enumerate(expected_first_6):
        col = chr(ord("A") + i)
        assert ws[f"{col}2"].value == h


def test_9c_source_dropdown(wb):
    ws = wb[SHEET_9C]
    dvs = ws.data_validations.dataValidation
    found = False
    for dv in dvs:
        if "Kisvalue" in (dv.formula1 or "") and "한경Compass" in (dv.formula1 or ""):
            found = True
    assert found, "Source column must have dropdown with Kisvalue, 한경Compass, etc."


def test_9c_auto_reliability_lookup(wb):
    ws = wb[SHEET_9C]
    q3 = ws["Q3"].value
    assert "XLOOKUP" in q3 or "VLOOKUP" in q3


def test_peer_summary_has_trading_and_transaction(wb):
    ws = wb[SHEET_PEER]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 60)]
    assert any("Trading Peer Summary" in (v or "") for v in col_a)
    assert any("Transaction Comps Summary" in (v or "") for v in col_a)


def test_applied_multiples_named_ranges(wb):
    assert "Applied_Trading_Multiple" in wb.defined_names
    assert "Applied_Trading_PBR" in wb.defined_names
    assert "Applied_Transaction_Multiple" in wb.defined_names


def test_three_year_average_of_average(wb):
    """설계 요구사항 7: 3개년 평균의 평균"""
    ws = wb[SHEET_PEER]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 60)]
    assert any("3개년 평균의 평균" in (v or "") for v in col_a)
