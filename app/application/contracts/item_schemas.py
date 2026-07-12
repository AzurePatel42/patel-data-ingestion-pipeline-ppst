from pydantic import BaseModel


class ItemCreateRequest(BaseModel):
    name: str
    quantity: int


class ItemResponse(BaseModel):
    id: int
    name: str
    quantity: int
    is_low_stock: bool

class ItemUpdateRequest(BaseModel):
    name: str | None = None
    quantity: int | None = None


    