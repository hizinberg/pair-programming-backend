from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.models import Room
from app.db import get_session
import uuid

router = APIRouter()


@router.post("/rooms",tags=["users endpoints"],summary="Create a new room")
def create_room():
    '''
     Create a new room and return its room_id
    '''

    room_id = uuid.uuid4().hex[:8]

    with get_session() as session:
        room = Room(room_id=room_id, code="// New room\n")
        session.add(room)
        session.commit()
        session.refresh(room)

    return {"roomId": room_id}


@router.get("/rooms/{room_id}",tags=["users endpoints"],summary="Get room details by room_id")
def get_room(room_id: str):
    '''
    Retrieve room details by room_id
    '''
    with get_session() as session:
        stmt = select(Room).where(Room.room_id == room_id)
        room = session.execute(stmt).scalar_one_or_none()

        if not room:
            raise HTTPException(status_code=404, detail="Room not found")

        return {"roomId": room.room_id, "code": room.code}
