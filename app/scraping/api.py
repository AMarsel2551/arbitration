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
    "risktoken": "dmVyMQ|NmZjNGRiNTRmNm0wejNqcGh0NTZ4aGw4ZjIzNWE0NWM1||==",
    "sec-ch-ua": "\"Chromium\";v=\"130\", \"Google Chrome\";v=\"130\", \"Not?A_Brand\";v=\"99\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "traceparent": "00-af7aee650685901febc6ea3d8b8b11dd-1baa464e6aad7666-00",
    "cookie": "_by_l_g_d=ccb301f0-c632-2af7-ea5a-0c30a8f519e5; deviceId=1d5cfd03-a669-39ba-f0f9-e45155b44597; _gcl_au=1.1.1336501309.1729011202; tmr_lvid=22fbaee3d028056ff58e9863d1cb3f36; tmr_lvidTS=1726679266586; _ga=GA1.1.279121471.1729011203; _ym_uid=16718774101025552297; _ym_d=1729011203; _tt_enable_cookie=1; _ttp=zCcKBwWh4NeXJqO9c0kVjC9i49S; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%2220275521%22%2C%22first_id%22%3A%22192911937f4848-059febc5d8cf54-16525637-1764000-192911937f5b71%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%2C%22_a_u_v%22%3A%220.0.6%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTkyOTExOTM3ZjQ4NDgtMDU5ZmViYzVkOGNmNTQtMTY1MjU2MzctMTc2NDAwMC0xOTI5MTE5MzdmNWI3MSIsIiRpZGVudGl0eV9sb2dpbl9pZCI6IjIwMjc1NTIxIn0%3D%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%2220275521%22%7D%7D; _fbp=fb.1.1729460280050.52454424765093864; _abck=595985AE80A1B2318540B76BC11EE5CA~0~YAAQ2f0zuMqGzbCSAQAA4Rc2tQwLsYv8ltLWjZJ/T0jP25E3UtsQdHF8/oksHrkof+4WvPnbwHCa9u0VR5NGadqEr6PVMxAlaQ5Zuv9Z5w+TgkHirSvwXi2zE4iFuFL20lP6+Uv3zuVxU/BYI2N7V0HoGpvQSloNvCSCp6SGB4nYSG/pdwxkiDYJ5rOAeGR+Cy6r+xYd5rcFp41f386/oWl3Gl942DTD9Pc6T1YLeHejjO3IxIvojfLwEKSQTbsFNAunv6o/RfI/WTZOCN3cweVGi5gG/Ul4C5KB+a5UNZ0sergKeMcU69pMHbxqdDveC2Ny/kaJXNIv+7fhtR/yQCKWCpm8/wgCRjcio9eTp3BaOkGaIVC4vYXA1Q039vxX5EaHSgL4ZIUrNZMEYpgsJK9rBgU8UUHs3CQzrgEIRRB2nlVisdsNbzz0FJGMgg/YA91SM4n0csM=~-1~-1~-1; ak_bmsc=B5EA63B2E1D483AE765A82390DAF0B31~000000000000000000000000000000~YAAQ2f0zuMWIzbCSAQAALx02tRk7M6htcIrdDV6Ah0ulMCCopXrR+GgHUdJeb04RoEkt+/g7fJBt5iHYHEu5/QhNezy6IMlSmN8WoD9/4bPks/ahjS4aSJuGcWVXDHI0xcTG8seccIOeU57hi6UZ5h1xk1pgWM18SVVI+foRkO9l8rkD35v/hGsSV08u59VxERcK1RFnjWLE4Dcss4DfoqRNoyqhWtxNVU4ZyvRK3WCOujNhBclDqJLXtdKOQgdwTyG6CW8YxcP51aWBNHe/5S2KOocfo1wo2BeEECGMA1jCOzaCZd05f6w2KHY6cndU4kSCmSLG3uDQLfatQz1rPGUpGf84rfuLqZs+5E2JfUo9rpHyw94Gh+PLYLGVxDZ04ihzNXr3UhZwRpdIzNAoBwcj1FT3ppxDJXyZzSEWbIDpnGRZb4Nda+1iwTVdb60pBT0qKoUpUJnJdP8PfA==; _ym_isad=2; detection_time=1729641600000; secure-token=eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMDI3NTUyMSwiYiI6MCwicCI6MywidWEiOiIiLCJnZW5fdHMiOjE3Mjk2MTcxMDIsImV4cCI6MTcyOTg3NjMwMiwibnMiOiIiLCJleHQiOnsibWN0IjoiMTY0NjU2ODQ2MyIsInNpZCI6IkJZQklUIn0sImQiOmZhbHNlfQ.oIa9t6GCxe9AddPMhPz1RWhiZ47NKePz7kQaIh77bOd8gmjpwjCTDPYRXrFzH9--ey2LHKO-nXkp3hTp700Lsw; bm_sz=533234C24C71A9A0F418AD956A02BC3B~YAAQlh8WAouXM62SAQAALj5atRlBq68eX7dnTFRLqcxV6JRqeOXmnXH0KjXSxzNkLE1uPkk/aCBjSXEov/dyRbJRXN1QTSa5zuzXPF/VmqyScAMCH8aTyDWlxkKRRV5tWU7vMQoFJklBZ7wFsLpvQdPLiTyKi/GWZtQHK7fPON/9lgzMhGwd7VaS04Ekd1yuxL7GIBGngVkFU0nKk+982BQH5g0Wg5kRwsD59jY9VL+qV9Jt945aLFk/pkxhMS5Pm5jW+elkZ77nlDgzZzOIxP3ZmFQ+0bZzR1O+hBfQD47Ze1PLecm4aCQqrO2UM6rNKbcQfW8n+Q39KrRSimRWnP7DIhFvbfCq3daYe3zs3d/NYY8Gh28T3CwfmvDFaN/pih6cYx3mGrrjurr0J33q2MvDYI1ZqQiEudX0GyEJA1dCFyt4r1PAIw==~3291187~4539697; BYBIT_REG_REF_EXTRA_prod={\"original_referrer\":\"\",\"original_source\":\"\",\"original_medium\":\"direct\",\"original_last_url\":\"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=75\",\"original_last_refresh_time\":\"Tue, 22 Oct 2024 17:50:43 GMT\"}; BYBIT_REG_REF_prod={\"lang\":\"ru-RU\",\"g\":\"ccb301f0-c632-2af7-ea5a-0c30a8f519e5\",\"medium\":\"direct\",\"url\":\"https://www.bybit.com/fiat/trade/otc/?actionType=1&token=USDT&fiat=RUB&paymentMethod=75\",\"last_refresh_time\":\"Tue, 22 Oct 2024 17:50:43 GMT\"}; _ga_SPS4ND2MGC=GS1.1.1729619443.9.0.1729619443.60.0.0; bm_sv=9E672445AC396E17CE41A0F68BED8003~YAAQlh8WAiybM62SAQAATk1atRm8WL/sdekiU/25rD2X+0Mm5wLDuJKsrTiT4tyvzwEY5ktCRnKEzxRUNF+EPAyxuJqmPhJFa8cS1wqv06X6O4mSh/qvST/F6D3XVQ5gUapr002Yew3F4HW8XjSZvaucxCsI9w5hsSq/EDqlbqLE3YKSs9Uf6xZd/Fy7xGQgRVc7NZ3MqFE+LiHJN6PhHSINlxZjXUi/OjgRwF5iBgkp1dtllMkuoJoqxdVNH9ab~1",
    "Referer": "https://www.bybit.com/",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
  }



TIMEOUT = 10


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
