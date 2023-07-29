import asyncio
from typing import List
from fastapi import APIRouter
from app.hotels.dao import HotelDAO
from datetime import date, datetime
from app.hotels.shemas import SHotelInfo
from fastapi_cache.decorator import cache


router = APIRouter(prefix='/hotels', tags=['Hotels & Rooms'])


@router.get('/{location}')
@cache(expire=30)
async def get_hotels(location: str = 'Алтай',
                     date_from: date = datetime(2023, 5, 15).date(),
                     date_to: date = datetime(2023, 6, 20).date()
                     ) -> List[SHotelInfo]:
    hotels = await HotelDAO.get_by_location(location, date_from, date_to)
    return hotels
