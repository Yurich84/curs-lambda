import json
import datetime
from privat_service import PrivatService
from telegram_service import TelegramService

def lambda_handler(event, context):
    private = PrivatService('USD').render_block()
    response = TelegramService().send_message(private)
    current_date = datetime.datetime.now().date()

    if(response['ok']):
        print('Message sent. ' + current_date.strftime('%d.%m.%Y') + ' Curs: ' + private)