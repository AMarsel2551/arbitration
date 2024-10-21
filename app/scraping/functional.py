import aiohttp
from typing import Union
from app.logger import log
from app.models import ErrorMessage
from app.scraping.api import get_payments
from app.scraping.database import db_getsettings
from app.settings import tb_settings
from cache import AsyncTTL


async def fgetsettings(connection) -> Union[dict, ErrorMessage]:
    settings = await db_getsettings(connection=connection)
    if not settings:
        return ErrorMessage(code=400, message="Ошибка базы")
    return {i['currency']: i['value'] for i in settings}


@AsyncTTL(time_to_live=60 * 60 * 24)
async def fget_payments() -> Union[dict, ErrorMessage]:
    payment_list = await get_payments()
    if isinstance(payment_list, ErrorMessage):
        return payment_list
    payment_dict = {}

    for payment in payment_list:
        paymentAlias = payment['paymentAlias']
        paymentType = payment['paymentType']
        checkType = payment['checkType']
        if checkType == 1:
            payment_dict[paymentType] = paymentAlias
    return payment_dict


async def fget_payment(payment: str) -> Union[str, None]:
    payments = await fget_payments()
    if isinstance(payments, ErrorMessage):
        return None
    return payments.get(payment)


async def send_message(user_id: int, message: str = ''):
    async with aiohttp.ClientSession() as session:
        r = await session.post(
            f'https://api.telegram.org/bot{tb_settings.TOKEN}/sendMessage',
            data={ 'chat_id': user_id, 'text': message, 'parse_mode': 'HTML'},
            ssl=False
        )
        try:
            r.raise_for_status()
        except aiohttp.ClientResponseError as e:
            log.error(f"status: {e.status} message: {str(e)}")
            return {'status': e.status, 'message': str(e)}

        return {'status': r.status, 'message': 'success'}