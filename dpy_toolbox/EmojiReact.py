import discord
from discord.ext import commands
from dpy_toolbox.core import EventFunctionWrapper
from typing import Optional, Union, Callable

class EmojiReact:
    def __init__(self, parent, table: Optional[dict] = None):
        self.parent = parent
        self.bot: commands.Bot = parent.bot
        self._table = table if table else {}
        self.callback_funcs = []

    def create_callback(self, message_id):
        @EventFunctionWrapper(events=["on_raw_reaction_add", "on_raw_reaction_remove"])
        async def callback(payload):
            if payload.emoji.name in self._table and payload.message_id == message_id and payload.member != self.bot.user:
                await self._table[payload.emoji.name](payload)

        return callback

    async def add(self, emoji: Union[str], func: Union[Callable]):
        self._table[emoji] = func

    async def remove(self, emoji: Union[str]):
        if emoji in self._table:
            self._table.pop(emoji)

    async def listen(self, message: Union[discord.Message]):
        for k in self._table:
            await message.add_reaction(k)
        f = self.create_callback(message.id)
        self.callback_funcs.append(f)
        self.parent.events.append(f)

    async def abort(self):
        for f in self.callback_funcs:
            self.callback_funcs.remove(f)
            self.parent.events.remove(f)

# dont inherit (had to rewrite whole class)
class EmojiReactRoler:
    def __init__(self, parent, table: Optional[dict] = None):
        self.parent = parent
        self.bot: commands.Bot = parent.bot
        self._table = table if table else {}
        self.callback_funcs = []

    def create_callback(self, message_id):
        @EventFunctionWrapper(events=["on_raw_reaction_add", "on_raw_reaction_remove"], pass_bot=True)
        async def callback(bot, payload):
            if payload.message_id == message_id and payload.emoji.name in self._table:
                if payload.event_type == "REACTION_ADD" and payload.member != self.bot.user:
                    await payload.member.add_roles(*self._table[payload.emoji.name][0])
                elif self._table[payload.emoji.name][1]:
                    guild = bot.get_guild(payload.guild_id)
                    member = discord.utils.get(guild.members, id=payload.user_id)

                    await member.remove_roles(*self._table[payload.emoji.name][0])

        return callback

    async def add(self, emoji: Union[str], role: Union[discord.Role, list[discord.Role]], remove_role: Union[bool] = True):
        self._table[emoji] = [[role] if isinstance(role, discord.Role) else role, [remove_role]]

    async def remove(self, emoji: Union[str]):
        if emoji in self._table:
            self._table.pop(emoji)

    async def listen(self, message: Union[discord.Message]):
        for k in self._table:
            await message.add_reaction(k)
        f = self.create_callback(message.id)
        self.callback_funcs.append(f)
        self.parent.events.append(f)

    async def abort(self):
        for f in self.callback_funcs:
            self.callback_funcs.remove(f)
            self.parent.events.remove(f)
