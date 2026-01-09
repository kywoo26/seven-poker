---
description: PR에 리뷰어 할당
argument-hint: <pr-number> <agent-name>
---

특정 PR에 에이전트를 리뷰어로 할당합니다.

## Arguments
- `pr-number`: 리뷰할 PR 번호
- `agent-name`: 리뷰를 요청할 에이전트 (game-logic, frontend, backend, devops)

## What to do

### 1. Validate
- PR이 존재하는지 확인
- 에이전트가 유효한지 확인
- 해당 에이전트가 PR 작성자가 아닌지 확인 (자기 PR 리뷰 불가)

### 2. Update State
에이전트 상태를 REVIEWING으로 업데이트 (IDLE 또는 PR_PENDING 상태인 경우에만)

```json
{
  "agents": {
    "<agent-name>": {
      "state": "REVIEWING",
      "reviewing_prs": [<pr-number>]
    }
  }
}
```

### 3. Launch Review Agent
Task tool을 사용하여 리뷰 에이전트를 실행합니다.

에이전트 지시사항:
```
You are the <agent-name> agent reviewing PR #<pr-number>.

## Your Task
Review the PR from your expertise perspective.

## Review Focus
Based on your agent role, focus on:
- game-logic: API 설계, 로직 정확성
- frontend: UI/UX, 타입 호환성
- backend: API 통합, 성능
- devops: CI 영향, 인프라 변경

## Instructions
1. Read the PR diff: gh pr diff <pr-number>
2. Check the PR description
3. Review code changes
4. Leave comments using: gh pr review <pr-number> --comment --body "..."
5. When done, either:
   - Approve: gh pr review <pr-number> --approve
   - Request changes: gh pr review <pr-number> --request-changes --body "..."
6. Update state.json: set your state back to previous state
```

### 4. Output
```
👀 Review requested

PR: #<pr-number> - <pr-title>
Reviewer: <agent-name>

The agent is now reviewing the PR.
You'll be notified when the review is complete.
```
