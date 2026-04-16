from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from models import RoleEnum
from datetime import datetime
import re

class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    role: RoleEnum = RoleEnum.buyer

class UserCreate(UserBase):
    password: str = Field(
        ..., 
        # Todo: 편의상 최소 1의 길이로 설정함, 추후에 수정할 것 (1~8)
        min_length=1, 
        # max_length=20,
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
