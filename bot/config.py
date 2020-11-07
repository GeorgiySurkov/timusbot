import os


class Config:
    DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite://db.sqlite3')
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DEPLOY = os.getenv('DEPLOY', 0) == 1

    WEBHOOK_HOST = os.getenv('WEBHOOK_HOST')  # name your app
    WEBHOOK_PATH = os.getenv('WEBHOOK_PATH')
    WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

    WEBAPP_HOST = '0.0.0.0'
    WEBAPP_PORT = os.getenv('PORT')
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'basic': {
                'format': '[%(levelname)s] %(asctime)s - %(message)s',
                'datefmt': '%d %b %y %H:%M:%S'
            },
            'telegram': {
                '()': 'bot.utils.formatters.MyHtmlFormatter',
                'format': '<code>%(asctime)s</code> <b>%(levelname)s</b>\nFrom %(name)s:%(funcName)s\n%(message)s',
                # 'use_emoji': True
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'basic',
                'level': 'INFO',
                'stream': 'ext://sys.stdout'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'basic',
                'filename': os.getenv('APP_LOG_PATH', 'app.log'),
                'maxBytes': 256 * 2 ** 20,
                'backupCount': 10,
                'encoding': 'utf-8'
            },
            'error': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'ERROR',
                'formatter': 'basic',
                'filename': os.getenv('ERROR_LOG_PATH', 'error.log'),
                'maxBytes': 256 * 2 ** 20,
                'backupCount': 10,
                'encoding': 'utf-8'
            },
            'timus': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'basic',
                'filename': os.getenv('TIMUS_LOG_PATH', 'timus.log'),
                'maxBytes': 512 * 2 ** 20,
                'backupCount': 10
            },
            'telegram': {
                'class': 'telegram_handler.TelegramHandler',
                'token': TELEGRAM_TOKEN,
                'chat_id': int(os.getenv('LOGGING_CHAT_ID')),
                'level': 'ERROR',
                'formatter': 'telegram'
            }
        },
        'loggers': {
            'bot': {
                'propagate': False,
                'level': 'DEBUG',
                'handlers': [
                    'console',
                    'file',
                    'error',
                    'telegram'
                ],
            },
            'bot.timus': {
                'level': 'DEBUG',
                'propagate': True,
                'handlers': [
                    'timus'
                ]
            }
        }
    }
