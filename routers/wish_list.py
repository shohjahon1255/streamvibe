from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from models.films import Films
from utils.auth import get_current_user
from database import database
from models.wish_list import Wish_list
from sqlalchemy.orm import Session
from models.users import Users

wish_list_router = APIRouter()


@wish_list_router.post("/add_to_wish_list")
def add_to_wish_list(film_id: int, db: Session = Depends(database),
                     current_user: Users = Depends(get_current_user)):
    film = db.query(Wish_list).filter(Wish_list.film_id == film_id, Wish_list.user_id == current_user.id).first()
    if film:
        db.delete(film)
        db.commit()
        raise HTTPException(200, "Film removed from wish list successfully!!!")

    wish_list = Wish_list(
        user_id=current_user.id,
        film_id=film_id
    )
    db.add(wish_list)
    db.commit()
    raise HTTPException(201, "Film added to wish list successfully!!!")



@wish_list_router.get("/wish_list")
def get_wish_list(db: Session = Depends(database),
                  current_user: Users = Depends(get_current_user)):
    wish_list = db.query(Wish_list).filter(Wish_list.user_id == current_user.id).all()
    return wish_list


@wish_list_router.get('/most_likes')
def get_most_likes(db: Session = Depends(database)):
    film_wishlist_count = db.query(
        Wish_list.film_id,
        func.count(Wish_list.id).label('like_count')
    ).group_by(Wish_list.film_id).subquery()

    most_liked_films = db.query(Films, film_wishlist_count.c.like_count).join(
        film_wishlist_count,
        Films.id == film_wishlist_count.c.film_id
    ).order_by(film_wishlist_count.c.like_count.desc()).all()

    result = [
        {
            "film": {
                "id": film.id,
                "title": film.title,
                "description": film.description,
                "year": film.year,
                "languages": film.languages,
                "genres": film.genres,
                "view": film.view,
                "video_url": film.video_url
            },
            "like_count": like_count
        }
        for film, like_count in most_liked_films
    ]

    return result

