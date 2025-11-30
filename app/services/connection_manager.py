from typing import List, Dict
from fastapi import WebSocket

class ConnectionManager:
    
    """
    Manages active WebSocket connections for a single room.
    """

    def __init__(self):
        self.active_connections: List[WebSocket] = []
        # Optionally track per-client metadata
        self.meta: Dict[str, dict] = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        text = json_dumps(message)
        for conn in list(self.active_connections):
            try:
                await conn.send_text(text)
            except Exception:
                # best-effort: remove broken connection
                try:
                    self.active_connections.remove(conn)
                except ValueError:
                    pass

# small helper to ensure consistent JSON serialization
def json_dumps(obj):
    import json
    return json.dumps(obj, default=str)
