import base64
import os
from bitrix24_client import AsyncBitrix24Client
from config.config import BITRIKS_URL, BITRIKS_ACCESS_KEY, BITRIKS_DISK_FOLDER_ID


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
        # Собираем текст комментария (без ссылок TG, так как по политике безопасности B24 они могут не открываться)
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

        lead_add = await b24.call_method(
            "crm.lead.add",
            params={
                "fields": {
                    "TITLE": title,
                    "NAME": gas_dict["name"],
                    "ADDRESS": gas_dict["terrain"],
                    "COMMENTS": comment_text,
                    "PHONE": [{"VALUE": gas_dict["number"], "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": "WEBFORM",
                    "SOURCE_DESCRIPTION": "Телеграм бот газификация",
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )

        # Пробуем надёжно извлечь числовой ID лида из ответа API
        def _extract_lead_id(maybe_id):
            if isinstance(maybe_id, int):
                return maybe_id
            if isinstance(maybe_id, str) and maybe_id.isdigit():
                return int(maybe_id)
            if isinstance(maybe_id, dict):
                for key in ("result", "ID", "id", "data"):
                    if key in maybe_id:
                        nested = maybe_id[key]
                        got = _extract_lead_id(nested)
                        if got is not None:
                            return got
            return None

        lead_id = _extract_lead_id(lead_add)
        if lead_id is None:
            print("Unable to extract lead ID from response:", lead_add)
            lead_id = lead_add

        # Только загрузка файлов на Диск с наименованием "<LEAD_ID> файл 1", "<LEAD_ID> файл 2", ...
        files = gas_dict.get('files') or []
        if files:
            try:
                folder_id = int(BITRIKS_DISK_FOLDER_ID)
                index = 1
                for f in files:
                    file_path = f.get('path')
                    original_name = f.get('name') or 'file'
                    if not file_path:
                        continue
                    base, ext = os.path.splitext(original_name)
                    safe_ext = ext if ext else ''
                    new_name = f"{lead_id} файл {index}{safe_ext}"
                    try:
                        with open(file_path, 'rb') as fh:
                            content_bytes = fh.read()
                        encoded = base64.b64encode(content_bytes).decode()
                        res = await b24.call_method(
                            "disk.folder.uploadfile",
                            params={
                                "id": folder_id,
                                "data": {"NAME": new_name},
                                "fileContent": encoded,
                                "generateUniqueName": "Y",
                            },
                        )
                        print("Uploaded to Disk:", new_name, res)
                        # Удаляем локальный файл после удачной загрузки
                        try:
                            os.remove(file_path)
                            print("Local file removed:", file_path)
                        except Exception as rm_err:
                            print("Local file remove failed:", file_path, rm_err)
                        index += 1
                    except Exception as up_err:
                        print(f"Disk upload failed for {new_name}:", up_err)
            except Exception as e:
                print("Upload to configured disk folder failed:", e)

        return lead_add


async def send_market_lead(delivery, name, number, comment,):
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
                    "COMMENTS": f'товар - {comment}, доставка - {delivery}',
                    "PHONE": [{"VALUE": number, "VALUE_TYPE": "WORK"}],
                    "SOURCE_ID": "WEBFORM",
                    "SOURCE_DESCRIPTION": "Телеграм бот магазин",
                },
                "params": {"REGISTER_SONET_EVENT": "Y"},
            },
        )
        return result
