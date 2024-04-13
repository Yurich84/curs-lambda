import json
import urllib3
from urllib3.exceptions import HTTPError
import os
from bank_service import BankService 

class TelegramService:
    http = urllib3.PoolManager()

    token = os.environ['TELEGRAM_CURS_TOKEN']
    base_url = 'https://api.telegram.org/bot'

    def __init__(self, chat_id='-4131032347'):
        self.chat_id = chat_id

    def send_message(self, text):
        try:
            url = f"{self.base_url}{self.token}/sendMessage?chat_id={self.chat_id}&text={text}"

            response = self.http.request('GET', url)
            return json.loads(response.data.decode('utf-8'))
        except HTTPError as e:
            raise NotFoundHttpException(str(e))
