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
        self.sell = 0
        self.buy = 0
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

    def get_label(self):
        return type(self).__name__ + ' ' + self.CURRENCY_SIGN[self.currency]

    def calc_percentage(self):
        return Decimal(str(round(((self.buy - self.sell) / self.buy) * 100, 2)))

    def formatted_values(self):
        percentage = self.calc_percentage()
        return f"{self.format_currency(self.sell)} / {self.format_currency(self.buy)} = {percentage}%"

    @staticmethod
    def format_currency(value: float) -> str:
        return "{:.2f}".format(value)

    def human_response(self):
        if not self.sell or not self.buy:
            return self.get_label() + '  ' + self.error_message
        return self.get_label() + '  ' + self.formatted_values()
