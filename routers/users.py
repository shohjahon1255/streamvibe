from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, Response
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.requests import Request
from database import database
from models.users import Users
from utils.auth import (
    hash_password,
    pwd_context,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    create_access_token,
    REFRESH_TOKEN_EXPIRE_MINUTES,
    create_refresh_token,
    get_current_user,
)
from utils.save_file import save_file
from utils.slowapi_configuration import limiter

user_router = APIRouter()


@user_router.post("/sign_up")
def sign_up(full_name: str, email: str, password: str, image: UploadFile, db: Session = Depends(database)):
    users = db.query(Users).filter(Users.email == email).first()
    if users:
        raise HTTPException(400, 'Email already registered')

    user = Users(
        full_name=full_name,
        email=email,
        password=hash_password(password),
        image=save_file(image),
        role="admin"
    )
    db.add(user)
    db.commit()
    raise HTTPException(201, "Sign up successful !!!")


@user_router.post("/sign_in")
@limiter.limit("5/minute")
def sign_in(request: Request, db: Session = Depends(database), form_data: OAuth2PasswordRequestForm = Depends(), response: Response = None):

    user = db.query(Users).filter(Users.email == form_data.username).first()
    if user:
        is_validate_password = pwd_context.verify(form_data.password, user.password)
    else:
        is_validate_password = False

    if not is_validate_password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login yoki parolda xatolik",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )

    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_refresh_token(
        data={"sub": user.email}, expires_delta=refresh_token_expires
    )


    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=int(refresh_token_expires.total_seconds()),
        path="/"
    )

    return {
        "id": user.id,
        "access_token": access_token,
        "token_type": "bearer",
    }

@user_router.put("/update")
def update_profil(full_name: str, email: str, password: str, image: UploadFile, db: Session = Depends(database),
                    current_user: Users = Depends(get_current_user)):

    user = db.query(Users).filter(Users.email == email).first()
    if user:
        raise HTTPException(400, 'Email already registered')

    db.query(Users).filter(Users.id == current_user.id).update(
        {
            Users.full_name:full_name,
            Users.email: email,
            Users.password: hash_password(password),
            Users.image: save_file(image)
        }
    )
    db.commit()
    raise HTTPException(200, "User update successful !!!")


@user_router.delete("/delete")
def delete_profil(db: Session = Depends(database), current_user: Users = Depends(get_current_user)):

    db.query(Users).filter(Users.id == current_user.id).delete()
    db.commit()
    raise HTTPException(200, "User delete successful !!!")
