from fastapi import FastAPI, WebSocket, WebSocketDisconnect


class ConnectionManager(object):
    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(ConnectionManager, cls).__new__(cls)
            cls.instance.active_connections: list[WebSocket] = []

        return cls.instance

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

    @staticmethod
    def init(app: FastAPI):
        self = ConnectionManager()

        # Example: simple WebSocket endpoint
        @app.websocket("/ws")
        async def websocket_endpoint(websocket: WebSocket):
            await self.connect(websocket)
            try:
                while True:
                    data = await websocket.receive_text()
                    # Echo back or broadcast
                    await self.broadcast(f"Server says: {data}")
            except WebSocketDisconnect:
                self.disconnect(websocket)
