from typing import Union, Iterable
import discord
from itertools import chain
from dpy_toolbox.ui.core import ButtonDisplay

class Page:
    def __init__(self, content: Union[str, discord.Embed]):
        self.content = content

class Book:
    def __init__(self, iterator: Union[Iterable]):
        self._iterator = iterator
        getattr(iterator, "__len__")

    @property
    def pages(self):
        return self._iterator

    @property
    def page_count(self):
        return len(self._iterator)

    @classmethod
    def from_args(cls, *args):
        b = cls.__new__(cls)
        pages = []
        for p in args:
            pages.append(Page(p))
        b.__init__(pages)
        return b

    @classmethod
    def from_iter(cls, *args):
        b = cls.__new__(cls)
        pages = []
        for p in chain(*args):
            pages.append(Page(p))
        b.__init__(pages)
        return b

class NavigationOptions:
    FIRST = ButtonDisplay("⏪")
    LEFT = ButtonDisplay("◀️")
    RIGHT = ButtonDisplay("▶️")
    LAST = ButtonDisplay("⏩")
    DISABLE = ButtonDisplay("🗑️")

    ALL = [FIRST, LEFT, RIGHT, LAST, DISABLE]
    SMALL_PAGERS = [LEFT, RIGHT]
    BIG_PAGERS = [FIRST, LAST]


class Paginator(discord.ui.View):
    def __init__(self, book: Union[Book],
                 options: Union[NavigationOptions] = None,
                 timeout: Union[int] = 120):
        self.page = 0
        self.options = options if options else NavigationOptions()
        self.message = None
        self.book = book

        super().__init__(timeout=timeout)
        table = {
            "First": self.options.FIRST,
            "Left": self.options.LEFT,
            "Right": self.options.RIGHT,
            "Last": self.options.LAST,
            "Delete": self.options.DISABLE,
        }
        for child in self.children:
            child.label, child.emoji, child.style = table[child.label].set_args(child.label, child.emoji, child.style)

    async def turn_page(self, turn: Union[int]):
        if -1 < self.page + turn < self.book.page_count:
            self.page += turn
            return True
        return False

    async def update_book(self, interaction=None):
        page = self.book.pages[self.page].content
        table = {
            discord.Embed: "embed",
            str: "content"
        }
        if interaction:
            await interaction.response.edit_message(**{table[type(page)]: page})
        elif self.message:
            await self.message.edit(**{table[type(page)]: page})

    @discord.ui.button(label="First", style=discord.ButtonStyle.blurple)
    async def first(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page = 0
            await self.update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Left", style=discord.ButtonStyle.blurple)
    async def left(self, interaction: discord.Interaction, button: discord.ui.Button):
        paged = await self.turn_page(-1)
        if paged:
            await self.update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Right", style=discord.ButtonStyle.blurple)
    async def right(self, interaction: discord.Interaction, button: discord.ui.Button):
        paged = await self.turn_page(1)
        if paged:
            await self.update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Last", style=discord.ButtonStyle.blurple)
    async def last(self, interaction: discord.Interaction, button: discord.ui.Button):
        l = self.book.page_count - 1
        if self.page < l:
            self.page = l
            await self.update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.disable(interaction)

    async def on_timeout(self) -> None:
        await self.disable()

    async def disable(self, inter=None):
        self.first.disabled = True
        self.right.disabled = True
        self.left.disabled = True
        self.last.disabled = True
        self.delete.disabled = True
        if inter:
            await inter.response.edit_message(view=self)
        elif self.message:
            await self.message.edit(view=self)
        self.stop()