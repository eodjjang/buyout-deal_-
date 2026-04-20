"""Entrypoint: assemble the workbook and save to disk."""
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
    """Assemble the complete LBO stress template workbook."""
    wb = Workbook()
    # Remove default sheet; all tabs created by individual builders below.
    default = wb.active
    wb.remove(default)
    # Build in ALL_SHEETS order (tab order matches design §0 Table of Tabs).
    s0_readme.build(wb)
    s1_input_base.build(wb)
    s2_stress_panel.build(wb)
    s3_overlay.build(wb)
    s4_debt.build(wb)
    s5_waterfall.build(wb)
    s6_dcf.build(wb)
    s7_returns_ltv.build(wb)
    s8_dashboard.build(wb)
    s9a_ciq_trading.build(wb)
    s9b_ciq_transaction.build(wb)
    s9c_manual.build(wb)
    s9_peer_summary.build(wb)
    return wb


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="build-lbo-template",
        description="Assemble the Lender-perspective LBO Stress Template workbook.",
    )
    parser.add_argument("--output", type=Path, default=Path("dist/LBO_Stress_Template_v0.5.xlsx"))
    args = parser.parse_args()
    wb = build_workbook()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    wb.save(args.output)
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
