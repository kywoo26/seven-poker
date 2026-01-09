# Architecture

## System Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (React)                        │
│                    PC + Mobile Responsive                    │
└─────────────────────────┬───────────────────────────────────┘
                          │ WebSocket + REST
┌─────────────────────────▼───────────────────────────────────┐
│                    Backend (FastAPI)                         │
│              Room Management, Game State, Auth               │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                    Game Logic (Python)                       │
│           Cards, Hand Evaluation, Betting Rules              │
└─────────────────────────────────────────────────────────────┘
```

## Package Structure

### packages/game-logic
순수 Python 게임 로직. 외부 의존성 최소화.

```
game-logic/
├── src/
│   ├── cards.py      # Card, Deck 클래스
│   ├── hand.py       # HandRank, evaluate_hand()
│   ├── betting.py    # BettingRound, BetAction
│   └── game.py       # GameState, GameEngine
├── tests/
└── pyproject.toml
```

### packages/backend
FastAPI 서버. WebSocket으로 실시간 통신.

```
backend/
├── src/
│   ├── main.py       # FastAPI app
│   ├── rooms.py      # Room CRUD API
│   ├── websocket.py  # Game WebSocket handler
│   └── models.py     # Pydantic models
├── tests/
└── Dockerfile
```

### packages/frontend
React + TypeScript SPA.

```
frontend/
├── src/
│   ├── components/   # Card, Table, Player, BettingPanel
│   ├── hooks/        # useWebSocket, useGame
│   ├── pages/        # Lobby, Game
│   └── App.tsx
├── package.json
└── Dockerfile
```

## Data Flow

### Game Start
```
1. Player creates room (REST)
2. Other players join (REST)
3. All connect via WebSocket
4. Host starts game
5. Server deals cards
6. Game loop begins
```

### Betting Round
```
1. Server sends game state to all
2. Active player sees betting options
3. Player makes bet (WebSocket)
4. Server validates & updates state
5. Broadcast new state
6. Next player's turn
```

### WebSocket Messages

```typescript
// Client → Server
{ type: "bet", action: "call" | "half" | "full" | "fold" }
{ type: "select_open_card", cardIndex: number }
{ type: "discard_card", cardIndex: number }

// Server → Client
{ type: "game_state", state: GameState }
{ type: "your_turn", options: BetOption[] }
{ type: "player_action", playerId: string, action: string }
{ type: "round_end", winner: string, hand: HandRank }
```

## Tech Stack

| Layer | Technology | Version |
|-------|------------|---------|
| Language | Python | 3.14 |
| Backend | FastAPI | latest |
| Frontend | React | 18 |
| TypeScript | | 5.x |
| Styling | Tailwind CSS | 3.x |
| Testing | pytest, vitest | |
| Container | Docker | |
| CI/CD | GitHub Actions | |
