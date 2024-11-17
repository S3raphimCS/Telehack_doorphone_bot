import json
from typing import List

import requests
from decouple import config

API_KEY_TYPE = config("API_KEY_TYPE")
API_TOKEN = config("API_TOKEN")


def get_user_tenant_id(telephone_number: str) -> int | None:
    url = "https://domo-dev.profintel.ru/tg-bot/check-tenant"

    payload = json.dumps({"phone": telephone_number})
    headers = {
        API_KEY_TYPE: API_TOKEN,
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    tenant_id = json.loads(response.content.decode('utf-8'))

    if tenant_id.get('tenant_id'):
        return tenant_id['tenant_id']
    return None


def get_tenants_apartments(tenant_id: int) -> List[tuple] | None:
    url = "https://domo-dev.profintel.ru/tg-bot/domo.apartment"

    params = {
        "tenant_id": tenant_id,
    }
    headers = {
        API_KEY_TYPE: API_TOKEN,
    }
    response = requests.request("GET", url, headers=headers, params=params)
    tenants_apartments = json.loads(response.content.decode('utf-8'))
    if "detail" not in tenants_apartments:
        apartments = [(apartment["id"], apartment["location"]["readable_address"]) for apartment in tenants_apartments]
        return apartments
    return None


def get_tenants_doorphones(apartment_id, tenant_id: int) -> List[tuple] | None:
    url = f"https://domo-dev.profintel.ru/tg-bot/domo.apartment/{apartment_id}/domofon"

    params = {
        "tenant_id": tenant_id,
    }
    headers = {
        API_KEY_TYPE: API_TOKEN,
    }
    response = requests.request("GET", url, headers=headers, params=params)
    tenants_doorphones = json.loads(response.content.decode('utf-8'))
    if "detail" not in tenants_doorphones:
        doorphones_data = [(doorphone["id"], doorphone["name"]) for doorphone in tenants_doorphones]
        return doorphones_data
    return None


def get_image_from_doorphone(tenant_id: int, intercoms_id: List[int], media_type: List[str]) -> str | None:
    url = "https://domo-dev.profintel.ru/tg-bot/domo.domofon/urlsOnType"

    params = {
        "tenant_id": tenant_id,
    }
    payload = json.dumps({"intercoms_id": intercoms_id, "media_type": media_type})
    headers = {
        API_KEY_TYPE: API_TOKEN,
    }
    response = requests.request("POST", url, headers=headers, params=params, data=payload)
    doorphone_image = json.loads(response.content.decode('utf-8'))
    if "detail" not in doorphone_image:
        return doorphone_image[0]["jpeg"]
    return None


def open_door(tenant_id: int, doorphone_id: int, door_id: int) -> str | None:
    url = "https://domo-dev.profintel.ru/tg-bot/domo.domofon/20/open"
    params = {
        "tenant_id": tenant_id,
        "domofon_id": doorphone_id,
    }
    headers = {
        API_KEY_TYPE: API_TOKEN,
    }
    payload = json.dumps({"door_id": door_id})
    response = requests.request("POST", url, headers=headers, params=params, data=payload)
    open_message = json.loads(response.content.decode('utf-8'))
    if "detail" not in open_message:
        return open_message["msg"]
    return None
