"""Shared pytest fixtures."""
from __future__ import annotations
import pytest
from openpyxl import Workbook
from lbo_template.build import build_workbook


@pytest.fixture(scope="session")
def wb() -> Workbook:
    """Build the workbook once per test session."""
    return build_workbook()
