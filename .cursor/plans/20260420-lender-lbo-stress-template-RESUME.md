# LBO Stress Template — 실행 재개 (Session Handoff)

> 이 문서는 `subagent-driven-development` 스킬로 `20260420-lender-lbo-stress-template-plan.md`를 실행하던 세션이 컨텍스트 한계로 중단될 때, **새 채팅 세션이 그대로 이어서 진행**하기 위한 상태 스냅샷입니다.

**마지막 갱신**: 2026-04-21 — `feat/lbo-template-v0.5` → **`main` 로컬 머지 + `origin/main` 푸시 완료** (`9f88a61`). 후속 하드닝 `30cb034` (전 시트 `define_name` 통일, DCF `PV(TV)` 지수 → `J11` 참조, `goldentest_v05.json` 수식 골든, README에 CI/Excel 한계 명시). `pytest` **72 passed**. 태그 **`v0.5.0`** 원격 푸시됨. Final 리뷰 당시 Important 항목은 상기 커밋으로 **대부분 소진**; **수기 Excel 10단계**·v0.6 **재계산 값** 골든은 여전히 **선택 후속**.

---

## TL;DR — 새 세션 즉시 재개 프롬프트

아래 문장을 새 채팅에 그대로 붙여넣으세요.

```
.cursor/plans/20260420-lender-lbo-stress-template-RESUME.md 를 읽고 §1·§5·§8 상태를 확인해줘.
플랜 구현은 완료·main 반영됨 → §5의 후속(수기 검증, v0.6, 워크트리 정리 등) 또는 사용자 지시를 따른다.
```

**또는** 채팅에서 `@20260420-lender-lbo-stress-template-RESUME.md` 첨부 후 `§1·§5·§8 확인해줘` 정도로 요청. (플랜 **재실행**이 아니라 **후속·수기 검증**이면 §5.1 참고.) 규칙 `.cursor/rules/lbo-stress-template-handoff.mdc`는 glob이 열릴 때 보강한다 — 내용이 RESUME과 어긋나면 **RESUME 우선**.

---

## § 자동 저장 / 핸드오프 프로토콜 (Task 6 ~ Task 16)

**한계**: Cursor는 Task 종료 시 새 창을 열거나, 채팅에 프롬프트를 **자동으로 넣어주는 API가 없다**. 대신 아래를 **매 Task 완료 직후** 컨트롤러가 실행하면, **새 세션에서 파일만 참조하면 곧바로 이어질 수 있다**.

### 매 Task 종료 시 컨트롤러 체크리스트 (같은 턴에서 처리)

1. `buyout-deal-lbo-impl` 워크트리: `git status` clean, `python -m pytest tests/ -v` 전부 통과, 최신 커밋 메시지·SHA 확인.
2. **이 RESUME 파일**을 갱신한다:
   - 상단 **「마지막 갱신」** 한 줄 (완료 Task 번호, spec/code review·polish 여부).
   - **§1** 저장소 상태(HEAD, 테스트 개수, 브랜치).
   - **§3** 완료 Task 요약(해당 Task만 추가/갱신).
   - **§5** 다음 Task용 implementer 요약·프롬프트 힌트·예상 테스트 개수.
   - **§6** 표에서 진행 행 업데이트.
   - **§8** 확인 명령 기대값(HEAD, pytest tail)을 다음 Task 기준으로 수정.
3. **TL;DR 블록**은 변경하지 않는다(고정 템플릿 유지).
4. **선택**: 메인 저장소 `git add` + `git commit`으로 RESUME·규칙 파일을 커밋하면 다른 클론/PC에서도 동일 핸드오프가 된다.

### 새 창에서 “거의 자동”으로 이어가는 방법

| 방법 | 설명 |
|------|------|
| `Ctrl+L` 새 채팅 후 `@` | `20260420-lender-lbo-stress-template-RESUME.md` 첨부 → 한 줄 지시 |
| TL;DR 붙여넣기 | 위 코드 블록 전체를 새 채팅에 붙여넣기 |
| 파일 고정 | RESUME을 에디터 탭에 열어두고 새 채팅에서 `@`로 참조 |

---

## 1. 저장소 상태 (**2026-04-21 갱신** — 머지·푸시 반영)

### 워크트리

| 항목 | 값 |
|---|---|
| 주 저장소 (메인) | `C:\vibecoding\works\buyout deal_모델분석\` — **`main` @ `9f88a61`**, `origin/main`과 동기화됨 (`git push` 완료) |
| (선택) 링크 워크트리 | `C:\vibecoding\works\buyout-deal-lbo-impl\` — 기존에 `feat/lbo-template-v0.5`를 체크아웃했을 수 있음. **패키지 소스는 이제 메인 클론에도 동일하게 존재** |

**이전 관행**: 구현 전용 워크트리 분리. **현재**: `main`에 `src/lbo_template`·`tests`·`pyproject.toml`가 합쳐졌으므로, 후속 작업은 **메인 폴더**에서 `pytest`/`build` 해도 된다. 플랜·RESUME·`.cursor` 문서 수정은 메인에서 유지. 메인 트리는 PowerShell — 커맨드 체이닝은 `;` (`&&` 비권장).

### 커밋 체인 (`feat/lbo-template-v0.5`)

```
f969309 docs: v0.5 README with verification steps and v0.6 roadmap                            ← Task 18 (+ tag v0.5.0)
b45e058 test(integrity): clarify self-ref heuristic docstring + guard Sources-Uses formula type   ← Task 17 polish
fc83825 test: add end-to-end integrity checks for named ranges, circular refs, MAX(0,...) discipline ← Task 17
7d54ec5 chore(s8_dashboard): normalize outflow signs + add scalar/formula contract tests          ← Task 16 polish
76bd740 feat(s8_dashboard): 5 summary tables + full DASH_* named range cluster (CFTable 8x5)      ← Task 16
b3d176c chore(conventions): add define_name helper + migrate s7 to use it                         ← Task 16 선행 리팩토 (M3)
ece0f88 chore(s7_returns_ltv): polish row-range comments + add anchor/row-formula contract tests   ← Task 15 polish
4d99510 feat(s7_returns_ltv): abstracted Method 1/2/3 with 8-type dropdown and 9-col LTV          ← Task 15
0f4a712 feat(s9_peer): unified Trading+Transaction summary with Applied_* named ranges   ← Task 14
97a521d feat(s9c): Manual Supplement with Source dropdown and auto-Reliability lookup   ← Task 13
cee5eab feat(s9b): Transaction Comps zone with 500-row capacity and overflow warning   ← Task 12
4ad62bd feat(s9a): CIQ Plug-in primary formulas, Mode cell, Paste Fallback warning, 15-col headers   ← Task 11
0e98ffa feat(s6_dcf): FCFF with mid-year 0.5-4.5, Gordon TV at 5.0, Active_WACC_Uplift wiring   ← Task 10
3ee6117 feat(s5_waterfall): UFCF→Div→Holdco cascade with Opco_Sweep_Avail and KPI row named ranges   ← Task 9
8e6b31d feat(s4_debt): Opco Senior / 2nd / Holdco schedules with sweep + Holdco PIK toggle   ← Task 8
d7bb4d5 feat(s3_overlay): cascade Stressed Rev/EBITDA/Capex/NWC/UFCF from Active_* deltas   ← Task 7
e42788c feat(s2_stress): add Case_Switch + 7-param table with Active_* named ranges and dropdown validations   ← Task 6
b993595 chore(s1_input): add formula/named-range contract tests + font name polish      ← Task 5 polish
55ab68f feat(s1_input): implement Section A/B/C with dual check rows and named ranges   ← Task 5
4ea6b00 feat(s0_readme): populate README with versioning, conventions, Preconditions    ← Task 4
95005e1 feat(skeleton): scaffold 13-tab workbook with empty sheet builders               ← Task 3
cb86b2c feat(conventions): add color/font/format constants and style helpers per design §0  ← Task 2
c6a36d7 chore: polish bootstrap scaffolding nits (argparse, future-annotations, gitignore, readme quoting)
459ef8b chore: bootstrap lbo-template package with openpyxl and pytest                   ← Task 1
6db3d2b 플랜 추가                                                                          ← main과 공통 베이스
1d69bcb Initial commit
```

### 현재 테스트 상태

```
pytest tests/ -v  →  72 passed
```
- `test_bootstrap.py` — 3
- `test_conventions.py` — 5
- `test_golden_snapshot.py` — 1 (`tests/fixtures/goldentest_v05.json` 수식 스냅샷; 머지 후 `30cb034`)
- `test_s0_readme.py` — 3
- `test_s1_input.py` — 9
- `test_s2_stress.py` — 7 (Task 6)
- `test_s3_overlay.py` — 3 (Task 7)
- `test_s4_debt.py` — 4 (Task 8)
- `test_s5_waterfall.py` — 3 (Task 9)
- `test_s6_dcf.py` — 4 (Task 10)
- `test_s7_returns_ltv.py` — 6 (Task 15: 플랜 4 + polish contract 2)
- `test_s8_dashboard.py` — 7 (Task 16: 플랜 4 + polish contract 3)
- `test_s9_ciq_and_peer.py` — 10 (Tasks 11–14: 9a 3 + 9b 2 + 9c 2 + Peer 3)
- `test_integrity.py` — 7 (Task 17)

---

## 2. 실행 결정 사항 (사용자 승인 완료)

| 결정 | 선택 | 근거 |
|---|---|---|
| 작업 위치 | **1-B 워크트리 격리** | 롤백 안전, 메인 브랜치 깨끗하게 유지 |
| 모델 할당 | **2-A 전체 동일 (부모 상속)** | 결정 부담 없음, 균일 품질 |
| 리뷰 루프 | **implementer → spec → code 3단**, Nit은 선택 적용 | 스킬 표준 |
| 병렬 디스패치 | Wave 3 (Tasks 11/12/13)에서만 단일 메시지 3×`Task` | 독립 분기 |

### Nit 적용 정책

- **Important**: 즉시 수정 후 재리뷰
- **Nit (code-reviewer APPROVED인 경우)**: 즉시 적용 가능한 저비용(≤1분) 것만 폴리시 커밋, 나머지는 후속 Task 착수 전 TODO
- 적용 여부는 컨트롤러가 판단 (사용자 물음 없이)

---

## 3. 완료 Task

### ✅ Task 1: 프로젝트 부트스트랩
- Commits: `459ef8b` + polish `c6a36d7`
- 8 files, 2 tests passing
- **Polish 적용된 Nits**: N2, N3, N7, N9
- **Deferred Nits**: N1 version SSOT, N4 `tests/__init__.py` 제거, N5 fixture scope 재설계(mutate 시 필요), N6 `wb.active` Optional 가드, N8 pyproject metadata

### ✅ Task 2: 엑셀 스타일 컨벤션 모듈
- Commit: `cb86b2c`
- 2 files, 4 tests passing (10 COLOR + 6 NUM_FMT + 3 FY_AXIS 상수, 17 헬퍼)
- **Code-reviewer 판정**: ✅ APPROVED with 4 Nits (전부 non-blocking)
- **Deferred Nits**:
  - Nit 1: `apply_*` 헬퍼 behavioral test — Task 4+ 진행 중 리그레션 시 추가
  - Nit 2: `cell` 파라미터 타입힌트 — mypy 도입 시
  - Nit 3: `FY_AXIS_COLUMNS`/`LABELS` tuple화 — 전역 mutate 방지
  - Nit 4: Font 팩토리 DRY 헬퍼

### ✅ Task 3: 13-탭 스켈레톤 + layout.py
- Commit: `95005e1` (17 files, +231/-1)
- `layout.py` (13 SHEET_* 상수 + `ALL_SHEETS` + 7 anchor 상수), `sheets/__init__.py`, 13 시트 stub, `build.py` 업데이트, `test_bootstrap.py` 확장
- 3 tests passing (`test_all_13_sheets_created_in_correct_order` 추가)
- **Code-reviewer 판정**: ✅ APPROVED, 6 Nits (전부 stylistic/non-blocking)
- **Tab order 결정**: `ALL_SHEETS` 순서대로 `create_sheet` 호출 (s0…s8, s9a, s9b, s9c, s9_peer). Python 시트 생성 순서 ≠ 수식 의존성.
- **Argparse polish 보존됨** (`prog`, `description`).
- **Deferred Nits**:
  - Nit 1: stub들의 `from openpyxl.workbook import Workbook` → 표준 공개 API `from openpyxl import Workbook`로 정리. **T5~T16에서 각 stub을 본격 구현할 때 같이 전환** 권장.
  - Nit 2: 13 stub + `sheets/__init__.py`에 `from __future__ import annotations` 미포함 → 같은 시점에 추가.
  - Nit 3~6: 현재 form 유지 (reviewer가 "fine" / "no action needed" 표기).
  - **플랜 Step 4 코드블록의 tab 순서와 Step 5 테스트 충돌** — 플랜 파일 자체는 수정하지 않고 RESUME에 기록 (역사 보존).

### ✅ Task 4: 0_README 시트
- Commit: `4ea6b00` (2 files, +101/-1)
- `s0_readme.py`: 9→79 lines, 6 섹션 (Version History / Conventions / Preconditions / CapIQ Saved Screen / Alt-A 재배포 / Sheet Map) × bullet lines. `apply_section_header`로 A1, `Font(bold=True, size=11)` + `Alignment(wrap_text=True, vertical="top")`로 본문.
- `test_s0_readme.py`: 3 tests passing
- **Code-reviewer 판정**: ✅ APPROVED, I-1 1건 + 6 Nit (모두 non-blocking)
- **플랜 자체 버그 2건 해결** (문서화됨):
  - 플랜 Step 1 test 3은 col A를 스캔, Step 3 impl은 bullet을 col B에 기록 → **test 3을 col B 스캔으로 수정** (시각적 레이아웃 의도 보존).
  - 플랜 Step 3가 `c.Font`/`c.Alignment` 사용하나 `conventions.py`는 재-export하지 않음 → **`from openpyxl.styles import Font, Alignment` 직접 import**. (플랜 문서 L772–784도 이 교정을 이미 인지하고 있음)
- **Task 5 착수 전 결정 (적용 완료, T5에서 채택)**:
  - **Font/Alignment House Style**: 모듈 상수 호이스트 채택 (T5 `_SECTION_TITLE_FONT` 패턴). `conventions.py` 확장은 **T6에서 2번째 호출자 확인 후 결정** (YAGNI 유지).
- **Deferred Nits**:
  - N-1: `range(1, 60)` / `range(1, 80)` 테스트 바운드 느슨 — 향후 `ws.max_row+1`로 정리 가능.
  - N-5: sheet-map bullet 텍스트가 `layout.py`의 `SHEET_*` 상수와 디커플링 — 시트명 리네임 시 수동 동기화 필요. (design-doc-pin이라 churn 가능성 낮음)
  - N-2/N-3/N-4/N-6: 현재 form 유지.

### ✅ Task 5: `1_Input_BaseCase` 시트
- Commits: `55ab68f` (impl) + `b993595` (polish, 리뷰어 Important 1건 + cheap Nits 2건 반영)
- 2 files (`s1_input_base.py` 9→167행, `tests/test_s1_input.py` 신규 100행), 9 tests passing
- **Spec reviewer 판정**: ✅ APPROVED — 7 requirement groups (Section A/B/C, dual check, named ranges, house style, plan-bug #1/#2/#3) 전부 코드 인스펙션으로 검증
- **Code reviewer 판정**: ✅ APPROVED with 1 Important + 7 Nit
  - Important: 테스트 커버리지 — 체크 row 수식·Section C IFERROR 템플릿·Named Range 어느 것도 *값* 검증 없음 → polish 커밋(`b993595`)에서 3 contract 테스트 추가 (`test_check_formulas`, `test_section_c_formula_shape`, `test_named_ranges`).
  - Cheap Nits 적용: (1) `_SECTION_TITLE_FONT`에 `name="Calibri"` 추가, (2) `range(39, 48)` → `range(40, 45)` 타이트닝.
- **플랜 자체 버그 3건 해결** (T5 implementer 프롬프트에 사전 인젝션, 코드에 `# CORRECTION #N` 주석):
  - **#1**: Plan Step 3가 row 19 라벨을 `"Check: Target Leverage (...)"`로 작성했지만 `test_dual_check_rows`는 `"Target Leverage Check"` 부분문자열을 assert. → 라벨을 `"Target Leverage Check ((Senior+2nd+Holdco)/LTM EBITDA ≤ Target)"`로 수정.
  - **#2**: Plan Step 3가 EBITDA 환원 Note를 row 33에 두고 라벨에 `"Adjusted"` 단어 포함 → `test_section_b_ebitda_is_reported`가 `range(24, 35)`에서 `"Adjusted"` 미존재를 assert하므로 충돌. → Note를 row 35로 이동(merge `B35:I35`), 라벨에서 "Adjusted" 제거 (`"Note (EBITDA 환원 내역, Mgmt vs Bank Case 등)"`).
  - **#3**: Plan Step 3 Section C 루프에서 `if "prev" in template`로 placeholder 검사 (literal "prev" 부분문자열 — 취약). → `if "{prev}" in template`로 명시적 brace 매칭. 또한 FY-2 YoY 셀에 `cell.value = ""` 대신 `continue`로 처리하여 None 유지 (test_section_c_formula_shape가 `is None` assert).
- **Deferred Nits (T6 착수 전 검토)**:
  - **N-typehint**: `SECTION_A_ROWS: list[tuple[str, str | None, bool]]` 같은 타입 힌트는 cross-module import 시작 시점(아마 T8 또는 T16)에 추가.
  - **N-row-constants**: `ROW_LTM_EBITDA = 27`, `ROW_TARGET_LEV = 14` 등 모듈 상수화 — T6가 cross-sheet 참조 본격 시작 시 결정.
  - **N-_dn-helper**: 7개 named range 등록 패턴 (`f"'{SHEET_INPUT}'!$X$N"`) DRY 헬퍼. T6에서 named range가 추가로 7개 더 늘면 도입.
  - **N-build-docstring**: `s0_readme.py`와 일관성 위해 보류.
  - **N-num-format-tuple**: Section A 번호 포맷 분기를 `SECTION_A_ROWS` 튜플의 4번째 필드로 통합. T6/T7에서 동일 패턴 반복되면 채택.
  - **N-ws-cell-style**: `ws["A1"]=` vs `ws.cell(row=18, column=1, value=)` 혼용 — 의식적 통일 필요.

### ✅ Task 6: `2_Stress_Panel` 시트
- Commit: `e42788c`
- `s2_stress_panel.py`: `Case_Switch` (`DefinedName` → `'2_Stress_Panel'!$B$3`), 산업 프리셋 DV, `PARAM_ROWS` 7행 + `SWITCH` 기반 Active 열, `apply_key_output` on Active(F), named ranges 8개.
- `tests/test_s2_stress.py`: 플랜 6개 + `test_active_named_ranges_attr_text` contract.

### ✅ Task 7: `3_Operating_Overlay` 시트
- Commit: `d7bb4d5`
- **플랜 Step 3 템플릿 행 번호 교정**: 설계 §3에 맞춰 오버레이 시트 **고정 행 그리드 r5~r19** (Base Revenue … UFCF)로 수식 참조 정리. 플랜 코드블록의 `{c}6/{prev}6` 등은 순환 참조/오행 참조가 되어 **컨트롤러 구현에서 수정**함 (`Base YoY` → `{c}5/{prev}5`, `Stressed Revenue` → `{prev}8*(1+{c}7)` 등).
- `tests/test_s3_overlay.py`: 플랜 3개 테스트.

### ✅ Task 8: `4_Debt_Schedule` 시트
- Commit: `8e6b31d`
- `s4_debt.py`: 3 트랜치(Senior r5~, 2nd r15~, Holdco r25~), `TRANCHE_ROWS` 6행, FY1~FY5 수식; Senior/2nd Cash Sweep에 `IFERROR(Opco_Sweep_Avail_{col},0)` 및 2nd에서 Senior 스윕 차감(`r-10`); Holdco `Holdco_PIK_Mode` + Ending 분기; `Holdco_PIK_Mode`·`Sweep_Pct`·`Opco_Sr_Interest` 등 named ranges.
- 트랜치 블록 헤더는 `c.apply_section_header` (플랜의 이중 `Font(bold=True)` 제거). A35/A37 라벨은 `_SECTION_TITLE_FONT` + `Alignment` (s2 패턴).
- `tests/test_s4_debt.py`: 플랜 4개 테스트.

### ✅ Task 9: `5_CF_Waterfall` 시트
- Commit: `3ee6117`
- `s3_overlay.py`: `FIRST_DATA_ROW`, `UFCF_ROW`, `STRESSED_EBITDA_ROW` (ROWS 인덱스 6 → 행 11) 추가.
- `s5_waterfall.py`: 메인 워터폴 r5~r18, KPI r21~r24, `Opco_Sweep_Avail_E..I` 단일 셀 named range(r14), KPI named ranges + `Dividend_Row`, Net Leverage 분모는 Stressed EBITDA 행(`STRESSED_EBITDA_ROW`), 분자는 부채 엔딩 r11/r21/r31. Holdco ICR 행 `E18:I18` 조건부 서식.
- `tests/test_s5_waterfall.py`: 플랜 3개 테스트.

### ✅ Task 10: `6_DCF_Valuation` 시트
- Commit: `0e98ffa`
- `s3_overlay.py`: `STRESSED_CAPEX_ROW`(13), `STRESSED_NWC_ROW`(15), `OVERLAY_CASH_TAXES_ROW`(18) 추가.
- `s6_dcf.py`: FY1~FY5(E~I)+TV(J), FCFF 브리지·mid-year 할인·Gordon TV(J14)·PV TV(J15)·EV(E17)·Equity(E20), `Base_WACC`/`DCF_EV`/`DCF_Equity_Value`. Cash Taxes DCF 라인은 플랜 `!{c}20` 대신 오버레이 **Cash Taxes 18행** 링크.
- `tests/test_s6_dcf.py`: 플랜 4개 테스트.

### ✅ Task 11: `9a_CIQ_Trading_Raw` 시트
- Commit: `4ad62bd`
- `s9a_ciq_trading.py`: 15열 헤더(r2), Mode `B1`(ISFORMULA(C3)), Last Refresh `D1`=NOW, peer 행 3–17에 `CIQ`/`IFERROR` 수식, `P`열 통화 경고, `apply_ciq`/숫자포맷 컨벤션.
- `tests/test_s9_ciq_and_peer.py`: 9a 계약 테스트 3개 신설.

### ✅ Task 12: `9b_CIQ_Transaction_Raw` 시트
- Commit: `cee5eab`
- `s9b_ciq_transaction.py`: 15열 헤더, Mode `B1`(ISFORMULA(D3)), `C1` 500행 초과 경고(COUNTA), 행 3–5 `A`열 `CIQTRANSACTION` 예시, 행 6–501 Paste/input 존.
- 동일 테스트 파일에 9b 테스트 2개 추가.

### ✅ Task 13: `9c_Manual_Supplement` 시트
- Commit: `97a521d`
- `s9c_manual.py`: 9b와 동형 15열 + Source/Reliability/Include/Memo, 행 50–56 기본 맵, `P` Source DV, `Q` Reliability `XLOOKUP`+DV, `R` Include `XLOOKUP`.
- 동일 테스트 파일에 9c 테스트 2개 추가.

### ✅ Task 14: `9_Peer_Summary` 시트
- Commit: `0f4a712`
- `s9_peer_summary.py`: Trading 블록(9a 링크 6–20행)·집계 22–24·`C27`/`G27` Applied Trading Multiple·PBR, Transaction 블록(9b 33–52, 9c 53–62)·`F65`–`F67`·`Applied_Transaction_Multiple`; `Applied_Trading_Multiple`/`Applied_Trading_PBR`/`Applied_Transaction_Multiple` named ranges.
- `tests/test_s9_ciq_and_peer.py`: Peer 계약 테스트 3개 추가.

### ✅ Task 15: `7_Returns_LTV` 시트
- Commits: `4d99510` (impl, 플랜 Step 2 verbatim) + `ece0f88` (polish — 코드 리뷰어 APPROVED with polish의 M1/M6 반영)
- `s7_returns_ltv.py`: 9→180 행. Method Declaration Block(rows 3–6) + 9-Column LTV Table(rows 9–13) + anchors(D27 `=LTM_EBITDA`, B28 `Target_Ownership=1.0`). `METHOD_TYPES` 8종 + `DEFAULTS` 3행, 단일 `DataValidation`을 `C4:C6`에 적용. D/E열 `SWITCH(C{r}, ...)` 수식 2벌(Multiple·Base Metric), LTV 행 `D{r}=IFERROR(SWITCH(C{method_r}, "DCF_Stressed",DCF_Equity_Value, ..., D{method_r}*LTM_EBITDA),"")` + F/H/J `IFERROR(...)` 가드.
- **신규 Named Ranges (16개)**: `Target_Ownership` + `DASH_Valuation_Method{1,2,3}_{Label,Multiple,EV}` (9) + `DASH_LTV_Method{1,2,3}_{Opco,Cumulative}` (6).
- `tests/test_s7_returns_ltv.py`: 플랜 4개(`test_three_method_rows`, `test_method_type_dropdown`, `test_named_ranges_method_abstraction`, `test_method_type_switch_formula`) + polish 2개(`test_ltv_anchors_and_target_ownership`, `test_ltv_row_formulas_wire_correctly`) = 6 tests.
- **Spec reviewer 판정**: ✅ APPROVED — R1–R8 전 요구사항 코드 인스펙션으로 검증. commit은 git reflog fallback으로 확인.
- **Code reviewer 판정**: ✅ APPROVED with polish — Critical/Important 0건, M1(주석 드리프트)·M6(D27·Target_Ownership·F/G/H/I/J 행 수식 contract 갭) cheap polish만 반영.
- **Deferred Nits (후속 Task에서 검토)**:
  - **M2 — 행 상수 호이스트**: `METHOD_DECL_START = 4`, `LTV_DATA_START = 11`, `LTM_ANCHOR_ROW = 27`, `TARGET_OWN_ROW = 28`. 두 블록 결합(`=B{method_r}`) 있어 행 이동 시 리스크 현실화. Task 17 Integrity·Task 18 리팩토 단계에서 함께 검토.
  - **M3 — `_dn` 헬퍼**: `wb.defined_names[name] = DefinedName(name, attr_text=...)` 패턴이 s1/s2/s4/s5/s6/s9/s7에서 누적 ~30+회. `conventions.py`에 `define_name(wb, name, ref)` 2-line 헬퍼 도입 기회. **Task 16이 `DASH_*` ~60개 등록 예정이라 T16 착수 직전에 먼저 헬퍼 추가하는 것이 더 큰 이득** (T16 프롬프트에서 도입 여부 사용자에 묻지 말고 컨트롤러가 판단).
  - **M5 — SWITCH/METHOD_TYPES 동기화 가드 주석**: METHOD_TYPES에 9번째 항목 추가 시 SWITCH 2벌이 silent fallthrough. 1줄 가드 주석. 가중치 낮음.
  - **M7 — `F{r}` 메모 placeholder**: free-form 의도지만 미래 독자용 trailing 주석. 낮음.
  - **M8 — `dv_mt.add("C4:C6")` 1회 호출**: micro-nit.

---

### ✅ Task 16: `8_Dashboard` 시트 + 선행 리팩토 (`define_name` 헬퍼)

- Commits: `b3d176c` (선행 리팩토 — T15 Deferred Nit M3 소화) + `76bd740` (impl, 플랜 §Task 16 + 컨트롤러 5건 교정) + `7d54ec5` (polish, code reviewer Important #1/#2 + Nits #3–#6 반영)
- `conventions.py`: `define_name(wb, name, ref)` 헬퍼 추가 (s7 5개 사이트 마이그레이션으로 회귀 없음 검증). Task 16에서 64× DASH_* 등록이 3줄→1줄로 압축.
- `s8_dashboard.py`: 9→234 행. 5개 표 + CFTable 8×5 + Scenario meta + IRR placeholder.
  - 표 1 Valuation 요약 (A6, r7–r10): 3 평가방식 × 6 열 (Label/Multiple/EV/LTV_Opco/LTV_Cumulative) ← s7 `DASH_Valuation_Method*_*` / `DASH_LTV_Method*_*` 참조.
  - 표 2 이자지급가능성 (A13, r14–r20): Dividend/Holdco ICR/Opco ICR/Opco DSCR (r15–r18) + Min 집계 (G16–G18) + Net Leverage (r20) ← s5 KPI named rows.
  - 표 3 만기상환가능성 (A22, r23): Method 2 Multiple + `Active_Exit_Multiple_Delta` ← B23 named range 경유 (text-label 함정 회피).
  - 표 4 차주기준 자금수지표 (A26, r27–r35): 8 rows × 5 FY = 40 cell + 8 Label named ranges; 기초현금 dedicated loop; 영업/투자 CF는 `STRESSED_EBITDA_ROW`/`STRESSED_CAPEX_ROW` import으로 참조.
  - 표 5 시나리오 메타 (A38, r39–r42): Active_* deltas pass-through.
- **신규 Named Ranges (64개, Task 16에서만)**: 6 scalars (`DASH_Case`/`Version`/`DSCR_Min`/`ICR_Opco_Min`/`ICR_Holdco_Min`/`IRR_Sponsor`) + `DASH_Div_FY1..5` (5) + `DASH_Lev_NetLeverage_FY1..5` (5) + `DASH_CFTable_Row{1..8}_Label` (8) + `DASH_CFTable_Row{1..8}_FY{1..5}` (40). 워크북 누적 `DASH_*` 79개 (s7 15개 + s8 64개).
- `tests/test_s8_dashboard.py`: 플랜 4개(`test_dashboard_five_tables`, `test_dash_cftable_40_named_ranges`, `test_dash_cftable_row_labels`, `test_dash_all_required_scalars`) + polish 3개(`test_dash_scalar_attr_text` 6 scalar attr_text, `test_cftable_row8_uses_sum` SUM 형태 contract, `test_cftable_rows_2_3_reference_correct_overlay_rows` overlay row drift 방지) = 7 tests.
- **플랜 자체 버그 5건 해결** (컨트롤러 사전 주입 + 코드 주석 `CORRECTION A..E`):
  - **A**: 테스트 `assert e in col_a`는 exact match — 플랜 Step 2의 `"표 N. …(괄호 부연)"` 제거하고 짧은 형태로 A6/A13/A22/A26/A38 작성.
  - **B**: 영업CF가 row 13 참조 (= STRESSED_CAPEX) → `STRESSED_EBITDA_ROW`(=11) import 후 참조.
  - **C**: 투자CF가 row 16 참조 (빈 행) → `STRESSED_CAPEX_ROW`(=13).
  - **D**: 기초현금 main-loop 수식이 broken 문자열 조작 (`chr(ord(col)-1).replace(...)`) → dedicated follow-up loop에서 FY1=0, FY2~FY5=`={prev}35`로 재기록.
  - **E**: `B23 = "=C11+Active_Exit_Multiple_Delta"` (C11은 text "EBITDA") → `"=DASH_Valuation_Method2_Multiple+Active_Exit_Multiple_Delta"`.
- **Code reviewer 판정 흐름**: ⚠️ CHANGES_REQUESTED (2 Important + 4 Nit) → polish `7d54ec5` → ✅ APPROVED.
  - Important #1 — row 8 sign-convention 통일: rows 6/7 을 `=-(...)` 로 stored-negative화, row 8을 `=SUM({col}28:{col}34)`로 단순화, `CFTABLE_ROW_LABELS` 상단에 sign-convention docstring 추가.
  - Important #2 — name-presence만 검증하는 테스트 갭 close: 3 contract tests 추가 (attr_text + SUM shape + overlay row drift).
  - Nits #3 (`DASH_IRR_Sponsor`를 `test_dash_all_required_scalars` 커버리지에 추가) / #4 (표 1 `apply_key_output` 루프를 `CDEF`로 좁혀 B열 text-label 제외) / #5 (`if cell.value is not None` → `if row_idx != 1`) / #6 (redundant `ws["B44"] = None` 삭제) 즉시 반영.
- **Deferred Nits (후속 Task에서 검토)**:
  - **#7 — 표 2/3/5 row anchor 상수**: `TABLE2_START = 13`, `TABLE3_START = 22`, `TABLE5_START = 38` 호이스트. 현재 file churn 예상 낮아 reviewer 권고상 defer. Task 17 Integrity 또는 최종 리팩토 라운드에서 검토.
  - **M2 — T15의 s7 행 상수 호이스트** (`METHOD_DECL_START`, `LTV_DATA_START`, `LTM_ANCHOR_ROW`, `TARGET_OWN_ROW`): Task 17 Integrity와 함께 검토.

### ✅ Task 17: Integrity + 전체 smoke (automated)

- Commits: `fc83825` (impl) + `b45e058` (polish — code reviewer Important: `test_no_iterative_calc_marker` docstring 현실화, `test_sources_equals_uses_check_formula_exists`에 `str` 가드 + 첫 매칭 후 `break`)
- `tests/test_integrity.py`: 플랜 7개 테스트 + DASH 정규식은 스칼라 `DASH_Case` 등 허용하도록 플랜 스니펫 대비 완화(주석 설명)
- **Spec reviewer**: ✅ APPROVED (플랜 발췌 “7 Active_*”는 실제 6개 `Active_*` + `Perm_Growth`와 정합)
- **Code reviewer**: ⚠️ With fixes → polish 후 ✅ APPROVED
- **Step 3 수기 Excel 검증**: RESUME §5대로 컨트롤러/사용자 — `python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx` 후 플랜 10단계

### ✅ Task 18: README + v0.5.0 태그

- Commit: `f969309` — 루트 `README.md`에 설치·빌드·`pytest -v`·수기 검증 10단계(Task 17 Step 3)·v0.6 로드맵·`.cursor` design/plan 링크. 플랜의 짧은 시트명은 실제 탭명(`1_Input_BaseCase`, `2_Stress_Panel`, `9a_CIQ_Trading_Raw` 등)으로 정확화.
- **Tag**: `v0.5.0` (annotated) — `LBO Stress Template v0.5 — MVP with all 13 sheets, Preconditions resolved`
- **Spec reviewer**: ✅ APPROVED
- **Code reviewer**: ✅ APPROVED (Minor: `goldentest_v05.json` 명명 혼동 가능 — 선택적 설명 한 줄, 미반영)

### Final: 전체 code-reviewer (`6db3d2b..f969309`)

- **판정**: **Ready to merge: Yes** (Critical 0건)
- **범위**: ~36 files / ~2905 +; `build.py` 오케스트레이션·`layout` SSOT·시트별 모듈·71 tests·`test_integrity`·대시보드–오버레이 행 계약 샘플 검증
- **Important (비차단, 2026-04-21 후속으로 상당 부분 반영)**: (1) `define_name` — **s1/s2/s4/s5/s6/s9_peer까지 `30cb034`에서 통일** (2) 순환참조·Excel 재계산 — **README에 CI 한계 명시됨**; 값 골든은 v0.6 (3) DCF TV 지수 — **`GORDON_TV_DISCOUNT_EXPONENT` + `J11` 연동·`PV(TV)=...^J11`** (`30cb034`)
- **Minor**: `s8_dashboard` 헤더 열 인덱스가 A–Z 가정
- 서브에이전트 참조: `929d5a00-b7ff-4873-a33b-17a7433f029a` (새 세션 resume 불가이므로 기록용)

---

## 4. 진행 중단된 Task

**없음.** **`main` @ `9f88a61`** 기준 · `pytest` **72 passed** · 태그 **`v0.5.0`** 로컬·**`origin` 푸시됨** (`2026-04-21`).

---

## 5. 다음 액션 (머지·푸시 완료 후)

### 완료된 것

- `feat/lbo-template-v0.5` → `main` **로컬 머지**, **`git push origin main`**, **`git push origin v0.5.0`**.
- 코드 후속: `define_name` 넓힘, DCF `J11` 연동, 수식 골든 `goldentest_v05.json`, README CI/Excel 구분 (`30cb034` / merge `9f88a61`).

### 권장 후속 (아직 안 했다면)

| 우선순위 | 작업 |
|---------|------|
| 1 | **수기 Excel 검증 10단계** — 아래 **§5.1** (또는 루트 `README.md` 동일 내용). CI가 Excel을 대신하지 못함. |
| 2 | **v0.6** — 실제 딜 입력으로 채운 `.xlsx` 저장 후 `8_Dashboard` **재계산 숫자** 스냅샷 (현재 JSON은 **빌더 수식** 회귀). |
| 3 | **워크트리 정리 (선택)** — `buyout-deal-lbo-impl`에서 `git checkout main`·`git pull` 후, 불필요하면 `git worktree remove ...`; 그다음 로컬 브랜치 `feat/...` 삭제 가능. |

### §5.1 수기 검증 10단계 (상세)

**전제**: 저장소 루트에서 `python -m pip install -e ".[dev]"` 후 `python -m lbo_template.build --output dist/LBO_Stress_Template_v0.5.xlsx`로 파일을 만든다. **Microsoft Excel(데스크톱)** 으로 연다.

1. **통합·탭**  
   생성된 `dist/LBO_Stress_Template_v0.5.xlsx`를 연다. 하단 시트 탭이 **13개**인지 본다 (`0_README` … `9_Peer_Summary` 등 설계 순서).

2. **Section A (입력)**  
   시트 **`1_Input_BaseCase`** 로 이동. **Section A**는 대개 상단 블록(EV·Net Debt·각종 Fee·트랜치 원금·Target Leverage 등). `B5`부터 라벨 옆 셀에 값을 넣는다. README 예시 그대로면 대략 — **EV 100,000** / **Net Debt 30,000** / **Fee 2,000** / **Senior 40,000** / **2nd 15,000** / **Holdco 15,000** / **Target Lev 6.0** (단위·스케일은 시트 옆注와 일치하게). *목적: Sources/Uses가 말이 되게 Link.*

3. **Section B (운전 항목, 8개 FY)**  
   같은 시트의 **Section B**에서 Revenue, EBITDA, Capex, NWC 등 **연도별(FY) 입력 줄**에 **더미 숫자**를 채운다(0이 아닌 값을 골고루). *목적: 오버레이·워터폴·DCF로 숫자가 흐르게.*

4. **Sources − Uses 체크**  
   셀 **`1_Input_BaseCase!B18`** (Sources−Uses 균형 체크 행)이 **0**인지 확인한다. 0이 아니면 입력/단위가 안 맞는 것.

5. **스트레스 → 대시보드**  
   시트 **`2_Stress_Panel`** 의 **`B3`** (`Case_Switch`)에서 드롭다운으로 **`Downside`** 선택. 시트 **`8_Dashboard`** 로 가서 LTV·DSCR·ICR 등 요약 수치가 **갱신**되는지 본다(수식 연결 스모크).

6. **Peer Raw (선택 스모크)**  
   `B3`을 다시 **`Base`** 등으로 되돌린 뒤, **`9a_CIQ_Trading_Raw`** 의 **`B3:B17`** 구간에 티커를 몇 개 넣는다 (예: `005930.KS`, `000660.KS`, `035420.KS` …). CapIQ 플러그인이 없으면 외부 갱신은 스킵.

7. **데이터 갱신**  
   CapIQ가 있으면 리본 **`데이터` → `모두 새로 고침` (`Refresh All`)** 을 실행한다. 없으면 이 단계는 생략하고 **수식·구조만** 확인.

8. **순환 계산 OFF**  
   **`파일` → `옵션` → `수식`** (영문: *File → Options → Formulas*)에서 **`반복 계산 사용`** 을 **끔(OFF)** 으로 둔다. 저장하고 시트로 돌아와 **노란색 순환 참조 경고 배너**가 뜨지 않는지 확인한다(설계상 비순환이어야 함).

9. **오류 검사**  
   리본 **`수식` → `오류 검사` → `오류 검사`** (영문: *Formulas → Error Checking*)를 실행해 **보고되는 오류가 0건**인지 본다.

10. **대시보드 `#REF!`**  
    시트 **`8_Dashboard`** 를 스크롤하며 이름이 걸린 요약 셀에 **`#REF!`** 이 없는지 확인한다(이름·참조 깨짐 여부).

**통과 기준 요약**: (4)=0, (8) 순환 배너 없음, (9) 오류 0, (10) `#REF!` 없음; (5)는 연쇄 갱신 확인.

**메모**: Mac Excel·웹 Excel은 메뉴 경로가 다를 수 있다. 동일한 **의미**(반복 계산 OFF, 오류 검사, 새로 고침)만 맞추면 됨.

---

## 6. 남은 Task 진행도 (Wave 지도)

| Wave | Task | 상태 | 비고 |
|---|---|---|---|
| W0 | T1 Bootstrap | ✅ | 459ef8b + c6a36d7 |
| W0 | T2 Conventions | ✅ | cb86b2c |
| W0 | T3 Skeleton | ✅ | 95005e1 |
| W1 | T4 0_README | ✅ | 4ea6b00 |
| W2 | T5 1_Input_BaseCase | ✅ | 55ab68f + b993595 — 7 named ranges 등록 (LTM_EBITDA, Target_Leverage, Closing_Date, Exit_Date, Opco_Senior_Principal, Opco_2L_Principal, Holdco_Sub_Principal) |
| W2 | T6 2_Stress_Panel | ✅ | e42788c — Case_Switch + 8 named ranges + DV |
| W2 | T7 3_Operating_Overlay | ✅ | d7bb4d5 — Active_* cascade (플랜 행번호 교정) |
| W2 | T8 4_Debt_Schedule | ✅ | 8e6b31d — 3 tranches + PIK + Sweep wiring (`Opco_Sweep_Avail_*`는 T9에서 정의) |
| W2 | T9 5_CF_Waterfall | ✅ | 3ee6117 — `Opco_Sweep_Avail_E..I`, KPI names, `UFCF_ROW`/`STRESSED_EBITDA_ROW` in s3 |
| W2 | T10 6_DCF_Valuation | ✅ | 0e98ffa — mid-year DCF, Gordon TV, overlay row constants for bridge |
| W3 | T11 9a / T12 9b / T13 9c | ✅ | `4ad62bd` / `cee5eab` / `97a521d` — 순차 커밋·공통 테스트 파일 |
| W4 | T14 9_Peer_Summary | ✅ | `0f4a712` — Trading+Transaction 집계, Applied_* 3개 |
| W4 | T15 7_Returns_LTV | ✅ | `4d99510` + polish `ece0f88` — Method 1/2/3 추상화, 16 named ranges, spec ✅ + code APPROVED w/ polish |
| W4 | T16 8_Dashboard | ✅ | 선행 `b3d176c` (`define_name` 헬퍼) + `76bd740` + polish `7d54ec5` — 5 tables, 64 DASH_* 등록, spec ✅ + code ⚠️→✅ APPROVED (sign convention 통일 + 3 contract tests) |
| W5 | T17 Integrity | ✅ | `fc83825` + `b45e058` — `test_integrity.py` 7 tests; DASH regex 스칼라 허용; spec ✅ code ✅ |
| W5 | T18 README + tag | ✅ | `f969309` + `v0.5.0`; spec ✅ code ✅ |
| Final | 전체 code-reviewer | ✅ | `6db3d2b..f969309` — Ready to merge **Yes**; 서브 `929d5a00-…` |
| Final | **finishing-a-development-branch** | ✅ | **2026-04-21** — `main` 머지 + `origin` 푸시 + `v0.5.0` 푸시; 워크트리 정리는 선택 |

---

## 7. 재개 시 주의 사항

1. **`subagent-driven-development` 스킬을 반드시 로드.** `C:\Users\영빈\.cursor\plugins\cache\cursor-public\superpowers\<hash>\skills\subagent-driven-development\` 경로의 SKILL.md + implementer-prompt.md + spec-reviewer-prompt.md + code-quality-reviewer-prompt.md 4개 파일 구조 그대로 따를 것.
2. **작업 경로.** 구현 코드는 이제 **메인 클론**에도 있다. 추가 빌더 작업 시 `Work ONLY in: C:\vibecoding\works\buyout deal_모델분석` 또는 기존 링크 워크트리 중 하나를 명시. 플랜·이 RESUME은 메인에서 유지.
3. **Spec reviewer의 shell 샌드박스 이슈.** 과거 3회 모두 readonly 서브에이전트 shell 출력이 부분적 또는 완전 공란. 프롬프트에 "shell 출력 없으면 `C:\vibecoding\works\buyout deal_모델분석\.git\worktrees\buyout-deal-lbo-impl\` 하위의 `HEAD` + `refs/heads/feat/lbo-template-v0.5`(주 저장소 refs) 직접 Read로 대체" 지시 포함.
4. **컨트롤러가 pytest/git log는 직접 실행.** 리뷰어 샌드박스 제약 때문에 최종 검증은 컨트롤러가 `Shell` 툴로 보완. 특히 `git show --stat <SHA>`로 커밋 스코프 확인.
5. **플랜 파일 경로 제공.** `.cursor/plans/20260420-lender-lbo-stress-template-plan.md`의 각 Task 원문을 implementer 프롬프트에 **붙여넣기** (서브에이전트에게 파일을 읽게 하지 말 것).
6. **디자인 문서 참조.** `.cursor/design-docs/20260420-0400-lender-lbo-stress-template-design.md` 의 섹션 번호(§0, §1, ...)가 플랜의 Task 번호와 맵핑됨.
7. **PowerShell 문법.** `&&` 사용 불가 → `;` 로 체이닝. 긴 출력은 `| Select-Object -Last 20` 으로 잘라 읽기.
8. **Font/Alignment house style (T5에서 확정 채택).** 모든 시트 빌더는 모듈 상수 패턴 + `Font(name="Calibri", ...)` 명시 (§3 Task 5 결정 참조).
9. **Deferred Nits 정리 타이밍.** T3/T4의 import·future-annotations Nits는 T5에서 자체 해소. T5의 row-constants/`_dn` 헬퍼 Nits는 T6에서 2번째 호출자 등장 시 도입 검토 (§3 Task 5 Deferred Nits 참조).
10. **플랜-test 충돌 사전 점검 (T5 교훈).** plan §Task N Step 3 코드를 implementer에 붙여넣기 전, controller가 (a) test의 셀 좌표·부분문자열 assert와 (b) 코드의 라벨·수식·row 번호를 cross-check. T5에서 3건 발견 (Target Leverage Check 라벨, Adjusted 단어, `{prev}` placeholder). T6도 동일 점검 권장.
11. **Contract test 사전 인젝션 (T5 polish 교훈).** named range·cross-sheet 참조 수식은 implementer 프롬프트에 처음부터 contract test로 명시. 폴리시 라운드 회피 + 다음 task에서 의존하기 전 검증 잠금.

---

## 8. 확인 명령어 (새 세션 첫 단계)

**메인 클론(권장)**:

```powershell
cd "C:\vibecoding\works\buyout deal_모델분석"
git branch --show-current                        # main
git rev-parse --short HEAD                       # 9f88a61 (또는 그 이후)
git status -sb                                   # ...origin/main (동기화 확인)
git describe --tags --always                     # v0.5.0-…-g… 또는 태그
python -m pip install -e ".[dev]" -q
python -m pytest tests/ -v                       # 72 passed
```

기대 출력 요약:
- HEAD: **`main`** 최신 (머지 커밋 `9f88a61` 포함)
- pytest: **`72 passed`**
- §5 — 선택 후속: **§5.1 수기 10단계**, v0.6, 워크트리 정리

---

## 9. Agent Transcript (누적)

- 플래너/컨트롤러 세션 UUID는 `agent-transcripts/` 폴더에서 식별 가능
- 주요 서브에이전트 ID (참고용, 새 세션은 일반적으로 resume 불가):
  - Task 1 implementer: `39c61af3-345a-48a2-a077-a5b73639c9ed`
  - Task 2 implementer: `236671fe-eba1-4194-aecb-3471123b5b45`
  - Task 3 implementer (재개 완료): `d0dc0a93-588e-4bd1-a88c-cab5c90da9b9`
  - Task 3 spec reviewer: `d329f709-56b3-4638-89ba-a96d1e33e3c5`
  - Task 3 code reviewer: `ed7ae1b6-4676-4f69-8248-5e9bfcec5484`
  - Task 4 implementer: `bbfc17fc-030b-4c5a-bb61-271707e1d896`
  - Task 4 spec reviewer: `ff2c886a-f0d4-4b17-806f-944df9ad1548`
  - Task 4 code reviewer: `551de0f1-b7e4-43b2-ba6a-93860861d528`
  - Task 5 implementer (impl + polish 양쪽 모두): `495a636e-223b-4b8f-bd8e-deef8e0a933c`
  - Task 5 spec reviewer: `ccdb8e7e-e787-4be2-ae62-2d504a28e593`
  - Task 5 code reviewer: `f316ed34-2556-4363-9675-e93b57a17663`
  - Task 15 implementer: `3b637aa3-7fc4-42ac-af66-bfb7884477e6`
  - Task 15 spec reviewer: `4be26a1d-648e-4f5c-ab30-72c1acb88dfa`
  - Task 15 code reviewer: `f7c003d3-a201-4bb2-a71c-07e30d92175a`
  - Task 16 implementer (impl + polish 분리): `02de52f6-1335-47ad-ad66-defbc874692e` / polish `95ee8d88-5458-4648-a245-8bb116ad0e5a`
  - Task 16 spec reviewer: `d8f90488-8e8a-4a15-9679-fe96b83ada4a`
  - Task 16 code reviewer (라운드 1 → 2): `30dd90da-3624-4928-9858-bf6b3e104f2d` / `5878ff36-a538-4c21-92e9-9780b2cf1f9a`
  - Final holistic code-reviewer (`6db3d2b..f969309`): `929d5a00-b7ff-4873-a33b-17a7433f029a`

**새 세션은 일반적으로 resume 불가**. 위 ID는 참고·감사용이며, 실제로는 §5의 새 프롬프트로 fresh subagent를 디스패치.
