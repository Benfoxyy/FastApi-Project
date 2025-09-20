from pydantic import BaseModel, Field, field_validator
from datetime import datetime


class UserLoginSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)


class UserRegisterSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=100)
    password_conf: str = Field(..., min_length=8, max_length=100)

    @field_validator("password_conf")
    def check_password_match(cls, password_conf, validation):
        if not validation.data.get("password") == password_conf:
            raise ValueError("passwords does not match")
        return password_conf


class GetMeSchema(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    is_active: bool = Field(...)
    created_date: datetime = Field(...)
