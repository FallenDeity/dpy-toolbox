from typing import Union, Iterable
import discord
from itertools import chain
from .ui.core import ButtonDisplay

class Page:
    """
    A page of a book
    """
    def __init__(self, content: Union[str, discord.Embed]):
        self.content = content

class Book:
    """
    A collection of pages
    """
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
    """
    Default option class for paginator
    """
    FIRST = ButtonDisplay("⏪")
    LEFT = ButtonDisplay("◀️")
    RIGHT = ButtonDisplay("▶️")
    LAST = ButtonDisplay("⏩")
    DISABLE = ButtonDisplay("🗑️")

    ALL = [FIRST, LEFT, RIGHT, LAST, DISABLE]
    SMALL_PAGERS = [LEFT, RIGHT]
    BIG_PAGERS = [FIRST, LAST]


class Paginator(discord.ui.View):
    """
    Custom Paginator
    :param Book book: A book that will be used as an iterator
    :param NavigationOptions options: The options that will be used to create each button
    :param int timeout: The view's timeout
    :return: The paginator
    :rtype: discord.ui.View
    """
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

    async def _turn_page(self, turn: Union[int]):
        if -1 < self.page + turn < self.book.page_count:
            self.page += turn
            return True
        return False

    async def _update_book(self, interaction=None):
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
    async def _first(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.page > 0:
            self.page = 0
            await self._update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Left", style=discord.ButtonStyle.blurple)
    async def _left(self, interaction: discord.Interaction, button: discord.ui.Button):
        paged = await self._turn_page(-1)
        if paged:
            await self._update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Right", style=discord.ButtonStyle.blurple)
    async def _right(self, interaction: discord.Interaction, button: discord.ui.Button):
        paged = await self._turn_page(1)
        if paged:
            await self._update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Last", style=discord.ButtonStyle.blurple)
    async def _last(self, interaction: discord.Interaction, button: discord.ui.Button):
        l = self.book.page_count - 1
        if self.page < l:
            self.page = l
            await self._update_book(interaction)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Delete", style=discord.ButtonStyle.red)
    async def _delete(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self._disable(interaction)

    async def on_timeout(self) -> None:
        await self._disable()

    async def _disable(self, inter=None):
        self._first.disabled = True
        self._right.disabled = True
        self._left.disabled = True
        self._last.disabled = True
        self._delete.disabled = True
        if inter:
            await inter.response.edit_message(view=self)
        elif self.message:
            await self.message.edit(view=self)
        self.stop()