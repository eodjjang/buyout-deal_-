# LBO Stress Template Builder v0.5

Python으로 13탭 LBO 스트레스 워크북(`dist/LBO_Stress_Template_v0.5.xlsx`)을 생성한다. KRW 백만원 기준, VBA 미사용.

## 설치 + 빌드

```bash
python -m pip install -e ".[dev]"
python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx
```

## 테스트

```bash
pytest -v
```

## 수기 검증 (처음 한 번)

먼저 위 빌드 명령으로 `dist/LBO_Stress_Template_v0.5.xlsx`를 만든 뒤, Excel에서 다음을 수행한다.

1. `dist/LBO_Stress_Template_v0.5.xlsx` 열기 → **13개 탭** 확인
2. `1_Input_BaseCase`의 `B5`부터 Section A에 임의 숫자 입력 (EV 100,000 / Net Debt 30,000 / Fee 2,000 / Senior 40,000 / 2nd 15,000 / Holdco 15,000 / Target Lev 6.0 등)
3. Section B에 Revenue/EBITDA/Capex/NWC 8개 FY 더미 숫자 입력
4. `1_Input_BaseCase!B18` (Sources−Uses 체크) = **0** 확인
5. `2_Stress_Panel!B3`에서 드롭다운으로 "Downside" 선택 → `8_Dashboard`의 LTV·DSCR·ICR이 즉시 갱신되는지 확인
6. "Base"로 되돌리고 `9a_CIQ_Trading_Raw!B3:B17`에 Ticker 5개 입력 (예: 005930.KS, 000660.KS, 035420.KS)
7. `Data → Refresh All` (Plug-in 미설치 PC는 스킵; 구조만 확인)
8. `File → Options → Formulas → Enable iterative calculation`이 OFF인 상태에서 순환참조 에러 배너 없는지 확인
9. `Formulas → Error Checking` 실행 후 에러 0건 확인
10. `8_Dashboard` 모든 named range 셀에 `#REF!` 없는지 훑기

## v0.6 로드맵 (Golden Test Fixture)

1. 과거 마감된 딜 1건으로 입력 셀 전부 채운 `.xlsx` 생성
2. 그 파일의 `8_Dashboard` 출력값 스냅샷을 `tests/fixtures/goldentest_v05.json`에 기록
3. 빌더 리그레션 시 스냅샷 불변 자동 검증

## Design & Plan Docs

- Design v0.5: `.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md`
- Plan: `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`
