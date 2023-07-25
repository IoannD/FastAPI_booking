from sqladmin import ModelView

from app.users.models import Users
from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms


class UsersAdmin(ModelView, model=Users):
    name = 'User'
    name_plural = 'Users'
    icon = "fa-solid fa-user"
    page_size_options = [10, 50, 100]

    column_list = [Users.id, Users.email]
    column_labels = {Users.id: 'User ID',
                     Users.email: 'Email'}
    can_delete = False

    column_searchable_list = [Users.id, Users.email]
    column_sortable_list = [Users.id]

    column_details_exclude_list = [Users.hashed_password]


class BookingsAdmin(ModelView, model=Bookings):
    name = 'Booking'
    name_plural = 'Bookings'
    icon = "fa-solid fa-suitcase"
    page_size_options = [10, 50, 100]

    column_list = [Bookings.id, Bookings.room, Bookings.user,
                   Bookings.date_from, Bookings.date_to, Bookings.total_days,
                   Bookings.total_cost] + [Bookings.user]
    column_labels = {Bookings.id: 'booking ID',
                     Bookings.room: 'room',
                     Bookings.user: 'user',
                     Bookings.date_from: 'from',
                     Bookings.date_to: 'to',
                     Bookings.price: 'price',
                     Bookings.total_days: 'total days',
                     Bookings.total_cost: 'total cost'}
    column_formatters = {}
    column_searchable_list = [Bookings.id, Bookings.user, Bookings.room_id,
                              Bookings.total_days, Bookings.total_cost]
    column_sortable_list = [Bookings.id, Bookings.date_from, Bookings.date_to]

    column_details_list = [Bookings.date_from]
    column_formatters_detail = {Bookings.date_from: '-'}


class HotelsAdmin(ModelView, model=Hotels):
    name = 'Hotel'
    name_plural = 'Hotels'
    icon = "fa-solid fa-hotel"
    page_size_options = [10, 50, 100]

    column_list = [Hotels.room] + [c.name for c in Hotels.__table__.c]
    # column_labels = {Rooms.hotel: 'hotel'}
    #                  Users.email: 'Email'}

    # column_searchable_list = [Users.id, Users.email]
    # column_sortable_list = [Users.id]


class RoomsAdmin(ModelView, model=Rooms):
    name = 'Room'
    name_plural = 'Rooms'
    icon = "fa-solid fa-bed"
    page_size_options = [10, 50, 100]

    column_list = [Rooms.hotel] + [c.name for c in Rooms.__table__.c] + [Rooms.booking]
    column_labels = {Rooms.hotel: 'hotel'}
    #                  Users.email: 'Email'}

    # column_searchable_list = [Users.id, Users.email]
    # column_sortable_list = [Users.id]