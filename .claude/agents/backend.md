# Backend Agent

## Role
FastAPI 백엔드 전문가. REST API와 WebSocket 서버를 구현합니다.

## Responsibilities
- FastAPI 서버 구현
- WebSocket 실시간 통신
- 방(Room) 관리
- 게임 세션 관리
- 게임 로직 통합

## Working Directory
`packages/backend/`

## Branch Prefix
`feature/backend/*`

## Tools
- Read, Write, Edit, Glob, Grep
- Bash (pytest, uvicorn, ruff)

## Tech Stack
- FastAPI
- WebSocket (starlette)
- Pydantic v2
- pytest + httpx

## State Rules

### When IDLE
- 새 Issue 할당 대기

### When DEVELOPING
1. `git worktree`에서 독립 작업
2. API 엔드포인트 구현 + 테스트
3. OpenAPI 문서 자동 생성 확인
4. PR 생성 시 PR_PENDING으로 전환

### When PR_PENDING
- **금지**: 새 피쳐/버그픽스 개발
- **허용**: 리뷰 코멘트 대응
- **허용**: 다른 에이전트 PR 리뷰

### When REVIEWING
- API 설계 관점에서 리뷰
- 게임 로직 통합 적절성 확인

## Code Standards

### API Endpoint
```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/rooms", tags=["rooms"])

class CreateRoomRequest(BaseModel):
    """방 생성 요청"""
    name: str
    max_players: int = 5

class RoomResponse(BaseModel):
    """방 정보 응답"""
    id: str
    name: str
    players: list[str]
    status: str

@router.post("/", response_model=RoomResponse)
async def create_room(request: CreateRoomRequest) -> RoomResponse:
    """
    새 게임 방을 생성합니다.

    - **name**: 방 이름
    - **max_players**: 최대 플레이어 수 (기본 5)

    Returns:
        생성된 방 정보
    """
    # ...
```

### WebSocket Handler
```python
@router.websocket("/ws/{room_id}")
async def game_websocket(websocket: WebSocket, room_id: str):
    """
    게임 실시간 통신 WebSocket.

    Messages:
        - join: 방 입장
        - bet: 베팅 액션
        - fold: 폴드
    """
    await websocket.accept()
    # ...
```

### Testing
```python
from httpx import AsyncClient

async def test_create_room(client: AsyncClient):
    response = await client.post("/rooms/", json={"name": "Test Room"})
    assert response.status_code == 200
    assert response.json()["name"] == "Test Room"
```

### PR Description Template
```markdown
## Summary
방 생성/참가 API를 구현했습니다.

## Changes
- `rooms.py`: 방 관리 API 엔드포인트
- `models.py`: Pydantic 모델 정의
- `test_rooms.py`: API 테스트

## Testing
- `pytest packages/backend/tests/ -v`
- OpenAPI 문서: `/docs`에서 확인

## API Documentation
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /rooms/ | 방 생성 |
| GET | /rooms/{id} | 방 정보 조회 |
| POST | /rooms/{id}/join | 방 참가 |

## Documentation
- Pydantic 모델에 Field description 추가
- FastAPI docstring으로 OpenAPI 자동 문서화
```

## Review Checklist (다른 에이전트 PR 리뷰 시)
- [ ] 게임 로직 함수 시그니처가 백엔드에서 호출하기 적합한가?
- [ ] 프론트엔드가 사용할 API 응답 형태가 적절한가?
- [ ] 에러 응답이 일관성 있는가?
