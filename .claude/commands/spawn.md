# /spawn <agent-name> <task-description>

에이전트를 백그라운드에서 실행하여 독립적으로 작업하게 합니다.

## Arguments
- `agent-name`: 실행할 에이전트 (game-logic, frontend, backend, devops)
- `task-description`: 작업 설명 (Issue 생성 및 개발에 사용)

## What to do

### 1. Validate Agent
에이전트 이름이 유효한지 확인합니다.
유효한 에이전트: game-logic, frontend, backend, devops

### 2. Check Agent State
`.claude/state.json`에서 해당 에이전트의 상태를 확인합니다.
- PR_PENDING 상태면 새 작업 할당 불가 (에러 메시지 출력)
- IDLE 또는 REVIEWING 상태면 진행

### 3. Create Git Worktree
```bash
# Worktree 디렉토리가 없으면 생성
git worktree add .worktrees/<agent-name> -b feature/<agent-name>/<task-slug>
```

### 4. Create GitHub Issue
```bash
gh issue create \
  --title "[<agent-name>] <task-description>" \
  --body "## Task\n<task-description>\n\n## Agent\n<agent-name>\n\n## Acceptance Criteria\n- [ ] Implementation complete\n- [ ] Tests passing\n- [ ] Documentation updated" \
  --label "agent:<agent-name>"
```

### 5. Update State
`.claude/state.json`을 업데이트합니다:
```json
{
  "agents": {
    "<agent-name>": {
      "state": "DEVELOPING",
      "current_issue": <issue-number>,
      "worktree": ".worktrees/<agent-name>",
      "branch": "feature/<agent-name>/<task-slug>",
      "started_at": "<timestamp>"
    }
  }
}
```

### 6. Launch Agent in Background
Task tool을 사용하여 에이전트를 백그라운드에서 실행합니다.

에이전트에게 전달할 컨텍스트:
- 에이전트 정의 파일 (`.claude/agents/<agent-name>.md`)
- CLAUDE.md
- Issue 내용
- Worktree 경로

에이전트 지시사항:
```
You are the <agent-name> agent for the Seven Poker project.

## Your Task
<task-description>

## Issue
#<issue-number>

## Working Directory
.worktrees/<agent-name>

## Instructions
1. Read your agent definition at .claude/agents/<agent-name>.md
2. Work in your worktree: cd .worktrees/<agent-name>
3. Implement the feature with tests and documentation
4. When complete, create a PR:
   gh pr create --title "[<agent-name>] <task-title>" --body "..." --base main
5. Update state.json: set your state to PR_PENDING

## Rules
- Follow the code standards in your agent definition
- Write comprehensive tests
- Document all public APIs
- Create detailed PR description
```

### 7. Output
```
🚀 Spawned <agent-name> agent

📋 Issue: #<issue-number> - <task-description>
🌿 Branch: feature/<agent-name>/<task-slug>
📁 Worktree: .worktrees/<agent-name>

Agent is now working in the background.
Use /agents to check status.
Use /logs <agent-name> to see progress.
```
