import logging
from decimal import Decimal

class BankService:
    CACHE_LIFETIME = 5 * 60

    CURRENCY_SIGN = {
        'UAH': '₴',
        'USD': '$',
        'EUR': '€',
    }

    def __init__(self, currency='EUR'):
        self._sell = 0
        self._buy = 0
        self.error_message = ''
        self.currency = currency
        try:
            self.set_sell()
            self.set_buy()
        except Exception as e:
            self.error_message = str(e)
            logging.error(e)

    def set_sell(self):
        raise NotImplementedError("Subclasses must implement set_sell method.")

    def set_buy(self):
        raise NotImplementedError("Subclasses must implement set_buy method.")

    def get_label(self) -> str:
        return type(self).__name__ + ' ' + self.CURRENCY_SIGN[self.currency]
    
    @property
    def bank_name(self) -> str:
        return type(self).__name__

    @property
    def koeficient(self) -> Decimal:
        return Decimal(str(round(((self.buy - self.sell) / self.buy) * 100, 2)))

    def formatted_values(self) -> str:
        percentage = self.get_koeficient()
        return f"{self.format_currency(self.sell)} / {self.format_currency(self.buy)} = {percentage}%"

    @staticmethod
    def format_currency(value: float) -> str:
        return "{:.2f}".format(value)

    def human_response(self) -> str:
        if not self.sell or not self.buy:
            return self.get_label() + '  ' + self.error_message
        return self.get_label() + '  ' + self.formatted_values()
