import aiohttp
from typing import Union
from app.models import ErrorMessage


HEADERS = {
    "accept": "application/json",
    "accept-language": "ru-RU",
    "content-type": "application/json;charset=UTF-8",
    "guid": "ccb301f0-c632-2af7-ea5a-0c30a8f519e5",
    "lang": "ru-RU",
    "platform": "PC",
    "priority": "u=1, i",
    "risktoken": "dmVyMQ|YmMzODQzMTM2N20wenBsbTFvemU2MGI4ZjIzNTVkYzU1||==",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "traceparent": "00-47bd97309629df8285a22f73cc531469-ada623745ea23e4a-00",
    "cookie": "_by_l_g_d=ccb301f0-c632-2af7-ea5a-0c30a8f519e5; deviceId=1d5cfd03-a669-39ba-f0f9-e45155b44597; _gcl_au=1.1.1336501309.1729011202; tmr_lvid=22fbaee3d028056ff58e9863d1cb3f36; tmr_lvidTS=1726679266586; _ga=GA1.1.279121471.1729011203; _ym_uid=16718774101025552297; _ym_d=1729011203; _tt_enable_cookie=1; _ttp=zCcKBwWh4NeXJqO9c0kVjC9i49S; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2220275521%22%2C%22first_id%22%3A%22192911937f4848-059febc5d8cf54-16525637-1764000-192911937f5b71%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_a_u_v%22%3A%220.0.6%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTExOTM3ZjQ4NDgtMDU5ZmViYzVkOGNmNTQtMTY1MjU2MzctMTc2NDAwMC0xOTI5MTE5MzdmNWI3MSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjIwMjc1NTIxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2220275521%22%7D%7D; _ym_isad=2; secure-token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDI3NTUyMSwiYiI6MCwicCI6MywidWEiOiIiLCJnZW5fdHMiOjE3Mjk0NjAyNDksImV4cCI6MTcyOTcxOTQ0OSwibnMiOiIiLCJleHQiOnsibWN0IjoiMTY0NjU2ODQ2MyIsInNpZCI6IkJZQklUIn0sImQiOmZhbHNlfQ.Pj0ScrKDCrigAvNZxfScMXkV-6rz6wj14CngpJvPY7qsm5WSBFUCD7VPL2a4dAUb-3S_pSu4LPIbeTzZKhTgGg; _fbp=fb.1.1729460280050.52454424765093864; _abck=595985AE80A1B2318540B76BC11EE5CA~0~YAAQpTQWAivYE6OSAQAAywvurwyIBC5MgfdL5QAEaUQc/llTCHaq5RTrJb1yHdQ5RXHpUfHsQVYRytKyd3WvCodJ/JBtVadEzQfseoIrYbnoLPl9FnJc6pV7RyKecgYs8DZInT8DTfrdz2CqRHz+Iosv6aQ4iEWxQTr7th+MX7f0Vv/MidUqIgNufLadH4KlgsdCMPUaOULXtT0fN763o9JLY3XoAQk/P286r0IKjeXyXd9+3Mmzc5kMDxAboJXtj4GID/Wjcl+ebW4SAdEJBGdIOPxaXVgMhou6iM9sOLZD+q/F+vFNV8xiVSAZkir5+uhjS+LkCAu9cJsvQFEsgw/YJu6K5OW2FY4L0yA+iT8VIoyvC4dEDphhugVNXNDxUoPNNBVbTk1CT63erdZILbulX5oNOW72fWsoi6qkF9LXfRUJreVudVTWeuUc/Ah051NX2K6p7NA=~-1~-1~-1; ak_bmsc=BDAAA681038C6D1DDD0F720A6EC884AB~000000000000000000000000000000~YAAQpTQWAizYE6OSAQAAywvurxkCIBSZoH6Pff8JIHm6YMhqWjhY+7y7WUbkqlLgmptVquR6n986Qfav+TgPwVVsaDqPot+KQed2QnBH8Bu/M6TJcnTFl1cvBqdItItX5GC8UT55DakqKuMGzWobaHrxVPKDMuRMug+tSMd0YgqQ5rixvR+mo6dPiFczjOHxPI7b9VBIMq9yPcGLjrKn+LjfMOmGNXFbi0qnBz/7oP3XGeKyc6o+/J4L0dTXQS0eaew7Ytl0U+/FjxF5nBnrJ3Lup3rflivPSk8HRiK/yvS2f2gS3oTklljQVmTaerYnZ4lOI3rPxlz3B5CqFcxZ3HopFlVygIORP2tOclrP9LBYyi46ssWtnpHtubNrIM28Gs39oCOpxQTL; bm_sz=5D21341B5ED05D7041955EDF7E3FE0FF~YAAQpTQWAi7YE6OSAQAAywvurxm7BN4DODkybZ+exq9AEDUEVgjLXFW6m2i4pY7SLdc+0F/gPK0ANTD3DVMAokYeATeEpz4tGUJCs4DcyjVkPIkM8/U7XJKLdUtODS5GQpGzWPL9XVP+zDVgGUiz4/FBCxPgnXVhplGdGHaCIuajl7fCQPZUIXpPUSO6h9FuW28QkxObeQMoHhy40Br7pLDij611kNcCXlYxxVGo5EQchJfNEd68JL/FO7QmRKiKQlU2K0aZtUv45cN26kyZynbZAv4CTEEUygmXc20MYHBqdRA4QQWugOg6FApsKuom1iozZrE2MLETsI37q6WII9fwPzpjEf8oapG1+kUQ3WVcIq14d0VV8KkDwFvBplkKMybOlTeZTC4lRDuaMg==~3748932~3491125; BYBIT_REG_REF_EXTRA_prod={\"original_referrer\":\"\",\"original_source\":\"\",\"original_medium\":\"direct\",\"original_last_url\":\"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=75\",\"original_last_refresh_time\":\"Mon, 21 Oct 2024 16:34:28 GMT\"}; BYBIT_REG_REF_prod={\"lang\":\"ru-RU\",\"g\":\"ccb301f0-c632-2af7-ea5a-0c30a8f519e5\",\"medium\":\"direct\",\"url\":\"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=75\",\"last_refresh_time\":\"Mon, 21 Oct 2024 16:34:28 GMT\"}; _ga_SPS4ND2MGC=GS1.1.1729528467.4.1.1729528481.46.0.0; bm_mi=CDCA85E5C8D74186DA766EA2769EE88E~YAAQ2P0zuGTCCK+SAQAA1E77rxnFvPqPjyJ1xyQsJK1u/B9YsJz3mlMAYAVQWBk9nW+dkTEUuelLb5ikTLVOd9h8DrJ6VSJOK1HE/z5e/+qcCzRtYCM8IzY90ooCqgqZMSHhMTM9aH/xucB/gqXPkI4tHrd9NzmJ5mPsB2PQr26aVupsNFUHr48uvpbsE9twoN2cOJW1V/dnYvS+XiPhBOQoVTYQE6AuIrDyYrczIGA4/YHJj4d4PmiwycKokQCaJRUxrrZN38NRvOiCKq9wjXkmo8pKqoDFAqgmel1DXF+Ei5qcFhGQshziOZr9luG5XcZ6jGhCa8TtT8E=~1; bm_sv=2DCFDDCA05B32B2AA0502099DE569EB2~YAAQ2P0zuGXCCK+SAQAA1E77rxndtN3NR7P7HIwRbTMcfAOBsv0IusvGQpii2PaI4tDXxs2nEDW6Oz7Y9I0loMdQEP+rl4grpI2oBtfOESOCju3zPLbVWxNp0T/UE5a25/vRL9bHVCHLk9Izo/UhL3/ZHUfgk5FyKj361kqElNwCYCv/umMQzsnXF8kcdSRtFjeflNVz5tGT5FDhUC4WM5K/OmvM4J2TQ9joZhyxAlYtzK7B8IWQp/0X8DQo7TVV~1",
    "Referer": "https://www.bybit.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
  }


TIMEOUT = 5


async def get_currency(data: dict) -> Union[list, ErrorMessage]:
    async with aiohttp.ClientSession() as session:
        r = await session.post(
            f"https://api2.bybit.com/fiat/otc/item/online",
            json=data,
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if r.status == 200:
            info = await r.json()
            return info['result']['items']
        else:
            return ErrorMessage(code=400, message=f"Ошибка запроса: {r.status}")


async def get_payments() -> Union[list, ErrorMessage]:
    async with aiohttp.ClientSession() as session:
        r = await session.post(
            f"https://api2.bybit.com/fiat/otc/configuration/queryAllPaymentList",
            headers=HEADERS,
            timeout=TIMEOUT
        )
        if r.status == 200:
            info = await r.json()
            return info['result']['paymentConfigVo']
        else:
            return ErrorMessage(code=400, message=f"Ошибка запроса: {r.status}")


async def get_well_kzt_rub() -> Union[list, ErrorMessage]:
    async with aiohttp.ClientSession() as session:
        r = await session.get(
            f"https://bankffin.kz/api/exchange-rates/getRates",
            timeout=TIMEOUT
        )
        if r.status == 200:
            info = await r.json()
            return info['data']['mobile']
        else:
            return ErrorMessage(code=400, message=f"Ошибка запроса: {r.status}")
