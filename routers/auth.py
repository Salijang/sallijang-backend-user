from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from database import get_db
import models
import schemas
import security
from deps import get_current_user, CurrentUser

router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

COOKIE_MAX_AGE = security.ACCESS_TOKEN_EXPIRE_MINUTES * 60


@router.post("/signup", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user: schemas.UserCreate, db: AsyncSession = Depends(get_db)):
    """새 사용자를 등록합니다. 이메일 중복 시 400 에러를 반환합니다."""
    result = await db.execute(select(models.User).filter(models.User.email == user.email))
    db_user = result.scalars().first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_password = security.get_password_hash(user.password)
    new_user = models.User(
        email=user.email,
        hashed_password=hashed_password,
        full_name=user.full_name,
        role=user.role
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


@router.post("/login")
async def login(
    response: Response,
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """이메일/비밀번호로 로그인하고 HttpOnly 쿠키로 JWT를 발급합니다."""
    result = await db.execute(select(models.User).filter(models.User.email == form_data.username))
    user = result.scalars().first()

    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = security.create_access_token(
        data={"sub": user.email, "role": user.role.value, "user_id": user.id},
        expires_delta=timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES),
    )

    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        domain=".sallijang.shop",
        max_age=COOKIE_MAX_AGE,
        path="/",
    )

    return {"role": user.role.value, "user_id": user.id, "full_name": user.full_name}


@router.post("/logout")
async def logout(response: Response):
    """HttpOnly 쿠키를 만료시켜 로그아웃합니다."""
    response.delete_cookie(
        key="access_token",
        domain=".sallijang.shop",
        path="/",
    )
    return {"message": "Logged out"}


@router.get("/me")
async def get_me(current_user: CurrentUser = Depends(get_current_user)):
    """현재 로그인된 사용자 정보를 반환합니다. 쿠키 유효성 확인용."""
    return {
        "user_id": current_user.user_id,
        "email": current_user.email,
        "role": current_user.role,
    }
