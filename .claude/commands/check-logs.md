---
description: 에이전트 작업 로그 확인
argument-hint: <agent-name>
---

에이전트의 작업 로그를 확인합니다.

## Arguments
- `agent-name`: 로그를 확인할 에이전트 (game-logic, frontend, backend, devops)

## What to do

### 1. Get Agent State
`.claude/state.json`에서 에이전트 정보를 읽습니다.

### 2. Get Worktree Commits
```bash
cd .worktrees/<agent-name>
git log --oneline -20
```

### 3. Get Background Task Output
에이전트가 백그라운드에서 실행 중이면, 출력 파일을 읽습니다.

### 4. Output Format

```
📜 Logs for <agent-name>
══════════════════════════════════════════════════════════════════════════

State: DEVELOPING
Issue: #5 - Card component implementation
Branch: feature/frontend/card-component
Worktree: .worktrees/frontend

📝 Recent Commits
  abc1234  feat: add Card component base structure
  def5678  test: add Card component tests
  ghi9012  docs: add Card component README

📤 Agent Output (last 50 lines)
───────────────────────────────────────────────────────────────────────────
Reading Card.tsx...
Writing test file...
Running tests: npm test
  ✓ renders card front (23ms)
  ✓ renders card back when hidden (18ms)
  ✓ handles click events (12ms)

All tests passed!
Creating PR...
───────────────────────────────────────────────────────────────────────────

Use Ctrl+C to stop following logs.
```
