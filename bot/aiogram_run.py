import nest_asyncio
from aiogram.webhook.aiohttp_server import (SimpleRequestHandler,
                                            setup_application)
from aiohttp import web
from bot_stop import stop_bot
from create_bot import admins, bot, dp, logger
from data_base.base import create_tables
from decouple import config
from handlers.contact import router as contact_router
from handlers.endpoint_handlers import doorbell_handler
from handlers.start import router as start_router
from handlers.tenant_logic import router as tenant_router

nest_asyncio.apply()


async def start_bot():
    await create_tables()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Я запущен🥳')
        except Exception as err:
            logger.error("Ошибка рассылки сообщения админам при запуске: ", err)
    await bot.delete_webhook(drop_pending_updates=True)

    webhook_url = f'{config("BASE_URL")}/{config("TG_BOT_SECRET_KEY")}'
    try:
        await bot.set_webhook(webhook_url)
        logger.info(f"Webhook set to {webhook_url}")
    except Exception as e:
        logger.info(f"Error setting webhook: {e}")


def main():
    # Регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрация роутеров
    dp.include_routers(start_router, contact_router, tenant_router)

    app = web.Application()
    webhook_request_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot
    )
    webhook_request_handler.register(app, path=f'/{config("TG_BOT_SECRET_KEY")}')
    app.router.add_route('*', f'/{config("TG_BOT_SECRET_KEY")}/notify-door', doorbell_handler)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=config("HOST"), port=int(config("PORT")))


if __name__ == "__main__":
    main()
