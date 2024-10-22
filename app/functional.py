import aiohttp, re
from app.logger import log
from app.models import ErrorMessage
from app.scraping.api import get_currency, get_well_kzt_rub
from app.scraping.functional import fget_payment
from app.settings import tb_settings, DATA_RUB, DATA_KZT


async def send_message(user_id: int, message: str = ''):
    async with aiohttp.ClientSession() as session:
        r = await session.post(
            f'https://api.telegram.org/bot{tb_settings.TOKEN}/sendMessage',
            data={'chat_id': user_id, 'text': message, 'parse_mode': 'HTML'},
            ssl=False
        )
        try:
            r.raise_for_status()
        except aiohttp.ClientResponseError as e:
            log.error(f"status: {e.status} message: {str(e)}")
            return {'status': e.status, 'message': str(e)}

        return {'status': r.status, 'message': 'success'}


def filter_callback(c, data):
    return c.data in data


def check_mail(mail: str):
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$'
    if re.match(email_regex, mail):
        return mail
    else:
        return ErrorMessage(code=400, message="Некорректная почта!")


async def check_need_currency(data: dict, need: int, skip: int=0) -> dict:
    currency1_sum = 0 # USDT
    currency2_sum = 0 # RUB
    payment_name_list = [await fget_payment(p) or 'Неизвестный' for p in data['payment']]
    new_data = {}

    items = await get_currency(
        data=data
    )

    for i in items[skip:]:
        if currency2_sum > need:
            break

        currency2 = float(i['lastQuantity']) * float(i['price'])
        if currency2_sum + currency2 > need:
            currency2 = need - currency2_sum

        currency1_sum += round(currency2 * float(i['price']), 2)
        currency2_sum += currency2

    if currency1_sum and currency2_sum:
        new_data['currency'] = data['currencyId']
        new_data['currency_sum'] = round(currency1_sum)

        new_data['currency_usdt'] = data['tokenId']
        new_data['currency_usdt_sum'] = round(currency2_sum)

        new_data['well'] = round(currency1_sum / currency2_sum)

        new_data['payment_method'] = ', '.join(payment_name_list)
        new_data['url'] = f"""<a href="https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod={','.join(data['payment'])}">Перейти</a>\n\n"""

    return new_data


async def generate_message(message: str, data: dict) -> str:
    message = f"Валюта: <b>{data['currency']}</b> \n"

    message += f"{data['currency']}: <b>{data['currency_sum']}</b> \n"
    message += f"{data['currency_usdt']}: <b>{data['currency_usdt_sum']}</b> \n"

    message += f"Курс: <b>{data['well']}</b> \n"
    message += f"Способ оплаты: <b>{data['payment_method']}</b> \n"
    message += data['url']
    return message


async def calculation_profit(sum_kzt: int, well_kzt_rub: float, commission_swift: float, start_money_rub: int) -> dict:
    total_money_rub = round(sum_kzt / well_kzt_rub)
    commission_swift_rub = round(total_money_rub / 100 * commission_swift)
    profit_money_rub = round(total_money_rub - start_money_rub - commission_swift_rub)
    profit_money_per = round(profit_money_rub / (start_money_rub/100), 2)
    return {
        "start_money_rub": start_money_rub,
        "end_money_rub": total_money_rub,
        "commission_swift": commission_swift,
        "commission_swift_rub": commission_swift_rub,
        "profit_money_rub": profit_money_rub,
        "profit_money_per": profit_money_per,
    }


async def check_need():
    message = ""
    need_usdt = 1000
    well_kzt_rub = 5.09
    bank_info = await get_well_kzt_rub()
    if bank_info:
        for bi in bank_info:
            if bi['buyCode'] == "RUB" and bi['sellCode'] == "KZT":
                well_kzt_rub = float(bi['sellRate'])

    commission_swift = 0.45
    data_rub = await check_need_currency(data=DATA_RUB, need=need_usdt)
    data_kzt = await check_need_currency(data=DATA_KZT, need=need_usdt, skip=2)

    if not data_rub or not data_kzt:
        message = "Пусто!"

    for data_cur in [data_rub, data_kzt]:
        message += await generate_message(message=message, data=data_cur)

    profit = await calculation_profit(
        sum_kzt=int(data_kzt['currency_sum']),
        well_kzt_rub=well_kzt_rub,
        commission_swift=commission_swift,
        start_money_rub=int(data_rub['currency_sum'])
    )

    message += f"Начальная сумма, руб: <b>{profit['start_money_rub']}</b> \n"
    message += f"Окончательная сумма, руб: <b>{profit['end_money_rub']}</b> \n"

    message += f"Комиссия swift, %: <b>{profit['commission_swift']}</b> \n"
    message += f"Комиссия swift, руб: <b>{profit['commission_swift_rub']}</b> \n"

    message += f"Курс KZT->RUB, %: <b>{well_kzt_rub}</b> \n"

    message += f"Доходность, руб: <b>{profit['profit_money_rub']}</b> \n"
    message += f"Доходность, %: <b>{profit['profit_money_per']}</b> \n"

    await send_message(user_id=1112458996, message=message)


