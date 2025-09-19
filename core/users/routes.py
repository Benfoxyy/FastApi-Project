from fastapi import APIRouter, Depends, HTTPException, status
from users.schemas import *
from sqlalchemy.orm import Session
from config.database import get_db
from users.models import UserModel

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
def user_login(request: UserLoginSchema ,db: Session = Depends(get_db)):
    user_obj = db.query(UserModel).filter_by(username=request.username.lower()).first()
    if not user_obj:
        raise HTTPException(detail="user does not exists", status_code=status.HTTP_400_BAD_REQUEST)
    if not user_obj.verify_password(request.password):
        raise HTTPException(detail="password is invalid", status_code=status.HTTP_400_BAD_REQUEST)
    return {}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if db.query(UserModel).filter_by(username=request.username.lower()).first():
        raise HTTPException(detail="user with this username alredy exists", status_code=status.HTTP_409_CONFLICT)
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    
    return {"message": "User registered successfuly"}