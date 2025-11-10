from fastapi import APIRouter, Depends, HTTPException
from schemas.films import FilmsModel
from utils.auth import get_current_user
from database import database
from models.films import Films
from sqlalchemy.orm import Session
from models.users import Users


film_router = APIRouter()


@film_router.post("/add")
def create_film(form: FilmsModel, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to create a film")
    film = Films(
        title=form.title,
        description=form.description,
        video_url=form.video_url,
        year=form.year,
        languages=form.languages,
        genres=form.genres,
        view = 0
    )
    db.add(film)
    db.commit()
    raise HTTPException(201, "Film created successfully!!!")


@film_router.get("/films")
def get_films(title: str = None, film_id: int = None,  db: Session = Depends(database)):
    if film_id:
        film = db.query(Films).filter(Films.id == film_id).first()
        if not film:
            raise HTTPException(status_code=404, detail="Film topilmadi")
        film.view += 1
        db.commit()
        db.refresh(film)
        return film

    if title:
        films = db.query(Films).filter(Films.title.contains(title)).all()
    else:
        films = db.query(Films).all()
    return films


@film_router.get("/most-viewed")
def get_most_viewed_film(db: Session = Depends(database)):
    film = db.query(Films).order_by(Films.view.desc()).first()
    return film


@film_router.get("/get_last_film")
def get_last_film(db: Session = Depends(database)):
    film = db.query(Films).order_by(Films.id.desc()).all()
    return film

@film_router.put("/update")
def update_film(id: int, form: FilmsModel, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to update a film")
    db.query(Films).filter(Films.id == id).update(
        {
            Films.title:form.title,
            Films.description: form.description,
            Films.video_url: form.video_url,
            Films.year: form.year,
            Films.languages: form.languages,
            Films.genres: form.genres
        }
    )
    db.commit()
    raise HTTPException(200, "Film updated successfully!!!")



@film_router.delete("/delete")
def delete_film(id: int, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to delete a film")
    db.query(Films).filter(Films.id == id).delete()
    db.commit()
    raise HTTPException(200, "Film deleted successfully!!!")




