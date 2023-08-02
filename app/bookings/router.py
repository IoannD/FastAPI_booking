from typing import List
from fastapi import APIRouter, Depends
from datetime import date
from pydantic import parse_obj_as, TypeAdapter
from app.bookings.dao import BookingDAO
from app.bookings.shemas import SBooking
from app.users.models import Users
from app.users.dependencies import get_current_user
from app.exception import RoomCannotBeBookedException
from app.tasks.tasks import send_booking_confirmation_email
from app.config import settings

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

    try:
        booking = TypeAdapter(SBooking).validate_python(booking).model_dump()
    except ValueError as e:
        print(e)
    
    if settings.MODE == 'DEV' or settings.MODE == 'PROD':
        send_booking_confirmation_email.delay(booking, user.email)
    return booking



@router.delete('/{booking_id}', status_code=204)
async def delete_booking(booking_id: int,
                         user: Users = Depends(get_current_user)):
    await BookingDAO.delete(user.id, booking_id)
