import json
import urllib3
from urllib3.exceptions import HTTPError
import os
from bank_service import BankService 

class PrivatService(BankService):
    http = urllib3.PoolManager()

    API_URL = 'https://api.privatbank.ua/p24api/pubinfo?exchange&coursid=11'
    BUSINESS_API_URL = 'https://acp.privatbank.ua/api/proxy/currency'
    token = os.environ['PB_TOKEN']

    def get_label(self) -> str:
        return 'PB ' + self.CURRENCY_SIGN[self.currency]

    def set_sell(self):
        data = self._get_business_data()
        self.sell = float(data[self.currency]['B']['rate'])

    def set_buy(self):
        data = self._get_user_data()
        for item in data:
            if item['ccy'] == self.currency:
                self.buy = float(item['sale'])
                break

    def _get_business_data(self):
        try:
            headers = {'token': self.token}
            response = self.http.request('GET', self.BUSINESS_API_URL, headers=headers)
            data = json.loads(response.data.decode('utf-8'))
            if 'error' in data:
                raise NotFoundHttpException(data['error'])
            return data
        except HTTPError as e:
            raise NotFoundHttpException(str(e))

    def _get_user_data(self):
        try:
            response = self.http.request('GET', self.API_URL)
            return json.loads(response.data.decode('utf-8'))
        except HTTPError as e:
            raise NotFoundHttpException(str(e))