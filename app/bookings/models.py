from sqlalchemy import JSON, Column, Integer, String, Computed, ForeignKey, Date
from app.database import Base


class Bookings(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id', ondelete='CASCADE'),
                     nullable=False)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'),
                     nullable=False)
    date_from = Column(Date, nullable=False)
    date_to = Column(Date, nullable=False)
    price = Column(Integer, nullable=False)
    total_days = Column(Integer, Computed('date_to - date_from'))
    total_cost = Column(Integer, Computed('(date_to - date_from) * price'))
