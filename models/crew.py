from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from database import Base

class Crew(Base):
    __tablename__ = "crew"
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    image = Column(String, nullable=True)
    role = Column(String, nullable=False)

    film_actor = relationship("FilmActor", back_populates="crew")