from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from database import get_db
import models
import schemas

router = APIRouter(prefix="/api/v1/wishlists", tags=["Wishlists"])


@router.post("/", response_model=schemas.WishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_wishlist(data: schemas.WishlistCreate, db: AsyncSession = Depends(get_db)):
    """가게를 찜 목록에 추가합니다. 이미 찜한 경우 409를 반환합니다."""
    result = await db.execute(
        select(models.Wishlist).filter(
            models.Wishlist.user_id == data.user_id,
            models.Wishlist.store_id == data.store_id,
        )
    )
    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Already in wishlist")

    item = models.Wishlist(user_id=data.user_id, store_id=data.store_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/", response_model=List[schemas.WishlistResponse])
async def list_wishlists(user_id: int | None = None, store_id: int | None = None, db: AsyncSession = Depends(get_db)):
    """찜 목록 조회. user_id(사용자별) 또는 store_id(가게별)로 필터링합니다."""
    query = select(models.Wishlist)
    if user_id is not None:
        query = query.filter(models.Wishlist.user_id == user_id)
    if store_id is not None:
        query = query.filter(models.Wishlist.store_id == store_id)
    query = query.order_by(models.Wishlist.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_wishlist(wishlist_id: int, db: AsyncSession = Depends(get_db)):
    """찜 항목을 삭제합니다."""
    result = await db.execute(
        select(models.Wishlist).filter(models.Wishlist.id == wishlist_id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    await db.delete(item)
    await db.commit()
    return None
