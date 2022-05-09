import discord
from discord.ext import commands
from dpy_toolbox.core import EventFunction
from typing import Optional, Union, Callable

class EmojiReact:
    def __init__(self, parent, table: Optional[dict] = None):
        self.parent = parent
        self.bot: commands.Bot = parent.bot
        self._table = table if table else {}
        self.callback_func = EventFunction(func=self.callback)
        self.callback_func.events = ["on_raw_reaction_add", "on_raw_reaction_remove"]

    async def callback(self, payload):
        if payload.member != self.bot.user and payload.emoji.name in self._table:
            await self._table[payload.emoji.name](payload)

    async def add(self, emoji: Union[str], func: Union[Callable]):
        self._table[emoji] = func

    async def remove(self, emoji: Union[str]):
        if emoji in self._table:
            self._table.pop(emoji)

    async def listen(self, message: Union[discord.Message]):
        for k in self._table:
            await message.add_reaction(k)
        self.parent.events.append(self.callback_func)

    async def abort(self):
        if self.callback_func in self.parent.events:
            self.parent.events.remove(self.callback_func)