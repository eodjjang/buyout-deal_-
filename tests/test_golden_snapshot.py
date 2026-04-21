"""Minimal golden regression: pinned formulas (and scalars) after fresh build."""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from lbo_template.build import build_workbook

_FIXTURE = Path(__file__).resolve().parent / "fixtures" / "goldentest_v05.json"


@pytest.fixture(scope="module")
def golden_cells() -> dict[str, str | float | int]:
    with open(_FIXTURE, encoding="utf-8") as f:
        data = json.load(f)
    return data["cells"]


def test_golden_formulas_match_builder(golden_cells):
    wb = build_workbook()
    mismatches: list[str] = []
    for ref, expected in golden_cells.items():
        sheet, addr = ref.split("!", 1)
        actual = wb[sheet][addr].value
        if actual != expected:
            mismatches.append(f"{ref!r}: expected {expected!r}, got {actual!r}")
    assert not mismatches, "\n".join(mismatches)
