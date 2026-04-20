# LBO Stress Template Builder

Design doc: `.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md` (v0.5 APPROVED)
Plan: `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`

## Build

```bash
python -m pip install -e ".[dev]"
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

## Test

```bash
pytest
```

## 산출물

`dist/LBO_Stress_Template_v0.5.xlsx` — 12개 탭, KRW 백만원 기준, VBA 미사용.
