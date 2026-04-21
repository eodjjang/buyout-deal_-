# `lbo_dashboard_export` (Word/LLM 파이프라인 공통 계약)

- **`lbo_dashboard_export_v1.schema.json`** — `8_Dashboard`의 `DASH_*` Named Range 묶음을 **중첩 JSON**으로 옮길 때의 스키마 (`schema_version`: `1.0`).
- **소스**: 빌드 산출물 `dist/LBO_Stress_Template_v0.5.xlsx`에 정의된 79개 `DASH_*` 이름(템플릿 버전이 오르면 스키마 메이저 버전 검토).
- **전체 매핑 표(1장)**: [`NAMED_RANGE_TO_JSON_v1.md`](NAMED_RANGE_TO_JSON_v1.md)

## 저장소 경계 (두 레포에서 동일 계약)

- **이 레포(`buyout deal_모델분석`)**: Excel 템플릿 빌더 + **`schemas/` 정본(SSoT)**.
- **Word/LLM 파이프라인 레포(별도)**: 문서 생성·프롬프트만 두고, JSON 계약은 **이 폴더를 git submodule / subtree / 특정 커밋 복사**로 가져와 동일 파일을 둔다(버전은 `schema_version` + 이 디렉터리의 커밋 SHA로 핀).
- 양쪽 README에 상대 링크가 아니라 **각 레포의 절대 URL**(또는 사내 Git 호스트 경로)을 한 줄씩 적어 “스키마는 템플릿 레포, 구현은 Word 레포”를 명시한다.

## Named Range → JSON 필드 매핑 (요약)

| Excel (prefix `DASH_`) | JSON 경로 |
|-------------------------|-----------|
| `Case`, `Version` | `scenario.case`, `scenario.template_version` |
| `Valuation_Method{1..3}_Label/Multiple/EV`, `LTV_Method{1..3}_Opco/Cumulative` | `valuation_methods[]` (3 elements, `method_index` 1..3) |
| `Div_FY1..FY5` | `coverage.dividend_received_by_fy[]` |
| `ICR_Holdco_Min`, `ICR_Opco_Min`, `DSCR_Min` | `coverage.*` |
| `Lev_NetLeverage_FY1..FY5` | `coverage.net_leverage_by_fy[]` |
| `CFTable_Row{1..8}_Label`, `_FY{1..5}` | `cashflow_summary_table[]` (8 rows × 5 FY) |
| `IRR_Sponsor` | `sponsor_irr` |

## 채워진 `.xlsx`에서 JSON 만들기

1. Excel에서 재계산 후 저장하거나, 파이썬에서 `openpyxl` `data_only=True`로 **값** 읽기.
2. 각 `DASH_*` 이름으로 `defined_names` → 셀 값 해석.
3. 출력 JSON이 위 스키마를 통과하는지 검증 (`jsonschema` 등).

별도 프로젝트는 이 레포의 **`schemas/`만 submodule·복사·URL 고정**으로 가져가도 됩니다.
