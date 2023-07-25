from sqlalchemy import JSON, Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Rooms(Base):
    __tablename__ = 'rooms'

    id = Column(Integer, primary_key=True)
    hotel_id = Column(Integer, ForeignKey('hotels.id', ondelete='CASCADE'),
                      nullable=False)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    services = Column(JSON)
    quantity = Column(Integer, nullable=False)
    image_id = Column(Integer)

    booking = relationship('Bookings', back_populates='room')
    hotel = relationship('Hotels', back_populates='room')

    def __str__(self):
        return f'{self.name}'
