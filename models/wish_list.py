from sqlalchemy import Column, Integer, ForeignKey
from database import Base
from sqlalchemy.orm import relationship


class Wish_list(Base):

    __tablename__ = "wish_list"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    film_id = Column(Integer, ForeignKey("films.id"), nullable=False)

    user = relationship("Users", back_populates="wish_list")
    film = relationship("Films", back_populates="wish_list")
