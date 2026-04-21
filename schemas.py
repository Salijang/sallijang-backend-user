from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from models import RoleEnum
from datetime import datetime


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum = RoleEnum.buyer


class UserCreate(UserBase):
    password: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="비밀번호는 문자, 숫자, 특수문자를 포함한 8~20자여야 합니다."
    )
    # Todo: 편의상 입력값 규칙확인하지 않도록 설정함, 추후에 수정할 것
    # @field_validator('password')
    # @classmethod
    # def validate_password_complexity(cls, v: str) -> str:
    #     if not re.match(r"^(?=.*[a-zA-Z])(?=.*\d)(?=.*[\W_]).{8,20}$", v):
    #         raise ValueError('비밀번호는 문자, 숫자, 특수문자를 모두 포함해야 합니다.')
    #     return v

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str
    role: str
    user_id: int
    full_name: str


class TokenData(BaseModel):
    email: Optional[str] = None


class WishlistCreate(BaseModel):
    user_id: int
    store_id: int


class WishlistResponse(BaseModel):
    id: int
    user_id: int
    store_id: int
    created_at: datetime

    class Config:
        from_attributes = True
