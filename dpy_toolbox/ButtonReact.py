import discord
from discord.ext import commands
from dpy_toolbox.core import EventFunction
from dpy_toolbox.ui.core import ButtonDisplay
from typing import Optional, Union, Callable

class ButtonReact(discord.ui.View):
    def __init__(self, timeout: Union[int] = 120):
        self._timeout = timeout

        super().__init__(timeout=self._timeout)

    def template(self, f,):
        async def wrapped(interaction: discord.Interaction):
            await f(interaction)

        return wrapped

    def add(self, text: Optional[str] = None, emoji: Optional[str] = None, callback: Union[Callable] = None):
        dis = ButtonDisplay(emoji, text)
        if not callback:
            callback = lambda i, b: None

        f = discord.ui.Button(**dis.to_kwargs)
        f.callback = self.template(callback)

        self.add_item(f)

    def remove(self, index: Union[int]):
        self.remove_item(self.children[index])