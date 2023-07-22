from app.dao.base import BaseDAO
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.bookings.models import Bookings
from datetime import date
from app.database import engine, async_session_maker
from sqlalchemy import select, func, and_, or_, insert, delete
from sqlalchemy import tuple_


class HotelDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def get_by_location(cls, location: str,
                              date_from: date, date_to: date):

        """
        WITH available_hotels AS (
            WITH searched_rooms AS (SELECT id, hotel_id, quantity  FROM rooms
                WHERE hotel_id in (SELECT id FROM hotels WHERE location LIKE '%Алтай%'))


            SELECT searched_rooms.hotel_id, searched_rooms.quantity - COUNT(bookings.room_id) AS rooms_left FROM bookings
                LEFT JOIN searched_rooms ON bookings.room_id = searched_rooms.id
                WHERE (date_from <= '2023-06-20' AND date_to >= '2023-05-15')
                GROUP BY searched_rooms.hotel_id, searched_rooms.quantity, bookings.room_id
        )

        SELECT id, name, location, services, rooms_quantity, image_id, rooms_left FROM hotels
        INNER JOIN available_hotels ON hotels.id = available_hotels.hotel_id
        WHERE rooms_left > '0'
        """

        searched_rooms = select(
            Rooms
        ).where(
            Rooms.hotel_id.in_(
                select(Hotels.id).where(Hotels.location.like(f'%{location}%'))
            )
        ).cte('searched_rooms')

        available_hotels = select(
            searched_rooms.c.hotel_id,
            (
                searched_rooms.c.quantity - func.count(Bookings.room_id)
            ).label('rooms_left')
        ).join(
            searched_rooms, Bookings.room_id == searched_rooms.c.id, isouter=True
        ).where(
            and_(Bookings.date_from <= date_to, Bookings.date_to >= date_from)
        ).group_by(
            searched_rooms.c.hotel_id,
            searched_rooms.c.quantity,
            Bookings.room_id
        ).cte(
            'available_hotels'
        )

        hotels = select(
            Hotels.id, Hotels.name, Hotels.location,
            Hotels.services, Hotels.rooms_quantity,
            Hotels.image_id, available_hotels.c.rooms_left
        ).join(
            available_hotels,
            Hotels.id == available_hotels.c.hotel_id,
            isouter=False
        ).where(
            available_hotels.c.rooms_left > 0
        )

        async with async_session_maker() as session:
            result = await session.execute(hotels)
            return result.mappings().all()
