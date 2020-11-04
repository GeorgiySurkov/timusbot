from aiogram import Bot, Dispatcher, executor, types
from logging.config import dictConfig
import asyncio

from . import db, timus
from .config import Config
from .middlewares import OnlyGroupsMiddleware

# Configure logging
dictConfig(Config.LOGGING)

bot = Bot(token=Config.TELEGRAM_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(
    OnlyGroupsMiddleware('Привет, я бот для [Тимуса](https://acm.timus.ru/)\.\n'
                         'Я могу вести рейтинг и отслеживать посылки привязанных аккаунтов\.'
                         'Я работаю только в групповых чатах, так что добавь меня в какой\-нибудь чат,'
                         ' чтобы протестировать меня\.', parse_mode=types.ParseMode.MARKDOWN_V2)
)


def run():
    loop = asyncio.get_event_loop()

    try:
        loop.run_until_complete(db.init(Config))
        if Config.DEPLOY:
            executor.start_webhook(dp, webhook_path=Config.WEBHOOK_PATH,
                                   host=Config.WEBAPP_HOST, port=Config.WEBAPP_PORT)
        else:
            executor.start_polling(dp, skip_updates=True)
    finally:
        # Graceful shutdown
        loop.run_until_complete(asyncio.gather(db.shutdown(), timus.shutdown()))


from . import handlers
