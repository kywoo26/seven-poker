# /check-prs

열린 PR 목록과 CI 상태를 확인합니다.

## What to do

### 1. Get Open PRs
```bash
gh pr list --state open --json number,title,author,headRefName,statusCheckRollup,reviewDecision,labels
```

### 2. Get CI Status for Each PR
```bash
gh pr checks <pr-number>
```

### 3. Output Format

```
🔀 Open Pull Requests
══════════════════════════════════════════════════════════════════════════

PR #3: [game-logic] Hand evaluation implementation
├─ Branch: feature/game-logic/hand-evaluation
├─ Author: game-logic-agent
├─ CI Status:
│   ├─ ✅ lint-python
│   ├─ ✅ test-game-logic
│   ├─ ✅ typecheck-python
│   ├─ ✅ integration
│   └─ ✅ e2e
├─ Reviews: None
└─ Status: ✅ Ready for merge

PR #4: [frontend] Card component
├─ Branch: feature/frontend/card-component
├─ Author: frontend-agent
├─ CI Status:
│   ├─ ✅ lint-typescript
│   ├─ ❌ test-frontend (2 failed)
│   └─ ⏳ build-frontend (running)
├─ Reviews: None
└─ Status: ❌ CI failing

══════════════════════════════════════════════════════════════════════════
Summary: 2 open PRs (1 ready, 1 failing)

Commands:
  gh pr view <number>        - View PR details
  gh pr merge <number>       - Merge PR (Maintainer)
  /assign-review <pr> <agent> - Request review
```
