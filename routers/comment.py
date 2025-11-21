from datetime import time
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import database
from models.comment import Comment
from models.users import Users
from models.films import Films
from utils.auth import get_current_user
from datetime import datetime

comment_router = APIRouter()

@comment_router.post("/add_comment")
def add_comment(
    film_id: int,
    text: str,
    rating: float,
    db: Session = Depends(database),
    current_user: Users = Depends(get_current_user)
):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to add a comment")

    film = db.query(Films).filter(Films.id == film_id).first()
    if not film:
        raise HTTPException(404, "Film topilmadi")

    comment = Comment(
        film_id=film_id,
        text=text,
        rating=rating,
        created_at=datetime.now(),
        user_id=current_user.id
    )

    db.add(comment)
    db.commit()
    db.refresh(comment)

    return {"message": "Comment added successfully!", "comment_id": comment.id}



@comment_router.get("/all_comments")
def get_all_comments(db: Session = Depends(database)):
    comments = db.query(Comment).all()
    return comments




@comment_router.delete("/delete_comment")
def delete_comment(comment_id: int, db: Session = Depends(database),
              current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to delete a comment")
    comment = db.query(Comment).filter(Comment.id == comment_id).first()
    if not comment:
        raise HTTPException(404, "Comment not found")
    db.delete(comment)
    db.commit()
    raise HTTPException(201, "Comment deleted successfully!!!")