from privat_service import PrivatService

def lambda_handler(event, context):
    private = PrivatService('USD').render_block()
    print(private)