from app.infrastructure.repositories.item_repository import ItemRepository
from app.application.item.item_service import ItemService


def get_item_service(db):
    repository = ItemRepository(db)
    service = ItemService(repository)
    return service