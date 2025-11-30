from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import Dict
from app.services.connection_manager import ConnectionManager
from app.db import get_session
from sqlalchemy import select
from app.models import Room
from app.logger import logger


router = APIRouter()

# One manager per room_id (in-memory)
managers: Dict[str, ConnectionManager] = {}

@router.websocket("/ws/{room_id}/{client_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: str, client_id: str):
    '''
    WebSocket endpoint for real-time code collaboration.
    '''

    logger.info(f"User {client_id} CONNECTED to room {room_id}")
    if room_id not in managers:
        managers[room_id] = ConnectionManager()

    manager = managers[room_id]
    await manager.connect(websocket)

    # Load initial state from DB
    code_text = "// New room\n"
    # Load initial state from DB
    db = get_session()
    try:
        stmt = select(Room).where(Room.room_id == room_id)
        room = db.execute(stmt).scalar_one_or_none()

        if room:
            code_text = room.code
            logger.info(f"Loaded room {room_id} initial code ({len(code_text)} chars)")
        else:
            new_room = Room(room_id=room_id, code=code_text)
            db.add(new_room)
            db.commit()
            logger.info(f"Created new room {room_id}")
    except Exception as e:
        logger.error(f"Error loading/creating room {room_id}: {e}")
    finally:
        db.close()


    # Send initial code
    await websocket.send_json({
        "type": "code_update",
        "clientId": "SERVER",
        "message": code_text
    })

    try:
        while True:
            data = await websocket.receive_text()
            logger.info(f"[{room_id}] UPDATE from {client_id}: {len(data)} chars")

            try:
                db = get_session()
                stmt = select(Room).where(Room.room_id == room_id)
                room = db.execute(stmt).scalar_one_or_none()

                if room:
                    room.code = data
                    db.add(room)
                    db.commit()
                    logger.info(f"[{room_id}] DB SAVE SUCCESS ({len(data)} chars)")
            except Exception as db_error:
                logger.error(f"[{room_id}] DB SAVE ERROR: {db_error}")
            finally:
                db.close()


            # Broadcast to others
            await manager.broadcast({
                "type": "code_update",
                "clientId": client_id,
                "message": data
            })

    except WebSocketDisconnect:
        logger.info(f"User {client_id} DISCONNECTED from room {room_id}")

        manager.disconnect(websocket)
        await manager.broadcast({
            "type": "notification",
            "clientId": "SERVER",
            "message": f"User {client_id} disconnected"
        })

    except Exception as ws_error:
        # -----------------------
        # ANY OTHER WEBSOCKET ERROR
        # -----------------------
        logger.error(f"Unexpected WebSocket error in room {room_id}: {ws_error}")
