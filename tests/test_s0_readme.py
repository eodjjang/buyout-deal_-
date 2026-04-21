"""Tests for 0_README sheet content."""
from __future__ import annotations

from lbo_template.layout import SHEET_README


def test_readme_title(wb):
    ws = wb[SHEET_README]
    assert ws["A1"].value == "LBO Stress Template v0.5 — 대주단 관점 범용"


def test_readme_sections_present(wb):
    ws = wb[SHEET_README]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 60)]
    expected_sections = [
        "1. Version History",
        "2. 색상·폰트·단위 컨벤션",
        "3. Phase 0 Preconditions 체크리스트",
        "4. CapIQ Saved Screen 사전 세팅",
        "5. Alt-A: Paste Fallback 시 재배포 절차",
        "6. 시트 맵",
    ]
    for section in expected_sections:
        assert section in col_a, f"section missing: {section}"


def test_readme_precondition_checkboxes(wb):
    ws = wb[SHEET_README]
    col_b = [ws.cell(row=r, column=2).value for r in range(1, 80)]
    assert any("Precondition 1" in str(v) for v in col_b if v)
    assert any("Precondition 2" in str(v) for v in col_b if v)
    assert any("Precondition 3" in str(v) for v in col_b if v)
