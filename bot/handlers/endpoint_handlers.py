from aiohttp import web
from create_bot import bot
from data_base.queries import get_tenant_id_by_user_id
from keyboards.all_kb import open_door_kb_with_tenant_id_and_domofon_id
from utils.http_queries import (get_image_from_doorphone,
                                get_tenants_apartments, get_tenants_doorphones)


async def doorbell_handler(request):
    try:
        if request.method == 'GET':
            domofon_id = int(request.query.get('domofon_id'))
            tenant_id = int(request.query.get('tenant_id'))
            user_id = await get_tenant_id_by_user_id(tenant_id)
            check = 0
            if not user_id:
                return web.Response(text="Данный жилец не зарегистрирован в боте", status=400)
            if domofon_id and tenant_id:
                apartments = get_tenants_apartments(tenant_id)
                for apartment in apartments:
                    doorphones = get_tenants_doorphones(apartment[0], tenant_id)
                    for i in doorphones:
                        if domofon_id in i:
                            check = 1
                            break
                if check:
                    await bot.send_message(
                        user_id,
                        "Вам поступил звонок в домофон",
                    )
                    image_url = get_image_from_doorphone(tenant_id, [domofon_id], ["JPEG"])
                    if image_url:
                        await bot.send_photo(user_id, photo=image_url,
                                             reply_markup=open_door_kb_with_tenant_id_and_domofon_id(
                                                 (domofon_id, tenant_id)))
                    else:
                        await bot.send_message(
                            user_id,
                            "Ошибка при получении изображения с камеры. Возможно, камера не работает",
                            reply_markup=open_door_kb_with_tenant_id_and_domofon_id((domofon_id, tenant_id))
                        )
                else:
                    return web.Response(text="Переданный домофон недоступен пользователю", status=400)
                return web.Response(text="Отправил GET.")
            else:
                return web.Response(
                    text="Ошибка в запросе, возможно отсутствие одного из необходимых полей "
                         "'domofon_id' или 'tenant_id'",
                    status=400)
        elif request.method == 'POST':
            data = await request.json()
            domofon_id = int(data.get('domofon_id'))
            tenant_id = int(data.get('tenant_id'))
            if domofon_id and tenant_id:
                event_details = f"id_домофона: {domofon_id}, id_жильца: {tenant_id}"
                await bot.send_message(get_tenant_id_by_user_id(tenant_id), f"Звонок в домофон: {event_details}")
                return web.Response(text="Отправил POST.")
            else:
                return web.Response(
                    text="Ошибка в запросе, возможно отсутствие одного из необходимых полей "
                         "'domofon_id' или 'tenant_id'",
                    status=400)
        return web.Response(text="Invalid method. Only GET or POST is allowed.", status=405)
    except Exception as e:
        return web.Response(text=f"Ошибка: {str(e)}", status=500)
