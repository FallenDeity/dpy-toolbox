import __main__
from typing import Union, Optional, Callable, Any, Iterable
from discord.ext import commands
import discord

from dpy_toolbox.exceptions import (
    NoEventFunction,
    NotAllowed
)

from dpy_toolbox.core import (
    EventFunction,
    EventFunctionWrapper
)

from dpy_toolbox.CustomContext import CustomContext

class Bot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.utils = self._utils(self)

    async def get_context(self, message, *, cls=CustomContext):
        return await super().get_context(message, cls=cls)

    class _utils:
        def __init__(self, bot):
            self.bot: commands.Bot = bot
            self.events = []
            self.patcher = self._patcher(self.bot)

            bot.add_listener(self.default_event_wrapper("on_message"), "on_message")
            bot.add_listener(self.default_event_wrapper("on_raw_reaction_add"), "on_raw_reaction_add")
            bot.add_listener(self.default_event_wrapper("on_raw_reaction_remove"), "on_raw_reaction_remove")

            self.events.append(self._AutoEmojiReact)
            self._auto_react_to_emojis = False
            self._auto_react_to_emojis_check = lambda m: not m.author.bot

        @property
        async def AutoReact(self):
            return self._auto_react_to_emojis

        @AutoReact.setter
        def AutoReact(self, emoji: Union[str, None], check: Union[Callable]=None):
            self._auto_react_to_emojis = emoji
            if check:
                self._auto_react_to_emojis_check = check

        @EventFunctionWrapper(events=["on_message"], pass_bot=True)
        async def _AutoEmojiReact(bot, message: discord.Message):
            if bot.utils._auto_react_to_emojis and bot.utils._auto_react_to_emojis_check(message):
                await message.add_reaction(bot.utils._auto_react_to_emojis)

        async def default_event(self, event_type, *args, **kwargs):
            for event in self.events:
                if event_type in event.wait_for_events:
                    call_with = []
                    if event.tags["pass_bot"]:
                        call_with.append(self.bot)
                    await event(*call_with, *args, **kwargs)

        def default_event_wrapper(self, event_type):
            async def func(*args, **kwargs):
                await self.default_event(event_type, *args, **kwargs)
            return func

        class _EmojiReact:
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

        def EmojiReact(self, **kwargs) -> _EmojiReact:
            return self._EmojiReact(self, **kwargs)

        class permissions:
            def is_user(*args):
                user_ids = [int(x) for x in args]
                async def predicate(ctx: commands.Context) -> bool:
                    if ctx.author.id not in user_ids:
                        raise NotAllowed(f"{ctx.author.id} is not allowed to use {ctx.invoked_with}")
                    return True

                return commands.core.check(predicate)

        class _patcher:
            def __init__(self, bot):
                self.bot = bot

            def patch_ctx(self):
                commands.Context = CustomContext
