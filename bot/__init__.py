from aiogram import Bot, Dispatcher, executor, types
from aiogram.utils.exceptions import BadRequest
from logging.config import dictConfig
from logging import getLogger
import asyncio

from . import db, timus
from .config import Config
from .middlewares import OnlyGroupsMiddleware

# Configure logging
dictConfig(Config.LOGGING)
logger = getLogger(__name__)

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher(bot, asyncio.get_event_loop())
dp.middleware.setup(
    OnlyGroupsMiddleware('Привет, я бот для [Тимуса](https://acm.timus.ru/)\.\n'
                         'Я могу вести рейтинг и отслеживать посылки привязанных аккаунтов\. '
                         'Я работаю только в групповых чатах, так что добавь меня в какой\-нибудь чат, '
                         'чтобы протестировать меня\.', parse_mode=types.ParseMode.MARKDOWN_V2)
)

from .background_tasks import track_submissions


@dp.errors_handler()
async def global_error_handler(update, exc) -> bool:
    if isinstance(exc, BadRequest) and str(exc) == 'Have no rights to send a message':
        return True
    logger.exception(exc, exc_info=True)
    return True


def run():
    try:
        dp.loop.run_until_complete(db.init(Config))
        dp.loop.create_task(track_submissions(15))
        if Config.DEPLOY:
            executor.start_webhook(dp, webhook_path=Config.WEBHOOK_PATH,
                                   host=Config.WEBAPP_HOST, port=Config.WEBAPP_PORT,
                                   skip_updates=True)
        else:
            executor.start_polling(dp, skip_updates=True)
    finally:
        # Graceful shutdown
        dp.loop.run_until_complete(asyncio.gather(db.shutdown(), timus.shutdown()))


from . import handlers
