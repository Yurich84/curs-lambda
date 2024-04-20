import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from decimal import Decimal
from bank_service import BankService 

class DbService:
    def __init__(self):
        self.create_resource()
        # self.create_client()

    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def set_data(self, bank_service: BankService):
        self.table.put_item(Item={
            "time": self.time, 
            "bank": bank_service.bank_name,
            "currency": bank_service.currency,
            "sell": bank_service.sell,
            "buy": bank_service.buy,
            "koeficient": bank_service.koeficient,
        })

    def get_data(self, bank_name: str, currency: str):
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)

        response = self.table.scan(
            FilterExpression=Key('time').gte(start_of_month.strftime("%d-%m-%Y %H:%M:%S")) & Key('bank').eq(bank_name) & Key('currency').eq(currency)
        )

        return response['Items']

    def create_client(self):
        self.dynamodb_client = boto3.client("dynamodb" )

    def create_resource(self):
        table_name ="curs-logs"
        self.dynamodb = boto3.resource("dynamodb" )
        self.table = self.dynamodb.Table(table_name)