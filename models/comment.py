from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Float
from database import Base

class Comment(Base):
    __tablename__ = "comment"
    id = Column(Integer, primary_key=True)
    film_id = Column(Integer, ForeignKey("films.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    text = Column(String(255), nullable=False)
    rating = Column(Float, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
