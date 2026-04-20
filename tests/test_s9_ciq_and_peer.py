"""Tests for 9a / 9b / 9c CIQ raw sheets and (later) 9_Peer_Summary."""
from __future__ import annotations

from lbo_template.layout import SHEET_9A


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
