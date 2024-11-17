import asyncio

from bot_stop import stop_bot
from create_bot import admins, bot, dp
from data_base.base import create_tables
from handlers.start import router as start_router
from handlers.contact import router as contact_router
from handlers.tenant_logic import router as tenant_router
from create_bot import logger


async def start_bot():
    await create_tables()
    for admin_id in admins:
        try:
            await bot.send_message(admin_id, 'Я запущен🥳')
        except Exception as err:
            logger.error("Ошибка рассылки сообщения админам при запуске: ", err)


async def main():
    # Регистрация функций
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    # Регистрация роутеров
    dp.include_routers(start_router, contact_router, tenant_router)

    # Запуск бота в режиме long polling при запуске бот очищает все обновления, которые были за его моменты бездействия
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())
