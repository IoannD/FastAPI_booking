from typing import Union, Optional
from fastapi import FastAPI, Query, Depends
from pydantic import BaseModel
from datetime import date
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from redis import asyncio as aioredis
from sqladmin import Admin
from app.admin.views import UsersAdmin, BookingsAdmin, RoomsAdmin, HotelsAdmin
from app.admin.auth import authentication_backend

from app.config import settings
from app.database import engine
from app.bookings.router import router as router_bookings
from app.users.router import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images


app = FastAPI()

# Включение основных роутеров
app.include_router(router_hotels)
app.include_router(router_rooms)
app.include_router(router_users)
app.include_router(router_bookings)

# Включение дополнительных роутеров
app.include_router(router_pages)
app.include_router(router_images)


app.mount("/static", StaticFiles(directory="app/static"), "static")

#  Подключение CORS, чтобы запросы к API могли приходить из браузера
origins = [
    # 3000 - порт, на котором работает фронтенд на React.js
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers",
                   "Access-Control-Allow-Origin",
                   "Authorization"],
)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url(f"redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}")
    FastAPICache.init(RedisBackend(redis), prefix="cache")


#  Admin views
admin = Admin(app=app, engine=engine, authentication_backend=authentication_backend)

admin.add_view(UsersAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
