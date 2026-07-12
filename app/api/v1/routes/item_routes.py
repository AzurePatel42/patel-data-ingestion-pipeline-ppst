from fastapi import APIRouter, Depends, HTTPException

from app.bootstrap.container import get_item_service
from sqlalchemy.orm import Session

from app.application.contracts.item_schemas import ItemCreateRequest, ItemResponse, ItemUpdateRequest

from app.bootstrap.container import get_item_service
from app.infrastructure.db.deps import get_db

router = APIRouter()


@router.post("/items", response_model=ItemResponse)
def create_item(payload: ItemCreateRequest, db = Depends(get_db)):

    service = get_item_service(db)

    item = service.create_item(

        name=payload.name,
        quantity=payload.quantity
    )

    return item

@router.get("/items", response_model=list[ItemResponse])
def get_items(db = Depends(get_db)):

    service = get_item_service(db)

    return service.get_items()


@router.get("/items/{item_id}", response_model=ItemResponse)
def get_item(item_id: int, db = Depends(get_db)):

    service = get_item_service(db)

    item = service.get_item(item_id)

    if not item:
        raise HTTPException(
            status_code=404,
            detail="Item not found"
        )

    return item

@router.put("/items/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, payload: ItemUpdateRequest, db: Session = Depends(get_db)):

    service = get_item_service(db)

    updated = service.update_item(item_id, payload.model_dump(exclude_unset=True))

    if not updated:
        raise HTTPException(status_code=404, detail="Item not found")

    return updated


@router.delete("/items/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):

    service = get_item_service(db)

    success = service.delete_item(item_id)

    if not success:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}
