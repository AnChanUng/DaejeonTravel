import asyncio

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["realtime"])


class ConnectionManager:
    """
    현재 접속 중인 WebSocket 연결을 모아두고,
    모든 접속자에게 메시지를 한 번에 보내는 역할을 한다.

    - 접속자 수는 연결이 열리고 닫힐 때마다 다시 알려준다.
    - 게시글이 새로 등록되면 posts 라우터에서 broadcast()를 호출한다.
    """

    def __init__(self) -> None:
        self.active: set[WebSocket] = set()

        # 여러 요청이 동시에 목록을 건드릴 수 있으므로 잠금을 사용
        self.lock = asyncio.Lock()

    async def connect(self, websocket: WebSocket) -> None:
        await websocket.accept()

        async with self.lock:
            self.active.add(websocket)

        await self.broadcast_online()

    async def disconnect(self, websocket: WebSocket) -> None:
        async with self.lock:
            self.active.discard(websocket)

        await self.broadcast_online()

    async def broadcast(self, message: dict) -> None:
        async with self.lock:
            targets = list(self.active)

        broken: list[WebSocket] = []

        for websocket in targets:
            try:
                await websocket.send_json(message)

            except Exception:
                # 이미 끊긴 연결은 목록에서 제거
                broken.append(websocket)

        if broken:
            async with self.lock:
                for websocket in broken:
                    self.active.discard(websocket)

    async def broadcast_online(self) -> None:
        await self.broadcast(
            {
                "type": "online",
                "count": len(self.active),
            }
        )


manager = ConnectionManager()


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)

    try:
        # 클라이언트가 보내는 ping을 계속 받아주며 연결을 유지한다.
        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

    except Exception:
        await manager.disconnect(websocket)