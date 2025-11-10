from fastapi import APIRouter, Depends, HTTPException, UploadFile
from database import database
from models.crew import Crew
from sqlalchemy.orm import Session
from models.users import Users
from utils.auth import get_current_user
from utils.save_file import save_file

crew_router = APIRouter()

@crew_router.post("/add")
def add_crew(full_name: str, image: UploadFile, role: str, db: Session = Depends(database),
             current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to create a crew")
    crew = Crew(
        full_name=full_name,
        image=save_file(image),
        role=role
    )
    db.add(crew)
    db.commit()
    raise HTTPException(201, "Crew created successfully!!!")

@crew_router.get("/get")
def get_crew(db: Session = Depends(database),
             current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to get crew")
    crew = db.query(Crew).all()
    return crew



@crew_router.put("/update")
def update_crew(id: int, full_name: str, image: UploadFile, role: str, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to update a crew")
    db.query(Crew).filter(Crew.id == id).update(
        {
            Crew.full_name: full_name,
            Crew.image: save_file(image),
            Crew.role: role
        }
    )
    db.commit()
    raise HTTPException(200, "Crew updated successfully!!!")


@crew_router.delete("/delete")
def delete_crew(id: int, db: Session = Depends(database),
                current_user: Users = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(403, "You are not authorized to delete a crew")
    db.query(Crew).filter(Crew.id == id).delete()
    db.commit()
    raise HTTPException(200, "Crew deleted successfully!!!")