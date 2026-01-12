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

### 3. Create/Update Worktree & Sync
```bash
# 먼저 메인에서 최신 master 가져오기
git fetch origin

# 기존 worktree 있으면 삭제 후 재생성
git worktree remove .worktrees/<agent-name> --force 2>/dev/null
git worktree add .worktrees/<agent-name> -b feature/<agent-name>/<task-slug> origin/master
```
**중요:** `origin/master`에서 생성해야 최신 CLAUDE.md 포함됨

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

## Setup (필수 - 순서대로 실행!)
1. cd C:\Users\K\dev\github\seven-poker\.worktrees\<agent-name>
2. Git author 설정:
   git config user.name "seven-poker-agent[bot]"
   git config user.email "2639463+seven-poker-agent[bot]@users.noreply.github.com"
3. 워크트리 동기화:
   git fetch origin && git rebase origin/master

## GH_TOKEN 사용법 (중요!)
모든 gh 명령은 반드시 이 형식으로:
GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") gh ...

예시:
GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") gh pr create ...

## Your Task
Issue #<issue-number>: <task-description>

## Development Steps
1. Read .claude/agents/<agent-name>.md for coding standards
2. Implement feature with tests
3. Commit (amend 절대 금지!):
   git add -A && git commit -m "feat(<agent-name>): <description>"
4. Push:
   git push -u origin feature/<agent-name>/<task-slug>
5. Create PR:
   GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") gh pr create --base master --repo kywoo26/seven-poker --title "[<agent-name>] <title>" --body "..."
6. Update .claude/state.json: state → "PR_PENDING", current_pr → PR번호

## Rules
- Only work in the worktree directory
- Write tests for all functionality
- Write detailed PR description
- 절대 --amend, --force 사용 금지
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
