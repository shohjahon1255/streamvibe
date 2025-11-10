from sqlalchemy import Column, String, Integer, Text,JSON
from database import Base
from sqlalchemy.orm import relationship

class Films(Base):

    __tablename__ = "films"
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    video_url = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    languages = Column(JSON, nullable=False)
    genres = Column(JSON, nullable=False)
    view = Column(Integer, nullable=False)

    wish_list = relationship("Wish_list", back_populates="film")
    film_actor = relationship("FilmActor", back_populates="film")