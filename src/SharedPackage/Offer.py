class Offer:
    def __init__(self, offer_type: str):
        self.offer_type = offer_type
        self.unit_price = 0
        self.amount = 0
        self.end_date = ""

    def __str__(self):
        return f'Offer(offer_type={self.offer_type}, unit_price={self.unit_price}, amount={self.amount}, end_date={self.end_date})'