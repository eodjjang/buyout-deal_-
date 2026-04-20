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
