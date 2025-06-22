import asyncio
from bitrix24_client import AsyncBitrix24Client
from config.config import BITRIKS_URL


async def crm_lead_add():
    async with AsyncBitrix24Client(
        base_url="https://b24-huyq93.bitrix24.ru", access_token="s3hjh9c7ryxjtnsc"
    ) as b24:
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": "API    Leaaad",
                    "NAME": "TIMUR",
                    "PHONE": [{"VALUE": "+7 9999999999", "VALUE_TYPE": "WORK"}],
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        print(result)


if __name__ == "__main__":
    asyncio.run(crm_lead_add())
