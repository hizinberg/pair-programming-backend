from fastapi import APIRouter, HTTPException
from sqlalchemy import select
from app.models import Room
from app.db import get_session
from app.logger import logger

router = APIRouter()

@router.get("/admin/rooms",tags=["admin endpoints"],summary="Get all rooms")
def get_all_rooms():
    '''
    Admin endpoint to retrieve all rooms and their details.
    '''

    with get_session() as session:
        stmt = select(Room)
        rooms = session.execute(stmt).scalars().all()

        logger.info(f"Admin fetched {len(rooms)} rooms.")
        return [
            {
                "roomId": r.room_id,
                "code": r.code
            }
            for r in rooms
        ]
