class ItemRules:
    LOW_STOCK_THRESHOLD = 5

    @staticmethod
    def is_low_stock(quantity: int) -> bool:
        return quantity <= ItemRules.LOW_STOCK_THRESHOLD