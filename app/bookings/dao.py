from app.dao.base import BaseDAO
from app.bookings.models import Bookings
from app.bookings.shemas import SBooking
from app.hotels.rooms.models import Rooms
from sqlalchemy import select, func, and_, or_, insert, delete, literal_column
from app.database import engine, async_session_maker
from datetime import date


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def add(cls, user_id: int, room_id: int,
                  date_from: date, date_to: date):

        async with async_session_maker() as session:
            """
            WITH booked_rooms AS (
                SELECT * FROM bookings
                WHERE room_id = '1' AND
                (date_from <= '2023-06-20' AND date_to >= '2023-05-15'))
            """
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == room_id,
                    and_(Bookings.date_from <= date_to,
                         Bookings.date_to >= date_from
                    )
                )
            ).cte('booked_rooms')

            """
            SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
                LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
                WHERE rooms.id = '1'
                GROUP BY rooms.quantity, booked_rooms.room_id
            """
            rooms_left = select(
                Rooms.quantity - func.count(booked_rooms.c.room_id)
            ).select_from(Rooms).where(Rooms.id == room_id).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id,
                isouter=True
            ).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            rooms_left = await session.execute(rooms_left)
            rooms_left: int = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = insert(Bookings).values(room_id=room_id,
                                                      user_id=user_id,
                                                      date_from=date_from,
                                                      date_to=date_to,
                                                      price=price
                ).returning(Bookings)

                new_booking = await session.execute(add_booking)
                await session.commit()
                return new_booking.scalar()

            else:
                print('Комнат нет')
                return None

    @classmethod
    async def delete(cls, user_id: int, booking_id: int):
        """
        DELETE FROM bookings
            WHERE id = '36' and user_id = '4';
        """
        query = delete(Bookings).where(and_(Bookings.id == booking_id,
                                            Bookings.user_id == user_id))
        async with async_session_maker() as session:
            await session.execute(query)
            await session.commit()
