from app.application.item.item_service import ItemService
from app.core.exceptions import NotFoundException
import pytest


class FakeItem:
    def __init__(self, id, name, quantity):
        self.id = id
        self.name = name
        self.quantity = quantity


class FakeRepository:

    def create(self, name, quantity):
        return FakeItem(
            id=1,
            name=name,
            quantity=quantity
        )

    def get_all(self):
        return [
            FakeItem(1, "Keyboard", 10),
            FakeItem(2, "Mouse", 2)
        ]

    def get_by_id(self, item_id):
        if item_id == 1:
            return FakeItem(1, "Keyboard", 10)

        return None


def test_create_item():

    repo = FakeRepository()
    service = ItemService(repo)

    item = service.create_item(
        name="Laptop",
        quantity=8
    )

    assert item.id == 1
    assert item.name == "Laptop"
    assert item.quantity == 8
    assert item.is_low_stock is False


def test_low_stock():

    repo = FakeRepository()
    service = ItemService(repo)

    item = service.create_item(
        name="Cable",
        quantity=2
    )

    assert item.is_low_stock is True


def test_get_existing_item():

    repo = FakeRepository()
    service = ItemService(repo)

    item = service.get_item(1)

    assert item.id == 1
    assert item.name == "Keyboard"


def test_get_missing_item():

    repo = FakeRepository()
    service = ItemService(repo)

    with pytest.raises(NotFoundException):
        service.get_item(999)