from create_bot import admins, bot
from decouple import config
from create_bot import logger


# Функция, которая выполнится когда бот завершит свою работу
async def stop_bot():
    try:
        for admin_id in admins:
            await bot.send_message(admin_id, 'Бот остановлен. За что?😔')
    except:
        pass

    await bot.delete_webhook()
    await bot.close()
