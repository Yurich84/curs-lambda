import json
import urllib3
from urllib3.exceptions import HTTPError
from bank_service import BankService 
from decimal import Decimal

class MonoService(BankService):

    def __init__(self, currency='EUR'):
        self.currency = currency
        self.obtain_rate()
        super().__init__(currency)

    http = urllib3.PoolManager()

    API_URL = 'https://api.monobank.ua/bank/currency'

    UAH = 980
    USD = 840
    EUR =978

    ISO_4217 = {
        'UAH': UAH,
        'USD': USD,
        'EUR': EUR,
    }

    @property
    def bank_name(self) -> str:
        return 'Mono'

    def get_label(self) -> str:
        return 'Mono ' + self.CURRENCY_SIGN[self.currency]

    def set_sell(self):
        self.sell = Decimal(str(self.rate['rateBuy']))

    def set_buy(self):
        self.buy = Decimal(str(self.rate['rateSell']))

    def obtain_rate(self):
        self.rate = next(
            (
                item for item in self._get_data() 
                if item['currencyCodeA'] == self.ISO_4217[self.currency] and item['currencyCodeB'] == self.UAH
            ), 
            None
        )

    def _get_data(self):
        try:
            response = self.http.request('GET', self.API_URL)
            return json.loads(response.data.decode('utf-8'))
        except HTTPError as e:
            raise NotFoundHttpException(str(e))