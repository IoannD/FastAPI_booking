from typing import List
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from datetime import date, datetime
from app.hotels.shemas import SHotelInfo


router = APIRouter(prefix='/hotels', tags=['Hotels & Rooms'])


@router.get('/{location}')
async def get_hotels(location: str = 'Алтай',
                     date_from: date = datetime(2023, 5, 15),
                     date_to: date = datetime(2023, 6, 20)
                     ) -> List[SHotelInfo]:
    hotels = await HotelDAO.get_by_location(location, date_from, date_to)
    return hotels
