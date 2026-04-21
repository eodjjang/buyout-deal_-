# Git worktrees (this repo)

**Skill:** `using-git-worktrees` — implementation uses a **linked worktree** at a fixed sibling path (not `.worktrees/` under this clone).

## Directory preference

| Role | Path | Typical branch |
|------|------|----------------|
| Plans, design docs, `.cursor/` rules | `C:\vibecoding\works\buyout deal_모델분석` | `main` |
| `lbo_template` package, `pytest`, builds | `C:\vibecoding\works\buyout-deal-lbo-impl` | `feat/lbo-template-v0.5` (or successor) |

## Verify

```powershell
cd "C:\vibecoding\works\buyout deal_모델분석"
git worktree list
```

Expect two lines: this repo (e.g. `main`) and `...\buyout-deal-lbo-impl` on the feature branch.

## Handoff

Session state: `.cursor/plans/20260420-lender-lbo-stress-template-RESUME.md`

## Notes

- New linked worktrees can be added with `git worktree add` under any path you choose; document new paths here.
- If you later switch to project-local `.worktrees\<branch>\`, add `.worktrees/` to `.gitignore` and run `git check-ignore -q .worktrees` before commits.
