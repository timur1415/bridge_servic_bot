import base64
import logging
import os
from bitrix24_client import AsyncBitrix24Client
from config.config import (
    BITRIKS_URL,
    BITRIKS_ACCESS_KEY,
    BITRIKS_LEAD_FILES_FIELD,
)

logger = logging.getLogger(__name__)


async def send_mounter_lead(name_mounter, comment_mounter, number_mounter):
    async with AsyncBitrix24Client(
        base_url=BITRIKS_URL,
        access_token=BITRIKS_ACCESS_KEY,
        user_id=1,
    ) as b24:
        title = f"Заявка от монтажника-{name_mounter}"
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": name_mounter,
                    "COMMENTS": comment_mounter,
                    "PHONE": [{"VALUE": number_mounter, "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": "WEBFORM",
                    "SOURCE_DESCRIPTION": "Телеграм бот монтажники",
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
        title = f"Заказ на газификацию от {gas_dict['name']}"
        comment_lines = [
            f"Заказчику удобнее получить расчёт через {gas_dict['apps']}",
            f"Давление в газопроводе: {gas_dict['pressure']}",
            f"По фасаду: {gas_dict['fasade']} м",
            f"От забора до угла: {gas_dict['metre']} м",
            f"Помещения: {gas_dict['room']}",
            f"Проект: {gas_dict['project']}",
            f"План начала: {gas_dict['when']}",
        ]

        comment_text = ", ".join(comment_lines)

        lead_fields = {
            "TITLE": title,
            "NAME": gas_dict["name"],
            "ADDRESS": gas_dict["terrain"],
            "COMMENTS": comment_text,
            "PHONE": [{"VALUE": gas_dict["number"], "VALUE_TYPE": "WORK"}],
            "SOURCE_ID": "WEBFORM",
            "SOURCE_DESCRIPTION": "Телеграм бот газификация",
        }

        lead_add = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": lead_fields,
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        logger.info("Добавил лид в CRM: %s", lead_add)

        
        lead_id = lead_add
        if lead_id is None:
            logger.warning("Не удалось извлечь ID лида из ответа: %s", lead_add)
            lead_id = lead_add

        files = gas_dict.get("files") or []
        payload = []
        paths_to_delete = []
        for f in files:
            file_path = f.get("path")
            original_name = f.get("name") or "file"
            if not file_path or not os.path.exists(file_path):
                continue
            try:
                with open(file_path, "rb") as fh:
                    content_bytes = fh.read()
                encoded = base64.b64encode(content_bytes).decode()
                payload.append({"fileData": [original_name, encoded]})
                paths_to_delete.append(file_path)
            except Exception as err:
                logger.error("Не удалось прочитать файл: %s %s", file_path, err)

        if lead_id and BITRIKS_LEAD_FILES_FIELD and payload:
            try:
                update_res = await b24.call_method(
                    "crm.lead.update",
                    params={
                        "id": lead_id,
                        "fields": {BITRIKS_LEAD_FILES_FIELD: payload},
                    },
                )
                logger.info("Добавил файлы в поле лида: %s %s", lead_id, update_res)
                for p in paths_to_delete:
                    try:
                        os.remove(p)
                        logger.info("Удалил локальный файл: %s", p)
                    except Exception as rm_err:
                        logger.warning("Не удалось удалить локальный файл: %s %s", p, rm_err)
            except Exception as upd_err:
                logger.error("Не удалось добавить файлы в поле лида: %s %s", lead_id, upd_err)

        return lead_add


async def send_market_lead(
    delivery,
    name,
    number,
    comment,
):
    async with AsyncBitrix24Client(
        base_url=BITRIKS_URL,
        access_token=BITRIKS_ACCESS_KEY,
        user_id=1,
    ) as b24:
        title = f"Заявка на покупку в магазине-{name}"
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": name,
                    "COMMENTS": f"товар - {comment}, доставка - {delivery}",
                    "PHONE": [{"VALUE": number, "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": "WEBFORM",
                    "SOURCE_DESCRIPTION": "Телеграм бот магазин",
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        return result


async def send_business_lead(phone, name):
    async with AsyncBitrix24Client(
        base_url=BITRIKS_URL,
        access_token=BITRIKS_ACCESS_KEY,
        user_id=1,
    ) as b24:
        title = f"Заявка на газификацию бизнеса {name}"
        result = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": name,
                    "PHONE": [{"VALUE": phone, "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": "WEBFORM",
                    "SOURCE_DESCRIPTION": "Телеграм бот газ бизнес",
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        return result
