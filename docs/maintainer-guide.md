# Maintainer Guide

## Overview

당신은 **Maintainer**입니다. 직접 코드를 작성하지 않고, 에이전트들의 작업을 조율합니다.

## Quick Start

```powershell
# 1. Orchestrator 시작
cd C:\Users\K\dev\github\seven-poker
claude

# 2. 대시보드 확인
> /dashboard

# 3. 에이전트에게 작업 할당
> /spawn game-logic "카드 덱 구현"

# 4. 새 터미널에서 에이전트 실행
> /start-agent game-logic
# 출력된 명령어를 새 터미널에서 실행

# 5. 모니터링 및 머지
> /check-prs
> gh pr merge <number>
```

## Multi-Instance Architecture

```
터미널 1 (Orchestrator)          터미널 2-5 (Agents)
┌──────────────────────┐        ┌──────────────────────┐
│ 👤 Maintainer        │        │ 🤖 Agent Instance    │
│ - /dashboard         │        │ - 독립 개발          │
│ - /spawn, /check-*   │        │ - PR 생성            │
│ - gh pr merge        │        │ - 리뷰 응답          │
└──────────────────────┘        └──────────────────────┘
         │                               │
         └───────────┬───────────────────┘
                     ▼
              Shared Resources
              - CLAUDE.md
              - .claude/state.json
              - GitHub Issues/PRs
```

## Commands

| Command | Description |
|---------|-------------|
| `/dashboard` | 전체 현황 |
| `/check-agents` | 에이전트 상태 |
| `/check-prs` | PR 목록 + CI |
| `/check-issues` | Issue 목록 |
| `/spawn <agent> <task>` | 작업 할당 |
| `/start-agent <agent>` | 에이전트 시작 명령 |
| `/assign-review <pr> <agent>` | 리뷰 요청 |

## Development Phases

### Phase 1: Game Logic
```
/spawn game-logic "카드 덱 구현"
/spawn game-logic "핸드 평가 구현"
/spawn game-logic "베팅 로직 구현"
```

### Phase 2: Backend
```
/spawn backend "FastAPI 구조 설정"
/spawn backend "WebSocket 서버 구현"
```

### Phase 3: Frontend
```
/spawn frontend "React 구조 설정"
/spawn frontend "카드 컴포넌트 구현"
```

### Phase 4: DevOps
```
/spawn devops "CI 파이프라인 설정"
/spawn devops "Docker 구성"
```

## PR Review Flow

1. 에이전트가 PR 생성
2. CI 자동 실행
3. (선택) 다른 에이전트에게 리뷰 요청: `/assign-review <pr> <agent>`
4. PR 코멘트로 피드백 → 에이전트가 응답/수정
5. Maintainer가 최종 머지

## Troubleshooting

### Worktree 재생성
```powershell
git worktree remove .worktrees/game-logic
git worktree add .worktrees/game-logic -b feature/game-logic/new-task
```

### 상태 수동 리셋
```powershell
# .claude/state.json 수정
code .claude/state.json
```
