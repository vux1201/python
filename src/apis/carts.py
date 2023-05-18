from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

import crud
import schemas
from apis.deps import get_current_user, get_db
from models.cart import CartItem, ShoppingSession
from models.user import User

router = APIRouter(prefix="/cart/items", tags=["Cart Item"])


@router.get(path="/me", response_model=list[schemas.CartItem])
async def read_items(
    *, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    shopping_session = current_user.shopping_session
    if not shopping_session:
        return []
    cart_items = shopping_session.cart_items
    return cart_items


@router.post(path="/me", response_model=schemas.CartItem)
async def create_item(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    item_in: schemas.CartItemCreate,
):
    shopping_session = current_user.shopping_session
    if not shopping_session:
        shopping_session = ShoppingSession(user_id=current_user.id)
    new_item = CartItem(product_variant_id=item_in.product_variant_id, qty=item_in.qty)
    shopping_session.cart_items.append(new_item)
    db.add(shopping_session)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.put(path="/me/{item_id}", response_model=schemas.CartItem)
async def update_item(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    item_id: int,
    item_in: schemas.CartItemUpdate,
):
    item = crud.cart_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    item = crud.cart_item.update(db=db, db_obj=item, obj_in=item_in)
    return item


@router.delete(path="/me/{item_id}", response_model=schemas.CartItem)
async def delete_item(
    *,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    item_id: int,
):
    item = crud.cart_item.get(db=db, id=item_id)
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="item not found"
        )
    item = crud.cart_item.remove(db=db, db_obj=item)
    return item
