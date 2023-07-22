from typing import List
from app.hotels.router import router
from app.hotels.rooms.shemas import SRoom
from app.hotels.rooms.models import Rooms
from app.hotels.rooms.dao import RoomDAO


@router.get('/{hotel_id}/rooms')
async def get_rooms(hotel_id: int) -> List[dict[str, SRoom]]:
    return await RoomDAO.find_all(hotel_id=hotel_id)
