
from app.domain.item.item_rules import ItemRules
from app.application.contracts.item_schemas import ItemResponse
from app.core.exceptions import NotFoundException


class ItemService:

    def __init__(self, repo):
        self.repo = repo

    def create_item(self, name: str, quantity: int):
        
        item =self.repo.create(name=name, quantity=quantity)

        return self._to_response(item)
    

    def get_items(self):
        items = self.repo.get_all()

        return [self._to_response(item) for item in items]
    

    def get_item(self, item_id: int):
        item = self.repo.get_by_id(item_id)

        if item is None:
            raise NotFoundException("Item not found")
        
        return self._to_response(item)


    def update_item(self, item_id: int, data: dict):
        item = self.repo.get_by_id(item_id)

        if item is None:
            raise NotFoundException("Item not found")

        updated = self.repo.update(item, data)

        return self._to_response(item)

        
    
    def delete_item(self, item_id: int):
        deleted = self.repo.get_by_id(item_id)
        if not deleted:
            raise NotFoundException("Item not found")
        
        self.repo.delete(deleted)
        return {"message": "Item deleted successfully"}

    def _to_response(self, item) -> ItemResponse:
         return ItemResponse(
             id=item.id,
             name=item.name,
             quantity=item.quantity,
             is_low_stock=ItemRules.is_low_stock(item.quantity),
         )
    