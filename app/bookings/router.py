from fastapi import APIRouter, Depends
from datetime import date

from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exception import RoomCannotBeBookedException

router = APIRouter(prefix='/bookings', tags=['Bookings'])


@router.get('')
async def get_bookings(user: Users =
                       Depends(get_current_user)) -> list[dict[str, SBooking]]:
    return await BookingDAO.find_all(user_id=user.id)


@router.post('')
async def add_booking(room_id: int, date_from: date, date_to: date,
                      user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBookedException


@router.delete('/{booking_id}', status_code=204)
async def delete_booking(booking_id: int,
                         user: Users = Depends(get_current_user)):
    await BookingDAO.delete(user.id, booking_id)
