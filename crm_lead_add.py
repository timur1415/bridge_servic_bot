import asyncio
from bitrix24_client import AsyncBitrix24Client
from config.config import BITRIKS_URL, BITRIKS_ACCESS_KEY


async def crm_lead_add():
    async with AsyncBitrix24Client(
        base_url="https://b24-huyq93.bitrix24.ru",
        access_token="s3hjh9c7ryxjtnsc",
        user_id=1,
    ) as b24:
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": "API    Lead",
                    "NAME": "TIMUR",
                    "PHONE": [{"VALUE": "+7 9999999999", "VALUE_TYPE": "WORK"}],
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        print(result)


async def send_mounter_lead(name_mounter, comment_mounter, number_mounter):
    async with AsyncBitrix24Client(
        base_url=BITRIKS_URL,
        access_token=BITRIKS_ACCESS_KEY,
        user_id=1,
    ) as b24:
        title = f'Заявка от монтажника-{name_mounter}'
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": name_mounter,
                    "COMMENTS": comment_mounter,
                    "PHONE": [{"VALUE": number_mounter, "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": 'WEBFORM',
                    "SOURCE_DESCRIPTION": 'Телеграм бот монтажники'
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        return result

async def send_gasification_lead(gas_dict):
    async with AsyncBitrix24Client(
        base_url=BITRIKS_URL,
        access_token=BITRIKS_ACCESS_KEY,
        user_id=1,
    ) as b24:
        title = f'Заказ на газификацию от {gas_dict['name']}'
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": gas_dict['name'],
                    "ADDRESS": gas_dict['terrain'],
                    'COMMENTS': f'Заказчику удобней получить расчёт через {gas_dict['apps']}, давление в газопроводе {gas_dict['pressure']}, {gas_dict['fasade']} метров по фасаду дома до дальней точки газа использующегося оборудования, {gas_dict['metre']} метров от забора до угла дома, Газоиспользующее оборудование находится в {gas_dict['room']} помешении, {gas_dict['project']} проект(а), {gas_dict['when']} планирует начать процесс газификации',
                    "PHONE": [{"VALUE": gas_dict['number'], "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": 'WEBFORM',
                    "SOURCE_DESCRIPTION": 'Телеграм бот газификация'
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        return result




if __name__ == "__main__":
    asyncio.run(send_gasification_lead('dima'))
