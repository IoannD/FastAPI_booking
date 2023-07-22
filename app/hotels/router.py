from typing import List
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from datetime import date
from app.hotels.shemas import SHotelInfo


router = APIRouter(prefix='/hotels', tags=['Hotels & Rooms'])


@router.get('/{location}')
async def get_hotels(location: str,
                     date_from: date,
                     date_to: date
                     ) -> List[SHotelInfo]:
    hotels = await HotelDAO.get_by_location(location, date_from, date_to)
    return hotels
