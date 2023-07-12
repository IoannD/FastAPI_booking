from fastapi import APIRouter

from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking


router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('')
async def get_bookings() -> list[dict[str, SBooking]]:
    return await BookingDAO.find_all()
