from sqlalchemy import JSON, Column, Integer, String, Computed, ForeignKey, Date
from sqlalchemy.orm import relationship
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

    user = relationship('Users', back_populates='booking')
    room = relationship('Rooms', back_populates='booking')

    def __str__(self):
        return f'{self.id}'

