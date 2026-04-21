# Git worktrees (this repo)

**Skill:** `using-git-worktrees` — Cursor 전용 문서는 `.cursor/skills/using-git-worktrees/SKILL.md` (저장소 버전). 구현은 아래 **linked worktree**에 두며, 프로젝트 루트의 `.worktrees\`는 사용하지 않는다.

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
