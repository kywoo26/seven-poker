---
description: PR 리뷰 코멘트에 대응
argument-hint: <agent-name>
---

에이전트가 자신의 PR에 달린 리뷰 코멘트를 확인하고 개별적으로 대응합니다.

## Arguments
- `agent-name`: PR 작성 에이전트 (game-logic, frontend, backend, devops)

## What to do

### 1. Validate
- 에이전트가 PR_PENDING 상태인지 확인
- 해당 에이전트의 current_pr 번호 확인

### 2. Launch Agent (Background)
**Task tool을 반드시 다음과 같이 호출:**
```
subagent_type: "general-purpose"
run_in_background: true
prompt: (아래 내용)
```

**프롬프트:**
```
You are the <agent-name> agent responding to review comments on your PR.

## Working Directory
C:\Users\K\dev\github\seven-poker\.worktrees\<agent-name>

## Setup
cd C:\Users\K\dev\github\seven-poker\.worktrees\<agent-name>

## Your PR
PR #<pr-number>

## Instructions

### 1. Fetch Review Comments
gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments --jq '.[] | {id, path, line, body, user: .user.login}'

Also check general PR comments:
gh pr view <pr-number> --repo kywoo26/seven-poker --comments

### 2. For Each Comment, Respond Individually
각 코멘트에 대해 개별적으로 판단하고 대응:

**코드 수정이 필요한 경우:**
1. 해당 파일/라인 수정
2. 수정 후 해당 코멘트에 reply:
   gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments/<comment-id>/replies -f body="수정했습니다. <변경 내용 설명>"

**수정이 불필요하거나 의견이 다른 경우:**
해당 코멘트에 reply로 이유 설명:
gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments/<comment-id>/replies -f body="<이유 설명>"

**일반 PR 코멘트 응답:**
gh pr comment <pr-number> --repo kywoo26/seven-poker --body "RE: <원래 코멘트 요약>\n\n<응답>"

### 3. Push Changes (if any)
수정사항이 있으면:
git add -A && git commit -m "fix(<agent-name>): address review comments" && git push

### 4. Summary
대응 완료 후 PR에 요약 코멘트:
gh pr comment <pr-number> --repo kywoo26/seven-poker --body "## Review Response Summary
- 수정한 항목: N개
- 답변한 항목: N개
- 반영하지 않은 항목: N개 (사유 포함)"

## Rules
- 각 코멘트에 개별적으로 대응 (일괄 처리 X)
- 수정 시 해당 리뷰 코멘트에 reply
- 정중하고 건설적인 답변
```

### 3. Output
```
💬 Review response started

Agent: <agent-name>
PR: #<pr-number>

Agent is responding to review comments in background.
Use /check-prs to see updated status.
```
