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

## Your PR
PR #<pr-number>

## Instructions

### 1. Fetch Review Comments
gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments --jq '.[] | {id, path, line, body, user: .user.login}'

Also check general PR comments:
gh pr view <pr-number> --repo kywoo26/seven-poker --comments

### 2. For Each Comment, Respond AND Act
각 코멘트에 대해 **반드시 판단 → 실행 → 응답** 순서로 처리:

**중요: 말만 하지 말고 실제로 코드를 수정해야 합니다!**

**코드 수정이 필요한 경우 (반드시 실행!):**
1. **먼저** 해당 파일/라인을 실제로 수정
2. 수정 완료 후 reply:
   gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments/<comment-id>/replies -f body="수정 완료: <구체적인 변경 내용>"

**수정이 불필요하거나 의견이 다른 경우:**
구체적인 기술적 이유와 함께 reply:
gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments/<comment-id>/replies -f body="<구체적 이유>"

**PR 범위를 벗어나는 경우 (Defer):**
모든 피드백을 이 PR에서 해결할 필요는 없습니다.
1. 범위 밖이라고 판단되면 GitHub Issue 생성:
   gh issue create --repo kywoo26/seven-poker --title "[follow-up] <제목>" --body "PR #<pr-number> 리뷰에서 제안된 사항\n\n<상세 내용>"
2. 해당 코멘트에 reply:
   gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments/<comment-id>/replies -f body="이 PR 범위를 벗어나므로 follow-up issue로 생성했습니다: #<issue-number>"

**이미 답변한 코멘트가 있는 경우:**
- 이전 답변에서 "~하겠습니다" 등 약속한 내용 중 PR 범위 내 것은 **반드시 실행**
- PR 범위 밖이면 issue 생성 후 defer

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
- **Action First**: 코드 수정이 필요하면 반드시 먼저 수정하고 reply
- **No Empty Promises**: "~하겠습니다"라고만 하고 안 하면 안됨
- 각 코멘트에 개별적으로 대응 (일괄 처리 X)
- 수정 시 해당 리뷰 코멘트에 reply
- 정중하고 건설적인 답변
- **절대 --amend 사용 금지** - 커밋은 항상 새로 생성하여 히스토리 유지
- 여러 수정사항은 개별 커밋 또는 하나의 새 커밋으로 (amend 아님)
```

### 3. Output
```
💬 Review response started

Agent: <agent-name>
PR: #<pr-number>

Agent is responding to review comments in background.
Use /check-prs to see updated status.
```
