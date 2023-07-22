from app.dao.base import BaseDAO
from app.hotels.rooms.models import Rooms
from app.database import async_session_maker, engine
from sqlalchemy import delete


class RoomDAO(BaseDAO):
    model = Rooms
