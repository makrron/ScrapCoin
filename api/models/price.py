""" Class representing the Bitcoin Price model in fiat."""


# Path: api/models/price.py
class Price:
    """Class representing the Bitcoin Price model in fiat."""

    def __init__(self, price: float, pair: str, exchange: str, timestamp):
        self.price = price
        self.pair = pair
        self.exchange = exchange
        self.timestamp = timestamp

    def to_dict(self) -> dict:
        """
        Return a dictionary representation of the object.
        Returns: dict
        """
        return {
            "price": self.price,
            "pair": self.pair,
            "exchange": self.exchange,
            "timestamp": self.timestamp
        }

    @staticmethod
    def from_dict(data):
        """Create a Price object from a dictionary.
        Args: data (dict): A dictionary representing a Price.
        Returns: Price
        """
        return Price(
            price=data.get("price"),
            pair=data.get("pair"),
            exchange=data.get("exchange"),
            timestamp=data.get("timestamp")
        )
