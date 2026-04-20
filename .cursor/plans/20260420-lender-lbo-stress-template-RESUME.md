# LBO Stress Template — 실행 재개 (Session Handoff)

> 이 문서는 `subagent-driven-development` 스킬로 `20260420-lender-lbo-stress-template-plan.md`를 실행하던 세션이 컨텍스트 한계로 중단될 때, **새 채팅 세션이 그대로 이어서 진행**하기 위한 상태 스냅샷입니다.

**마지막 갱신**: 2026-04-20 Task 7 완료 (컨트롤러 직접 구현·커밋; T6/T7 spec/code 서브리뷰는 후속 세션에서 보완 가능)

---

## TL;DR — 새 세션 즉시 재개 프롬프트

아래 문장을 새 채팅에 그대로 붙여넣으세요.

```
LBO Stress Template 플랜을 subagent-driven-development 스킬로 계속 실행 중이야.
.cursor/plans/20260420-lender-lbo-stress-template-RESUME.md 를 먼저 읽고,
거기 §5 "다음 액션" 부터 이어서 디스패치해줘.
```

**또는** 새 Composer/채팅 입력창에서 `@` → `20260420-lender-lbo-stress-template-RESUME.md` 파일을 첨부해 한 줄로 `@이 파일만 읽고 §5부터 이어줘` 라고 해도 된다. 프로젝트 규칙 `.cursor/rules/lbo-stress-template-handoff.mdc`가 해당 파일이 열릴 때 동일한 흐름을 보강한다.

---

## § 자동 저장 / 핸드오프 프로토콜 (Task 6 ~ Task 14)

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

## 1. 저장소 상태 (Task 7 완료 시점)

### 워크트리

| 항목 | 값 |
|---|---|
| 주 저장소 (메인) | `C:\vibecoding\works\buyout deal_모델분석\` (branch: `main`) |
| 작업 워크트리 | `C:\vibecoding\works\buyout-deal-lbo-impl\` (branch: `feat/lbo-template-v0.5`) |

**구현은 모두 워크트리에서 수행. 플랜·디자인 문서(이 파일 포함) 수정은 메인에서.** 메인 트리는 PowerShell이므로 커맨드 체이닝은 `;` 사용 (`&&` 사용 불가).

### 커밋 체인 (`feat/lbo-template-v0.5`)

```
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
pytest tests/ -v  →  29 passed
```
- `test_bootstrap.py` — 3
- `test_conventions.py` — 4
- `test_s0_readme.py` — 3
- `test_s1_input.py` — 9
- `test_s2_stress.py` — 7 (Task 6)
- `test_s3_overlay.py` — 3 (Task 7)

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

---

## 4. 진행 중단된 Task

**없음.** HEAD `d7bb4d5` 기준 워크트리 클린·`pytest` 29 passed.

---

## 5. 다음 액션 — Task 8: `4_Debt_Schedule` 시트

### 개요

- **위치**: 플랜 §Task 8 (라인 1437~), 디자인 §4.
- **Wave**: W2 직렬. **병렬 디스패치 금지.**
- **Files**: `src/lbo_template/sheets/s4_debt.py`, `tests/test_s4_debt.py` (현재 `s4_debt.py`는 stub).
- **테스트 4개** (플랜 Step 1): `test_three_tranches_present` / `test_interest_uses_opening_balance` / `test_holdco_pik_dropdown` / `test_ending_balance_never_negative`.
- **주의**: 플랜 Step 3 빌더는 `Opco_Sweep_Avail_*`·`IFERROR` 등 **5_CF_Waterfall(Task 9)에서 정의될 named range**를 참조할 수 있음. Task 8 착수 전 플랜 §Task 8 전문을 인젝션하고, **순환 의존성이면** Task 8에서 placeholder(`0` 또는 단순 `MIN`)로 두고 Task 9에서 연결하는지 컨트롤러가 판단.
- **커밋 메시지 (플랜)**: `feat(s4_debt): Opco Senior / 2nd / Holdco schedules with sweep + Holdco PIK toggle`
- **검증**: `pytest tests/ -v` → **33 passed** 예상 (29 + 4).

### Task 8 implementer 프롬프트에 넣을 고정 정보

1. **Work directory**: `C:\vibecoding\works\buyout-deal-lbo-impl`, branch `feat/lbo-template-v0.5`, HEAD = `d7bb4d5` (Task 7).
2. **House style**: `from __future__ import annotations`, `from openpyxl import Workbook`, `_SECTION_TITLE_FONT`, 루프 내 `Font()` 생성 금지 — 플랜에 `Font(bold=True)` 직접 생성이 있으면 **섹션 헤더는 `_SECTION_TITLE_FONT` + `apply_section_header`/`section_header_fill` 패턴으로 통일** (T5~T7과 동일).
3. **T5 named ranges**: `Opco_Senior_Principal`, `Opco_2L_Principal`, `Holdco_Sub_Principal` — Opening FY1 링크에 사용.
4. 플랜 **Step 1·Step 3 전체 코드 블록**을 프롬프트에 붙여넣기 (파일 읽기 금지).

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
| W2 | **T8 4_Debt_Schedule** | **⏳ 다음** | T5 principal + T7(선택) 의존; sweep↔waterfall 순환 주의 |
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
git log --oneline -8                             # d7bb4d5, e42788c, b993595, …
git status --short                               # (empty — clean tree)
python -m pytest tests/ -v                       # 29 passed
```

기대 출력 요약:
- HEAD = `d7bb4d5 feat(s3_overlay): cascade Stressed Rev/EBITDA/Capex/NWC/UFCF from Active_* deltas`
- pytest tail: `tests/test_s3_overlay.py::test_ufcf_formula PASSED [100%]` + `29 passed in 0.X s`

모두 정상이면 §5 Task 8 디스패치 시작.

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
