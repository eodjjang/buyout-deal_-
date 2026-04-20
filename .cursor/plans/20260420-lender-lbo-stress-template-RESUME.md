# LBO Stress Template — 실행 재개 (Session Handoff)

> 이 문서는 `subagent-driven-development` 스킬로 `20260420-lender-lbo-stress-template-plan.md`를 실행하던 세션이 컨텍스트 한계로 중단될 때, **새 채팅 세션이 그대로 이어서 진행**하기 위한 상태 스냅샷입니다.

**마지막 갱신**: 2026-04-20 Task 5 완료 직후 (spec ✅ + code ✅ + polish 커밋 포함)

---

## TL;DR — 새 세션 즉시 재개 프롬프트

아래 문장을 새 채팅에 그대로 붙여넣으세요.

```
LBO Stress Template 플랜을 subagent-driven-development 스킬로 계속 실행 중이야.
.cursor/plans/20260420-lender-lbo-stress-template-RESUME.md 를 먼저 읽고,
거기 §5 "다음 액션" 부터 이어서 디스패치해줘.
```

---

## 1. 저장소 상태 (Task 5 완료 시점, polish 포함)

### 워크트리

| 항목 | 값 |
|---|---|
| 주 저장소 (메인) | `C:\vibecoding\works\buyout deal_모델분석\` (branch: `main`) |
| 작업 워크트리 | `C:\vibecoding\works\buyout-deal-lbo-impl\` (branch: `feat/lbo-template-v0.5`) |

**구현은 모두 워크트리에서 수행. 플랜·디자인 문서(이 파일 포함) 수정은 메인에서.** 메인 트리는 PowerShell이므로 커맨드 체이닝은 `;` 사용 (`&&` 사용 불가).

### 커밋 체인 (`feat/lbo-template-v0.5`)

```
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
pytest tests/ -v  →  19 passed
```
- `test_bootstrap.py` — 3 (Task 1 2개 + Task 3 skeleton 1개)
- `test_conventions.py` — 4 (Task 2)
- `test_s0_readme.py` — 3 (Task 4)
- `test_s1_input.py` — 9 (Task 5: 6 spec tests + 3 contract tests from polish)

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

---

## 4. 진행 중단된 Task

**없음.** Task 5 polish 커밋 완료 후 클린 워크트리. `git status --short` → empty.

---

## 5. 다음 액션 — Task 6: `2_Stress_Panel` 시트

### 개요

- **위치**: 플랜 §Task 6 (라인 1073~약 1340), 디자인 §2.
- **Wave**: W2 (Tasks 5~10 직렬, Named Range 체인). **병렬 디스패치 금지.**
- **복잡도**: 중간. T5 만큼은 아니지만 **새 openpyxl 기능 2개 도입**:
  1. `DataValidation` (드롭다운) — `from openpyxl.worksheet.datavalidation import DataValidation`
  2. `Case_Switch` named range — T7~T15 모든 시나리오 분기의 진입점 (CIQ 보다 더 핵심)
- **신규 Named Range 8개**: `Case_Switch`, `Active_Revenue_Growth_Delta`, `Active_EBITDA_Margin_Delta`, `Active_Capex_Pct_Delta`, `Active_NWC_Pct_Delta`, `Active_WACC_Uplift`, `Active_Exit_Multiple_Delta`, `Perm_Growth`. 모두 T7+ 시트에서 참조됨.
- **테스트 6개** (플랜 §Task 6 Step 1, 라인 1083~1156): `test_case_switch_cell` / `test_case_switch_validation` / `test_param_table_structure` / `test_default_values` / `test_active_formula_uses_switch` / `test_named_ranges_for_active_values`.

### Task 6 implementer 프롬프트 작성 시 필수 포함 사항

1. **Work directory**: `C:\vibecoding\works\buyout-deal-lbo-impl`, branch `feat/lbo-template-v0.5`, HEAD = `b993595` (Task 5 polish).
2. **현재 stub 상태**: `src/lbo_template/sheets/s2_stress_panel.py`는 빈 `build()` (시트만 생성). `tests/test_s2_stress.py` 미존재.
3. **재사용 가능한 컨벤션 모듈** (T1~T5에서 검증됨):
   - `from lbo_template.layout import SHEET_STRESS, CASE_SWITCH_CELL` — `SHEET_STRESS = "2_Stress_Panel"`, `CASE_SWITCH_CELL = "B3"` (이미 layout.py에 존재).
   - `from lbo_template import conventions as c` — `apply_section_header`, `apply_input`, `apply_calc`, `column_header_font`, `column_header_fill`, `NUM_FMT_PERCENT`, `NUM_FMT_BPS`, `NUM_FMT_MULTIPLE`.
4. **House style (T4 결정, T5에서 채택, 모든 후속 시트 강제)**:
   - 파일 최상단 `from __future__ import annotations`
   - `from openpyxl import Workbook` (공개 API)
   - `_SECTION_TITLE_FONT = Font(name="Calibri", bold=True, size=11)` 모듈 상수 (T5에서 `name="Calibri"` 명시 확정)
   - 어떤 `Font`/`PatternFill`/`Alignment`도 루프 내부에서 신규 생성 금지
5. **플랜 §Task 6 원문 전체 인젝션** (서브에이전트가 파일 읽지 말 것). 특히 다음 코드 단편들을 그대로 붙여넣을 것:
   - Step 1: 6개 테스트 (라인 1083~1156)
   - Step 3: `PARAM_ROWS` 7-튜플 리스트 + `INDUSTRY_PRESETS` 6-list + `build()` 구현 (라인 1166~1280 범위)
6. **`Case_Switch` named range 등록 형식**:
   ```python
   wb.defined_names["Case_Switch"] = DefinedName(
       "Case_Switch",
       attr_text=f"'{SHEET_STRESS}'!$B$3",  # CASE_SWITCH_CELL = "B3"
   )
   ```
   주의: 플랜 라인 1208의 `attr_text=f"'{SHEET_STRESS}'!${CASE_SWITCH_CELL[0]}${CASE_SWITCH_CELL[1:]}"` 슬라이싱은 `B3`만 작동, `AA10` 같은 multi-letter column은 깨짐. 현재는 `B3`이라 무방하나 implementer에게 **명시적 `$B$3` 하드코드를 권장**하거나 `from openpyxl.utils.cell import coordinate_from_string` 사용을 알려줄 것.
7. **`Active_*` 수식**: 플랜은 `=SWITCH(Case_Switch, "Base", B8, "Upside", C8, "Downside", D8)` 또는 `CHOOSE` 또는 `MATCH` 중 하나로 충족 (`test_active_formula_uses_switch` assert). **권장: `SWITCH`** (Excel 2019+ / O365 표준, 가장 가독성 좋음).
8. **테스트 → 7개로 보강 권장 (T5 polish 교훈)**: 플랜 6개 외에 `test_active_named_ranges_attr_text` (각 `Active_*` 의 `attr_text`가 정확한 셀 좌표인지) 추가. T5 `test_named_ranges`와 동일 패턴. **Important로 분류된 contract test이므로 implementer 프롬프트에 처음부터 포함**해 polish 라운드 회피.
9. **커밋 메시지**: `feat(s2_stress): add Case_Switch + 7-param table with Active_* named ranges and dropdown validations`
10. **검증**: `pytest tests/ -v` → **27 passed** 예상 (기존 19 + Task 6 신규 7~8).

### 권장 실행 흐름 (T5에서 검증된 패턴)

```
1. TodoWrite 6항목: t6-impl / t6-controller-verify / t6-spec / t6-code / t6-nit-policy / t6-resume-update
2. Task(generalPurpose) implementer 디스패치 — fresh subagent (resume 금지)
3. 컨트롤러: git log -3, git show --stat HEAD, pytest tests/ -v
4. Task(generalPurpose, readonly=true) spec reviewer
5. Task(code-reviewer) code quality reviewer
6. Important 즉시 수정 + cheap Nits (≤1분 짜리만) polish 커밋
7. RESUME 갱신 → Task 7 진입 또는 세션 종료
```

### Task 6 잠재 지뢰

- **`CASE_SWITCH_CELL` 슬라이싱 버그**: 위 §6번 항목 — `attr_text` 생성 시 `B3` 하드코드 권장.
- **Default values 정확도**: 플랜 라인 1124~1133 (`B8=0.0, C8=0.02, D8=-0.05` 등). float vs int 주의: `B14=0.01`은 1.0% (float), `B/C/D14=0.01` 동일 (Permanent Growth 고정).
- **`DataValidation` 등록 순서**: openpyxl은 `ws.add_data_validation(dv)` 호출 후 `dv.add(cell_ref)`. 플랜 코드는 `dv.add()` 후 `ws.add_data_validation()` — 어느 순서든 작동하지만 `ws.add` 먼저가 안전. `data_validations.dataValidation` 리스트로 enumerate 가능 (test_case_switch_validation).
- **Industry preset formula1 길이**: `f'"{",".join(INDUSTRY_PRESETS)}"'` → `'"(수동),소매,제조,SaaS,헬스케어,해운·시황주"'` — 한글 포함. Excel 데이터 검증 formula1은 255자 제한. 현재 합 ~30자라 OK.
- **`Active` 컬럼 (F열) 출력 셀 스타일**: T5 패턴(`apply_calc`) 적용. 단위는 행마다 다름 (`F8` % / `F12` bps / `F13` multiple) — `unit_fmt`로 PARAM_ROWS 5번째 필드 활용.
- **`Perm_Growth` 행 (row 14)**: B/C/D 모두 동일하므로 Active도 같은 값. 플랜 Step 3가 7번째 PARAM_ROWS 항목으로 통합 처리. 단, 시나리오 무관 상수임을 시각적으로 표시 (예: 회색 fill) 권장.
- **deferred T5 Nit 검토**: T6 시점에 (a) `_dn(name, coord)` named-range 헬퍼 도입 검토 (T5 7개 + T6 8개 = 15개), (b) `conventions.py`에 subsection-header font factory 추가 검토 (T5 `_SECTION_TITLE_FONT` + T6 동일 패턴 = 2번째 호출자 등장 → YAGNI 해제 시점).

### Task 6 후 Task 7 디자인 의존성 미리 노트

- T7 `3_Operating_Overlay`는 `Active_Revenue_Growth_Delta`, `Active_EBITDA_Margin_Delta`, `Active_Capex_Pct_Delta`, `Active_NWC_Pct_Delta`를 입력 항목 외 모든 FY 컬럼에서 참조. T6 named range 이름이 잘못되면 T7 전체가 깨짐 → T6 contract 테스트 (위 §8번)가 결정적.

---

## 6. 남은 Task 진행도 (Wave 지도)

| Wave | Task | 상태 | 비고 |
|---|---|---|---|
| W0 | T1 Bootstrap | ✅ | 459ef8b + c6a36d7 |
| W0 | T2 Conventions | ✅ | cb86b2c |
| W0 | T3 Skeleton | ✅ | 95005e1 |
| W1 | T4 0_README | ✅ | 4ea6b00 |
| W2 | T5 1_Input_BaseCase | ✅ | 55ab68f + b993595 — 7 named ranges 등록 (LTM_EBITDA, Target_Leverage, Closing_Date, Exit_Date, Opco_Senior_Principal, Opco_2L_Principal, Holdco_Sub_Principal) |
| W2 | **T6 2_Stress_Panel** | **⏳ 다음** | **직렬** — Case_Switch + 7 Active_* named range |
| W2 | T7 3_Operating_Overlay | ⏳ | T6 Case_Switch + Active_* 의존 |
| W2 | T8 4_Debt_Schedule | ⏳ | T5 tranche 금액 의존 |
| W2 | T9 5_CF_Waterfall | ⏳ | T7 UFCF + T8 debt 의존 (`UFCF_ROW=19` 모듈 상수 export 필요) |
| W2 | T10 6_DCF_Valuation | ⏳ | T7 UFCF 의존 |
| W3 | T11 9a_CIQ_Trading | ⏳ | **병렬 디스패치** (단일 메시지 3×Task) |
| W3 | T12 9b_CIQ_Transaction | ⏳ | 병렬 |
| W3 | T13 9c_Manual | ⏳ | 병렬 |
| W4 | T14 9_Peer_Summary | ⏳ | T11~13 의존 |
| W4 | T15 7_Returns_LTV | ⏳ | T14 + T10 의존 |
| W4 | T16 8_Dashboard | ⏳ | 전 시트 의존 |
| W5 | T17 Integrity | ⏳ | 전체 smoke + manual Excel 검증 |
| W5 | T18 README + tag | ⏳ | 마감 |
| Final | 전체 code-reviewer | ⏳ | `Task(code-reviewer)` |
| Final | finishing-a-development-branch | ⏳ | 병합/PR 스킬 |

---

## 7. 재개 시 주의 사항

1. **`subagent-driven-development` 스킬을 반드시 로드.** `C:\Users\영빈\.cursor\plugins\cache\cursor-public\superpowers\<hash>\skills\subagent-driven-development\` 경로의 SKILL.md + implementer-prompt.md + spec-reviewer-prompt.md + code-quality-reviewer-prompt.md 4개 파일 구조 그대로 따를 것.
2. **워크트리 경로 프롬프트에 명시.** 모든 implementer 프롬프트에 `Work ONLY in: C:\vibecoding\works\buyout-deal-lbo-impl` 고정. 메인(`buyout deal_모델분석`)은 플랜·디자인·이 RESUME 문서 외에 건드리지 말 것.
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

```powershell
cd C:\vibecoding\works\buyout-deal-lbo-impl
git branch --show-current                        # feat/lbo-template-v0.5
git log --oneline -8                             # b993595, 55ab68f, 4ea6b00, 95005e1, cb86b2c, c6a36d7, 459ef8b, 6db3d2b
git status --short                               # (empty — clean tree)
python -m pytest tests/ -v                       # 19 passed
```

기대 출력 요약:
- HEAD = `b993595 chore(s1_input): add formula/named-range contract tests + font name polish`
- pytest tail: `tests/test_s1_input.py::test_named_ranges PASSED [100%]` + `19 passed in 0.X s`

모두 정상이면 §5 Task 6 디스패치 시작.

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

**새 세션은 일반적으로 resume 불가**. 위 ID는 참고·감사용이며, 실제로는 §5의 새 프롬프트로 fresh subagent를 디스패치.
