import uuid
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Room

'''
Service layer for room-related database operations.
'''

async def create_room(db: AsyncSession) -> str:
    room_id = uuid.uuid4().hex[:8]

    new_room = Room(
        room_id=room_id,
        code="",
    )

    db.add(new_room)
    await db.commit()
    await db.refresh(new_room)

    return room_id


async def get_room(db: AsyncSession, room_id: str) -> Room | None:
    stmt = select(Room).where(Room.room_id == room_id)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()


async def update_room_code(db: AsyncSession, room_id: str, code: str):
    stmt = (
        update(Room)
        .where(Room.room_id == room_id)
        .values(code=code)
    )
    await db.execute(stmt)
    await db.commit()
