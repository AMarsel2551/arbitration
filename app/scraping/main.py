from decimal import Decimal
from app.databases.main import Database
from app.logger import log
from app.models import ErrorMessage
from app.scraping.api import get_currency
from app.scraping.functional import fgetsettings, send_message, fget_payments, fget_payment
from app.settings import DATA_RUB


def decomposition_type_payment():
    pass


async def start(data: dict):
    async with Database() as connection:
        settings = await fgetsettings(connection=connection)
        if isinstance(settings, ErrorMessage):
            log.error(f"settings is {settings}")
            return None

    info = await get_currency(data=data)
    if isinstance(info, ErrorMessage):
        log.error(f"info is {info}")
        return None

    message = ""

    for i in info:
        value = settings[i['currencyId']]
        if Decimal(i['price']) < value and float(i['frozenQuantity']) > 0:
            payment_list = data['payment']
            payment_name_list = [await fget_payment(p) or 'Неизвестный' for p in payment_list]

            message = f"Валюта: <b>{i['currencyId']}</b> \n"
            message += f"Курс: <b>{i['price']}</b> руб \n"
            message += f"Объем: <b>{i['lastQuantity']}</b> USDT \n"
            message += f"Лимиты: <b>{i['minAmount']}</b> руб - <b>{i['maxAmount']}</b> руб \n"
            message += f"Способ оплаты: {', '.join(payment_name_list)} \n"
            message += f"""<a href="https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod={','.join(payment_list)}">Перейти</a>\n\n"""

    if message:
        await send_message(user_id=1112458996, message=message)


async def main():
    for data in [DATA_RUB]:  # , data_kzt
        await start(data=data)


# import asyncio
#
# asyncio.run(main())
