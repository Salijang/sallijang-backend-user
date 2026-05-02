from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import List

from database import get_db
from deps import get_current_user, CurrentUser
import models
import schemas

router = APIRouter(prefix="/api/v1/wishlists", tags=["Wishlists"])


@router.get("/count")
async def count_store_wishlists(store_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(func.count(models.Wishlist.id)).filter(models.Wishlist.store_id == store_id)
    )
    return {"count": result.scalar()}


@router.post("/", response_model=schemas.WishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_wishlist(
    data: schemas.WishlistCreate,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Wishlist).filter(
            models.Wishlist.user_id == current_user.user_id,
            models.Wishlist.store_id == data.store_id,
        )
    )
    if result.scalars().first():
        raise HTTPException(status_code=409, detail="Already in wishlist")

    item = models.Wishlist(user_id=current_user.user_id, store_id=data.store_id)
    db.add(item)
    await db.commit()
    await db.refresh(item)
    return item


@router.get("/", response_model=List[schemas.WishlistResponse])
async def list_wishlists(
    store_id: int | None = None,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    query = select(models.Wishlist).filter(models.Wishlist.user_id == current_user.user_id)
    if store_id is not None:
        query = query.filter(models.Wishlist.store_id == store_id)
    query = query.order_by(models.Wishlist.created_at.desc())
    result = await db.execute(query)
    return result.scalars().all()


@router.delete("/{wishlist_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_wishlist(
    wishlist_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user),
):
    result = await db.execute(
        select(models.Wishlist).filter(models.Wishlist.id == wishlist_id)
    )
    item = result.scalars().first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlist item not found")
    if item.user_id != current_user.user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    await db.delete(item)
    await db.commit()
    return None
