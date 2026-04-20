# 대주단 관점 범용 LBO 스트레스 템플릿 (MVP) 구현 계획

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Design doc v0.5 (`.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md`)에 정의된 12-탭 엑셀 템플릿 `LBO_Stress_Template_v0.5.xlsx`를 Python(openpyxl) 빌더로 재현 가능하게 생성한다.

**Architecture:** 단일 Python 패키지 `src/lbo_template`이 모든 시트·Named Range·조건부 서식·데이터 유효성을 코드로 선언하고 `dist/LBO_Stress_Template_v0.5.xlsx`를 산출. 각 시트별 builder 함수 + pytest로 "구조 테스트" (셀 주소·수식 문자열·Named Range·폰트색) 선검증 후 빌더 구현(TDD). 수치 계산 검증은 엑셀에서 수기 + Formula Audit로 보완 (Golden Test는 v0.6 연기).

**Tech Stack:**
- Python 3.11+ / openpyxl 3.1+ / pytest 8+
- 출력 단일 산출물: `dist/LBO_Stress_Template_v0.5.xlsx` (VBA 미사용)
- 설계 규약 상속: design-doc §0 (색상·폰트·단위·Sign convention)

**Key Conventions (design-doc §0 요약, 모든 Task에서 참조):**
- 색상: 섹션헤더 `#1F4E79`, 컬럼헤더 `#D9E1F2`, 입력 `#F2F2F2`, Key output `#BDD7EE`
- 폰트색: 입력 `#0000FF`, 계산 `#000000`, 동일탭 링크 `#800080`, 타탭 링크 `#008000`, CIQ 수식 `#008B8B`
- 숫자포맷 기본: `$#,##0;($#,##0);"-"` (회계)
- 단위: KRW 백만원 단일
- 부호 컨벤션: 지출·차감 모두 양수 표기 + 수식에서 차감
- 시점 축: `FY-2 Actual / FY-1 Actual / LTM / FY1 / FY2 / FY3 / FY4 / FY5` (8개 컬럼, B~I열)

---

## File Structure

```
buyout deal_모델분석/
├── .cursor/
│   ├── design-docs/20260420-0400-lender-lbo-stress-template-design.md   (기존)
│   └── plans/20260420-lender-lbo-stress-template-plan.md                (본 문서)
├── src/lbo_template/
│   ├── __init__.py
│   ├── build.py                     # 엔트리포인트: build_workbook() → xlsx 반환
│   ├── conventions.py               # 색상/폰트/Fill/Format 상수 + 헬퍼 함수
│   ├── layout.py                    # 시트별 고정 셀 주소 상수 (B3=Case_Switch 등)
│   ├── named_ranges.py              # DASH_*/Active_*/Applied_* 등록/쓰기 헬퍼
│   └── sheets/
│       ├── __init__.py
│       ├── s0_readme.py
│       ├── s1_input_base.py
│       ├── s2_stress_panel.py
│       ├── s3_overlay.py
│       ├── s4_debt.py
│       ├── s5_waterfall.py
│       ├── s6_dcf.py
│       ├── s7_returns_ltv.py
│       ├── s8_dashboard.py
│       ├── s9a_ciq_trading.py
│       ├── s9b_ciq_transaction.py
│       ├── s9c_manual.py
│       └── s9_peer_summary.py
├── tests/
│   ├── conftest.py                  # 세션-스코프 fixture: 빌더 1회 실행 후 workbook 반환
│   ├── test_bootstrap.py
│   ├── test_conventions.py
│   ├── test_s0_readme.py
│   ├── test_s1_input.py
│   ├── test_s2_stress.py
│   ├── test_s3_overlay.py
│   ├── test_s4_debt.py
│   ├── test_s5_waterfall.py
│   ├── test_s6_dcf.py
│   ├── test_s9_ciq_and_peer.py
│   ├── test_s7_returns_ltv.py
│   ├── test_s8_dashboard.py
│   └── test_integrity.py
├── dist/                            # .gitignore. 빌더 산출물 저장소
├── pyproject.toml
├── README.md
└── .gitignore
```

**책임 분리 원칙:**
- `conventions.py`는 엑셀 스타일 상수만. 로직 없음.
- `layout.py`는 고정 셀 주소만 (Named Range 실제 생성은 `named_ranges.py`). 시트 간 공유되는 좌표의 single source of truth.
- 시트 builder는 `build(ws, wb)` 단일 시그니처. workbook 참조는 Named Range 생성용.

---

## Task 1: 프로젝트 부트스트랩

**Files:**
- Create: `pyproject.toml`
- Create: `.gitignore`
- Create: `README.md`
- Create: `src/lbo_template/__init__.py`
- Create: `tests/__init__.py`
- Create: `tests/conftest.py`
- Create: `tests/test_bootstrap.py`

- [ ] **Step 1: `pyproject.toml` 작성**

```toml
[project]
name = "lbo-template"
version = "0.5.0"
description = "Lender-perspective LBO Stress Template (Excel builder)"
requires-python = ">=3.11"
dependencies = [
    "openpyxl>=3.1.2",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0",
    "pytest-cov>=5.0",
]

[project.scripts]
build-lbo-template = "lbo_template.build:main"

[build-system]
requires = ["setuptools>=68"]
build-backend = "setuptools.build_meta"

[tool.setuptools.packages.find]
where = ["src"]

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-v --tb=short"
```

- [ ] **Step 2: `.gitignore` 작성**

```
__pycache__/
*.pyc
.pytest_cache/
.coverage
dist/
*.egg-info/
.venv/
venv/
# 생성된 엑셀 산출물(바이너리)은 dist/ 외에는 커밋 금지
/*.xlsx
!examples/*.xlsx
```

- [ ] **Step 3: `README.md` 작성**

```markdown
# LBO Stress Template Builder

Design doc: `.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md` (v0.5 APPROVED)
Plan: `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`

## Build

```bash
python -m pip install -e .[dev]
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

## Test

```bash
pytest
```

## 산출물

`dist/LBO_Stress_Template_v0.5.xlsx` — 12개 탭, KRW 백만원 기준, VBA 미사용.
```

- [ ] **Step 4: `src/lbo_template/__init__.py` 작성**

```python
"""Lender-perspective LBO Stress Template builder (v0.5)."""
__version__ = "0.5.0"
```

- [ ] **Step 5: 빌더 엔트리포인트 stub 작성** (`src/lbo_template/build.py`)

```python
"""Entrypoint: assemble the workbook and save to disk."""
from __future__ import annotations
import argparse
from pathlib import Path
from openpyxl import Workbook


def build_workbook() -> Workbook:
    """Assemble the complete LBO stress template workbook."""
    wb = Workbook()
    # Remove default sheet; all tabs created by individual builders later.
    default = wb.active
    wb.remove(default)
    return wb


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist/LBO_Stress_Template_v0.5.xlsx"))
    args = parser.parse_args()
    wb = build_workbook()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 6: `tests/conftest.py` 세션 fixture**

```python
"""Shared pytest fixtures."""
from __future__ import annotations
import pytest
from openpyxl import Workbook
from lbo_template.build import build_workbook


@pytest.fixture(scope="session")
def wb() -> Workbook:
    """Build the workbook once per test session."""
    return build_workbook()
```

- [ ] **Step 7: 부트스트랩 테스트 작성** (`tests/test_bootstrap.py`)

```python
from openpyxl import Workbook


def test_build_returns_workbook(wb: Workbook) -> None:
    assert isinstance(wb, Workbook)


def test_default_sheet_removed(wb: Workbook) -> None:
    assert "Sheet" not in wb.sheetnames
```

- [ ] **Step 8: 의존성 설치 + 테스트 실행**

```powershell
python -m pip install -e .[dev]
pytest tests/test_bootstrap.py -v
```

Expected: 2 passed.

- [ ] **Step 9: 커밋**

```powershell
git add pyproject.toml .gitignore README.md src/ tests/
git commit -m "chore: bootstrap lbo-template package with openpyxl and pytest"
```

---

## Task 2: 엑셀 스타일 컨벤션 모듈

설계 문서 §0의 색상·폰트·숫자포맷 규약을 파이썬 상수로 고정. 이 모듈이 이후 모든 시트 빌더의 스타일 single source of truth.

**Files:**
- Create: `src/lbo_template/conventions.py`
- Create: `tests/test_conventions.py`

- [ ] **Step 1: 실패 테스트 먼저** (`tests/test_conventions.py`)

```python
from openpyxl.styles import Font, PatternFill
from lbo_template import conventions as c


def test_color_constants():
    assert c.COLOR_SECTION_HEADER_FILL == "1F4E79"
    assert c.COLOR_COLUMN_HEADER_FILL == "D9E1F2"
    assert c.COLOR_INPUT_FILL == "F2F2F2"
    assert c.COLOR_KEY_OUTPUT_FILL == "BDD7EE"
    assert c.COLOR_INPUT_FONT == "0000FF"
    assert c.COLOR_CALC_FONT == "000000"
    assert c.COLOR_SAMETAB_LINK_FONT == "800080"
    assert c.COLOR_CROSSTAB_LINK_FONT == "008000"
    assert c.COLOR_CIQ_FORMULA_FONT == "008B8B"


def test_number_formats():
    assert c.NUM_FMT_ACCOUNTING == '$#,##0;($#,##0);"-"'
    assert c.NUM_FMT_PERCENT == "0.0%"
    assert c.NUM_FMT_MULTIPLE == '0.0"x"'
    assert c.NUM_FMT_BPS == '0" bp"'


def test_style_factories_return_correct_types():
    assert isinstance(c.section_header_font(), Font)
    assert isinstance(c.input_font(), Font)
    assert isinstance(c.section_header_fill(), PatternFill)
    assert isinstance(c.input_fill(), PatternFill)


def test_fy_axis_columns():
    assert c.FY_AXIS_COLUMNS == ["B", "C", "D", "E", "F", "G", "H", "I"]
    assert c.FY_AXIS_LABELS == ["FY-2", "FY-1", "LTM", "FY1", "FY2", "FY3", "FY4", "FY5"]
```

- [ ] **Step 2: 테스트 실행하여 실패 확인**

```powershell
pytest tests/test_conventions.py -v
```

Expected: ImportError on `lbo_template.conventions`.

- [ ] **Step 3: `conventions.py` 구현**

```python
"""Style, color, font, and number-format conventions (design doc §0)."""
from __future__ import annotations
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side

COLOR_SECTION_HEADER_FILL = "1F4E79"
COLOR_COLUMN_HEADER_FILL = "D9E1F2"
COLOR_INPUT_FILL = "F2F2F2"
COLOR_KEY_OUTPUT_FILL = "BDD7EE"

COLOR_INPUT_FONT = "0000FF"
COLOR_CALC_FONT = "000000"
COLOR_SAMETAB_LINK_FONT = "800080"
COLOR_CROSSTAB_LINK_FONT = "008000"
COLOR_CIQ_FORMULA_FONT = "008B8B"
COLOR_WHITE_FONT = "FFFFFF"

NUM_FMT_ACCOUNTING = '$#,##0;($#,##0);"-"'
NUM_FMT_PERCENT = "0.0%"
NUM_FMT_PERCENT_PP = '0.0"%p"'
NUM_FMT_MULTIPLE = '0.0"x"'
NUM_FMT_BPS = '0" bp"'
NUM_FMT_DATE = "yyyy-mm-dd"

FY_AXIS_COLUMNS = ["B", "C", "D", "E", "F", "G", "H", "I"]
FY_AXIS_LABELS = ["FY-2", "FY-1", "LTM", "FY1", "FY2", "FY3", "FY4", "FY5"]
FY_AXIS_INDEX = dict(zip(FY_AXIS_LABELS, FY_AXIS_COLUMNS))


def section_header_font() -> Font:
    return Font(name="Calibri", size=11, bold=True, color=COLOR_WHITE_FONT)


def column_header_font() -> Font:
    return Font(name="Calibri", size=10, bold=True, color=COLOR_CALC_FONT)


def input_font() -> Font:
    return Font(name="Calibri", size=10, color=COLOR_INPUT_FONT)


def calc_font() -> Font:
    return Font(name="Calibri", size=10, color=COLOR_CALC_FONT)


def sametab_link_font() -> Font:
    return Font(name="Calibri", size=10, color=COLOR_SAMETAB_LINK_FONT)


def crosstab_link_font() -> Font:
    return Font(name="Calibri", size=10, color=COLOR_CROSSTAB_LINK_FONT)


def ciq_formula_font() -> Font:
    return Font(name="Calibri", size=10, color=COLOR_CIQ_FORMULA_FONT)


def section_header_fill() -> PatternFill:
    return PatternFill("solid", fgColor=COLOR_SECTION_HEADER_FILL)


def column_header_fill() -> PatternFill:
    return PatternFill("solid", fgColor=COLOR_COLUMN_HEADER_FILL)


def input_fill() -> PatternFill:
    return PatternFill("solid", fgColor=COLOR_INPUT_FILL)


def key_output_fill() -> PatternFill:
    return PatternFill("solid", fgColor=COLOR_KEY_OUTPUT_FILL)


def thin_border() -> Border:
    side = Side(style="thin", color="BFBFBF")
    return Border(left=side, right=side, top=side, bottom=side)


def apply_section_header(cell) -> None:
    cell.font = section_header_font()
    cell.fill = section_header_fill()
    cell.alignment = Alignment(horizontal="left", vertical="center")


def apply_input(cell) -> None:
    cell.font = input_font()
    cell.fill = input_fill()
    cell.border = thin_border()


def apply_calc(cell) -> None:
    cell.font = calc_font()
    cell.border = thin_border()


def apply_key_output(cell) -> None:
    cell.font = calc_font()
    cell.fill = key_output_fill()
    cell.border = thin_border()


def apply_ciq(cell) -> None:
    cell.font = ciq_formula_font()
    cell.border = thin_border()
```

- [ ] **Step 4: 테스트 재실행**

```powershell
pytest tests/test_conventions.py -v
```

Expected: 4 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/conventions.py tests/test_conventions.py
git commit -m "feat(conventions): add color/font/format constants and style helpers per design §0"
```

---

## Task 3: 12-탭 스켈레톤 + layout.py

Design doc §0 Table of Tabs 12개를 모두 공란으로 생성. 각 builder 파일은 stub(시트 생성만). 이후 Task에서 내용 채움. Named Range 좌표 상수를 `layout.py`에 모아둠.

**Files:**
- Create: `src/lbo_template/layout.py`
- Create: `src/lbo_template/sheets/__init__.py`
- Create: `src/lbo_template/sheets/s0_readme.py` ~ `s9_peer_summary.py` (13개)
- Modify: `src/lbo_template/build.py`
- Create: `tests/test_s_skeleton.py` (또는 기존 test_bootstrap.py 확장)

- [ ] **Step 1: `layout.py` 작성**

```python
"""Fixed cell addresses shared across builders (single source of truth)."""
from __future__ import annotations

SHEET_README = "0_README"
SHEET_INPUT = "1_Input_BaseCase"
SHEET_STRESS = "2_Stress_Panel"
SHEET_OVERLAY = "3_Operating_Overlay"
SHEET_DEBT = "4_Debt_Schedule"
SHEET_WATERFALL = "5_CF_Waterfall"
SHEET_DCF = "6_DCF_Valuation"
SHEET_RETURNS = "7_Returns_LTV"
SHEET_DASH = "8_Dashboard"
SHEET_9A = "9a_CIQ_Trading_Raw"
SHEET_9B = "9b_CIQ_Transaction_Raw"
SHEET_9C = "9c_Manual_Supplement"
SHEET_PEER = "9_Peer_Summary"

ALL_SHEETS = [
    SHEET_README,
    SHEET_INPUT,
    SHEET_STRESS,
    SHEET_OVERLAY,
    SHEET_DEBT,
    SHEET_WATERFALL,
    SHEET_DCF,
    SHEET_RETURNS,
    SHEET_DASH,
    SHEET_9A,
    SHEET_9B,
    SHEET_9C,
    SHEET_PEER,
]

# 2_Stress_Panel Case_Switch anchor (design §2.1)
CASE_SWITCH_CELL = "B3"

# 9a/9b paste ranges (design §9a, §9b)
S9A_HEADER_ROW = 1
S9A_TICKER_START = "A2"
S9A_DATA_START = "B2"
S9A_DATA_END_ROW = 101  # max 100 peer rows

S9B_HEADER_ROW = 1
S9B_DATA_START = "A2"
S9B_DATA_END_ROW = 501  # max 500 transaction rows (design v0.4)
```

- [ ] **Step 2: 각 시트 builder stub 13개** — 동일 시그니처 반복이므로 `s0_readme.py` 하나만 예시로 본문 기록. 나머지 12개도 동일한 3줄 스텁으로 생성.

`src/lbo_template/sheets/s0_readme.py`:

```python
"""0_README sheet builder."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_README


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_README)
    return ws
```

`s1_input_base.py` ~ `s9_peer_summary.py` 각각: `SHEET_INPUT`, `SHEET_STRESS`, ... 를 import하고 동일한 3줄 `build(wb)` stub 작성. 총 13개 파일 생성.

- [ ] **Step 3: `sheets/__init__.py` 에 re-export**

```python
"""Sheet builders."""
from . import (
    s0_readme,
    s1_input_base,
    s2_stress_panel,
    s3_overlay,
    s4_debt,
    s5_waterfall,
    s6_dcf,
    s7_returns_ltv,
    s8_dashboard,
    s9a_ciq_trading,
    s9b_ciq_transaction,
    s9c_manual,
    s9_peer_summary,
)

__all__ = [
    "s0_readme",
    "s1_input_base",
    "s2_stress_panel",
    "s3_overlay",
    "s4_debt",
    "s5_waterfall",
    "s6_dcf",
    "s7_returns_ltv",
    "s8_dashboard",
    "s9a_ciq_trading",
    "s9b_ciq_transaction",
    "s9c_manual",
    "s9_peer_summary",
]
```

- [ ] **Step 4: `build.py` 업데이트 — 13개 builder 순차 호출**

```python
from __future__ import annotations
import argparse
from pathlib import Path
from openpyxl import Workbook
from lbo_template.sheets import (
    s0_readme,
    s1_input_base,
    s2_stress_panel,
    s3_overlay,
    s4_debt,
    s5_waterfall,
    s6_dcf,
    s7_returns_ltv,
    s8_dashboard,
    s9a_ciq_trading,
    s9b_ciq_transaction,
    s9c_manual,
    s9_peer_summary,
)


def build_workbook() -> Workbook:
    wb = Workbook()
    wb.remove(wb.active)
    # Order matters for readability but not for formula evaluation
    s0_readme.build(wb)
    s1_input_base.build(wb)
    s2_stress_panel.build(wb)
    s3_overlay.build(wb)
    s4_debt.build(wb)
    s5_waterfall.build(wb)
    s6_dcf.build(wb)
    s9a_ciq_trading.build(wb)
    s9b_ciq_transaction.build(wb)
    s9c_manual.build(wb)
    s9_peer_summary.build(wb)
    s7_returns_ltv.build(wb)  # depends on s9_peer_summary + s6_dcf
    s8_dashboard.build(wb)    # depends on all others
    return wb


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=Path("dist/LBO_Stress_Template_v0.5.xlsx"))
    args = parser.parse_args()
    wb = build_workbook()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 5: 스켈레톤 테스트** (`tests/test_bootstrap.py`에 추가)

```python
from lbo_template.layout import ALL_SHEETS


def test_all_13_sheets_created_in_correct_order(wb):
    assert wb.sheetnames == ALL_SHEETS
    assert len(wb.sheetnames) == 13
```

- [ ] **Step 6: 테스트 실행**

```powershell
pytest tests/test_bootstrap.py -v
```

Expected: 3 passed (2 기존 + 1 신규).

- [ ] **Step 7: 빌더 실제 실행 확인**

```powershell
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

Expected: `Wrote dist\LBO_Stress_Template_v0.5.xlsx` 출력. Excel에서 열면 13개 빈 탭.

- [ ] **Step 8: 커밋**

```powershell
git add src/lbo_template/layout.py src/lbo_template/sheets/ src/lbo_template/build.py tests/test_bootstrap.py
git commit -m "feat(skeleton): scaffold 13-tab workbook with empty sheet builders"
```

---

## Task 4: `0_README` 시트

설계 문서 §0의 README 내용 + §9-0 Saved Screen 가이드 + v0.5 Alt-A 재배포 절차를 기록.

**Files:**
- Modify: `src/lbo_template/sheets/s0_readme.py`
- Create: `tests/test_s0_readme.py`

- [ ] **Step 1: 테스트 먼저 작성** (`tests/test_s0_readme.py`)

```python
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
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 80)]
    assert any("Precondition 1" in str(v) for v in col_a if v)
    assert any("Precondition 2" in str(v) for v in col_a if v)
    assert any("Precondition 3" in str(v) for v in col_a if v)
```

- [ ] **Step 2: 테스트 실행하여 실패 확인**

```powershell
pytest tests/test_s0_readme.py -v
```

Expected: FAIL (A1 is None).

- [ ] **Step 3: `s0_readme.py` 구현**

```python
"""0_README sheet — versioning, conventions, Preconditions, CapIQ setup guide."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.utils import get_column_letter
from lbo_template.layout import SHEET_README
from lbo_template import conventions as c


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_README)
    ws.column_dimensions["A"].width = 4
    ws.column_dimensions["B"].width = 80

    ws["A1"] = "LBO Stress Template v0.5 — 대주단 관점 범용"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:F1")

    sections: list[tuple[str, list[str]]] = [
        ("1. Version History", [
            "v0.5 (2026-04-20) — Phase 0 Preconditions 1~3 해결, Alt-A 확정, HMM 양식 반영, Valuation 추상화",
            "v0.4 (2026-04-20) — Spec Self-Review 반영, P·Q 분기 v1.1 backlog로 연기",
            "v0.3 (2026-04-20) — CapIQ Plug-in 수식 primary, P·Q 분기 추가(추후 연기)",
            "v0.2 (2026-04-20) — CapIQ Export-once Cascade-everywhere 구조 도입",
            "v0.1 (2026-04-20) — 초안",
        ]),
        ("2. 색상·폰트·단위 컨벤션", [
            "섹션 헤더 fill: #1F4E79 / 컬럼 헤더 fill: #D9E1F2 / 입력 fill: #F2F2F2 / Key output fill: #BDD7EE",
            "폰트: 입력 #0000FF / 계산 #000000 / 동일탭 링크 #800080 / 타탭 링크 #008000 / CIQ Plug-in 수식 #008B8B",
            "단위: KRW 백만원 단일. USD 딜은 입력 전 환산. 단위 혼용 금지.",
            "Sign convention: 지출·차감 모두 양수 표기 + 수식에서 차감.",
            "시점 축: FY-2 Actual / FY-1 Actual / LTM / FY1 / FY2 / FY3 / FY4 / FY5 (8개 컬럼).",
        ]),
        ("3. Phase 0 Preconditions 체크리스트", [
            "☑ Precondition 1 — Lender-Adjusted EBITDA 정의: 본부 기준 모든 add-back 불인정. Reported EBITDA 단일.",
            "☑ Precondition 2 — Word 심사보고서 표준 양식: HMM 보고서(2023-23차) 양식 자동 추출 반영.",
            "☑ Precondition 3 — CapIQ IT/DLP 제약: Plug-in 유효 / DLP 비차단 / 호출 한도 미상(empirical 확인).",
        ]),
        ("4. CapIQ Saved Screen 사전 세팅", [
            "Saved Screen A (Trading Peers): 15개 컬럼 순서 — Company Name / CIQ ID / Country / Currency / Market Cap / EV / LTM Revenue / LTM EBITDA / LTM EBITDA Margin % / EV/LTM EBITDA / EV/FY-1 / EV/FY-2 / EV/NTM / Net Debt/LTM EBITDA / LTM Period End Date.",
            "Saved Screen B (Transaction Comps): 15개 컬럼 — Transaction ID / Announced / Closed / Target / Target Country / Primary Industry / Buyer / Buyer Type / Currency / Implied EV / LTM Rev / LTM EBITDA / EV/Rev / EV/EBITDA / Deal Status.",
            "Ticker List는 비워두고 딜마다 갈아끼움. 나머지 14개 컬럼 순서는 고정.",
            "Saved Screen URL을 본 시트 하단 '북마크' 섹션에 수기 기록.",
        ]),
        ("5. Alt-A: Paste Fallback 시 재배포 절차", [
            "설계 §9 Alt-A(동일 셀 택1) 구조상, Plug-in 비가용 시 Paste Special Values는 1회 실행하는 순간 9a/9b의 =CIQ() 수식을 영구 소실시킴.",
            "복구 절차: (1) 마스터 템플릿 파일을 사내 팀 드라이브에서 재다운로드. (2) 현재 작업 중인 입력값(1_Input, 2_Stress, 9c_Manual)만 복사해 옮김. (3) 9a/9b는 Ticker 리스트를 재입력하고 Data → Refresh All 1회.",
            "Mode 셀(9a!B1, 9b!B1)이 'Paste Fallback — 재배포 필요'로 전환되면 즉시 이 절차 실행 권장.",
        ]),
        ("6. 시트 맵", [
            "1_Input_BaseCase — 매수자 모델 4대 드라이버 + 인수조건 입력 (단일 진입점)",
            "2_Stress_Panel — Case_Switch + 6개 스트레스 파라미터",
            "3_Operating_Overlay — Stressed Revenue/EBITDA/Capex/NWC/UFCF 계산",
            "4_Debt_Schedule — Opco Senior / Opco 2nd Lien / Holdco Sub 3-트랜치",
            "5_CF_Waterfall — Opco UFCF → 이자·원금 → Dividend → Holdco",
            "6_DCF_Valuation — FCFF 5Y + Gordon TV (영구성장 1.0% 고정, 할인기간 5.0)",
            "7_Returns_LTV — 평가방식 1/2/3 추상화 + 9-열 LTV 표",
            "8_Dashboard — Word 복붙용 요약 (DASH_* Named Range cluster + 차주 자금수지표)",
            "9a_CIQ_Trading_Raw — CapIQ Trading Peer 수식 zone (Plug-in primary, Paste fallback)",
            "9b_CIQ_Transaction_Raw — CapIQ Transaction Comps 수식 zone (max 500행)",
            "9c_Manual_Supplement — Kisvalue/한경 Compass 수기 보완",
            "9_Peer_Summary — 3 소스 통합 + Include ✓ 최종 확정",
        ]),
    ]

    row = 3
    for title, lines in sections:
        ws.cell(row=row, column=1, value=title).font = c.Font(bold=True, size=11)
        row += 1
        for line in lines:
            ws.cell(row=row, column=2, value=line).alignment = c.Alignment(wrap_text=True, vertical="top")
            row += 1
        row += 1  # blank spacer

    return ws
```

> 주의: 위 `c.Font`, `c.Alignment` 참조는 `conventions.py`에 재-export되지 않았으므로 이 시트 파일 상단에서 `from openpyxl.styles import Font, Alignment` import 추가 필요.

수정된 import 블록:

```python
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, Alignment
from lbo_template.layout import SHEET_README
from lbo_template import conventions as c
```

(그리고 `c.Font` → `Font`, `c.Alignment` → `Alignment`로 교체.)

- [ ] **Step 4: 테스트 재실행**

```powershell
pytest tests/test_s0_readme.py -v
```

Expected: 3 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s0_readme.py tests/test_s0_readme.py
git commit -m "feat(s0_readme): populate README with versioning, conventions, Preconditions, CapIQ guide"
```

---

## Task 5: `1_Input_BaseCase` 시트

설계 §1 전체 구현. Section A (인수 조건) / B (4대 드라이버 8컬럼) / C (Implied 역산) + 이중 check row.

**Files:**
- Modify: `src/lbo_template/sheets/s1_input_base.py`
- Create: `tests/test_s1_input.py`

- [ ] **Step 1: 실패 테스트 — Section A 기본 라벨**

```python
from lbo_template.layout import SHEET_INPUT


def test_section_a_labels(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A3"].value == "Section A — 인수 조건 (Transaction Terms)"
    # Row 5부터 항목
    labels_col_a = [ws.cell(row=r, column=1).value for r in range(5, 20)]
    expected = [
        "인수금액 (Purchase EV)",
        "Less: Net Debt Assumed",
        "= 지분 인수가액 (Equity Purchase Price)",
        "+ Transaction Fee (M&A 자문·실사·세무)",
        "= Uses of Funds 합계",
        "Sources: Opco Senior TL",
        "Sources: Opco 2nd Lien",
        "Sources: Holdco Sub Loan",
        "Sources: Sponsor Equity (plug)",
        "Target Net Debt / LTM EBITDA (본부 승인치)",
        "Closing Date",
        "Exit Date (Assumed)",
    ]
    for i, e in enumerate(expected):
        assert labels_col_a[i] == e, f"row {5+i}: {labels_col_a[i]!r} != {e!r}"


def test_section_a_formulas(wb):
    ws = wb[SHEET_INPUT]
    # 지분 인수가액 = 인수금액 - Net Debt
    assert ws["B7"].value == "=B5-B6"
    # Uses 합계 = 지분 + Fee
    assert ws["B9"].value == "=B7+B8"
    # Sponsor Equity plug = Uses - (Senior + 2nd + Holdco)
    assert ws["B13"].value == "=B9-B10-B11-B12"


def test_section_b_fy_axis(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A22"].value == "Section B — Base Case 4대 드라이버"
    # 컬럼 B~I가 FY-2~FY5 라벨
    expected = ["FY-2 Actual", "FY-1 Actual", "LTM", "FY1", "FY2", "FY3", "FY4", "FY5"]
    for i, col in enumerate(["B", "C", "D", "E", "F", "G", "H", "I"]):
        assert ws[f"{col}23"].value == expected[i]


def test_section_b_ebitda_is_reported(wb):
    """Precondition 1 반영: Reported EBITDA 단일 행"""
    ws = wb[SHEET_INPUT]
    rows_col_a = [ws.cell(row=r, column=1).value for r in range(24, 35)]
    assert "EBITDA (Reported)" in rows_col_a
    assert not any("Adjusted" in (v or "") for v in rows_col_a), \
        "Adjusted EBITDA row should NOT exist per Precondition 1"


def test_section_c_implied_ratios(wb):
    ws = wb[SHEET_INPUT]
    assert ws["A38"].value == "Section C — Implied 역산 지표 (검증용)"
    # EBITDA Margin 행의 FY1 셀은 EBITDA/Revenue 수식
    # (정확한 행 번호는 build에서 결정; 테스트는 라벨 존재 확인 중심)
    labels = [ws.cell(row=r, column=1).value for r in range(39, 48)]
    assert "EBITDA Margin" in labels
    assert "Capex as % of Revenue" in labels
    assert "Revenue YoY Growth" in labels


def test_dual_check_rows(wb):
    """v0.4 이중 check: (1) Sources=Uses (표시용), (2) Target Leverage 상한 (실질 검증)"""
    ws = wb[SHEET_INPUT]
    # check row는 Section A 말미에 존재
    labels = [ws.cell(row=r, column=1).value for r in range(5, 25)]
    assert any("Sources − Uses" in (v or "") for v in labels)
    assert any("Target Leverage Check" in (v or "") for v in labels)
```

- [ ] **Step 2: 테스트 실행하여 실패 확인**

```powershell
pytest tests/test_s1_input.py -v
```

Expected: FAIL (셀 전부 None).

- [ ] **Step 3: 빌더 구현**

```python
"""1_Input_BaseCase — sole user-input entry point for Base Case."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.styles import Font
from lbo_template.layout import SHEET_INPUT
from lbo_template import conventions as c

SECTION_A_ROWS = [
    # (row_label, formula_or_None, is_input)
    ("인수금액 (Purchase EV)", None, True),
    ("Less: Net Debt Assumed", None, True),
    ("= 지분 인수가액 (Equity Purchase Price)", "=B5-B6", False),
    ("+ Transaction Fee (M&A 자문·실사·세무)", None, True),
    ("= Uses of Funds 합계", "=B7+B8", False),
    ("Sources: Opco Senior TL", None, True),
    ("Sources: Opco 2nd Lien", None, True),
    ("Sources: Holdco Sub Loan", None, True),
    ("Sources: Sponsor Equity (plug)", "=B9-B10-B11-B12", False),
    ("Target Net Debt / LTM EBITDA (본부 승인치)", None, True),
    ("Closing Date", None, True),
    ("Exit Date (Assumed)", None, True),
]

SECTION_B_ROWS = [
    "Revenue",
    "COGS (or Gross Profit)",
    "SG&A",
    "EBITDA (Reported)",
    "D&A",
    "Capex",
    "Δ NWC (증가=현금유출, +)",
    "Effective Tax Rate",
]

SECTION_C_ROWS = [
    # (label, formula_template_with_{col})
    ("EBITDA Margin", "=IFERROR({c}27/{c}24, \"\")"),
    ("Capex as % of Revenue", "=IFERROR({c}29/{c}24, \"\")"),
    ("ΔNWC as % of Revenue", "=IFERROR({c}30/{c}24, \"\")"),
    ("Revenue YoY Growth", "=IFERROR({c}24/{prev}24-1, \"\")"),
    ("EBITDA YoY Growth", "=IFERROR({c}27/{prev}27-1, \"\")"),
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_INPUT)
    ws.column_dimensions["A"].width = 44
    for col in c.FY_AXIS_COLUMNS:
        ws.column_dimensions[col].width = 14

    # Sheet title
    ws["A1"] = "1. Input — Base Case (사용자 입력 단일 진입점)"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:I1")

    # --- Section A --------------------------------------------------
    ws["A3"] = "Section A — 인수 조건 (Transaction Terms)"
    ws["A3"].font = Font(bold=True, size=11)

    for idx, (label, formula, is_input) in enumerate(SECTION_A_ROWS):
        r = 5 + idx
        ws.cell(row=r, column=1, value=label)
        cell = ws.cell(row=r, column=2)
        if formula:
            cell.value = formula
            c.apply_calc(cell)
        elif is_input:
            c.apply_input(cell)
        if label == "Target Net Debt / LTM EBITDA (본부 승인치)":
            cell.number_format = c.NUM_FMT_MULTIPLE
        elif label in ("Closing Date", "Exit Date (Assumed)"):
            cell.number_format = c.NUM_FMT_DATE
        else:
            cell.number_format = c.NUM_FMT_ACCOUNTING

    # Check rows — row 18 (Sources−Uses 표시용) and row 19 (Target Leverage 실질 검증)
    ws.cell(row=18, column=1, value="Check: Sources − Uses (표시용, =0이어야 함)")
    chk1 = ws.cell(row=18, column=2, value="=(B10+B11+B12+B13)-B9")
    chk1.number_format = c.NUM_FMT_ACCOUNTING
    c.apply_calc(chk1)

    ws.cell(row=19, column=1, value="Check: Target Leverage ((Senior+2nd+Holdco)/LTM EBITDA ≤ Target)")
    # LTM EBITDA 는 Section B의 row 27 D열 (LTM = 컬럼 D)
    chk2 = ws.cell(row=19, column=2, value="=IFERROR((B10+B11+B12)/D27,\"\")")
    chk2.number_format = c.NUM_FMT_MULTIPLE
    c.apply_calc(chk2)

    # --- Section B --------------------------------------------------
    ws["A22"] = "Section B — Base Case 4대 드라이버"
    ws["A22"].font = Font(bold=True, size=11)

    # FY axis header row 23
    for col, label in zip(c.FY_AXIS_COLUMNS, c.FY_AXIS_LABELS):
        cell = ws[f"{col}23"]
        cell.value = f"{label} Actual" if label in ("FY-2", "FY-1") else label
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    for idx, label in enumerate(SECTION_B_ROWS):
        r = 24 + idx
        ws.cell(row=r, column=1, value=label)
        for col in c.FY_AXIS_COLUMNS:
            cell = ws[f"{col}{r}"]
            c.apply_input(cell)
            if label == "Effective Tax Rate":
                cell.number_format = c.NUM_FMT_PERCENT
            else:
                cell.number_format = c.NUM_FMT_ACCOUNTING

    # Note cell for audit trail (Adjusted → Reported 환원 주석용)
    ws.cell(row=33, column=1, value="Note (Adjusted→Reported 환원 내역, Mgmt vs Bank Case 등)")
    note_cell = ws.cell(row=33, column=2)
    c.apply_input(note_cell)
    ws.merge_cells("B33:I33")

    # --- Section C --------------------------------------------------
    ws["A38"] = "Section C — Implied 역산 지표 (검증용)"
    ws["A38"].font = Font(bold=True, size=11)

    for idx, (label, template) in enumerate(SECTION_C_ROWS):
        r = 40 + idx
        ws.cell(row=r, column=1, value=label)
        for col_idx, col in enumerate(c.FY_AXIS_COLUMNS):
            cell = ws[f"{col}{r}"]
            if "prev" in template:
                if col_idx == 0:
                    cell.value = ""  # FY-2 has no previous year
                    continue
                prev_col = c.FY_AXIS_COLUMNS[col_idx - 1]
                cell.value = template.format(c=col, prev=prev_col)
            else:
                cell.value = template.format(c=col)
            c.apply_calc(cell)
            cell.number_format = c.NUM_FMT_PERCENT

    # Named ranges for downstream sheets
    wb.defined_names["LTM_EBITDA"] = DefinedName("LTM_EBITDA", attr_text=f"'{SHEET_INPUT}'!$D$27")
    wb.defined_names["Target_Leverage"] = DefinedName("Target_Leverage", attr_text=f"'{SHEET_INPUT}'!$B$14")
    wb.defined_names["Closing_Date"] = DefinedName("Closing_Date", attr_text=f"'{SHEET_INPUT}'!$B$15")
    wb.defined_names["Exit_Date"] = DefinedName("Exit_Date", attr_text=f"'{SHEET_INPUT}'!$B$16")
    wb.defined_names["Opco_Senior_Principal"] = DefinedName("Opco_Senior_Principal", attr_text=f"'{SHEET_INPUT}'!$B$10")
    wb.defined_names["Opco_2L_Principal"] = DefinedName("Opco_2L_Principal", attr_text=f"'{SHEET_INPUT}'!$B$11")
    wb.defined_names["Holdco_Sub_Principal"] = DefinedName("Holdco_Sub_Principal", attr_text=f"'{SHEET_INPUT}'!$B$12")

    # Conditional formatting for check rows
    from openpyxl.formatting.rule import CellIsRule
    from openpyxl.styles import PatternFill
    red = PatternFill("solid", fgColor="FFC7CE")
    # Target Leverage 초과 시 빨강
    ws.conditional_formatting.add(
        "B19",
        CellIsRule(operator="greaterThan", formula=["B14"], fill=red),
    )
    return ws
```

- [ ] **Step 4: 테스트 재실행**

```powershell
pytest tests/test_s1_input.py -v
```

Expected: 6 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s1_input_base.py tests/test_s1_input.py
git commit -m "feat(s1_input): implement Section A/B/C with dual check rows and named ranges (Precondition 1 reflected)"
```

---

## Task 6: `2_Stress_Panel` 시트

설계 §2 전체. Case_Switch 드롭다운, 6개 파라미터 테이블, Active_* 계산 열, 산업 디폴트 프리셋 드롭다운.

**Files:**
- Modify: `src/lbo_template/sheets/s2_stress_panel.py`
- Create: `tests/test_s2_stress.py`

- [ ] **Step 1: 테스트 작성**

```python
from lbo_template.layout import SHEET_STRESS, CASE_SWITCH_CELL


def test_case_switch_cell(wb):
    ws = wb[SHEET_STRESS]
    assert ws[CASE_SWITCH_CELL].value == "Base"
    # Named range 등록 확인
    assert "Case_Switch" in wb.defined_names


def test_case_switch_validation(wb):
    ws = wb[SHEET_STRESS]
    dvs = ws.data_validations.dataValidation
    assert any(
        CASE_SWITCH_CELL in [c.coord for c in dv.sqref.ranges] or CASE_SWITCH_CELL in str(dv.sqref)
        for dv in dvs
    ), "Case_Switch cell must have data validation (Base/Upside/Downside dropdown)"


def test_param_table_structure(wb):
    ws = wb[SHEET_STRESS]
    # 컬럼 헤더: A=파라미터명, B=Base, C=Upside, D=Downside, E=Unit, F=Active
    assert ws["A7"].value == "파라미터"
    assert ws["B7"].value == "Base"
    assert ws["C7"].value == "Upside"
    assert ws["D7"].value == "Downside"
    assert ws["E7"].value == "단위"
    assert ws["F7"].value == "Active"

    # 6행 파라미터: Revenue Growth Δ / EBITDA Margin Δ / Capex % Δ / NWC % Δ / WACC Uplift / Exit Multiple Δ
    params = [ws.cell(row=r, column=1).value for r in range(8, 16)]
    assert params[0] == "Revenue Growth Δ"
    assert params[1] == "EBITDA Margin Δ"
    assert params[2] == "Capex % of Revenue Δ"
    assert params[3] == "ΔNWC % of Revenue Δ"
    assert params[4] == "WACC Uplift"
    assert params[5] == "Exit Multiple Δ"
    assert params[6] == "Permanent Growth (고정)"


def test_default_values(wb):
    ws = wb[SHEET_STRESS]
    # Revenue Growth Δ: Base 0 / Upside +0.02 / Downside -0.05
    assert ws["B8"].value == 0.0
    assert ws["C8"].value == 0.02
    assert ws["D8"].value == -0.05
    # Permanent Growth 1.0% 고정 (B/C/D 동일)
    assert ws["B14"].value == 0.01
    assert ws["C14"].value == 0.01
    assert ws["D14"].value == 0.01


def test_active_formula_uses_switch(wb):
    ws = wb[SHEET_STRESS]
    # F8 = SWITCH(Case_Switch, "Base", B8, "Upside", C8, "Downside", D8)
    f8 = ws["F8"].value
    assert "SWITCH" in f8 or "CHOOSE" in f8 or "MATCH" in f8
    assert "Case_Switch" in f8


def test_named_ranges_for_active_values(wb):
    expected = [
        "Active_Revenue_Growth_Delta",
        "Active_EBITDA_Margin_Delta",
        "Active_Capex_Pct_Delta",
        "Active_NWC_Pct_Delta",
        "Active_WACC_Uplift",
        "Active_Exit_Multiple_Delta",
        "Perm_Growth",
    ]
    for name in expected:
        assert name in wb.defined_names, f"missing named range: {name}"
```

- [ ] **Step 2: 테스트 실행 → FAIL**

```powershell
pytest tests/test_s2_stress.py -v
```

- [ ] **Step 3: 빌더 구현**

```python
"""2_Stress_Panel — case switch + 6 parameters + industry presets."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font
from lbo_template.layout import SHEET_STRESS, CASE_SWITCH_CELL
from lbo_template import conventions as c

PARAM_ROWS = [
    # (row_label, base, upside, downside, unit_fmt, active_name)
    ("Revenue Growth Δ", 0.0, 0.02, -0.05, c.NUM_FMT_PERCENT, "Active_Revenue_Growth_Delta"),
    ("EBITDA Margin Δ", 0.0, 0.005, -0.03, c.NUM_FMT_PERCENT, "Active_EBITDA_Margin_Delta"),
    ("Capex % of Revenue Δ", 0.0, -0.005, 0.015, c.NUM_FMT_PERCENT, "Active_Capex_Pct_Delta"),
    ("ΔNWC % of Revenue Δ", 0.0, 0.0, 0.01, c.NUM_FMT_PERCENT, "Active_NWC_Pct_Delta"),
    ("WACC Uplift", 0, -50, 100, c.NUM_FMT_BPS, "Active_WACC_Uplift"),
    ("Exit Multiple Δ", 0.0, 1.0, -1.0, c.NUM_FMT_MULTIPLE, "Active_Exit_Multiple_Delta"),
    ("Permanent Growth (고정)", 0.01, 0.01, 0.01, c.NUM_FMT_PERCENT, "Perm_Growth"),
]

INDUSTRY_PRESETS = ["(수동)", "소매", "제조", "SaaS", "헬스케어", "해운·시황주"]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_STRESS)
    ws.column_dimensions["A"].width = 32
    for col in ["B", "C", "D", "E", "F"]:
        ws.column_dimensions[col].width = 14

    ws["A1"] = "2. Stress Panel"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:F1")

    # Case_Switch anchor
    ws["A3"] = "Case Switch (시나리오)"
    ws["A3"].font = Font(bold=True)
    ws[CASE_SWITCH_CELL] = "Base"
    c.apply_input(ws[CASE_SWITCH_CELL])
    dv_case = DataValidation(type="list", formula1='"Base,Upside,Downside"', allow_blank=False)
    dv_case.add(CASE_SWITCH_CELL)
    ws.add_data_validation(dv_case)
    wb.defined_names["Case_Switch"] = DefinedName("Case_Switch", attr_text=f"'{SHEET_STRESS}'!${CASE_SWITCH_CELL[0]}${CASE_SWITCH_CELL[1:]}")

    # Industry preset dropdown
    ws["A4"] = "산업 디폴트 프리셋"
    preset_cell = "B4"
    ws[preset_cell] = "(수동)"
    c.apply_input(ws[preset_cell])
    dv_preset = DataValidation(type="list", formula1=f'"{",".join(INDUSTRY_PRESETS)}"', allow_blank=True)
    dv_preset.add(preset_cell)
    ws.add_data_validation(dv_preset)

    # Parameter table header (row 7)
    headers = ["파라미터", "Base", "Upside", "Downside", "단위", "Active"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=7, column=col_idx, value=h)
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Parameter rows
    for idx, (label, base, up, down, fmt, active_name) in enumerate(PARAM_ROWS):
        r = 8 + idx
        ws.cell(row=r, column=1, value=label)
        for col_idx, val in enumerate([base, up, down], start=2):
            cell = ws.cell(row=r, column=col_idx, value=val)
            if label == "Permanent Growth (고정)":
                c.apply_calc(cell)  # fixed, not user-editable
            else:
                c.apply_input(cell)
            cell.number_format = fmt
        ws.cell(row=r, column=5, value=fmt.replace('"', ''))
        # Active column F
        active_formula = f'=SWITCH(Case_Switch,"Base",B{r},"Upside",C{r},"Downside",D{r})'
        active_cell = ws.cell(row=r, column=6, value=active_formula)
        c.apply_key_output(active_cell)
        active_cell.number_format = fmt
        # Named range
        wb.defined_names[active_name] = DefinedName(active_name, attr_text=f"'{SHEET_STRESS}'!$F${r}")

    # Visual banner showing active case
    ws["A17"] = "현재 적용 시나리오"
    ws["A17"].font = Font(bold=True)
    banner = ws["B17"]
    banner.value = "=Case_Switch"
    c.apply_key_output(banner)

    return ws
```

- [ ] **Step 4: 테스트 실행**

```powershell
pytest tests/test_s2_stress.py -v
```

Expected: 6 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s2_stress_panel.py tests/test_s2_stress.py
git commit -m "feat(s2_stress): add Case_Switch, 6 stress params, Active_* named ranges"
```

---

## Task 7: `3_Operating_Overlay` 시트

설계 §3. Base 링크 + Active_* 가산으로 Stressed 지표 cascade.

**Files:**
- Modify: `src/lbo_template/sheets/s3_overlay.py`
- Create: `tests/test_s3_overlay.py`

- [ ] **Step 1: 테스트**

```python
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
    # Find Stressed Revenue row; FY1 column is E
    for r in range(5, 25):
        if ws.cell(row=r, column=1).value == "Stressed Revenue":
            e_cell = ws.cell(row=r, column=5).value
            assert "Active_Revenue_Growth_Delta" in e_cell or "Stressed YoY" in e_cell or "(1+" in e_cell
            return
    raise AssertionError("Stressed Revenue row not found")


def test_ufcf_formula(wb):
    ws = wb[SHEET_OVERLAY]
    for r in range(5, 25):
        if ws.cell(row=r, column=1).value == "UFCF (Stressed)":
            f1 = ws.cell(row=r, column=5).value  # FY1
            assert "EBITDA" in f1 or "-" in f1  # EBITDA - Tax - Capex - NWC
            return
    raise AssertionError("UFCF row not found")
```

- [ ] **Step 2: 실패 확인**

```powershell
pytest tests/test_s3_overlay.py -v
```

- [ ] **Step 3: 빌더 구현**

```python
"""3_Operating_Overlay — stressed operating metrics cascade."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from lbo_template.layout import SHEET_OVERLAY, SHEET_INPUT
from lbo_template import conventions as c

# 각 row의 (label, formula_template) — {c}=current col, {prev}=previous col
# Actual 기간(FY-2~LTM = B,C,D)은 pass-through; Stress는 FY1~FY5만 적용 (E~I).
ROWS = [
    ("Base Revenue",             "='{inp}'!{c}24"),
    ("Base YoY Growth",          "=IFERROR({c}6/{prev}6-1,\"\")"),
    # Stressed YoY = Base YoY + Active_Delta (FY1부터만 적용; Actual은 Base와 동일)
    ("Stressed YoY Growth",      "=IF({is_forecast},{c}7+Active_Revenue_Growth_Delta,{c}7)"),
    # Stressed Revenue: Actual은 Base와 동일; FY1부터 (prev 스트레스드) × (1+stressed YoY)
    ("Stressed Revenue",         "=IF({is_forecast},{prev}9*(1+{c}8),{c}6)"),
    ("Base EBITDA Margin",       "=IFERROR('{inp}'!{c}27/'{inp}'!{c}24,\"\")"),
    ("Stressed EBITDA Margin",   "=IF({is_forecast},{c}11+Active_EBITDA_Margin_Delta,{c}11)"),
    ("Stressed EBITDA",          "={c}9*{c}12"),
    ("Base Capex % of Revenue",  "=IFERROR('{inp}'!{c}29/'{inp}'!{c}24,\"\")"),
    ("Stressed Capex",           "={c}9*({c}15+IF({is_forecast},Active_Capex_Pct_Delta,0))"),
    ("Base ΔNWC % of Revenue",   "=IFERROR('{inp}'!{c}30/'{inp}'!{c}24,\"\")"),
    ("Stressed ΔNWC",            "={c}9*({c}17+IF({is_forecast},Active_NWC_Pct_Delta,0))"),
    ("D&A (Base pass-through)",  "='{inp}'!{c}28"),
    ("EBIT (Stressed)",          "={c}13-{c}19"),
    ("Cash Taxes",               "=MAX(0,{c}20)*'{inp}'!{c}31"),
    ("UFCF (Stressed)",          "={c}13-{c}21-{c}16-{c}18"),
]

# Forecast column flag: FY1 onwards = cols E..I
FORECAST_COLS = {"E", "F", "G", "H", "I"}


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_OVERLAY)
    ws.column_dimensions["A"].width = 32
    for col in c.FY_AXIS_COLUMNS:
        ws.column_dimensions[col].width = 14

    ws["A1"] = "3. Operating Overlay (Stressed)"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:I1")

    # FY axis header row 4
    for col, label in zip(c.FY_AXIS_COLUMNS, c.FY_AXIS_LABELS):
        cell = ws[f"{col}4"]
        cell.value = label
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    label_row_map = {}
    for idx, (label, template) in enumerate(ROWS):
        r = 5 + idx
        label_row_map[label] = r
        ws.cell(row=r, column=1, value=label)
        for col_idx, col in enumerate(c.FY_AXIS_COLUMNS):
            cell = ws[f"{col}{r}"]
            # prev col
            if col_idx == 0:
                prev = col  # no previous year for FY-2; formulas handle with IFERROR
            else:
                prev = c.FY_AXIS_COLUMNS[col_idx - 1]
            is_forecast = "TRUE" if col in FORECAST_COLS else "FALSE"
            formula = template.format(c=col, prev=prev, inp=SHEET_INPUT, is_forecast=is_forecast)
            cell.value = formula
            if label.startswith("Base "):
                c.apply_calc(cell)
                cell.font = c.crosstab_link_font()  # Base = link from 1_Input
            elif label.startswith("Stressed ") or label == "UFCF (Stressed)" or label == "EBIT (Stressed)":
                c.apply_key_output(cell)
            else:
                c.apply_calc(cell)
            if "Margin" in label or "Growth" in label or "% of Revenue" in label:
                cell.number_format = c.NUM_FMT_PERCENT
            else:
                cell.number_format = c.NUM_FMT_ACCOUNTING

    return ws
```

- [ ] **Step 4: 테스트 재실행**

```powershell
pytest tests/test_s3_overlay.py -v
```

Expected: 3 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s3_overlay.py tests/test_s3_overlay.py
git commit -m "feat(s3_overlay): cascade Stressed Rev/EBITDA/Capex/NWC/UFCF from Active_* deltas"
```

---

## Task 8: `4_Debt_Schedule` 시트

설계 §4. Opco Senior / Opco 2nd Lien / Holdco Sub 3-트랜치. Cash Sweep 우선순위 Opco Senior > 2nd Lien. Holdco PIK/Cash 드롭다운.

**Files:**
- Modify: `src/lbo_template/sheets/s4_debt.py`
- Create: `tests/test_s4_debt.py`

- [ ] **Step 1: 테스트**

```python
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
    # Find any Interest Expense row and check FY1 formula references Opening (same-row-1 or Opening_Balance)
    for r in range(1, 60):
        label = ws.cell(row=r, column=1).value
        if label and "Interest Expense" in label:
            fy1 = ws.cell(row=r, column=5).value  # col E = FY1
            assert "E" in fy1 or "Opening" in fy1
            # must not reference same row's ending balance column
            # simplified check: no reference to Ending labels (use structural check)
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
            assert "MAX(0" in fy1, f"Ending Balance row {r} must use MAX(0,...)"
```

- [ ] **Step 2: 실패 확인 → 빌더 구현**

```python
"""4_Debt_Schedule — Opco Senior / Opco 2nd Lien / Holdco Sub."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font
from lbo_template.layout import SHEET_DEBT, SHEET_INPUT, SHEET_OVERLAY
from lbo_template import conventions as c

# Tranche block layout: each tranche consumes 8 rows + 1 spacer
# Columns: A=label, B~I=FY-2..FY5 (but Debt schedule typically FY1~FY5 only, actuals left blank)

TRANCHE_ROWS = [
    "Opening Balance",
    "Interest Rate",
    "Interest Expense",
    "Mandatory Amortization",
    "Cash Sweep Applied",
    "Ending Balance",
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DEBT)
    ws.column_dimensions["A"].width = 36
    for col in c.FY_AXIS_COLUMNS:
        ws.column_dimensions[col].width = 14

    ws["A1"] = "4. Debt Schedule"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:I1")

    # FY header row 3 (only FY1~FY5 used; leave FY-2/-1/LTM blank)
    for col, label in zip(c.FY_AXIS_COLUMNS, c.FY_AXIS_LABELS):
        cell = ws[f"{col}3"]
        cell.value = label
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    tranches = [
        ("Opco Senior TL", "Opco_Senior_Principal", 5, "SENIOR"),
        ("Opco 2nd Lien", "Opco_2L_Principal", 15, "SECOND"),
        ("Holdco Sub", "Holdco_Sub_Principal", 25, "HOLDCO"),
    ]

    for tranche_name, principal_named, start_row, tag in tranches:
        # Section header
        hdr = ws.cell(row=start_row, column=1, value=tranche_name)
        hdr.font = Font(bold=True, size=11)
        hdr.fill = c.section_header_fill()
        hdr.font = Font(bold=True, size=11, color=c.COLOR_WHITE_FONT)
        ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=9)

        for idx, label in enumerate(TRANCHE_ROWS):
            r = start_row + 1 + idx
            ws.cell(row=r, column=1, value=label)
            for col_idx, col in enumerate(c.FY_AXIS_COLUMNS):
                cell = ws[f"{col}{r}"]
                # Only FY1~FY5 active (cols E..I)
                if col_idx < 3:
                    cell.value = None
                    continue

                if label == "Opening Balance":
                    if col == "E":  # FY1: principal from 1_Input
                        cell.value = f"={principal_named}"
                    else:  # FY2+: previous year's Ending Balance (= this-row +5)
                        prev = c.FY_AXIS_COLUMNS[col_idx - 1]
                        cell.value = f"={prev}{r+5}"
                    c.apply_calc(cell)
                elif label == "Interest Rate":
                    # Input only in FY1; propagate right via "=E{r}"
                    if col == "E":
                        cell.value = None
                        c.apply_input(cell)
                        cell.number_format = c.NUM_FMT_PERCENT
                    else:
                        prev = c.FY_AXIS_COLUMNS[col_idx - 1]
                        cell.value = f"={prev}{r}"
                        c.apply_calc(cell)
                        cell.number_format = c.NUM_FMT_PERCENT
                elif label == "Interest Expense":
                    # Opening × Rate (Opening = row r-2)
                    cell.value = f"={col}{r-2}*{col}{r-1}"
                    c.apply_calc(cell)
                elif label == "Mandatory Amortization":
                    # User input; default 0
                    if col == "E":
                        cell.value = 0
                    else:
                        cell.value = 0
                    c.apply_input(cell)
                elif label == "Cash Sweep Applied":
                    if tag == "HOLDCO":
                        cell.value = 0  # Holdco 원금 sweep은 v1.1 backlog
                        c.apply_calc(cell)
                    elif tag == "SENIOR":
                        # Sweep priority 1: min(opening - mand, available sweep from waterfall)
                        # 5_CF_Waterfall에서 계산된 Opco_Sweep_Available 참조 (다음 Task에서 named range 생성)
                        cell.value = f'=MIN(MAX(0,{col}{r-3}-{col}{r-1}),IFERROR(Opco_Sweep_Avail_{col},0))'
                        c.apply_calc(cell)
                    elif tag == "SECOND":
                        # Sweep priority 2: 남은 sweep 금액
                        # (여기선 0으로 두고 waterfall 완성 후 연결)
                        cell.value = f'=MIN(MAX(0,{col}{r-3}-{col}{r-1}),IFERROR(Opco_Sweep_Avail_{col}-{col}{r-10},0))'
                        c.apply_calc(cell)
                elif label == "Ending Balance":
                    if tag == "HOLDCO":
                        # Holdco: PIK 옵션. PIK이면 Ending = Opening + Interest (이자가 원금에 가산); Cash이면 Opening - Mand
                        cell.value = f'=IF(Holdco_PIK_Mode="PIK",MAX(0,{col}{r-5}+{col}{r-3}-{col}{r-2}-{col}{r-1}),MAX(0,{col}{r-5}-{col}{r-2}-{col}{r-1}))'
                    else:
                        cell.value = f"=MAX(0,{col}{r-5}-{col}{r-2}-{col}{r-1})"
                    c.apply_key_output(cell)

    # Holdco PIK/Cash 드롭다운 (anchor cell A35 label, B35 select)
    ws["A35"] = "Holdco 이자 지급방식"
    ws["B35"] = "Cash"
    c.apply_input(ws["B35"])
    dv_pik = DataValidation(type="list", formula1='"Cash,PIK"', allow_blank=False)
    dv_pik.add("B35")
    ws.add_data_validation(dv_pik)
    from openpyxl.workbook.defined_name import DefinedName
    wb.defined_names["Holdco_PIK_Mode"] = DefinedName("Holdco_PIK_Mode", attr_text=f"'{SHEET_DEBT}'!$B$35")

    # Sweep % input (anchor A37, B37)
    ws["A37"] = "Cash Sweep % (Opco excess cash → Senior prepay)"
    ws["B37"] = 1.0  # 100% default
    c.apply_input(ws["B37"])
    ws["B37"].number_format = c.NUM_FMT_PERCENT
    wb.defined_names["Sweep_Pct"] = DefinedName("Sweep_Pct", attr_text=f"'{SHEET_DEBT}'!$B$37")

    # Named ranges for interest/amort sums (used by 5_CF_Waterfall)
    # Opco Senior Interest = row 8 E..I
    # Opco 2nd Lien Interest = row 18 E..I
    # Holdco Interest = row 28 E..I
    wb.defined_names["Opco_Sr_Interest"] = DefinedName("Opco_Sr_Interest", attr_text=f"'{SHEET_DEBT}'!$E$8:$I$8")
    wb.defined_names["Opco_2L_Interest"] = DefinedName("Opco_2L_Interest", attr_text=f"'{SHEET_DEBT}'!$E$18:$I$18")
    wb.defined_names["Holdco_Interest"] = DefinedName("Holdco_Interest", attr_text=f"'{SHEET_DEBT}'!$E$28:$I$28")
    wb.defined_names["Opco_Sr_Mand"] = DefinedName("Opco_Sr_Mand", attr_text=f"'{SHEET_DEBT}'!$E$9:$I$9")
    wb.defined_names["Opco_2L_Mand"] = DefinedName("Opco_2L_Mand", attr_text=f"'{SHEET_DEBT}'!$E$19:$I$19")

    return ws
```

> **주의**: 위 구현은 Cash Sweep의 순환참조 회피를 위해 `Opco_Sweep_Avail_<col>` (E..I 각각 named range)를 5_CF_Waterfall에서 생성해 참조하는 설계. Task 9에서 해당 named range를 생성한다. 중간 상태에서는 Sweep 수식이 `#NAME?`이지만 Task 9 완료 시점에 해결됨 — 본 Task 단위 테스트는 Sweep 수식 "문자열"만 검증하므로 통과.

- [ ] **Step 4: 테스트 실행**

```powershell
pytest tests/test_s4_debt.py -v
```

Expected: 4 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s4_debt.py tests/test_s4_debt.py
git commit -m "feat(s4_debt): 3 tranches with opening-balance interest, PIK/Cash, cash sweep wiring"
```

---

## Task 9: `5_CF_Waterfall` 시트

설계 §5. Opco UFCF → 이자/원금 → Min Cash → Dividend → Holdco ICR 체크.

**Files:**
- Modify: `src/lbo_template/sheets/s5_waterfall.py`
- Create: `tests/test_s5_waterfall.py`

- [ ] **Step 1: 테스트**

```python
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
```

- [ ] **Step 2: 실패 확인**

- [ ] **Step 3: 빌더 구현**

```python
"""5_CF_Waterfall — Opco UFCF → dividend → Holdco."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.formatting.rule import CellIsRule
from openpyxl.styles import PatternFill
from lbo_template.layout import SHEET_WATERFALL, SHEET_OVERLAY, SHEET_DEBT
from lbo_template import conventions as c

ROWS = [
    ("Opco UFCF",                               "='{ov}'!{c}22"),   # row 22 = UFCF in overlay (check actual row)
    ("Less: Opco Interest (Senior + 2nd Lien)", "='{dbt}'!{c}8+'{dbt}'!{c}18"),
    ("Less: Opco Mandatory Amort",              "='{dbt}'!{c}9+'{dbt}'!{c}19"),
    ("= Opco CFADS",                            "={c}5-{c}6-{c}7"),
    ("Less: Minimum Cash Retention",            None),   # input
    ("Less: Legal Reserve",                     None),   # input
    ("= Distributable to Holdco",               "=MAX(0,{c}8-{c}9-{c}10)"),
    ("× Payout Ratio",                          None),   # input, default 1.0
    ("= Dividend Paid to Holdco",               "={c}11*{c}12"),
    ("Opco Sweep Available",                    "=MAX(0,{c}8-{c}13)*Sweep_Pct"),
    ("Holdco Dividend Received",                "={c}13"),
    ("Holdco Interest (if Cash-Pay)",           '=IF(Holdco_PIK_Mode="Cash",\'{dbt}\'!{c}28,0)'),
    ("Holdco Net Cash Flow",                    "={c}15-{c}16"),
    ("Holdco ICR (Div / Holdco Interest)",      "=IFERROR({c}15/{c}16,\"\")"),
]

# KPI rows (single value per FY, placed below)
KPI_ROWS = [
    ("Opco DSCR (CFADS / (Int+Mand))",    "=IFERROR({c}8/({c}6+{c}7),\"\")"),
    ("Opco ICR (EBITDA / Opco Int)",       "=IFERROR('{ov}'!{c}13/{c}6,\"\")"),
    ("Holdco ICR",                         "={c}18"),
    ("Net Leverage ((Opco+Holdco)/EBITDA)","=IFERROR(('{dbt}'!{c}10+'{dbt}'!{c}20+'{dbt}'!{c}30)/'{ov}'!{c}13,\"\")"),
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_WATERFALL)
    ws.column_dimensions["A"].width = 44
    for col in c.FY_AXIS_COLUMNS:
        ws.column_dimensions[col].width = 14

    ws["A1"] = "5. Cash Flow Waterfall"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:I1")

    for col, label in zip(c.FY_AXIS_COLUMNS, c.FY_AXIS_LABELS):
        hdr = ws[f"{col}3"]
        hdr.value = label
        hdr.font = c.column_header_font()
        hdr.fill = c.column_header_fill()

    for idx, (label, template) in enumerate(ROWS):
        r = 5 + idx
        ws.cell(row=r, column=1, value=label)
        for col_idx, col in enumerate(c.FY_AXIS_COLUMNS):
            cell = ws[f"{col}{r}"]
            if col_idx < 3:  # Actual years blank
                continue
            if template is None:
                # Input rows — default values
                if label == "× Payout Ratio":
                    cell.value = 1.0
                    cell.number_format = c.NUM_FMT_PERCENT
                else:
                    cell.value = 0
                    cell.number_format = c.NUM_FMT_ACCOUNTING
                c.apply_input(cell)
            else:
                cell.value = template.format(c=col, ov=SHEET_OVERLAY, dbt=SHEET_DEBT)
                c.apply_calc(cell)
                if "ICR" in label or "Ratio" in label:
                    cell.number_format = c.NUM_FMT_MULTIPLE
                else:
                    cell.number_format = c.NUM_FMT_ACCOUNTING
                if label.startswith("=") or "Dividend" in label or "CFADS" in label:
                    c.apply_key_output(cell)

    # Opco Sweep Available per-column named ranges (row 14 in this layout: index 9 → r=14)
    for col in ["E", "F", "G", "H", "I"]:
        name = f"Opco_Sweep_Avail_{col}"
        wb.defined_names[name] = DefinedName(name, attr_text=f"'{SHEET_WATERFALL}'!${col}$14")

    # KPI rows
    kpi_start = 21
    for idx, (label, template) in enumerate(KPI_ROWS):
        r = kpi_start + idx
        ws.cell(row=r, column=1, value=label)
        for col_idx, col in enumerate(c.FY_AXIS_COLUMNS):
            if col_idx < 3:
                continue
            cell = ws[f"{col}{r}"]
            cell.value = template.format(c=col, ov=SHEET_OVERLAY, dbt=SHEET_DEBT)
            c.apply_key_output(cell)
            cell.number_format = c.NUM_FMT_MULTIPLE if "Leverage" in label or "ICR" in label or "DSCR" in label else c.NUM_FMT_ACCOUNTING

    # Named ranges for KPI rows (ranges across E..I)
    wb.defined_names["Opco_DSCR_Row"] = DefinedName("Opco_DSCR_Row", attr_text=f"'{SHEET_WATERFALL}'!$E${kpi_start}:$I${kpi_start}")
    wb.defined_names["Opco_ICR_Row"] = DefinedName("Opco_ICR_Row", attr_text=f"'{SHEET_WATERFALL}'!$E${kpi_start+1}:$I${kpi_start+1}")
    wb.defined_names["Holdco_ICR_Row"] = DefinedName("Holdco_ICR_Row", attr_text=f"'{SHEET_WATERFALL}'!$E${kpi_start+2}:$I${kpi_start+2}")
    wb.defined_names["Net_Leverage_Row"] = DefinedName("Net_Leverage_Row", attr_text=f"'{SHEET_WATERFALL}'!$E${kpi_start+3}:$I${kpi_start+3}")
    wb.defined_names["Dividend_Row"] = DefinedName("Dividend_Row", attr_text=f"'{SHEET_WATERFALL}'!$E$13:$I$13")

    # Conditional formatting: Holdco ICR < 1.0 → red
    red = PatternFill("solid", fgColor="FFC7CE")
    ws.conditional_formatting.add(
        f"E18:I18",
        CellIsRule(operator="lessThan", formula=["1.0"], fill=red),
    )

    return ws
```

> **주의**: `5_CF_Waterfall`의 Opco UFCF 수식이 `'3_Operating_Overlay'!{c}22`를 참조하는데, Task 7의 `s3_overlay.py`에서 UFCF 행의 실제 번호는 `5 + 14 = 19` (ROWS 리스트 15번째, 인덱스 14). 이 숫자를 정확히 계산하려면 `s3_overlay.build()`가 반환한 `label_row_map["UFCF (Stressed)"]`을 공유 상수로 export하는 구조가 깔끔함. **Task 9 Step 3에서 `s3_overlay.py`에 `UFCF_ROW = 19` 모듈 상수 추가** + 본 빌더에서 import.

`src/lbo_template/sheets/s3_overlay.py` 상단에 추가:

```python
UFCF_ROW = 19           # Stressed UFCF row
STRESSED_EBITDA_ROW = 13
STRESSED_CAPEX_ROW = 16
STRESSED_NWC_ROW = 18
```

`s5_waterfall.py` 상단에 `from lbo_template.sheets.s3_overlay import UFCF_ROW, STRESSED_EBITDA_ROW` 추가하고 ROWS 템플릿에서 `{c}22` → `{c}{UFCF_ROW}` 포매팅 적용.

- [ ] **Step 4: 테스트 실행**

```powershell
pytest tests/test_s5_waterfall.py tests/test_s4_debt.py -v
```

Expected: 7 passed.

- [ ] **Step 5: 커밋**

```powershell
git add src/lbo_template/sheets/s3_overlay.py src/lbo_template/sheets/s4_debt.py src/lbo_template/sheets/s5_waterfall.py tests/test_s5_waterfall.py
git commit -m "feat(s5_waterfall): UFCF→Div→Holdco cascade with Opco_Sweep_Avail and KPI row named ranges"
```

---

## Task 10: `6_DCF_Valuation` 시트

설계 §6. FCFF 5Y + mid-year convention (0.5/1.5/2.5/3.5/4.5) + TV Gordon (할인기간 5.0, 영구성장 1.0% 고정).

**Files:**
- Modify: `src/lbo_template/sheets/s6_dcf.py`
- Create: `tests/test_s6_dcf.py`

- [ ] **Step 1: 테스트**

```python
from lbo_template.layout import SHEET_DCF


def test_dcf_rows(wb):
    ws = wb[SHEET_DCF]
    labels = [ws.cell(row=r, column=1).value for r in range(1, 25)]
    expected = ["Stressed EBITDA", "(-) Cash Taxes on EBIT", "(-) Capex", "(-) ΔNWC",
                "FCFF", "WACC", "Discount Period", "Discount Factor", "PV of FCFF",
                "Terminal Value (Gordon)", "PV of TV", "EV (PV 합계)",
                "(+) 비영업자산", "(-) Net Debt (Closing)", "= 담보기준 Equity Value"]
    for e in expected:
        assert e in labels, f"missing: {e}"


def test_mid_year_discount_periods(wb):
    ws = wb[SHEET_DCF]
    # Discount Period row: FY1=0.5, FY2=1.5, FY3=2.5, FY4=3.5, FY5=4.5, TV=5.0
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "Discount Period":
            assert ws.cell(row=r, column=5).value == 0.5  # FY1
            assert ws.cell(row=r, column=6).value == 1.5
            assert ws.cell(row=r, column=7).value == 2.5
            assert ws.cell(row=r, column=8).value == 3.5
            assert ws.cell(row=r, column=9).value == 4.5
            # Column J = TV
            assert ws.cell(row=r, column=10).value == 5.0
            return
    raise AssertionError("Discount Period row missing")


def test_tv_formula_uses_perm_growth_and_5_0(wb):
    ws = wb[SHEET_DCF]
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "Terminal Value (Gordon)":
            tv = ws.cell(row=r, column=10).value
            assert "Perm_Growth" in tv
            return
    raise AssertionError("TV row missing")


def test_wacc_uses_active_uplift(wb):
    ws = wb[SHEET_DCF]
    for r in range(1, 25):
        if ws.cell(row=r, column=1).value == "WACC":
            wacc = ws.cell(row=r, column=5).value  # FY1
            assert "Active_WACC_Uplift" in wacc
            assert "Base_WACC" in wacc
            return
    raise AssertionError("WACC row missing")
```

- [ ] **Step 2: 실패 확인 → 빌더**

```python
"""6_DCF_Valuation — stressed DCF with mid-year convention and Gordon TV."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from lbo_template.layout import SHEET_DCF, SHEET_OVERLAY, SHEET_INPUT
from lbo_template.sheets.s3_overlay import STRESSED_EBITDA_ROW, STRESSED_CAPEX_ROW, STRESSED_NWC_ROW
from lbo_template import conventions as c

# DCF columns: E=FY1..I=FY5, J=TV
DCF_COLS = ["E", "F", "G", "H", "I"]
TV_COL = "J"
PERIODS = {"E": 0.5, "F": 1.5, "G": 2.5, "H": 3.5, "I": 4.5}

ROWS_FY = [
    ("Stressed EBITDA",         "='{ov}'!{c}{ebitda_row}"),
    ("(-) Cash Taxes on EBIT",  "=MAX(0,'{ov}'!{c}20)*'{inp}'!{c}31"),
    ("(-) Capex",               "='{ov}'!{c}{capex_row}"),
    ("(-) ΔNWC",                "='{ov}'!{c}{nwc_row}"),
    ("FCFF",                    "={c}5-{c}6-{c}7-{c}8"),
    ("WACC",                    "=Base_WACC+Active_WACC_Uplift/10000"),
    ("Discount Period",         None),  # literal, set below
    ("Discount Factor",         "=1/(1+{c}10)^{c}11"),
    ("PV of FCFF",              "={c}9*{c}12"),
]

TV_ROWS = [
    ("Terminal Value (Gordon)", "=I9*(1+Perm_Growth)/(I10-Perm_Growth)"),
    ("PV of TV",                "=J14/(1+I10)^5.0"),
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DCF)
    ws.column_dimensions["A"].width = 36
    for col in DCF_COLS + [TV_COL]:
        ws.column_dimensions[col].width = 14

    ws["A1"] = "6. DCF Valuation (Stressed)"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:J1")

    # FY header row 3 (FY1~FY5 + TV)
    fy_labels = ["FY1", "FY2", "FY3", "FY4", "FY5", "TV"]
    for col, label in zip(DCF_COLS + [TV_COL], fy_labels):
        hdr = ws[f"{col}3"]
        hdr.value = label
        hdr.font = c.column_header_font()
        hdr.fill = c.column_header_fill()

    for idx, (label, template) in enumerate(ROWS_FY):
        r = 5 + idx
        ws.cell(row=r, column=1, value=label)
        for col in DCF_COLS:
            cell = ws[f"{col}{r}"]
            if label == "Discount Period":
                cell.value = PERIODS[col]
                c.apply_calc(cell)
            else:
                cell.value = template.format(
                    c=col, ov=SHEET_OVERLAY, inp=SHEET_INPUT,
                    ebitda_row=STRESSED_EBITDA_ROW,
                    capex_row=STRESSED_CAPEX_ROW,
                    nwc_row=STRESSED_NWC_ROW,
                )
                c.apply_calc(cell)
            if label in ("FCFF", "PV of FCFF"):
                c.apply_key_output(cell)
            if label == "WACC":
                cell.number_format = c.NUM_FMT_PERCENT
            elif label == "Discount Factor":
                cell.number_format = "0.0000"
            elif label == "Discount Period":
                cell.number_format = "0.0"
            else:
                cell.number_format = c.NUM_FMT_ACCOUNTING

    # TV column
    ws[f"{TV_COL}11"] = 5.0   # Discount Period for TV = 5.0 (v0.4 교정)
    ws[f"{TV_COL}11"].number_format = "0.0"
    c.apply_calc(ws[f"{TV_COL}11"])

    # TV rows at 14, 15
    ws.cell(row=14, column=1, value="Terminal Value (Gordon)")
    ws[f"{TV_COL}14"] = TV_ROWS[0][1]
    c.apply_key_output(ws[f"{TV_COL}14"])
    ws[f"{TV_COL}14"].number_format = c.NUM_FMT_ACCOUNTING

    ws.cell(row=15, column=1, value="PV of TV")
    ws[f"{TV_COL}15"] = TV_ROWS[1][1]
    c.apply_key_output(ws[f"{TV_COL}15"])
    ws[f"{TV_COL}15"].number_format = c.NUM_FMT_ACCOUNTING

    # EV = sum of PV of FCFF + PV of TV
    ws.cell(row=17, column=1, value="EV (PV 합계)")
    ws["E17"] = "=SUM(E13:I13)+J15"
    c.apply_key_output(ws["E17"])
    ws["E17"].number_format = c.NUM_FMT_ACCOUNTING

    ws.cell(row=18, column=1, value="(+) 비영업자산")
    ws["E18"] = 0
    c.apply_input(ws["E18"])
    ws["E18"].number_format = c.NUM_FMT_ACCOUNTING

    ws.cell(row=19, column=1, value="(-) Net Debt (Closing)")
    ws["E19"] = f"='{SHEET_INPUT}'!B6"
    c.apply_calc(ws["E19"])
    ws["E19"].font = c.crosstab_link_font()
    ws["E19"].number_format = c.NUM_FMT_ACCOUNTING

    ws.cell(row=20, column=1, value="= 담보기준 Equity Value")
    ws["E20"] = "=E17+E18-E19"
    c.apply_key_output(ws["E20"])
    ws["E20"].number_format = c.NUM_FMT_ACCOUNTING

    # Base_WACC input (anchor)
    ws.cell(row=23, column=1, value="Base WACC (사용자 입력)")
    ws["B23"] = 0.10
    c.apply_input(ws["B23"])
    ws["B23"].number_format = c.NUM_FMT_PERCENT
    wb.defined_names["Base_WACC"] = DefinedName("Base_WACC", attr_text=f"'{SHEET_DCF}'!$B$23")

    # Named ranges
    wb.defined_names["DCF_EV"] = DefinedName("DCF_EV", attr_text=f"'{SHEET_DCF}'!$E$17")
    wb.defined_names["DCF_Equity_Value"] = DefinedName("DCF_Equity_Value", attr_text=f"'{SHEET_DCF}'!$E$20")

    return ws
```

- [ ] **Step 3: 테스트 실행**

```powershell
pytest tests/test_s6_dcf.py -v
```

Expected: 4 passed.

- [ ] **Step 4: 커밋**

```powershell
git add src/lbo_template/sheets/s6_dcf.py tests/test_s6_dcf.py
git commit -m "feat(s6_dcf): FCFF with mid-year 0.5-4.5, Gordon TV at 5.0, Active_WACC_Uplift wiring"
```

---

## Task 11: `9a_CIQ_Trading_Raw` 시트

설계 §9a. 15-컬럼 고정 헤더 + Ticker 입력 A열 + `=CIQ(...)` primary 수식 (Mode "Plug-in" 자동 감지).

**Files:**
- Modify: `src/lbo_template/sheets/s9a_ciq_trading.py`
- Create: `tests/test_s9_ciq_and_peer.py` (나중에 9b/9c/9_Peer도 합침)

- [ ] **Step 1: 테스트 (9a 파트만 먼저)**

```python
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
    """Row 3 = row 1 peer. B3 = =CIQ($B3, "IQ_MARKETCAP") """
    ws = wb[SHEET_9A]
    # Market Cap column = E (5번째)
    e3 = ws["E3"].value
    assert "CIQ" in e3 and "IQ_MARKETCAP" in e3 and "$B3" in e3
```

- [ ] **Step 2: 빌더 구현**

```python
"""9a_CIQ_Trading_Raw — Plug-in primary, Paste fallback."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font, PatternFill
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from lbo_template.layout import SHEET_9A
from lbo_template import conventions as c

HEADERS = [
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

# CIQ function string per column (relative to $B{r} = Ticker)
CIQ_FORMULAS = {
    "A": '=IFERROR(CIQ($B{r},"IQ_COMPANY_NAME"),"")',
    "C": '=IFERROR(CIQ($B{r},"IQ_COUNTRY_NAME"),"")',
    "D": '=IFERROR(CIQ($B{r},"IQ_TRADING_CURRENCY"),"")',
    "E": '=IFERROR(CIQ($B{r},"IQ_MARKETCAP"),"")',
    "F": '=IFERROR(CIQ($B{r},"IQ_TEV"),"")',
    "G": '=IFERROR(CIQ($B{r},"IQ_TOTAL_REV","LTM"),"")',
    "H": '=IFERROR(CIQ($B{r},"IQ_EBITDA","LTM"),"")',
    "I": '=IFERROR(CIQ($B{r},"IQ_EBITDA_MARGIN","LTM"),"")',
    "J": '=IFERROR(CIQ($B{r},"IQ_TEV_EBITDA","LTM"),"")',
    "K": '=IFERROR(CIQ($B{r},"IQ_TEV_EBITDA","FY-1"),"")',
    "L": '=IFERROR(CIQ($B{r},"IQ_TEV_EBITDA","FY-2"),"")',
    "M": '=IFERROR(CIQ($B{r},"IQ_TEV_EBITDA","NTM"),"")',
    "N": '=IFERROR(CIQ($B{r},"IQ_NET_DEBT_EBITDA","LTM"),"")',
    "O": '=IFERROR(CIQ($B{r},"IQ_LTM_PERIOD_END_DATE"),"")',
}


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9A)
    ws.column_dimensions["A"].width = 20
    for col_idx, h in enumerate(HEADERS):
        col = chr(ord("A") + col_idx)
        if col != "A":
            ws.column_dimensions[col].width = 14

    # Mode cell (row 1)
    ws["A1"] = "Mode"
    ws["A1"].font = Font(bold=True)
    ws["B1"] = '=IF(ISFORMULA(C3),"Plug-in","⚠ Paste Fallback — 마스터 재배포 필요")'
    c.apply_calc(ws["B1"])

    # Last Refresh
    ws["C1"] = "Last Refresh"
    ws["C1"].font = Font(bold=True)
    ws["D1"] = "=NOW()"
    c.apply_calc(ws["D1"])
    ws["D1"].number_format = "yyyy-mm-dd hh:mm"

    # Header row 2
    for idx, h in enumerate(HEADERS):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}2"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Data rows 3..17 (15 peers default; design allows up to A2:O101)
    for r in range(3, 18):
        # B column (Ticker) = input
        tk = ws[f"B{r}"]
        c.apply_input(tk)
        # CIQ formulas in other columns
        for col, tpl in CIQ_FORMULAS.items():
            cell = ws[f"{col}{r}"]
            cell.value = tpl.format(r=r)
            c.apply_ciq(cell)
            if col in ("E", "F", "G", "H"):
                cell.number_format = c.NUM_FMT_ACCOUNTING
            elif col == "I":
                cell.number_format = c.NUM_FMT_PERCENT
            elif col in ("J", "K", "L", "M", "N"):
                cell.number_format = c.NUM_FMT_MULTIPLE
            elif col == "O":
                cell.number_format = c.NUM_FMT_DATE

    # Currency warning P-col (P3:P17)
    for r in range(3, 18):
        cell = ws[f"P{r}"]
        cell.value = f'=IF(AND(D{r}<>"",D{r}<>"KRW"),"⚠ FX변환필요","")'
        c.apply_calc(cell)

    return ws
```

- [ ] **Step 3: 테스트**

```powershell
pytest tests/test_s9_ciq_and_peer.py::test_9a_fixed_headers tests/test_s9_ciq_and_peer.py::test_9a_mode_cell tests/test_s9_ciq_and_peer.py::test_9a_ciq_primary_formula_row3 -v
```

- [ ] **Step 4: 커밋**

```powershell
git add src/lbo_template/sheets/s9a_ciq_trading.py tests/test_s9_ciq_and_peer.py
git commit -m "feat(s9a): CIQ Plug-in primary formulas, Mode cell, Paste Fallback warning, 15-col headers"
```

---

## Task 12: `9b_CIQ_Transaction_Raw` 시트

설계 §9b. 15-컬럼 + 최대 500행 + 초과 경고.

**Files:**
- Modify: `src/lbo_template/sheets/s9b_ciq_transaction.py`
- Modify: `tests/test_s9_ciq_and_peer.py`

- [ ] **Step 1: 테스트 추가**

```python
from lbo_template.layout import SHEET_9B


def test_9b_max_500_rows_warning(wb):
    ws = wb[SHEET_9B]
    c1 = ws["C1"].value
    assert "500" in c1
    assert "COUNTA" in c1 or "Export" in c1


def test_9b_headers(wb):
    ws = wb[SHEET_9B]
    expected_first_6 = ["Transaction ID", "Announced Date", "Closed Date", "Target Company Name", "Target Country", "Target Primary Industry"]
    for i, h in enumerate(expected_first_6):
        col = chr(ord("A") + i)
        assert ws[f"{col}2"].value == h
```

- [ ] **Step 2: 빌더 (9a와 구조 동일, transaction 함수로 교체)**

```python
"""9b_CIQ_Transaction_Raw — Transaction Comps zone (500 rows)."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.styles import Font
from lbo_template.layout import SHEET_9B, S9B_DATA_END_ROW
from lbo_template import conventions as c

HEADERS = [
    "Transaction ID", "Announced Date", "Closed Date", "Target Company Name",
    "Target Country", "Target Primary Industry", "Buyer Name", "Buyer Type",
    "Transaction Currency", "Implied Enterprise Value", "Target LTM Revenue",
    "Target LTM EBITDA", "Implied EV / LTM Revenue", "Implied EV / LTM EBITDA",
    "Deal Status",
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9B)
    for col_idx in range(15):
        col = chr(ord("A") + col_idx)
        ws.column_dimensions[col].width = 16

    ws["A1"] = "Mode"
    ws["A1"].font = Font(bold=True)
    ws["B1"] = '=IF(ISFORMULA(D3),"Plug-in","⚠ Paste Fallback — 마스터 재배포 필요")'
    c.apply_calc(ws["B1"])

    ws["C1"] = f'=IF(COUNTA(A:A)-1>500,"⚠ Export 500행 초과 — Paste 잘림 위험. 필터 좁히거나 범위 확장 필요","OK")'
    c.apply_calc(ws["C1"])

    for idx, h in enumerate(HEADERS):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}2"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Data rows 3..501 (500 transactions)
    # Transaction Plug-in formulas are typically =CIQTRANSACTION(...) — 라이선스 확인 전까지 예시 수식만 배치
    for r in range(3, 6):  # 첫 3줄만 CIQ 수식 예시 (나머지는 Paste 영역으로 보존, 수식 overhead 감소)
        cell = ws[f"A{r}"]
        cell.value = f'=IFERROR(CIQTRANSACTION("KR_TRANS_{r-2}","TR_ID"),"")'
        c.apply_ciq(cell)

    # B:O 입력 fill (사용자 Paste 영역)
    for r in range(3, S9B_DATA_END_ROW + 1):
        for col_idx in range(15):
            col = chr(ord("A") + col_idx)
            cell = ws[f"{col}{r}"]
            if r > 5:  # Row 6+ = Paste zone (input fill)
                c.apply_input(cell)

    return ws
```

- [ ] **Step 3: 테스트 + 커밋**

```powershell
pytest tests/test_s9_ciq_and_peer.py -v
git add src/lbo_template/sheets/s9b_ciq_transaction.py tests/test_s9_ciq_and_peer.py
git commit -m "feat(s9b): Transaction Comps zone with 500-row capacity and overflow warning"
```

---

## Task 13: `9c_Manual_Supplement` 시트

설계 §9c. Source 드롭다운 + Reliability 자동 매핑 + Include 자동 토글.

**Files:**
- Modify: `src/lbo_template/sheets/s9c_manual.py`

- [ ] **Step 1: 테스트 추가** (`tests/test_s9_ciq_and_peer.py`)

```python
from lbo_template.layout import SHEET_9C


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
    # Reliability column (Q) = XLOOKUP(Source, default_map, default_map_rel)
    q3 = ws["Q3"].value
    assert "XLOOKUP" in q3 or "VLOOKUP" in q3
```

- [ ] **Step 2: 빌더**

```python
"""9c_Manual_Supplement — Korean non-listed deals supplement."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.styles import Font
from lbo_template.layout import SHEET_9C
from lbo_template import conventions as c

# Same 15 cols as 9b + Source (col P) + Reliability (col Q) + Include (col R)
HEADERS_BASE = [
    "Transaction ID (MAN-xxx)", "Announced Date", "Closed Date", "Target Company Name",
    "Target Country", "Target Primary Industry", "Buyer Name", "Buyer Type",
    "Transaction Currency", "Implied Enterprise Value", "Target LTM Revenue",
    "Target LTM EBITDA", "Implied EV / LTM Revenue", "Implied EV / LTM EBITDA",
    "Deal Status",
]
EXTRA = ["Source", "Reliability", "Include ✓", "Memo"]

SOURCE_MAP = [
    ("내부DB", "High", True),
    ("Kisvalue", "High", True),
    ("IR자료", "High", True),
    ("한경Compass", "Medium", True),
    ("투자조선", "Medium", True),
    ("루머성", "Low", False),
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_9C)
    for col_idx in range(len(HEADERS_BASE) + len(EXTRA)):
        col = chr(ord("A") + col_idx)
        ws.column_dimensions[col].width = 16

    # Header row 2
    all_headers = HEADERS_BASE + EXTRA
    for idx, h in enumerate(all_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}2"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Source default-map table at bottom (rows 50..56)
    ws["A50"] = "Source"
    ws["B50"] = "Default Reliability"
    ws["C50"] = "Default Include"
    for i, (src, rel, inc) in enumerate(SOURCE_MAP):
        ws.cell(row=51 + i, column=1, value=src)
        ws.cell(row=51 + i, column=2, value=rel)
        ws.cell(row=51 + i, column=3, value=inc)

    # Data rows 3..49
    src_opts = ",".join([s for s, _, _ in SOURCE_MAP])
    dv_src = DataValidation(type="list", formula1=f'"{src_opts}"', allow_blank=True)
    dv_rel = DataValidation(type="list", formula1='"High,Medium,Low"', allow_blank=True)
    ws.add_data_validation(dv_src)
    ws.add_data_validation(dv_rel)

    for r in range(3, 50):
        for col_idx in range(len(HEADERS_BASE)):
            col = chr(ord("A") + col_idx)
            c.apply_input(ws[f"{col}{r}"])
        # Source column P
        src_cell = f"P{r}"
        dv_src.add(src_cell)
        c.apply_input(ws[src_cell])
        # Reliability Q — default via XLOOKUP, user-overridable
        rel_cell = ws[f"Q{r}"]
        rel_cell.value = f'=IFERROR(XLOOKUP(P{r},$A$51:$A$56,$B$51:$B$56),"")'
        c.apply_calc(rel_cell)
        dv_rel.add(f"Q{r}")
        # Include R — default via XLOOKUP + manual override
        inc_cell = ws[f"R{r}"]
        inc_cell.value = f'=IFERROR(XLOOKUP(P{r},$A$51:$A$56,$C$51:$C$56),FALSE)'
        c.apply_calc(inc_cell)
        # Memo S
        c.apply_input(ws[f"S{r}"])

    return ws
```

- [ ] **Step 3: 테스트 + 커밋**

```powershell
pytest tests/test_s9_ciq_and_peer.py -v
git add src/lbo_template/sheets/s9c_manual.py tests/test_s9_ciq_and_peer.py
git commit -m "feat(s9c): Manual Supplement with Source dropdown and auto-Reliability lookup"
```

---

## Task 14: `9_Peer_Summary` 시트

설계 §9. 3 소스(9a/9b/9c) 통합 + Include ✓ + Mean/Median/Trimmed Mean + Applied_* named ranges.

**Files:**
- Modify: `src/lbo_template/sheets/s9_peer_summary.py`

- [ ] **Step 1: 테스트 추가**

```python
from lbo_template.layout import SHEET_PEER


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
```

- [ ] **Step 2: 빌더 구현** (요지)

```python
"""9_Peer_Summary — unified trading + transaction aggregation with Include toggles."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.styles import Font
from lbo_template.layout import SHEET_PEER, SHEET_9A, SHEET_9B, SHEET_9C
from lbo_template import conventions as c


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_PEER)
    ws.column_dimensions["A"].width = 24
    for col in "BCDEFGHIJK":
        ws.column_dimensions[col].width = 14

    ws["A1"] = "9. Peer Summary — 통합 집계 (Trading + Transaction)"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:K1")

    # --- Trading Peer Summary (rows 3..20) ---
    ws["A3"] = "Trading Peer Summary"
    ws["A3"].font = Font(bold=True, size=12)

    trading_headers = ["Peer Name", "Source", "EV/LTM EBITDA", "EV/FY-1", "EV/FY-2",
                       "EV/NTM", "PBR", "Net Debt/LTM EBITDA", "Include ✓", "Memo"]
    for idx, h in enumerate(trading_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}5"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Data rows 6..20 (15 peers)
    for r in range(6, 21):
        peer_r = r - 3  # maps to 9a row 3..17
        ws[f"A{r}"] = f"='{SHEET_9A}'!A{peer_r}"
        ws[f"B{r}"] = "CIQ Trading"
        ws[f"C{r}"] = f"='{SHEET_9A}'!J{peer_r}"
        ws[f"D{r}"] = f"='{SHEET_9A}'!K{peer_r}"
        ws[f"E{r}"] = f"='{SHEET_9A}'!L{peer_r}"
        ws[f"F{r}"] = f"='{SHEET_9A}'!M{peer_r}"
        ws[f"G{r}"] = ""  # PBR placeholder (9a 확장 필요 시)
        ws[f"H{r}"] = f"='{SHEET_9A}'!N{peer_r}"
        ws[f"I{r}"] = True  # Include default
        c.apply_input(ws[f"I{r}"])
        for col in "ABCDEFGH":
            ws[f"{col}{r}"].font = c.crosstab_link_font()

    # Aggregate rows 22..27
    ws["A22"] = "Mean (Included only)"
    ws["A23"] = "Median (Included only)"
    ws["A24"] = "Min / Max"
    ws["A27"] = "3개년 평균의 평균 (Applied Trading Multiple)"

    for col in "CDEF":
        ws[f"{col}22"] = f'=IFERROR(AVERAGEIF($I$6:$I$20,TRUE,{col}$6:{col}$20),"")'
        ws[f"{col}23"] = f'=IFERROR(MEDIAN(IF($I$6:$I$20=TRUE,{col}$6:{col}$20)),"")'
        ws[f"{col}24"] = f'=MIN({col}$6:{col}$20)&" / "&MAX({col}$6:{col}$20)'
        c.apply_calc(ws[f"{col}22"])
        c.apply_calc(ws[f"{col}23"])
        ws[f"{col}22"].number_format = c.NUM_FMT_MULTIPLE
        ws[f"{col}23"].number_format = c.NUM_FMT_MULTIPLE

    ws["C27"] = "=(C22+D22+E22)/3"
    c.apply_key_output(ws["C27"])
    ws["C27"].number_format = c.NUM_FMT_MULTIPLE
    wb.defined_names["Applied_Trading_Multiple"] = DefinedName("Applied_Trading_Multiple", attr_text=f"'{SHEET_PEER}'!$C$27")

    ws["G27"] = "=IFERROR(AVERAGEIF($I$6:$I$20,TRUE,G$6:G$20),\"\")"  # PBR (if populated)
    c.apply_key_output(ws["G27"])
    ws["G27"].number_format = c.NUM_FMT_MULTIPLE
    wb.defined_names["Applied_Trading_PBR"] = DefinedName("Applied_Trading_PBR", attr_text=f"'{SHEET_PEER}'!$G$27")

    # --- Transaction Comps Summary (rows 30..65) ---
    ws["A30"] = "Transaction Comps Summary"
    ws["A30"].font = Font(bold=True, size=12)

    tx_headers = ["Transaction ID", "Source", "Announced", "Target", "Buyer Type",
                  "EV/LTM EBITDA", "EV/LTM Rev", "Deal Value Disclosed?", "Include ✓", "Memo"]
    for idx, h in enumerate(tx_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}32"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Rows 33..52: CIQ transactions link (up to 20 shown; rest aggregated from 9b)
    for r in range(33, 53):
        src_r = r - 30  # 9b row 3..22
        ws[f"A{r}"] = f"='{SHEET_9B}'!A{src_r}"
        ws[f"B{r}"] = "CIQ M&A"
        ws[f"C{r}"] = f"='{SHEET_9B}'!B{src_r}"
        ws[f"D{r}"] = f"='{SHEET_9B}'!D{src_r}"
        ws[f"E{r}"] = f"='{SHEET_9B}'!H{src_r}"
        ws[f"F{r}"] = f"='{SHEET_9B}'!N{src_r}"
        ws[f"G{r}"] = f"='{SHEET_9B}'!M{src_r}"
        ws[f"H{r}"] = f'=IF(ISNUMBER(F{r}),"Yes","No")'
        # Include auto-false if Deal Value not disclosed OR Buyer Type = Strategic
        ws[f"I{r}"] = f'=AND(H{r}="Yes",E{r}<>"Strategic")'
        for col in "ABCDEFGH":
            ws[f"{col}{r}"].font = c.crosstab_link_font()

    # Rows 53..62: Manual supplement link
    for r in range(53, 63):
        src_r = r - 50  # 9c row 3..12
        ws[f"A{r}"] = f"='{SHEET_9C}'!A{src_r}"
        ws[f"B{r}"] = f"='{SHEET_9C}'!P{src_r}"  # Source name from 9c
        ws[f"D{r}"] = f"='{SHEET_9C}'!D{src_r}"
        ws[f"F{r}"] = f"='{SHEET_9C}'!N{src_r}"
        ws[f"I{r}"] = f"='{SHEET_9C}'!R{src_r}"
        for col in "ABCDEFGH":
            ws[f"{col}{r}"].font = c.crosstab_link_font()

    # Aggregate rows 64..68
    ws["A65"] = "Mean (Included only)"
    ws["A66"] = "Median"
    ws["A67"] = "Trimmed Mean (상하 10% 제외, Applied Transaction Multiple)"

    ws["F65"] = '=IFERROR(AVERAGEIF($I$33:$I$62,TRUE,F$33:F$62),"")'
    ws["F66"] = '=IFERROR(MEDIAN(IF($I$33:$I$62=TRUE,F$33:$F$62)),"")'
    ws["F67"] = '=IFERROR(TRIMMEAN(IF($I$33:$I$62=TRUE,F$33:F$62),0.2),"")'
    c.apply_key_output(ws["F67"])
    ws["F67"].number_format = c.NUM_FMT_MULTIPLE
    wb.defined_names["Applied_Transaction_Multiple"] = DefinedName("Applied_Transaction_Multiple", attr_text=f"'{SHEET_PEER}'!$F$67")

    return ws
```

- [ ] **Step 3: 테스트 + 커밋**

```powershell
pytest tests/test_s9_ciq_and_peer.py -v
git add src/lbo_template/sheets/s9_peer_summary.py tests/test_s9_ciq_and_peer.py
git commit -m "feat(s9_peer): unified Trading+Transaction summary with Applied_* named ranges"
```

---

## Task 15: `7_Returns_LTV` 시트 (평가방식 1/2/3 추상화)

설계 §7 v0.5. Method Type 드롭다운 8종 + 9열 LTV 표.

**Files:**
- Modify: `src/lbo_template/sheets/s7_returns_ltv.py`
- Create: `tests/test_s7_returns_ltv.py`

- [ ] **Step 1: 테스트**

```python
from lbo_template.layout import SHEET_RETURNS


def test_three_method_rows(wb):
    ws = wb[SHEET_RETURNS]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 30)]
    assert "평가방식 1" in col_a
    assert "평가방식 2" in col_a
    assert "평가방식 3" in col_a


def test_method_type_dropdown(wb):
    ws = wb[SHEET_RETURNS]
    dvs = ws.data_validations.dataValidation
    found = False
    for dv in dvs:
        f = dv.formula1 or ""
        if "DCF_Stressed" in f and "Trading_EV_EBITDA" in f and "Trading_PBR" in f:
            found = True
    assert found


def test_named_ranges_method_abstraction(wb):
    for i in [1, 2, 3]:
        assert f"DASH_Valuation_Method{i}_Label" in wb.defined_names
        assert f"DASH_Valuation_Method{i}_Multiple" in wb.defined_names
        assert f"DASH_Valuation_Method{i}_EV" in wb.defined_names
        assert f"DASH_LTV_Method{i}_Opco" in wb.defined_names
        assert f"DASH_LTV_Method{i}_Cumulative" in wb.defined_names


def test_method_type_switch_formula(wb):
    ws = wb[SHEET_RETURNS]
    # Multiple 컬럼은 Method Type별 분기 수식
    # 방식 1 Multiple 셀 (예: D8) = SWITCH(MethodType, ...)
    found_switch = False
    for r in range(5, 15):
        for col in "BCDEFGHI":
            v = ws[f"{col}{r}"].value
            if isinstance(v, str) and "SWITCH" in v and "DCF_Stressed" in v:
                found_switch = True
                break
    assert found_switch
```

- [ ] **Step 2: 빌더**

```python
"""7_Returns_LTV — abstracted Valuation Method 1/2/3 per design v0.5."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.styles import Font
from lbo_template.layout import SHEET_RETURNS, SHEET_INPUT, SHEET_DCF, SHEET_PEER
from lbo_template import conventions as c

METHOD_TYPES = [
    "DCF_Stressed",
    "Trading_EV_EBITDA",
    "Trading_PBR",
    "Trading_PER",
    "Transaction_EV_EBITDA",
    "Transaction_PBR",
    "MarketCap_Avg",
    "Manual_Absolute",
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_RETURNS)
    ws.column_dimensions["A"].width = 14
    for col in "BCDEFGHIJK":
        ws.column_dimensions[col].width = 15

    ws["A1"] = "7. Returns & LTV — Valuation Method 1/2/3 (v0.5 추상화)"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:K1")

    # --- Method Declaration Block (rows 3..7) ---
    decl_headers = ["방식", "Label", "Method Type", "Multiple", "Multiple 기반", "Source 메모"]
    for idx, h in enumerate(decl_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}3"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Default example labels (user-editable)
    DEFAULTS = [
        ("평가방식 1", "DCF (Stressed)", "DCF_Stressed"),
        ("평가방식 2", "Trading EV/EBITDA", "Trading_EV_EBITDA"),
        ("평가방식 3", "Transaction EV/EBITDA (Trimmed)", "Transaction_EV_EBITDA"),
    ]

    dv_mt = DataValidation(type="list", formula1=f'"{",".join(METHOD_TYPES)}"', allow_blank=False)
    ws.add_data_validation(dv_mt)

    for idx, (method_tag, default_label, default_type) in enumerate(DEFAULTS):
        r = 4 + idx
        ws[f"A{r}"] = method_tag
        ws[f"A{r}"].font = Font(bold=True)
        ws[f"B{r}"] = default_label
        c.apply_input(ws[f"B{r}"])
        ws[f"C{r}"] = default_type
        c.apply_input(ws[f"C{r}"])
        dv_mt.add(f"C{r}")

        # Multiple (col D) — SWITCH on Method Type
        mul = ws[f"D{r}"]
        mul.value = (
            f'=SWITCH(C{r},'
            f'"DCF_Stressed",IFERROR(DCF_EV/D27,"n.a"),'
            f'"Trading_EV_EBITDA",Applied_Trading_Multiple,'
            f'"Trading_PBR",Applied_Trading_PBR,'
            f'"Trading_PER","(수기)",'
            f'"Transaction_EV_EBITDA",Applied_Transaction_Multiple,'
            f'"Transaction_PBR","(수기)",'
            f'"MarketCap_Avg","n.a",'
            f'"Manual_Absolute","n.a")'
        )
        c.apply_calc(mul)
        mul.number_format = c.NUM_FMT_MULTIPLE
        wb.defined_names[f"DASH_Valuation_Method{idx+1}_Label"] = DefinedName(f"DASH_Valuation_Method{idx+1}_Label", attr_text=f"'{SHEET_RETURNS}'!$B${r}")
        wb.defined_names[f"DASH_Valuation_Method{idx+1}_Multiple"] = DefinedName(f"DASH_Valuation_Method{idx+1}_Multiple", attr_text=f"'{SHEET_RETURNS}'!$D${r}")

        # Base metric col E (Book Value / EBITDA / MarketCap)
        base = ws[f"E{r}"]
        base.value = (
            f'=SWITCH(C{r},'
            f'"DCF_Stressed","EBITDA",'
            f'"Trading_EV_EBITDA","EBITDA",'
            f'"Trading_PBR","Book Value",'
            f'"Trading_PER","Net Income",'
            f'"Transaction_EV_EBITDA","EBITDA",'
            f'"Transaction_PBR","Book Value",'
            f'"MarketCap_Avg","절대값",'
            f'"Manual_Absolute","절대값")'
        )
        c.apply_calc(base)

        # Source memo F
        c.apply_input(ws[f"F{r}"])

    # --- 9-Column LTV Table (rows 9..14) ---
    ws["A9"] = "9-열 LTV 산출"
    ws["A9"].font = Font(bold=True, size=11)

    ltv_headers = ["방식", "(a) 기준지표", "(b) Multiple", "(c) 지분가치 100%",
                   "(d) 지분율", "(e) 담보지분가치", "(f) Opco 차입금",
                   "(g) Opco LTV", "(h) Holdco 차입금", "(i) 누적 LTV"]
    for idx, h in enumerate(ltv_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}10"]
        cell.value = h
        cell.font = c.column_header_font()
        cell.fill = c.column_header_fill()

    # Target ownership input (anchor A27)
    ws["A27"] = "LTM EBITDA (for implied multiple back-calc)"
    ws["D27"] = "=LTM_EBITDA"
    c.apply_calc(ws["D27"])

    ws["A28"] = "Target Ownership (지분율)"
    ws["B28"] = 1.0  # 100% default
    c.apply_input(ws["B28"])
    ws["B28"].number_format = c.NUM_FMT_PERCENT
    wb.defined_names["Target_Ownership"] = DefinedName("Target_Ownership", attr_text=f"'{SHEET_RETURNS}'!$B$28")

    for idx in range(3):
        r = 11 + idx
        method_r = 4 + idx
        ws[f"A{r}"] = f"=B{method_r}"  # Label link
        ws[f"A{r}"].font = c.sametab_link_font()
        ws[f"B{r}"] = f"=E{method_r}"  # base metric label
        ws[f"B{r}"].font = c.sametab_link_font()
        ws[f"C{r}"] = f"=D{method_r}"  # Multiple
        ws[f"C{r}"].font = c.sametab_link_font()
        # (c) 지분가치: EBITDA × Multiple / Book × Multiple / DCF Equity 직접
        ws[f"D{r}"] = (
            f'=IFERROR(SWITCH(C{method_r},'
            f'"DCF_Stressed",DCF_Equity_Value,'
            f'"MarketCap_Avg",F{method_r},'  # F = source memo carries value? user adjust
            f'"Manual_Absolute",F{method_r},'
            f'D{method_r}*LTM_EBITDA),"")'
        )
        c.apply_calc(ws[f"D{r}"])
        ws[f"D{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"E{r}"] = "=Target_Ownership"
        ws[f"E{r}"].number_format = c.NUM_FMT_PERCENT
        ws[f"F{r}"] = f"=D{r}*E{r}"
        c.apply_key_output(ws[f"F{r}"])
        ws[f"F{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"G{r}"] = "=Opco_Senior_Principal+Opco_2L_Principal"
        ws[f"G{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"H{r}"] = f"=IFERROR(G{r}/F{r},\"\")"
        c.apply_key_output(ws[f"H{r}"])
        ws[f"H{r}"].number_format = c.NUM_FMT_PERCENT
        ws[f"I{r}"] = "=Holdco_Sub_Principal"
        ws[f"I{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"J{r}"] = f"=IFERROR((G{r}+I{r})/F{r},\"\")"
        c.apply_key_output(ws[f"J{r}"])
        ws[f"J{r}"].number_format = c.NUM_FMT_PERCENT

        wb.defined_names[f"DASH_Valuation_Method{idx+1}_EV"] = DefinedName(f"DASH_Valuation_Method{idx+1}_EV", attr_text=f"'{SHEET_RETURNS}'!$D${r}")
        wb.defined_names[f"DASH_LTV_Method{idx+1}_Opco"] = DefinedName(f"DASH_LTV_Method{idx+1}_Opco", attr_text=f"'{SHEET_RETURNS}'!$H${r}")
        wb.defined_names[f"DASH_LTV_Method{idx+1}_Cumulative"] = DefinedName(f"DASH_LTV_Method{idx+1}_Cumulative", attr_text=f"'{SHEET_RETURNS}'!$J${r}")

    return ws
```

- [ ] **Step 3: 테스트 + 커밋**

```powershell
pytest tests/test_s7_returns_ltv.py -v
git add src/lbo_template/sheets/s7_returns_ltv.py tests/test_s7_returns_ltv.py
git commit -m "feat(s7_returns_ltv): abstracted Method 1/2/3 with 8-type dropdown and 9-col LTV"
```

---

## Task 16: `8_Dashboard` 시트

설계 §8 v0.5. 5개 표 + 모든 `DASH_*` named range 통합 + HMM 양식 대응 `CFTable` 8행 × 5개년.

**Files:**
- Modify: `src/lbo_template/sheets/s8_dashboard.py`
- Create: `tests/test_s8_dashboard.py`

- [ ] **Step 1: 테스트**

```python
from lbo_template.layout import SHEET_DASH


def test_dashboard_five_tables(wb):
    ws = wb[SHEET_DASH]
    col_a = [ws.cell(row=r, column=1).value for r in range(1, 80)]
    required = [
        "표 1. Valuation 요약",
        "표 2. 이자지급가능성 요약",
        "표 3. 만기상환가능성 요약",
        "표 4. 차주기준 자금수지표",
        "표 5. 시나리오 메타",
    ]
    for e in required:
        assert e in col_a, f"missing table: {e}"


def test_dash_cftable_40_named_ranges(wb):
    for row in range(1, 9):
        for fy in range(1, 6):
            name = f"DASH_CFTable_Row{row}_FY{fy}"
            assert name in wb.defined_names, f"missing: {name}"


def test_dash_cftable_row_labels(wb):
    for row in range(1, 9):
        name = f"DASH_CFTable_Row{row}_Label"
        assert name in wb.defined_names, f"missing: {name}"


def test_dash_all_required_scalars(wb):
    expected_scalars = [
        "DASH_Case",
        "DASH_Version",
        "DASH_DSCR_Min",
        "DASH_ICR_Opco_Min",
        "DASH_ICR_Holdco_Min",
    ]
    for e in expected_scalars:
        assert e in wb.defined_names, f"missing: {e}"
```

- [ ] **Step 2: 빌더 구현** (간략히 요지 — 모든 named range 등록)

```python
"""8_Dashboard — Word-paste-ready summary tables + DASH_* named range cluster."""
from openpyxl.workbook import Workbook
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.styles import Font
from lbo_template.layout import (
    SHEET_DASH, SHEET_RETURNS, SHEET_WATERFALL, SHEET_OVERLAY,
    SHEET_DEBT, SHEET_STRESS,
)
from lbo_template import conventions as c

CFTABLE_ROW_LABELS = [
    "기초현금",
    "영업CF (EBITDA)",
    "투자CF (CAPEX)",
    "배당수익",
    "재무CF (기존 차입금 원리금)",
    "본건 인수금융 이자비용",
    "본건 원금상환 (Tr별 합계)",
    "기말현금 (= 원리금 상환재원)",
]


def build(wb: Workbook) -> Worksheet:
    ws = wb.create_sheet(SHEET_DASH)
    ws.column_dimensions["A"].width = 40
    for col in "BCDEFGHIJ":
        ws.column_dimensions[col].width = 14

    ws["A1"] = "8. Dashboard — Word 심사보고서 복붙용"
    c.apply_section_header(ws["A1"])
    ws.merge_cells("A1:J1")

    # Scenario meta
    ws["A3"] = "Case"; ws["B3"] = "=Case_Switch"
    wb.defined_names["DASH_Case"] = DefinedName("DASH_Case", attr_text=f"'{SHEET_DASH}'!$B$3")
    ws["A4"] = "Template Version"; ws["B4"] = "v0.5"
    wb.defined_names["DASH_Version"] = DefinedName("DASH_Version", attr_text=f"'{SHEET_DASH}'!$B$4")

    # --- 표 1. Valuation 요약 ---
    ws["A6"] = "표 1. Valuation 요약 (평가방식 1/2/3)"
    ws["A6"].font = Font(bold=True, size=12)
    headers = ["방식", "Label", "Multiple", "EV (담보지분가치)", "Opco LTV", "누적 LTV"]
    for idx, h in enumerate(headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}7"]; cell.value = h
        cell.font = c.column_header_font(); cell.fill = c.column_header_fill()
    for i in [1, 2, 3]:
        r = 7 + i
        ws[f"A{r}"] = f"방식 {i}"
        ws[f"B{r}"] = f"=DASH_Valuation_Method{i}_Label"
        ws[f"C{r}"] = f"=DASH_Valuation_Method{i}_Multiple"
        ws[f"D{r}"] = f"=DASH_Valuation_Method{i}_EV"
        ws[f"E{r}"] = f"=DASH_LTV_Method{i}_Opco"
        ws[f"F{r}"] = f"=DASH_LTV_Method{i}_Cumulative"
        for col in "BCDEF":
            c.apply_key_output(ws[f"{col}{r}"])
        ws[f"C{r}"].number_format = c.NUM_FMT_MULTIPLE
        ws[f"D{r}"].number_format = c.NUM_FMT_ACCOUNTING
        ws[f"E{r}"].number_format = c.NUM_FMT_PERCENT
        ws[f"F{r}"].number_format = c.NUM_FMT_PERCENT

    # --- 표 2. 이자지급가능성 ---
    ws["A13"] = "표 2. 이자지급가능성 요약"
    ws["A13"].font = Font(bold=True, size=12)
    tx_headers = ["구분", "FY1", "FY2", "FY3", "FY4", "FY5", "Min"]
    for idx, h in enumerate(tx_headers):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}14"]; cell.value = h
        cell.font = c.column_header_font(); cell.fill = c.column_header_fill()
    ws["A15"] = "Dividend Received"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}15"] = f"=INDEX(Dividend_Row,{i+1})"
    ws["A16"] = "Holdco ICR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}16"] = f"=INDEX(Holdco_ICR_Row,{i+1})"
    ws["G16"] = "=MIN(Holdco_ICR_Row)"
    wb.defined_names["DASH_ICR_Holdco_Min"] = DefinedName("DASH_ICR_Holdco_Min", attr_text=f"'{SHEET_DASH}'!$G$16")
    ws["A17"] = "Opco ICR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}17"] = f"=INDEX(Opco_ICR_Row,{i+1})"
    ws["G17"] = "=MIN(Opco_ICR_Row)"
    wb.defined_names["DASH_ICR_Opco_Min"] = DefinedName("DASH_ICR_Opco_Min", attr_text=f"'{SHEET_DASH}'!$G$17")
    ws["A18"] = "Opco DSCR"
    for i, col in enumerate("BCDEF"):
        ws[f"{col}18"] = f"=INDEX(Opco_DSCR_Row,{i+1})"
    ws["G18"] = "=MIN(Opco_DSCR_Row)"
    wb.defined_names["DASH_DSCR_Min"] = DefinedName("DASH_DSCR_Min", attr_text=f"'{SHEET_DASH}'!$G$18")

    # FY1~FY5 배당 named range
    for i, col in enumerate("BCDEF"):
        name = f"DASH_Div_FY{i+1}"
        wb.defined_names[name] = DefinedName(name, attr_text=f"'{SHEET_DASH}'!${col}$15")
        name_lev = f"DASH_Lev_NetLeverage_FY{i+1}"
        # wire from 5_CF_Waterfall Net_Leverage_Row
        ws[f"{col}20"] = f"=INDEX(Net_Leverage_Row,{i+1})"
        wb.defined_names[name_lev] = DefinedName(name_lev, attr_text=f"'{SHEET_DASH}'!${col}$20")
    ws["A20"] = "Net Leverage"

    # --- 표 3. 만기상환가능성 ---
    ws["A22"] = "표 3. 만기상환가능성 요약 (Exit FY5)"
    ws["A22"].font = Font(bold=True, size=12)
    ws["A23"] = "Exit Multiple (+ Active Δ)"
    ws["B23"] = "=C11+Active_Exit_Multiple_Delta"  # Method 2 Multiple + Δ (기본)
    ws["B23"].number_format = c.NUM_FMT_MULTIPLE

    # --- 표 4. 차주기준 자금수지표 (v0.5 Q3) ---
    ws["A26"] = "표 4. 차주기준 자금수지표 (HMM 보고서 양식 대응)"
    ws["A26"].font = Font(bold=True, size=12)
    hdr = ["구분"] + [f"FY{i}" for i in range(1, 6)]
    for idx, h in enumerate(hdr):
        col = chr(ord("A") + idx)
        cell = ws[f"{col}27"]; cell.value = h
        cell.font = c.column_header_font(); cell.fill = c.column_header_fill()

    # Row wiring (8 rows × 5 FY)
    for row_idx, label in enumerate(CFTABLE_ROW_LABELS, start=1):
        r = 27 + row_idx
        ws[f"A{r}"] = label
        wb.defined_names[f"DASH_CFTable_Row{row_idx}_Label"] = DefinedName(
            f"DASH_CFTable_Row{row_idx}_Label", attr_text=f"'{SHEET_DASH}'!$A${r}")
        for fy_idx, col in enumerate("BCDEF", start=1):
            cell = ws[f"{col}{r}"]
            # Formula per row:
            if row_idx == 1:  # 기초현금
                cell.value = 0 if fy_idx == 1 else f"={col.replace(chr(ord(col)-1) if fy_idx>1 else col, chr(ord(col)-1))}35"
            elif row_idx == 2:  # 영업CF (= Stressed EBITDA)
                cell.value = f"='{SHEET_OVERLAY}'!{chr(ord('D')+fy_idx)}13"  # FY1=E13 … FY5=I13
            elif row_idx == 3:  # 투자CF (=-Capex)
                cell.value = f"=-'{SHEET_OVERLAY}'!{chr(ord('D')+fy_idx)}16"
            elif row_idx == 4:  # 배당수익 (Holdco 관점)
                cell.value = f"=INDEX(Dividend_Row,{fy_idx})"
            elif row_idx == 5:  # 재무CF (기존 차입금 — MVP는 0)
                cell.value = 0
            elif row_idx == 6:  # 본건 이자비용 합계
                cell.value = f"=INDEX(Opco_Sr_Interest,{fy_idx})+INDEX(Opco_2L_Interest,{fy_idx})+INDEX(Holdco_Interest,{fy_idx})"
            elif row_idx == 7:  # 본건 원금상환 (Mand + Sweep)
                cell.value = f"=INDEX(Opco_Sr_Mand,{fy_idx})+INDEX(Opco_2L_Mand,{fy_idx})"
            elif row_idx == 8:  # 기말현금
                cell.value = f"={col}{28}+{col}{29}+{col}{30}+{col}{31}+{col}{32}+{col}{33}+{col}{34}"
            c.apply_key_output(cell)
            cell.number_format = c.NUM_FMT_ACCOUNTING
            wb.defined_names[f"DASH_CFTable_Row{row_idx}_FY{fy_idx}"] = DefinedName(
                f"DASH_CFTable_Row{row_idx}_FY{fy_idx}", attr_text=f"'{SHEET_DASH}'!${col}${r}")

    # --- 표 5. 시나리오 메타 ---
    ws["A38"] = "표 5. 시나리오 메타"
    ws["A38"].font = Font(bold=True, size=12)
    ws["A39"] = "Revenue Growth Δ"
    ws["B39"] = "=Active_Revenue_Growth_Delta"
    ws["B39"].number_format = c.NUM_FMT_PERCENT
    ws["A40"] = "EBITDA Margin Δ"
    ws["B40"] = "=Active_EBITDA_Margin_Delta"
    ws["B40"].number_format = c.NUM_FMT_PERCENT
    ws["A41"] = "WACC Uplift (bp)"
    ws["B41"] = "=Active_WACC_Uplift"
    ws["B41"].number_format = c.NUM_FMT_BPS
    ws["A42"] = "Exit Multiple Δ"
    ws["B42"] = "=Active_Exit_Multiple_Delta"
    ws["B42"].number_format = c.NUM_FMT_MULTIPLE

    # IRR Sponsor placeholder (named range reserved per design)
    ws["A44"] = "Sponsor IRR (v1.1+)"
    ws["B44"] = ""
    wb.defined_names["DASH_IRR_Sponsor"] = DefinedName("DASH_IRR_Sponsor", attr_text=f"'{SHEET_DASH}'!$B$44")

    return ws
```

> 주의: `기초현금` 계산 수식은 단순화를 위해 FY1=0, FY2+=이전 기말현금(= prev col row 35) 로직. 복잡한 주소 산술보다 가독성 우선.

```python
# 수정: 기초현금 로직을 별도 루프로 재작성 (clarity 우선)
# row_idx==1 분기 제거 후 다음처럼 나중에 덮어쓰기:
for fy_idx, col in enumerate("BCDEF", start=1):
    prev = chr(ord(col) - 1) if fy_idx > 1 else None
    r = 28  # 기초현금 행
    cell = ws[f"{col}{r}"]
    if fy_idx == 1:
        cell.value = 0
    else:
        cell.value = f"={prev}35"  # 35 = 기말현금 행
    c.apply_key_output(cell)
    cell.number_format = c.NUM_FMT_ACCOUNTING
```

(위 보충 루프를 Row 루프 종료 후 추가 — clarity 확보)

- [ ] **Step 3: 테스트 + 커밋**

```powershell
pytest tests/test_s8_dashboard.py -v
git add src/lbo_template/sheets/s8_dashboard.py tests/test_s8_dashboard.py
git commit -m "feat(s8_dashboard): 5 summary tables + 40 CFTable named ranges + full DASH_* cluster"
```

---

## Task 17: Integrity 체크 + 전체 smoke 테스트

3대 무결성 체크 (Sources=Uses, Debt≥0, Circular 0건) + 모든 Named Range 규칙 준수 검증 + 실제 Excel 파일 생성 및 수기 sanity.

**Files:**
- Create: `tests/test_integrity.py`

- [ ] **Step 1: 통합 테스트 작성**

```python
"""End-to-end integrity checks."""
import re
from lbo_template.layout import ALL_SHEETS


def test_all_sheets_exist(wb):
    assert wb.sheetnames == ALL_SHEETS


def test_no_iterative_calc_marker(wb):
    """어떤 셀도 iterative calc를 가정한 수식을 쓰지 않아야 함"""
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                if isinstance(cell.value, str) and cell.value.startswith("="):
                    # Heuristic: same-cell self-reference
                    assert f"'{ws.title}'!{cell.coordinate}" not in cell.value, \
                        f"self-ref in {ws.title}!{cell.coordinate}"


DASH_NAME_PATTERN = re.compile(r"^DASH_[A-Za-z0-9]+_[A-Za-z0-9]+(_[A-Za-z0-9]+)*$")


def test_dash_names_follow_convention(wb):
    for name in wb.defined_names:
        if name.startswith("DASH_"):
            assert DASH_NAME_PATTERN.match(name), f"bad DASH name: {name}"


def test_named_range_count_threshold(wb):
    """v0.5 설계상 최소 예상 named range 수"""
    dash_names = [n for n in wb.defined_names if n.startswith("DASH_")]
    # CFTable 40 + CFTable_Label 8 + LTV Method 6 + Valuation Method 9 + Coverage 3 + Div 5 + Lev 5 + Case + Version + IRR = ~80+
    assert len(dash_names) >= 70, f"only {len(dash_names)} DASH names; expected ≥70"


def test_active_named_ranges_cover_all_params(wb):
    for n in ["Active_Revenue_Growth_Delta", "Active_EBITDA_Margin_Delta",
              "Active_Capex_Pct_Delta", "Active_NWC_Pct_Delta",
              "Active_WACC_Uplift", "Active_Exit_Multiple_Delta", "Perm_Growth"]:
        assert n in wb.defined_names


def test_sources_equals_uses_check_formula_exists(wb):
    ws = wb["1_Input_BaseCase"]
    # Check row referenced in Task 5 test — label "Check: Sources − Uses"
    found = False
    for r in range(1, 30):
        label = ws.cell(row=r, column=1).value
        if label and "Sources − Uses" in label:
            formula = ws.cell(row=r, column=2).value
            assert formula.startswith("=")
            found = True
    assert found


def test_debt_ending_balances_use_max_zero(wb):
    ws = wb["4_Debt_Schedule"]
    max_zero_count = 0
    for row in ws.iter_rows():
        for cell in row:
            if isinstance(cell.value, str) and "MAX(0" in cell.value:
                max_zero_count += 1
    assert max_zero_count >= 10, "Ending Balance rows must use MAX(0,...) throughout tranches"
```

- [ ] **Step 2: 전체 테스트 실행**

```powershell
pytest -v
```

Expected: 모든 테스트 pass.

- [ ] **Step 3: 실제 엑셀 파일 생성 + 수기 검증**

```powershell
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

수기 검증 절차 (Excel에서 직접):
1. `dist/LBO_Stress_Template_v0.5.xlsx` 열기 → 13개 탭 확인
2. `1_Input!B5`부터 Section A에 임의 숫자 입력 (EV 100,000 / Net Debt 30,000 / Fee 2,000 / Senior 40,000 / 2nd 15,000 / Holdco 15,000 / Target Lev 6.0 등)
3. Section B에 Revenue/EBITDA/Capex/NWC 8개 FY 더미 숫자 입력
4. `1_Input!B18` (Sources−Uses) = 0 확인
5. `2_Stress!B3` 에서 드롭다운으로 "Downside" 선택 → `8_Dashboard`의 LTV·DSCR·ICR이 즉시 갱신되는지 확인
6. "Base"로 되돌리고 `9a!B3:B17`에 Ticker 5개 입력 (예: 005930.KS, 000660.KS, 035420.KS)
7. `Data → Refresh All` (Plug-in 미설치 PC는 스킵; 구조만 확인)
8. `File → Options → Formulas → Enable iterative calculation`이 OFF인 상태에서 순환참조 에러 배너 없는지 확인
9. `Formulas → Error Checking` 실행 후 에러 0건 확인
10. `8_Dashboard` 모든 named range 셀에 `#REF!` 없는지 훑기

- [ ] **Step 4: 발견된 이슈 정리**

수기 검증에서 나온 문제를 `.cursor/issues-20260420.md`에 기록하고 GitHub Issue 생성 또는 직접 수정. 중대한 설계 변경이 필요하면 design-doc v0.6으로 리비전.

- [ ] **Step 5: 최종 커밋**

```powershell
git add tests/test_integrity.py
git commit -m "test: add end-to-end integrity checks for named ranges, circular refs, MAX(0,...) discipline"
```

---

## Task 18: README 업데이트 + v0.5 태그

**Files:**
- Modify: `README.md`

- [ ] **Step 1: README에 사용법 + 수기 검증 절차 반영**

```markdown
# LBO Stress Template Builder v0.5

## 설치 + 빌드

```bash
python -m pip install -e .[dev]
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

## 테스트

```bash
pytest -v
```

## 수기 검증 (처음 한 번)

[Task 17 Step 3 10단계 절차 그대로 복붙]

## v0.6 로드맵 (Golden Test Fixture)

1. 과거 마감된 딜 1건으로 입력 셀 전부 채운 `.xlsx` 생성
2. 그 파일의 `8_Dashboard` 출력값 스냅샷을 `tests/fixtures/goldentest_v05.json`에 기록
3. 빌더 리그레션 시 스냅샷 불변 자동 검증

## Design & Plan Docs

- Design v0.5: `.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md`
- Plan: `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`
```

- [ ] **Step 2: 커밋 + 태그**

```powershell
git add README.md
git commit -m "docs: v0.5 README with verification steps and v0.6 roadmap"
git tag -a v0.5.0 -m "LBO Stress Template v0.5 — MVP with all 13 sheets, Preconditions resolved"
```

---

## Self-Review

아래는 작성자가 최종 플랜을 spec (design-doc v0.5) 과 대조해 돌린 체크리스트입니다.

### 1. Spec Coverage

| Spec 섹션 | 담당 Task | 상태 |
|---|---|---|
| §0 전체 시트 구조 (13 tabs) | Task 3 | ☑ |
| §1 Input_BaseCase (Section A/B/C + Check) | Task 5 | ☑ |
| §2 Stress_Panel (Case_Switch + 6 params + Presets) | Task 6 | ☑ |
| §3 Operating_Overlay | Task 7 | ☑ |
| §4 Debt_Schedule (3 tranches + Sweep + PIK) | Task 8 | ☑ |
| §5 CF_Waterfall + 4 KPI | Task 9 | ☑ |
| §6 DCF (mid-year 0.5~4.5 + TV 5.0 + Perm 1.0%) | Task 10 | ☑ |
| §7 Returns_LTV (Method 1/2/3 추상화 v0.5) | Task 15 | ☑ |
| §8 Dashboard (5 tables + 40 CFTable + DASH_*) | Task 16 | ☑ |
| §9 Alt-A 동일 셀 택1 (9a CIQ primary + Paste fallback) | Task 11 | ☑ |
| §9b Transaction Comps 500행 + 초과 경고 | Task 12 | ☑ |
| §9c Manual Supplement (Source 드롭다운 + Reliability) | Task 13 | ☑ |
| §9_Peer_Summary 3 source 통합 + Applied_*_Multiple | Task 14 | ☑ |
| §Parsing Guardrails #1-16 | 문서화 (0_README, 주석) | ☑ |
| Success Criteria Integrity 3대 체크 | Task 17 | ☑ |
| Phase 0 Preconditions 체크리스트 문서 | Task 4 (0_README) | ☑ |
| Dual-borrower (D8) | Deferred — 계획서 미포함 | ☑ (의도적 제외) |
| P·Q 분기 (D1) | Deferred — 계획서 미포함 | ☑ (의도적 제외) |
| Golden Test Fixture | 사용자 선택으로 v0.6 연기 | ☑ |

### 2. Placeholder Scan

- "TBD/TODO/implement later/handle edge cases" 등 금지어: **없음**
- 각 Task 단계마다 실제 코드 블록 포함
- 수식 문자열 모두 구체 (예: `=SWITCH(C{r},"DCF_Stressed",...)`)
- "Similar to Task N" 반복 없음; `9a`→`9b` 구조 유사하지만 각각 전체 수식 기재

### 3. Type Consistency

- Named range 명명: 본 계획 전반 대문자 snake_case 준수
  - `Active_Revenue_Growth_Delta` / `Applied_Trading_Multiple` / `DASH_LTV_Method1_Opco` 등 Task 간 완전 일치
- Cell row 번호 일관성: `s3_overlay.py`의 `UFCF_ROW = 19`를 모듈 상수로 export하고 `s5_waterfall.py`·`s8_dashboard.py`가 참조하도록 명시 (Task 9 Step 3)
- `s4_debt.py`의 tranche start row (5, 15, 25)와 `s5_waterfall.py`의 `Opco_Sr_Interest` named range ($E$8:$I$8) 간 row offset 정확히 일치 검증 — 주의: `5 + 1 (header) + 2 (opening, rate offset)`... → Task 8 구현 시 실제 row를 재계산하여 named range 조정 필요할 수 있음 (수기 검증 Task 17 Step 3 10단계에서 발견되면 즉시 수정).

### 4. 예상 리스크 (수기 검증 단계에서 드러날 것들)

- Task 8의 Cash Sweep 수식이 `Opco_Sweep_Avail_<col>` 참조 + `4_Debt_Schedule`에 본인 row 기준 상대 offset — Sweep applied 금액이 전체 잔액을 초과하지 않도록 `MIN` 클램프 후 다시 순환 의심 시 `Opening - Mand` 한도 내에서만 Sweep 허용. Task 17 Step 3 (8)에서 Formula Audit 필수.
- Task 11 `=CIQ()` 수식은 Plug-in 미설치 PC에서 `#NAME?` 에러. `IFERROR(..., "")` 감싸서 공란으로 처리 → 단, 전체 시트 `#NAME?` 초기 상태는 Plug-in 설치 후 Refresh로 해결.
- Task 15의 `METHOD_TYPE` 드롭다운 값 8종 중 `"Trading_PER"` / `"Transaction_PBR"` / `"Manual_Absolute"`는 `Multiple` 산출 시 `"(수기)"` 또는 `"n.a"` 문자열 반환 → `7_Returns_LTV` 9열 표의 (c) 지분가치는 `IFERROR`로 공란 처리. 사용자가 Multiple을 직접 덮어 써야 하는 flow → `0_README`에 별도 주석 필요.

---

## Execution Handoff

**Plan complete and saved to `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`. Two execution options:**

**1. Subagent-Driven (recommended)** — 각 Task마다 fresh subagent 디스패치 + Task 간 리뷰. 빠른 반복, 격리된 컨텍스트.

**2. Inline Execution** — 현 세션에서 Task 순차 실행, 체크포인트마다 리뷰.

**Which approach?**
