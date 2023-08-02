import pytest
from datetime import datetime

from app.bookings.dao import BookingDAO


async def test_add_and_get_booking():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime('2023-07-10', '%Y-%m-%d'),
        date_to=datetime.strptime('2023-07-24', '%Y-%m-%d'),
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None


async def test_add_and_get_booking_tmp():
    new_booking = await BookingDAO.add(
        user_id=2,
        room_id=2,
        date_from=datetime.strptime('2030-05-01', '%Y-%m-%d'),
        date_to=datetime.strptime('2030-05-15', '%Y-%m-%d'),
    )
    assert new_booking.user_id == 2
    assert new_booking.room_id == 2

    await BookingDAO.find_by_id(new_booking.id)
    assert new_booking is not None
