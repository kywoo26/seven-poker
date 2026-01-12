# Seven Poker - Multi-Agent Development Project

## Project Overview

5인 한국식 세븐 포커 웹 게임을 멀티 에이전트 체제로 개발하는 프로젝트입니다.

**핵심 목표**: Claude Code의 기능을 총동원하여 **실제 팀 개발 프로세스**를 시뮬레이션

## Development Process

### Roles

- **Maintainer (User)**: PR 최종 머지 권한, 전체 진행 상황 관찰, 작업 할당
- **Development Agents**: 비동기적으로 병렬 개발, PR 생성, 상호 리뷰

### Agent State Machine

```
IDLE → DEVELOPING → PR_PENDING → (PR merged) → IDLE
                         ↓
                    REVIEWING (다른 PR 리뷰 가능)
```

**규칙**:
- PR_PENDING 상태에서는 새 피쳐/버그픽스 개발 금지
- PR_PENDING 상태에서도 다른 에이전트 PR 리뷰는 가능
- 리뷰어는 기본 자동 할당 없음, Maintainer가 필요시 지정
- 머지 조건: Maintainer 승인이 최우선

### Workflow

1. Maintainer가 Issue 생성 또는 `/spawn` 으로 작업 할당
2. **Agent가 작업 시작 전 worktree 동기화** (필수):
   ```bash
   git fetch origin
   git rebase origin/master
   ```
3. Agent가 worktree에서 독립 개발
4. Agent가 PR 생성 (상세 description + 문서화 필수)
5. (선택) 다른 Agent가 리뷰
6. CI 통과 확인
7. Maintainer가 최종 머지

## Tech Stack

| Area | Technology |
|------|------------|
| Game Logic | Python 3.14 |
| Backend | FastAPI + WebSocket |
| Frontend | React + TypeScript + Tailwind CSS |
| Testing | pytest, vitest |
| Container | Docker + docker-compose |
| CI/CD | GitHub Actions |

## Project Structure

```
seven-poker/
├── .claude/
│   ├── agents/           # Agent definitions
│   ├── commands/         # Custom slash commands
│   ├── hooks/            # Pre/Post tool hooks
│   ├── state.json        # Agent state tracking
│   └── settings.json
├── packages/
│   ├── game-logic/       # Pure Python game logic
│   ├── backend/          # FastAPI server
│   └── frontend/         # React app
├── .github/workflows/    # CI/CD
└── docs/                 # Documentation
    ├── maintainer-guide.md
    ├── game-rules.md
    └── architecture.md
```

## Korean Seven Poker Rules (Summary)

상세 규칙: [docs/game-rules.md](docs/game-rules.md)

### Card Distribution
1. 최초 4장 배분 (모두 비공개)
2. 1장 버림 (discard)
3. 남은 3장 중 1장을 선택하여 오픈
4. 4th~6th 카드: 오픈으로 배분
5. 7th 카드: 히든으로 배분
6. 최종: 3장 히든 + 4장 오픈

### Hand Rankings (높은 순)
1. 로열 스트레이트 플러시
2. 백 스트레이트 플러시 (A-2-3-4-5 같은 무늬)
3. 스트레이트 플러시
4. 포카드
5. 풀하우스
6. 플러시
7. 마운틴 (A-K-Q-J-10)
8. 백스트레이트 (A-2-3-4-5)
9. 스트레이트
10. 트리플
11. 투페어
12. 원페어
13. 하이카드

### Suit Rankings (동점시)
스페이드 > 다이아몬드 > 하트 > 클로버

## Commands

- `/dashboard` - 전체 개발 현황 대시보드
- `/check-agents` - 에이전트 상태 확인
- `/check-prs` - 열린 PR 목록 + CI 상태
- `/check-issues` - 열린 Issue 목록
- `/check-logs <agent>` - 에이전트 작업 로그
- `/spawn <agent> <task>` - 에이전트에게 작업 할당
- `/start-agent <agent>` - 에이전트 시작 명령어 생성
- `/assign-review <pr> <agent>` - 리뷰어 할당

## Documentation Requirements

**중요: 모든 코드 변경 시 관련 문서도 함께 업데이트해야 합니다.**

### PR 필수 요소
- **PR Description**: Summary, Changes, Testing, Documentation 섹션
- **Code Documentation**: Public 함수 docstring 필수
- **README**: 각 패키지별 README.md 유지

### 문서 업데이트 규칙
- 게임 로직 변경 → `docs/game-rules.md` 업데이트
- 아키텍처 변경 → `docs/architecture.md` 업데이트
- API 변경 → 해당 패키지 README 업데이트
- 새 기능 추가 → CLAUDE.md 요약 업데이트 (필요시)

## Agents

- `game-logic` - 게임 로직 (카드, 핸드 평가, 베팅)
- `frontend` - React UI
- `backend` - FastAPI 서버
- `devops` - Docker, CI/CD

각 에이전트 상세: `.claude/agents/<name>.md`

## Bot Identity (GitHub App)

모든 에이전트는 GitHub 작업 시 `seven-poker-agent[bot]` 아이덴티티를 사용합니다.

### gh 명령 실행 방법 (중요!)
**각 gh 명령 앞에 토큰을 붙여야 합니다:**
```bash
# 올바른 방법 - 명령 앞에 토큰 지정
GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") gh pr comment ...
GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") gh api ...

# 또는 한 세션에서 여러 명령 실행
export GH_TOKEN=$(node "C:/Users/K/dev/github/seven-poker/scripts/generate-app-token.js") && gh pr comment ... && gh api ...
```

**잘못된 방법 (토큰이 적용되지 않음):**
```bash
# ❌ export 후 별도 명령 - 세션이 달라서 적용 안됨
export GH_TOKEN=$(node ...)
gh pr comment ...  # 토큰 없이 실행됨
```

### Git author 설정 (커밋용)
```bash
git config user.name "seven-poker-agent[bot]"
git config user.email "2639463+seven-poker-agent[bot]@users.noreply.github.com"
```

### Git 규칙
- **절대 `--amend` 사용 금지** - 커밋 히스토리를 유지해야 변경사항 추적 가능
- 수정사항은 항상 새 커밋으로 생성
- `--force` push 금지

### 결과
- 모든 커밋: `seven-poker-agent[bot]` 작성자로 표시
- 모든 PR/이슈/코멘트: `seven-poker-agent[bot]`으로 표시
- GitHub UI에서 봇 뱃지 표시됨

## PR Comment Response

에이전트는 자신의 PR에 달린 코멘트에 응답해야 합니다:
1. `gh pr view <number> --comments` 로 코멘트 확인
2. 코멘트 내용에 따라 코드 수정 또는 답변
3. `gh pr comment <number> --body "..."` 로 응답
4. 수정 사항이 있으면 커밋 후 푸시
