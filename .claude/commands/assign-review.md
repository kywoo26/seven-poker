---
description: PR에 리뷰어 할당
argument-hint: <pr-number> <agent-name>
---

에이전트에게 PR 리뷰를 요청합니다. 실제 개발자처럼 라인별 코멘트를 답니다.

## Arguments
- `pr-number`: 리뷰할 PR 번호
- `agent-name`: 리뷰어 에이전트 (game-logic, frontend, backend, devops)

## What to do

### 1. Validate
- PR이 존재하는지: `gh pr view <pr-number> --repo kywoo26/seven-poker`
- 에이전트가 유효한지 확인
- 해당 에이전트가 PR 작성자가 아닌지 확인 (자기 PR 리뷰 불가)
- 에이전트가 IDLE 또는 PR_PENDING 상태인지 확인

### 2. Update State
`.claude/state.json`에서 에이전트 상태 업데이트:
```json
{
  "<agent-name>": {
    "state": "REVIEWING",
    "reviewing_pr": <pr-number>
  }
}
```

### 3. Launch Review Agent (Background)
**Task tool을 반드시 다음과 같이 호출:**
```
subagent_type: "general-purpose"
run_in_background: true
prompt: (아래 내용)
```

**프롬프트:**
```
You are the <agent-name> agent reviewing PR #<pr-number>.

## Review Focus (based on your role)
- game-logic: 게임 로직 정확성, API 설계, 테스트 커버리지
- frontend: UI/UX, 타입 안전성, 컴포넌트 설계
- backend: API 통합, 성능, 보안
- devops: CI 영향, 빌드 설정, 인프라

## Instructions

### 1. Read PR
gh pr view <pr-number> --repo kywoo26/seven-poker
gh pr diff <pr-number> --repo kywoo26/seven-poker

### 2. Line-by-Line Review (중요한 것만!)
실제 개발자처럼 **정말 중요한 부분에만** 라인별 코멘트를 답니다.
과하게 많이 달지 마세요. 3-5개 정도가 적당합니다.

**라인별 코멘트 다는 방법:**
gh api repos/kywoo26/seven-poker/pulls/<pr-number>/comments \
  -f body="<코멘트 내용>" \
  -f path="<파일 경로>" \
  -f commit_id="$(gh pr view <pr-number> --repo kywoo26/seven-poker --json headRefOid --jq .headRefOid)" \
  -F line=<라인 번호> \
  -f side="RIGHT"

**코멘트 기준:**
- ✅ 버그 가능성
- ✅ 성능 문제
- ✅ 보안 취약점
- ✅ 중요한 설계 개선
- ❌ 스타일/포맷팅 (린터가 처리)
- ❌ 사소한 네이밍 제안
- ❌ "이것도 좋을 것 같아요" 류의 optional 제안

### 3. Final Review Decision
모든 라인 코멘트 후 최종 결정:

**승인 (문제 없음):**
gh pr review <pr-number> --repo kywoo26/seven-poker --approve --body "LGTM! <간단한 요약>"

**변경 요청 (중요한 문제 있음):**
gh pr review <pr-number> --repo kywoo26/seven-poker --request-changes --body "## Summary
<주요 문제점 요약>

Please address the comments above."

**코멘트만 (사소한 제안):**
gh pr review <pr-number> --repo kywoo26/seven-poker --comment --body "## Review Summary
몇 가지 제안사항을 남겼습니다. 전체적으로 좋습니다."

### 4. Update State
리뷰 완료 후 .claude/state.json 업데이트:
- state: 이전 상태로 복원 (IDLE 또는 PR_PENDING)
- reviewing_pr: null

## Rules
- 정말 중요한 것만 코멘트 (3-5개 권장, 최대 10개)
- 건설적인 피드백
- 구체적인 개선 방안 제시
- 칭찬할 부분은 칭찬
```

### 4. Output
```
👀 Review requested

PR: #<pr-number>
Reviewer: <agent-name>

Agent is reviewing in background.
Use /check-prs to see review status.
```
