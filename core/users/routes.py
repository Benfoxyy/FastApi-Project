from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from users.schemas import *
from sqlalchemy.orm import Session
from config.database import get_db
from users.models import UserModel
from users.jwt_auth import generate_access_token, get_authenticated_user

router = APIRouter(tags=["users"], prefix="/users")


@router.post("/login")
def user_login(request: UserLoginSchema, db: Session = Depends(get_db)):
    user_obj = (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    )
    if not user_obj:
        raise HTTPException(
            detail="user does not exists",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    if not user_obj.verify_password(request.password):
        raise HTTPException(
            detail="password is invalid",
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    access_token = generate_access_token(user_obj.id)
    return {
        "detail": "usre logged in successfuly",
        "access_token": access_token,
    }


@router.post("/register")
def user_register(request: UserRegisterSchema, db: Session = Depends(get_db)):
    if (
        db.query(UserModel)
        .filter_by(username=request.username.lower())
        .first()
    ):
        raise HTTPException(
            detail="user with this username alredy exists",
            status_code=status.HTTP_409_CONFLICT,
        )
    user_obj = UserModel(username=request.username.lower())
    user_obj.set_password(request.password)
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)

    access_token = generate_access_token(user_obj.id)
    return JSONResponse(
        content={
            "detail": "user registered in successfuly",
            "access_token": access_token,
        },
        status_code=status.HTTP_201_CREATED,
    )


@router.get(
    "/get-me", status_code=status.HTTP_201_CREATED, response_model=GetMeSchema
)
def get_me(
    db: Session = Depends(get_db),
    user: UserModel = Depends(get_authenticated_user),
):
    user_obj = db.query(UserModel).filter_by(id=user.id).one_or_none()
    if not user_obj:
        raise HTTPException(
            detail="user does not exists",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return user_obj
