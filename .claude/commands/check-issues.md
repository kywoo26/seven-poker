# /check-issues

열린 Issue 목록을 확인합니다.

## What to do

### 1. Get Open Issues
```bash
gh issue list --state open --json number,title,labels,assignees,state
```

### 2. Categorize by Agent
라벨을 기준으로 에이전트별로 분류합니다:
- `agent:game-logic`
- `agent:frontend`
- `agent:backend`
- `agent:devops`

### 3. Output Format

```
📋 Open Issues
══════════════════════════════════════════════════════════════════════════

🎮 game-logic (2)
  #8  Implement betting logic                    📝 Ready
  #9  Implement winner determination             📝 Ready

🖥️ frontend (3)
  #5  Card component implementation              🔨 In Progress
  #10 Table layout component                     📝 Ready
  #11 Betting panel UI                           📝 Ready

⚙️ backend (2)
  #6  WebSocket server setup                     📝 Ready
  #12 Room management API                        📝 Ready

🔧 devops (1)
  #7  Docker configuration                       📝 Ready

📦 Unassigned (0)
  (none)

══════════════════════════════════════════════════════════════════════════
Summary: 8 open issues

Commands:
  gh issue view <number>     - View issue details
  /spawn <agent> <task>      - Create and assign new issue
  /assign <issue> <agent>    - Assign existing issue to agent
```

## Status Icons
| Icon | Meaning |
|------|---------|
| 📝 | Ready - 작업 가능 |
| 🔨 | In Progress - 작업 중 |
| 🔄 | PR Created - PR 생성됨 |
