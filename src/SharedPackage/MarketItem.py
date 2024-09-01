class MarketItem:
    def __init__(self, name: str):
        self.name = name
        self.unit_price = 0
        self.amount = 0
        self.end_date = ""

    def __str__(self):
        return f'MarketItem(name={self.name}, unit_price={self.unit_price}, amount={self.amount}, end_date={self.end_date})'