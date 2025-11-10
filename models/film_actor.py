from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from database import Base


class FilmActor(Base):
    __tablename__ = "film_actor"
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey("films.id"))
    actor_id = Column(Integer, ForeignKey("crew.id"))

    film = relationship("Films", back_populates="film_actor")
    crew = relationship("Crew", back_populates="film_actor")
