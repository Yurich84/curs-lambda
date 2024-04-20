import datetime
from privat_service import PrivatService
from telegram_service import TelegramService
from db_service import DbService

GOOD_PERSENTAGE = 0.5
DAY_FROM_SEND = 7

def lambda_handler(event, context):
    now = datetime.datetime.now()
    privat = PrivatService('USD')

    if should_send(now.day, privat):
        response = TelegramService().send_message(privat.human_response())
        if(response['ok']):
            print('Message sent. ' + now.date().strftime('%d.%m.%Y') + ' Curs: ' + privat.human_response())

    DbService().set_data('Privat', privat.sell, privat.buy, privat.calc_percentage())

def should_send(day_of_month, privat):
    if privat.calc_percentage() <= GOOD_PERSENTAGE:
        return True
    
    items = DbService().get_data()
    
    if not items:
        return False
    
    min_item = min(items, key=lambda x: x["koeficient"])
    if day_of_month >= DAY_FROM_SEND and privat.calc_percentage() < min_item['koeficient']:
        print(privat.calc_percentage(), type(privat.calc_percentage()), min_item['koeficient'], type(min_item['koeficient']))
        return True

if __name__ == '__main__':
    lambda_handler(None, None)
