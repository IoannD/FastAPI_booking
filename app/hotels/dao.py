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

        # """
        # WITH available_hotels AS (
        #     WITH searched_rooms AS (SELECT id, hotel_id, quantity  FROM rooms
        #         WHERE hotel_id in (SELECT id FROM hotels WHERE location LIKE '%Алтай%'))


        #     SELECT searched_rooms.hotel_id, searched_rooms.quantity - COUNT(bookings.room_id) AS rooms_left FROM bookings
        #         LEFT JOIN searched_rooms ON bookings.room_id = searched_rooms.id
        #         WHERE (date_from <= '2023-06-20' AND date_to >= '2023-05-15')
        #         GROUP BY searched_rooms.hotel_id, searched_rooms.quantity, bookings.room_id
        # )

        # SELECT id, name, location, services, rooms_quantity, image_id, rooms_left FROM hotels
        # INNER JOIN available_hotels ON hotels.id = available_hotels.hotel_id
        # WHERE rooms_left > '0'
        # """

        # searched_rooms = select(
        #     Rooms
        # ).where(
        #     Rooms.hotel_id.in_(
        #         select(Hotels.id).where(Hotels.location.like(f'%{location}%'))
        #     )
        # ).cte('searched_rooms')

        # available_hotels = select(
        #     searched_rooms.c.hotel_id,
        #     (
        #         searched_rooms.c.quantity - func.count(Bookings.room_id)
        #     ).label('rooms_left')
        # ).join(
        #     searched_rooms, Bookings.room_id == searched_rooms.c.id, isouter=True
        # ).where(
        #     and_(Bookings.date_from <= date_to, Bookings.date_to >= date_from)
        # ).group_by(
        #     searched_rooms.c.hotel_id,
        #     searched_rooms.c.quantity,
        #     Bookings.room_id
        # ).cte(
        #     'available_hotels'
        # )

        # hotels = select(
        #     Hotels.id, Hotels.name, Hotels.location,
        #     Hotels.services, Hotels.rooms_quantity,
        #     Hotels.image_id, available_hotels.c.rooms_left
        # ).join(
        #     available_hotels,
        #     Hotels.id == available_hotels.c.hotel_id,
        #     isouter=False
        # ).where(
        #     available_hotels.c.rooms_left > 0
        # )

        # async with async_session_maker() as session:
        #     result = await session.execute(hotels)
        #     return result.mappings().all()

        """
        WITH booked_rooms AS (
            SELECT room_id, COUNT(room_id) AS rooms_booked
            FROM bookings
            WHERE 
                (date_from >= '2023-05-15' AND date_from <= '2023-06-20') OR
                (date_from <= '2023-05-15' AND date_to > '2023-05-15')
            GROUP BY room_id
        ),
        booked_hotels AS (
            SELECT hotel_id, SUM(rooms.quantity - COALESCE(rooms_booked, 0)) AS rooms_left
            FROM rooms
            LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
            GROUP BY hotel_id
        )
        SELECT * FROM hotels
        LEFT JOIN booked_hotels ON booked_hotels.hotel_id = hotels.id
        WHERE rooms_left > 0 AND location LIKE '%Алтай%';
        """
        booked_rooms = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(
                        Bookings.date_from >= date_from,
                        Bookings.date_from <= date_to,
                    ),
                    and_(
                        Bookings.date_from <= date_from,
                        Bookings.date_to > date_from,
                    ),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels = (
            select(Rooms.hotel_id, func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
            ).label("rooms_left"))
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )

        get_hotels_with_rooms = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.rooms_left,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .where(
                and_(
                    booked_hotels.c.rooms_left > 0,
                    Hotels.location.like(f"%{location}%"),
                )
            )
        )
        async with async_session_maker() as session:
            # logger.debug(get_hotels_with_rooms.compile(engine, compile_kwargs={"literal_binds": True}))
            hotels_with_rooms = await session.execute(get_hotels_with_rooms)
            return hotels_with_rooms.mappings().all()
