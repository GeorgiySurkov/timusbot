from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler
from aiogram import types


class OnlyGroupsMiddleware(BaseMiddleware):
    """
    Middleware for providing bot functionality only in group chats.
    """

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        super(OnlyGroupsMiddleware, self).__init__()

    async def on_process_message(self, msg: types.Message, data: dict) -> None:
        if msg.chat.type == 'private':
            if len(self.args) > 0 or len(self.kwargs) > 0:
                await msg.answer(*self.args, **self.kwargs)
            raise CancelHandler()
