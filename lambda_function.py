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
    koeficient = bank_service.koeficient
    if koeficient <= GOOD_PERSENTAGE:
        return True

    now = datetime.datetime.now()
    start_of_month = int(datetime.datetime(now.year, now.month, 1).timestamp())
    thirty_days_ago = int((now - datetime.timedelta(days=30)).timestamp())

    items = DbService().get_data(
        bank_service.bank_name, bank_service.currency, min(start_of_month, thirty_days_ago)
    )

    def is_lowest(since):
        window = [x for x in items if x["timestamp"] >= since]
        return bool(window) and koeficient < min(x["koeficient"] for x in window)

    if day_of_month >= DAY_FROM_SEND and is_lowest(start_of_month):
        return True
    if is_lowest(thirty_days_ago):
        return True

    return False

if __name__ == '__main__':
    lambda_handler(None, None)
