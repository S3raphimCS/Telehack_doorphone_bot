import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.redis import RedisStorage
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from decouple import config


scheduler = AsyncIOScheduler(timezone='Asia/Vladivostok')
admins = [int(admin_id) for admin_id in config('ADMINS').split(',')]

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

storage = RedisStorage.from_url(config("REDIS_URL"))

bot = Bot(token=config('TG_BOT_SECRET_KEY'), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=storage)
