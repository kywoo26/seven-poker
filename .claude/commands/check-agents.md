# /check-agents

모든 에이전트의 현재 상태를 확인합니다.

## What to do

### 1. Read State
`.claude/state.json` 파일에서 모든 에이전트의 상태를 읽습니다.

### 2. Get Additional Info
각 에이전트에 대해:
- PR_PENDING 상태: `gh pr view <pr-number> --json state,statusCheckRollup`
- DEVELOPING 상태: `gh issue view <issue-number> --json title`

### 3. Output Format

```
👥 Agent Status
══════════════════════════════════════════════════════════════════════════

🎮 game-logic
   State: PR_PENDING
   PR: #3 - Hand evaluation implementation
   CI: ✅ All checks passed
   Waiting for: Maintainer review

🖥️ frontend
   State: DEVELOPING
   Issue: #5 - Card component implementation
   Branch: feature/frontend/card-component
   Started: 2 hours ago

⚙️ backend
   State: IDLE
   Available for new tasks

🔧 devops
   State: REVIEWING
   Reviewing: PR #3 (game-logic)

══════════════════════════════════════════════════════════════════════════
Commands:
  /spawn <agent> <task>  - Assign new task to idle agent
  /check-logs <agent>    - View agent's work log
  /check-prs             - View all open PRs
```

## State Indicators

| State | Icon | Description |
|-------|------|-------------|
| IDLE | ⚪ | 대기 중, 새 작업 할당 가능 |
| DEVELOPING | 🔨 | 개발 중 |
| PR_PENDING | 🔄 | PR 생성됨, 머지 대기 |
| REVIEWING | 👀 | 다른 PR 리뷰 중 |
