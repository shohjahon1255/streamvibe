from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models.comment import Comment
from models.users import Users
from models.films import Films
from utils.auth import get_current_user

comment_router = APIRouter()


@comment_router.post("/add_comment")
def add_comment(film_id: int, text: str, rating: int, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    film = db.query(Films).filter(Films.id == film_id).all()
    if not film:
        raise HTTPException(404, "Film topilmadi")

    comment = Comment(
        film_id=film_id,
        user_id=current_user.id,
        text=text,
        rating=rating,
        created_at=datetime.utcnow()
    )
    db.add(comment)
    db.commit()
    raise HTTPException(201, "Comment added successfully!!!")

@comment_router.get("/comments")
def get_comments(db: Session = Depends(database)):
    return db.query(Comment).all()



@comment_router.delete("/delete_comment")
def delete_comment(id: int, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    comment = db.query(Comment).filter(Comment.id == id, Comment.user_id == current_user.id).all()
    if not comment:
        raise HTTPException(404, "Comment topilmadi")
    db.delete(comment)
    db.commit()
    raise HTTPException(200, "Comment deleted successfully!!!")
