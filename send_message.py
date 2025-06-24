import asyncio
from bitrix24_client import AsyncBitrix24Client
from config.config import BITRIKS_URL

from config.config import DATA_IMAGE

async def crm_lead_add():
    async with AsyncBitrix24Client(
        base_url="https://b24-huyq93.bitrix24.ru", access_token="s3hjh9c7ryxjtnsc", user_id = 1
    ) as b24:
        result =await b24.call_method(
            "imconnector.register",
            {'ID':'15', 'NAME': 'CON15', 'ICON':{'DATA_IMAGE': DATA_IMAGE,},
             'PLACEMENT_HANDLER': ''}
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(crm_lead_add())