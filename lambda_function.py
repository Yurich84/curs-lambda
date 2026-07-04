import datetime
from privat_service import PrivatService
from mono_service import MonoService
from telegram_service import TelegramService
from db_service import DbService

GOOD_PERSENTAGE = 0.9
DAY_FROM_SEND = 7

def lambda_handler(event, context):
    now = datetime.datetime.now()
    banks = []
    banks.append(PrivatService('USD'))
    banks.append(PrivatService('EUR'))
    banks.append(MonoService('EUR'))

    for bank in banks:
        if should_send(now.day, bank):
            response = TelegramService().send_message(bank.human_response())
            if(response['ok']):
                print('Message sent. ' + now.date().strftime('%d.%m.%Y') + ' Curs: ' + bank.human_response())
        DbService().set_data(bank)
        print(now.date().strftime('%d.%m.%Y') + ' Curs: ' + bank.human_response())

def should_send(day_of_month, bank_service):
    if bank_service.koeficient <= GOOD_PERSENTAGE:
        return True

    db = DbService()

    items = db.get_data(bank_service.bank_name, bank_service.currency)
    if items:
        min_item = min(items, key=lambda x: x["koeficient"])
        if day_of_month >= DAY_FROM_SEND and bank_service.koeficient < min_item['koeficient']:
            return True

    last_30_days = db.get_data_last_days(bank_service.bank_name, bank_service.currency, 30)
    if last_30_days:
        min_30_days = min(last_30_days, key=lambda x: x["koeficient"])
        if bank_service.koeficient < min_30_days['koeficient']:
            return True

    return False

if __name__ == '__main__':
    lambda_handler(None, None)
