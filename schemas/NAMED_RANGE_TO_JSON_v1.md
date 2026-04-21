# Named Range → JSON (`lbo_dashboard_export` v1.0)

Excel 워크북 **`8_Dashboard`** 및 연결 시트에 정의된 **`DASH_*`** 이름을 `lbo_dashboard_export_v1.schema.json`이 기대하는 **중첩 JSON**으로 옮길 때의 1:1 매핑이다.  
(이름 정의는 주로 `7_Returns_LTV` + `8_Dashboard` 빌더 코드에 있으며, 빌드 산출물 기준 **79개** `DASH_*`.)

| Excel Named Range | JSON 경로 | 비고 |
|-------------------|-----------|------|
| `DASH_Case` | `scenario.case` | `Case_Switch`와 동일 값 |
| `DASH_Version` | `scenario.template_version` | 예: `v0.5` |
| `DASH_Valuation_Method1_Label` | `valuation_methods[0].label` | `method_index` 1 |
| `DASH_Valuation_Method1_Multiple` | `valuation_methods[0].multiple` | |
| `DASH_Valuation_Method1_EV` | `valuation_methods[0].ev` | KRW mn |
| `DASH_LTV_Method1_Opco` | `valuation_methods[0].opco_ltv` | 소수(0.45=45%) |
| `DASH_LTV_Method1_Cumulative` | `valuation_methods[0].cumulative_ltv` | |
| `DASH_Valuation_Method2_Label` | `valuation_methods[1].label` | `method_index` 2 |
| `DASH_Valuation_Method2_Multiple` | `valuation_methods[1].multiple` | |
| `DASH_Valuation_Method2_EV` | `valuation_methods[1].ev` | |
| `DASH_LTV_Method2_Opco` | `valuation_methods[1].opco_ltv` | |
| `DASH_LTV_Method2_Cumulative` | `valuation_methods[1].cumulative_ltv` | |
| `DASH_Valuation_Method3_Label` | `valuation_methods[2].label` | `method_index` 3 |
| `DASH_Valuation_Method3_Multiple` | `valuation_methods[2].multiple` | |
| `DASH_Valuation_Method3_EV` | `valuation_methods[2].ev` | |
| `DASH_LTV_Method3_Opco` | `valuation_methods[2].opco_ltv` | |
| `DASH_LTV_Method3_Cumulative` | `valuation_methods[2].cumulative_ltv` | |
| `DASH_Div_FY1` | `coverage.dividend_received_by_fy[0]` | KRW mn |
| `DASH_Div_FY2` | `coverage.dividend_received_by_fy[1]` | |
| `DASH_Div_FY3` | `coverage.dividend_received_by_fy[2]` | |
| `DASH_Div_FY4` | `coverage.dividend_received_by_fy[3]` | |
| `DASH_Div_FY5` | `coverage.dividend_received_by_fy[4]` | |
| `DASH_ICR_Holdco_Min` | `coverage.icr_holdco_min` | |
| `DASH_ICR_Opco_Min` | `coverage.icr_opco_min` | |
| `DASH_DSCR_Min` | `coverage.dscr_opco_min` | 스키마 필드명 `dscr_opco_min` |
| `DASH_Lev_NetLeverage_FY1` | `coverage.net_leverage_by_fy[0]` | |
| `DASH_Lev_NetLeverage_FY2` | `coverage.net_leverage_by_fy[1]` | |
| `DASH_Lev_NetLeverage_FY3` | `coverage.net_leverage_by_fy[2]` | |
| `DASH_Lev_NetLeverage_FY4` | `coverage.net_leverage_by_fy[3]` | |
| `DASH_Lev_NetLeverage_FY5` | `coverage.net_leverage_by_fy[4]` | |
| `DASH_CFTable_Row1_Label` | `cashflow_summary_table[0].label` | `row_index` 1 |
| `DASH_CFTable_Row1_FY1` | `cashflow_summary_table[0].fy1` | |
| `DASH_CFTable_Row1_FY2` | `cashflow_summary_table[0].fy2` | |
| `DASH_CFTable_Row1_FY3` | `cashflow_summary_table[0].fy3` | |
| `DASH_CFTable_Row1_FY4` | `cashflow_summary_table[0].fy4` | |
| `DASH_CFTable_Row1_FY5` | `cashflow_summary_table[0].fy5` | |
| `DASH_CFTable_Row2_Label` | `cashflow_summary_table[1].label` | `row_index` 2 |
| `DASH_CFTable_Row2_FY1` | `cashflow_summary_table[1].fy1` | |
| `DASH_CFTable_Row2_FY2` | `cashflow_summary_table[1].fy2` | |
| `DASH_CFTable_Row2_FY3` | `cashflow_summary_table[1].fy3` | |
| `DASH_CFTable_Row2_FY4` | `cashflow_summary_table[1].fy4` | |
| `DASH_CFTable_Row2_FY5` | `cashflow_summary_table[1].fy5` | |
| `DASH_CFTable_Row3_Label` | `cashflow_summary_table[2].label` | `row_index` 3 |
| `DASH_CFTable_Row3_FY1` | `cashflow_summary_table[2].fy1` | |
| `DASH_CFTable_Row3_FY2` | `cashflow_summary_table[2].fy2` | |
| `DASH_CFTable_Row3_FY3` | `cashflow_summary_table[2].fy3` | |
| `DASH_CFTable_Row3_FY4` | `cashflow_summary_table[2].fy4` | |
| `DASH_CFTable_Row3_FY5` | `cashflow_summary_table[2].fy5` | |
| `DASH_CFTable_Row4_Label` | `cashflow_summary_table[3].label` | `row_index` 4 |
| `DASH_CFTable_Row4_FY1` | `cashflow_summary_table[3].fy1` | |
| `DASH_CFTable_Row4_FY2` | `cashflow_summary_table[3].fy2` | |
| `DASH_CFTable_Row4_FY3` | `cashflow_summary_table[3].fy3` | |
| `DASH_CFTable_Row4_FY4` | `cashflow_summary_table[3].fy4` | |
| `DASH_CFTable_Row4_FY5` | `cashflow_summary_table[3].fy5` | |
| `DASH_CFTable_Row5_Label` | `cashflow_summary_table[4].label` | `row_index` 5 |
| `DASH_CFTable_Row5_FY1` | `cashflow_summary_table[4].fy1` | |
| `DASH_CFTable_Row5_FY2` | `cashflow_summary_table[4].fy2` | |
| `DASH_CFTable_Row5_FY3` | `cashflow_summary_table[4].fy3` | |
| `DASH_CFTable_Row5_FY4` | `cashflow_summary_table[4].fy4` | |
| `DASH_CFTable_Row5_FY5` | `cashflow_summary_table[4].fy5` | |
| `DASH_CFTable_Row6_Label` | `cashflow_summary_table[5].label` | `row_index` 6 |
| `DASH_CFTable_Row6_FY1` | `cashflow_summary_table[5].fy1` | |
| `DASH_CFTable_Row6_FY2` | `cashflow_summary_table[5].fy2` | |
| `DASH_CFTable_Row6_FY3` | `cashflow_summary_table[5].fy3` | |
| `DASH_CFTable_Row6_FY4` | `cashflow_summary_table[5].fy4` | |
| `DASH_CFTable_Row6_FY5` | `cashflow_summary_table[5].fy5` | |
| `DASH_CFTable_Row7_Label` | `cashflow_summary_table[6].label` | `row_index` 7 |
| `DASH_CFTable_Row7_FY1` | `cashflow_summary_table[6].fy1` | |
| `DASH_CFTable_Row7_FY2` | `cashflow_summary_table[6].fy2` | |
| `DASH_CFTable_Row7_FY3` | `cashflow_summary_table[6].fy3` | |
| `DASH_CFTable_Row7_FY4` | `cashflow_summary_table[6].fy4` | |
| `DASH_CFTable_Row7_FY5` | `cashflow_summary_table[6].fy5` | |
| `DASH_CFTable_Row8_Label` | `cashflow_summary_table[7].label` | `row_index` 8 |
| `DASH_CFTable_Row8_FY1` | `cashflow_summary_table[7].fy1` | |
| `DASH_CFTable_Row8_FY2` | `cashflow_summary_table[7].fy2` | |
| `DASH_CFTable_Row8_FY3` | `cashflow_summary_table[7].fy3` | |
| `DASH_CFTable_Row8_FY4` | `cashflow_summary_table[7].fy4` | |
| `DASH_CFTable_Row8_FY5` | `cashflow_summary_table[7].fy5` | |
| `DASH_IRR_Sponsor` | `sponsor_irr` | v0.5 placeholder 허용(null) |

## 선택 필드

| Excel Named Range | JSON 경로 | 비고 |
|-------------------|-----------|------|
| (전체 `DASH_*` 키–값) | `flat_named_ranges` | 디버그·라운드트립용, Word 채움에 필수 아님 |

## 스키마·예시 파일

- 스키마: [`lbo_dashboard_export_v1.schema.json`](lbo_dashboard_export_v1.schema.json)
- 구조 참고용 예시(수치는 더미): [`examples/lbo_dashboard_export_v1.example.json`](examples/lbo_dashboard_export_v1.example.json) — **재계산된 실제 `.xlsx`에서 뽑은 값 예시는 별도로 추가**하면 계약 고정에 유리하다.
