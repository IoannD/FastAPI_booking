from typing import Union, Optional
from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from datetime import date

from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms


app = FastAPI()

app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_bookings)


class SBooking(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class SHotel(BaseModel):
    address: str
    name: str
    stars: int


class HotelsSearchArgs():
    def __init__(
                self,
                location: str,
                date_from: date,
                date_to: date,
                has_spa: Optional[bool] = False,
                stars: Optional[int] = Query(None, ge=1, le=5)
                ):

        self.location = location
        self.date_from = date_from
        self.date_to = date_to
        self.has_spa = has_spa
        self.stars = stars


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get('/hotels')
def get_hotels(search_args: HotelsSearchArgs = Depends()) -> list[SHotel]:
    hotels = [
        {
            'address': 'ул. Ю. Гагарина, 1, Алтай',
            'name': 'Super Hotel',
            'stars': 6,
        },
    ]
    return hotels
