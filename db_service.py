import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime
import random
from bank_service import BankService

class DbService:
    def __init__(self):
        self.create_resource()
        # self.create_client()

    time = datetime.now()

    def set_data(self, bank_service: BankService):
        item = {
            "id": int(random.randint(1000000, 9999999)),
            "timestamp": int(self.time.timestamp()),
            "time": self.time.strftime("%d-%m-%Y %H:%M:%S"),
            "bank": bank_service.bank_name,
            "currency": bank_service.currency,
            "sell": bank_service.sell,
            "buy": bank_service.buy,
            "koeficient": bank_service.koeficient,
        }
        self.table.put_item(Item=item)

    def get_data(self, bank_name: str, currency: str):
        now = datetime.now()
        start_of_month = int(datetime(now.year, now.month, 1).timestamp())

        response = self.table.scan(
            FilterExpression=
            Key('timestamp').gte(start_of_month) & 
            Key('bank').eq(bank_name) & 
            Key('currency').eq(currency)
        )

        return response['Items']

    def create_client(self):
        self.dynamodb_client = boto3.client("dynamodb" )

    def create_resource(self):
        table_name ="curs-lambda"
        self.dynamodb = boto3.resource("dynamodb" )
        self.table = self.dynamodb.Table(table_name)