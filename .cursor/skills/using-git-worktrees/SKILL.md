---
name: using-git-worktrees
description: >-
  Cursor + Git: 격리 워크스페이스가 필요할 때(플랜 실행, 피처 브랜치, 메인과 병렬 작업).
  저장소 루트의 CLAUDE.md·기존 .worktrees를 우선하고, 프로젝트 로컬 워크트리는 gitignore 검증 후 생성한다.
  Windows PowerShell·에이전트 cwd·멀티루트 워크스페이스 관행을 따른다.
---

# Using Git Worktrees (Cursor)

**I'm using the using-git-worktrees skill to set up or verify an isolated workspace.**

## Overview

Git worktrees share one `.git` object database but give **separate working directories** for different branches. In **Cursor**, you usually:

- Open the **main clone** for plans, `.cursor/` rules, and design docs, **or**
- Open the **linked worktree folder** for implementation/tests, **or**
- Use **File → Add Folder to Workspace…** so both appear in one window (multi-root).

**Core principle:** Pick directory deliberately (`CLAUDE.md` / existing `.worktrees` / ask) + **safety checks** before creating project-local trees.

## Cursor-specific behavior

| Topic | Guidance |
|--------|----------|
| **Where the agent runs shell** | Every `cd` matters. State whether commands run from **repo root** or **worktree path**. Implementation prompts often say: `Work ONLY in: <worktree>`. |
| **PowerShell** | Chain with `;`, not `&&` (failure mode differs). Quote paths with spaces. |
| **@ mentions** | User can `@Folder` or `@CLAUDE.md` so the agent uses the right root without guessing. |
| **Rules / RESUME** | Handoff docs (e.g. `.cursor/plans/*RESUME.md`) may name a fixed worktree path—**respect that** over generic `.worktrees/` defaults. |
| **Terminals** | Cursor’s integrated terminal starts in workspace folder; multi-root → pick correct root or `cd` explicitly. |

## Directory selection (priority)

### 1. Existing project-local directories

Check, in order (use PowerShell from **repository root**):

```powershell
Test-Path .\.worktrees; Test-Path .\worktrees
```

If **`.worktrees`** exists → prefer it. If **both** exist → **`.worktrees` wins**.

### 2. `CLAUDE.md` at repository root

```powershell
if (Test-Path .\CLAUDE.md) { Select-String -Path .\CLAUDE.md -Pattern 'worktree|워크트리' }
```

If paths or branch roles are documented → **use them without asking** (update `CLAUDE.md` when paths change).

### 3. Ask the user

If neither (1) nor (2) gives a convention:

```
No worktree directory found. Where should we create worktrees?

1. .worktrees\ (project-local; must be gitignored)
2. %USERPROFILE%\.cursor\worktrees\<repo-name>\ (global, outside repo)

Which do you prefer?
```

## Safety: project-local `.worktrees` or `worktrees`

Before `git worktree add` under a **project-local** folder:

```powershell
git check-ignore -q .worktrees 2>$null; if (-not $?) { git check-ignore -q worktrees }
```

If **not** ignored:

1. Add `.worktrees/` or `worktrees/` to `.gitignore` (as appropriate).
2. Commit that change.
3. Then create the worktree.

**Why:** Prevents accidental tracking of duplicate worktrees.

**Paths outside the repo** (e.g. `%USERPROFILE%\.cursor\worktrees\...`): no `.gitignore` step.

## Creation (PowerShell)

From the **main clone** (not from inside another worktree unless intentional):

```powershell
$root = git rev-parse --show-toplevel
$branch = "feat/your-feature"   # or use -b with git worktree add
$dest = Join-Path $root ".worktrees\$($branch -replace '[\\/]','-')"  # example layout

# After .worktrees is ignored:
git worktree add $dest -b $branch
Set-Location $dest
```

Adjust `$dest` if `CLAUDE.md` specifies a sibling path (e.g. `C:\vibecoding\works\buyout-deal-lbo-impl`).

## Setup + baseline tests

Auto-detect from manifest files, then run tests **in the worktree**:

| Signal | Command (examples) |
|--------|---------------------|
| `package.json` | `npm install` then `npm test` |
| `pyproject.toml` | `python -m pip install -e ".[dev]"` then `python -m pytest` |
| `Cargo.toml` | `cargo build` then `cargo test` |
| `go.mod` | `go test ./...` |

**If tests fail:** report output; ask whether to fix or stop.

**If tests pass:** record counts and path for handoff.

## Report template (for chat / RESUME)

```
Worktree ready at <absolute-path>
Tests: <N> passed, 0 failed (<command used>)
Ready to implement <feature-name>
```

## Quick reference

| Situation | Action |
|-----------|--------|
| `.worktrees\` exists | Use it; verify gitignored |
| `worktrees\` exists | Use it; verify gitignored |
| Both exist | Prefer `.worktrees\` |
| Neither | Read `CLAUDE.md` → else ask |
| Path in `CLAUDE.md` | Use documented paths |
| Not ignored | Fix `.gitignore`, commit, then add worktree |
| Baseline tests fail | Report; get explicit OK to continue |

## Common mistakes (Cursor)

- Running `git` or `pytest` from the **wrong folder** in a multi-root workspace.
- Using `&&` in PowerShell when `;` or separate lines are clearer.
- Creating `.worktrees` **without** `git check-ignore`.
- Ignoring **project-specific** RESUME/handoff that overrides generic layout.

## Red flags

**Never:**

- Create a project-local worktree folder without verifying it is ignored.
- Skip baseline tests on a **new** tree without user acknowledgment.
- Assume worktree location when `CLAUDE.md` or RESUME specifies otherwise.

**Always:**

- Prefer documented paths: existing dir > `CLAUDE.md` > ask.
- Run verification commands from the correct workspace root.
- State the active path when dispatching subagents or writing implementer prompts.

## Integration

**Pairs with:**

- **subagent-driven-development** / **executing-plans** — isolate implementation in a worktree; keep plans in main clone if that’s your split.
- **finishing-a-development-branch** — remove or prune worktrees after merge.

**This repo’s note:** `CLAUDE.md` at the repository root documents a **linked worktree** at a sibling path for the LBO template builder. Prefer that file when it exists.
