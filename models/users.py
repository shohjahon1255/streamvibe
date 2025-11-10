from sqlalchemy import Column, String, Integer
from database import Base
from sqlalchemy.orm import relationship

class Users(Base):

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String, nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(30), nullable=False)
    image = Column(String, nullable=False)

    wish_list = relationship("Wish_list", back_populates="user")