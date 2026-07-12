from app.infrastructure.db.models import ItemModel


class ItemRepository:

    def __init__(self, db):
        self.db = db

    def create(self, name: str, quantity: int):
        item = ItemModel(name=name, quantity=quantity)

        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)

        return item

    def get_all(self):
        return self.db.query(ItemModel).all()

    def get_by_id(self, item_id: int):
        return self.db.query(ItemModel).filter(ItemModel.id == item_id).first()
    
    def update(self, item: ItemModel, data: dict):
        for key, value in data.items():
            setattr(item, key, value)

        self.db.commit()
        self.db.refresh(item)
        return item

    def delete(self, item: ItemModel):
        self.db.delete(item)
        self.db.commit()