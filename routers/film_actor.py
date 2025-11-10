from fastapi import APIRouter, Depends, HTTPException
from database import database
from models.crew import Crew
from models.film_actor import FilmActor
from sqlalchemy.orm import Session, joinedload
from utils.auth import get_current_user
from models.films import Films
from models.users import Users


film_actor_router = APIRouter()


@film_actor_router.post("/add_actor")
def add_film_actor(film_id: int, actor_id: int, db: Session = Depends(database),
              current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to add an actor to a film")
    film = db.query(Films).filter(Films.id == film_id).first()
    if not film:
        raise HTTPException(404, "Film topilmadi")
    actor = db.query(Crew).filter(Crew.id == actor_id).first()
    if not actor:
        raise HTTPException(404, "Actor topilmadi")
    film_actor = FilmActor(
        film_id=film_id,
        actor_id=actor_id
    )
    db.add(film_actor)
    db.commit()
    raise HTTPException(201, "Actor added to film successfully!!!")


@film_actor_router.get("/actors")
def get_actors(db: Session = Depends(database)):
    return db.query(FilmActor).options(joinedload(FilmActor.film), joinedload(FilmActor.crew)).all()




@film_actor_router.put("/update")
def update_actor(film_id: int, actor_id: int, db: Session = Depends(database),
              current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to update an actor")
    film_actor = db.query(FilmActor).filter(FilmActor.film_id == film_id, FilmActor.actor_id == actor_id).first()
    if not film_actor:
        raise HTTPException(404, "Film actor topilmadi")
    film_actor.film_id = film_id
    film_actor.actor_id = actor_id
    db.commit()
    raise HTTPException(200, "Actor updated successfully!!!")

@film_actor_router.delete("/delete")
def delete_actor(film_id: int, actor_id: int, db: Session = Depends(database),
              current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to delete an actor")
    film_actor = db.query(FilmActor).filter(FilmActor.film_id == film_id, FilmActor.actor_id == actor_id).first()
    if not film_actor:
        raise HTTPException(404, "Film actor topilmadi")
    db.delete(film_actor)
    db.commit()
    raise HTTPException(200, "Actor deleted successfully!!!")
