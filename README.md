# Seven Poker

5인 한국식 세븐 포커 웹 게임

## About

이 프로젝트는 **멀티 에이전트 개발 체제**로 개발됩니다. 여러 AI 에이전트가 실제 개발팀처럼 병렬로 작업하며, 각자 PR을 올리고 리뷰하는 방식으로 진행됩니다.

## Features

- 5인 멀티플레이어 지원
- 한국식 세븐 포커 룰 적용
- 실시간 WebSocket 통신
- PC/모바일 반응형 UI

## Tech Stack

| Area | Technology |
|------|------------|
| Game Logic | Python 3.14 |
| Backend | FastAPI + WebSocket |
| Frontend | React + TypeScript + Tailwind CSS |
| Container | Docker |
| CI/CD | GitHub Actions |

## Project Structure

```
seven-poker/
├── packages/
│   ├── game-logic/     # 게임 로직 (Python)
│   ├── backend/        # API 서버 (FastAPI)
│   └── frontend/       # 웹 클라이언트 (React)
├── docs/               # 문서
└── .github/workflows/  # CI/CD
```

## Development

이 프로젝트는 Claude Code 멀티 에이전트 체제로 개발됩니다.

- **Maintainer Guide**: [MAINTAINER.md](./MAINTAINER.md)
- **Multi-Instance Guide**: [docs/multi-instance-guide.md](./docs/multi-instance-guide.md)
- **Project Guidelines**: [CLAUDE.md](./CLAUDE.md)

## Game Rules

한국식 세븐 포커 규칙을 따릅니다.

### 카드 배분
1. 최초 3장 (2장 히든 + 1장 오픈 선택)
2. 4th~6th: 오픈 카드
3. 7th: 히든 카드

### 족보 (높은 순)
1. 로열 스트레이트 플러시
2. 백 스트레이트 플러시
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

### 무늬 순위 (동점시)
스페이드 > 다이아몬드 > 하트 > 클로버

## License

MIT
