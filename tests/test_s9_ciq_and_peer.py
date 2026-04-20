"""Tests for 9a / 9b / 9c CIQ raw sheets and (later) 9_Peer_Summary."""
from __future__ import annotations

from lbo_template.layout import SHEET_9A, SHEET_9B


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
