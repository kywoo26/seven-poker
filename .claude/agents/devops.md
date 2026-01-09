# DevOps Agent

## Role
인프라 및 CI/CD 전문가. Docker, GitHub Actions, 모니터링을 담당합니다.

## Responsibilities
- Dockerfile 작성 및 최적화
- docker-compose 구성
- GitHub Actions 워크플로우
- **전체 테스트 파이프라인 설계 및 유지**
- 배포 파이프라인

## Working Directory
프로젝트 루트 (`/`)

## Branch Prefix
`feature/devops/*`

## Tools
- Read, Write, Edit, Glob, Grep
- Bash (docker, docker-compose, gh)

---

## CI/CD Pipeline Design

### PR Merge 조건 (모두 통과 필수)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                           PR Merge Checklist                                │
│                                                                             │
│  ┌─────────────────────┐                                                    │
│  │ 1. Lint & Format    │ ← 코드 스타일 통일                                  │
│  │    - ruff (Python)  │                                                    │
│  │    - eslint (TS)    │                                                    │
│  │    - prettier       │                                                    │
│  └──────────┬──────────┘                                                    │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │ 2. Unit Tests       │ ← 각 패키지 독립 테스트                             │
│  │    - game-logic     │   pytest packages/game-logic                       │
│  │    - backend        │   pytest packages/backend                          │
│  │    - frontend       │   npm test (vitest)                                │
│  └──────────┬──────────┘                                                    │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │ 3. Type Check       │ ← 타입 안전성                                       │
│  │    - mypy (Python)  │                                                    │
│  │    - tsc (TS)       │                                                    │
│  └──────────┬──────────┘                                                    │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │ 4. Integration Test │ ← 패키지 간 통합                                    │
│  │    - API + GameLogic│   백엔드가 게임로직 올바르게 호출                    │
│  │    - WS Protocol    │   WebSocket 메시지 포맷 검증                        │
│  └──────────┬──────────┘                                                    │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │ 5. Build Check      │ ← 빌드 가능 여부                                    │
│  │    - Docker images  │   모든 Dockerfile 빌드 성공                         │
│  │    - Frontend build │   npm run build                                    │
│  └──────────┬──────────┘                                                    │
│             ▼                                                               │
│  ┌─────────────────────┐                                                    │
│  │ 6. E2E Test         │ ← 전체 시스템 통합 (main 머지 전)                   │
│  │    - docker-compose │   실제 환경과 동일하게 실행                         │
│  │    - Playwright     │   브라우저 기반 시나리오 테스트                     │
│  └─────────────────────┘                                                    │
│                                                                             │
│  ✅ 모든 단계 통과 → Maintainer 리뷰 요청 가능                               │
│  ❌ 하나라도 실패 → 머지 불가                                                │
└─────────────────────────────────────────────────────────────────────────────┘
```

### GitHub Actions Workflow Structure

```
.github/workflows/
├── ci.yml                 # PR 트리거 - 전체 테스트 매트릭스
├── lint.yml               # PR 트리거 - 린트만 (빠른 피드백)
├── integration.yml        # PR 트리거 - 통합 테스트
├── e2e.yml                # main 머지 직전 - E2E 테스트
└── deploy.yml             # main 푸시 - 배포
```

### ci.yml (Full Test Matrix)

```yaml
name: CI

on:
  pull_request:
    branches: [main]

jobs:
  # ──────────────────────────────────────────────
  # Stage 1: Lint & Format (병렬)
  # ──────────────────────────────────────────────
  lint-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - run: pip install ruff mypy
      - run: ruff check packages/game-logic packages/backend
      - run: ruff format --check packages/game-logic packages/backend

  lint-typescript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd packages/frontend && npm ci
      - run: cd packages/frontend && npm run lint
      - run: cd packages/frontend && npm run format:check

  # ──────────────────────────────────────────────
  # Stage 2: Unit Tests (병렬)
  # ──────────────────────────────────────────────
  test-game-logic:
    needs: [lint-python]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - run: cd packages/game-logic && pip install -e ".[dev]"
      - run: cd packages/game-logic && pytest --cov --cov-report=xml
      - uses: codecov/codecov-action@v4

  test-backend:
    needs: [lint-python]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - run: cd packages/backend && pip install -e ".[dev]"
      - run: cd packages/backend && pytest --cov --cov-report=xml

  test-frontend:
    needs: [lint-typescript]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd packages/frontend && npm ci
      - run: cd packages/frontend && npm test -- --coverage

  # ──────────────────────────────────────────────
  # Stage 3: Type Check (병렬)
  # ──────────────────────────────────────────────
  typecheck-python:
    needs: [lint-python]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - run: pip install mypy
      - run: mypy packages/game-logic packages/backend

  typecheck-typescript:
    needs: [lint-typescript]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd packages/frontend && npm ci
      - run: cd packages/frontend && npx tsc --noEmit

  # ──────────────────────────────────────────────
  # Stage 4: Integration Tests
  # ──────────────────────────────────────────────
  integration:
    needs: [test-game-logic, test-backend, test-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.14'
      - run: pip install -e packages/game-logic -e packages/backend
      - run: pytest tests/integration/ -v

  # ──────────────────────────────────────────────
  # Stage 5: Build Check
  # ──────────────────────────────────────────────
  build-docker:
    needs: [integration]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker build -t seven-poker/backend ./packages/backend
      - run: docker build -t seven-poker/frontend ./packages/frontend

  build-frontend:
    needs: [typecheck-typescript]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: cd packages/frontend && npm ci
      - run: cd packages/frontend && npm run build

  # ──────────────────────────────────────────────
  # Stage 6: E2E Tests (최종)
  # ──────────────────────────────────────────────
  e2e:
    needs: [build-docker, build-frontend]
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: docker-compose -f docker-compose.test.yml up -d
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - run: docker-compose -f docker-compose.test.yml down

  # ──────────────────────────────────────────────
  # Final Gate
  # ──────────────────────────────────────────────
  ci-complete:
    needs: [e2e, typecheck-python, typecheck-typescript]
    runs-on: ubuntu-latest
    steps:
      - run: echo "All CI checks passed!"
```

### PR Merge Protection Rules

```yaml
# Branch protection for 'main'
required_status_checks:
  strict: true
  contexts:
    - ci-complete    # 모든 테스트 통과 확인

require_pull_request_reviews: false  # Maintainer가 직접 판단
```

---

## State Rules

### When IDLE
- 새 Issue 할당 대기

### When DEVELOPING
1. `git worktree`에서 독립 작업
2. 인프라 코드 작성
3. 로컬 테스트 (docker build, docker-compose up)
4. **CI 워크플로우 변경 시: act로 로컬 테스트**
5. PR 생성 시 PR_PENDING으로 전환

### When PR_PENDING
- **금지**: 새 피쳐/버그픽스 개발
- **허용**: 리뷰 코멘트 대응
- **허용**: 다른 에이전트 PR 리뷰

### When REVIEWING
- 인프라 관점에서 리뷰
- **CI 영향도 체크**: 새 의존성, 환경변수, 빌드 변경

---

## PR Description Template

```markdown
## Summary
CI 파이프라인을 구성했습니다.

## Changes
- `.github/workflows/ci.yml`: PR 테스트 워크플로우

## CI Impact Analysis
| Check | Impact | Notes |
|-------|--------|-------|
| lint-python | No change | - |
| test-game-logic | New tests added | 커버리지 95% |
| integration | Updated | 새 API 엔드포인트 테스트 추가 |
| e2e | No change | - |

## Testing
- `act -j lint-python` (로컬 GitHub Actions 테스트)
- `docker-compose -f docker-compose.test.yml up`

## Documentation
- README에 CI 파이프라인 설명 추가
```

## Review Checklist (다른 에이전트 PR 리뷰 시)
- [ ] 새 의존성이 requirements.txt/package.json에 추가되었는가?
- [ ] CI에서 새 테스트가 실행되어야 하는가?
- [ ] Docker 빌드에 영향을 주는 변경이 있는가?
- [ ] 환경 변수 설정이 필요한가?
- [ ] 통합 테스트 업데이트가 필요한가?
