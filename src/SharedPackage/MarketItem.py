class MarketItem:
    def __init__(self, name: str):
        self.name = name
        self.offers = list()

    def __str__(self):
        return f'MarketItem(name={self.name})'