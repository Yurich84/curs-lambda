import boto3
from boto3.dynamodb.conditions import Key
from datetime import datetime, timedelta
from decimal import Decimal

class DbService:
    def __init__(self):
        self.create_resource()
        # self.create_client()

    time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    def set_data(self, bank, sell, buy, koeficient):
        self.table.put_item(Item={
            "time": self.time, 
            "bank": bank,
            "sell": Decimal(str(sell)),
            "buy": Decimal(str(buy)),
            "koeficient": Decimal(str(koeficient)),
        })

    def get_data(self):
        now = datetime.now()
        start_of_month = datetime(now.year, now.month, 1)
        end_of_month = datetime(now.year, now.month + 1, 1) - timedelta(days=1)

        response = self.table.scan(
            FilterExpression=Key('time').gte(start_of_month.strftime("%d-%m-%Y %H:%M:%S"))
        )

        return response['Items']

    def create_client(self):
        self.dynamodb_client = boto3.client("dynamodb" )

    def create_resource(self):
        table_name ="curs-logs"
        self.dynamodb = boto3.resource("dynamodb" )
        self.table = self.dynamodb.Table(table_name)