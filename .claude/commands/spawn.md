---
description: 에이전트에게 작업 할당
argument-hint: <agent-name> <task-description>
---

에이전트에게 개발 작업을 할당하고 백그라운드에서 실행합니다.

## Arguments
- `agent-name`: 실행할 에이전트 (game-logic, frontend, backend, devops)
- `task-description`: 작업 설명

## What to do

### 1. Validate Agent
에이전트 이름이 유효한지 확인: game-logic, frontend, backend, devops

### 2. Check Agent State
`.claude/state.json`에서 에이전트 상태 확인:
- PR_PENDING 상태면 → 에러: "에이전트가 PR 대기 중입니다. 머지 후 다시 시도하세요."
- IDLE 또는 REVIEWING 상태면 → 진행

### 3. Create/Update Worktree
```bash
# 기존 worktree 있으면 삭제 후 재생성
git worktree remove .worktrees/<agent-name> --force 2>/dev/null
git worktree add .worktrees/<agent-name> -b feature/<agent-name>/<task-slug> master
```

### 4. Create GitHub Issue
```bash
gh issue create --repo kywoo26/seven-poker \
  --title "[<agent-name>] <task-description>" \
  --body "## Task
<task-description>

## Agent
<agent-name>

## Acceptance Criteria
- [ ] Implementation complete
- [ ] Tests passing
- [ ] Documentation updated"
```
Issue 번호를 저장합니다.

### 5. Update State
`.claude/state.json` 업데이트:
```json
{
  "agents": {
    "<agent-name>": {
      "state": "DEVELOPING",
      "current_issue": <issue-number>,
      "current_pr": null,
      "branch": "feature/<agent-name>/<task-slug>",
      "started_at": "<ISO timestamp>"
    }
  }
}
```

### 6. Launch Agent (Background)
**Task tool을 반드시 다음과 같이 호출:**
```
subagent_type: "general-purpose"
run_in_background: true
prompt: (아래 내용)
```

**프롬프트:**
```
You are the <agent-name> agent for Seven Poker.

## Working Directory
C:\Users\K\dev\github\seven-poker\.worktrees\<agent-name>

## Setup (필수)
1. cd C:\Users\K\dev\github\seven-poker\.worktrees\<agent-name>
2. Read CLAUDE.md - Bot Identity 섹션에 따라 GH_TOKEN과 git config 설정
3. git fetch origin && git rebase origin/master

## Your Task
Issue #<issue-number>: <task-description>

## Development Steps
1. Read .claude/agents/<agent-name>.md
2. Implement feature with tests
3. Commit: git add -A && git commit -m "feat(<agent-name>): <description>"
4. Push: git push -u origin feature/<agent-name>/<task-slug>
5. Create PR: gh pr create --base master --repo kywoo26/seven-poker --title "[<agent-name>] <title>" --body "## Summary\n..."
6. Update state.json: state → "PR_PENDING", current_pr → PR번호

## Rules
- Only work in the worktree directory above
- Write tests for all functionality
- Write detailed PR description
```

### 7. Output
```
🚀 Spawned <agent-name> agent

📋 Issue: #<issue-number> - <task-description>
🌿 Branch: feature/<agent-name>/<task-slug>
📁 Worktree: .worktrees/<agent-name>

Agent is working in background.
Use /check-agents to monitor progress.
```
