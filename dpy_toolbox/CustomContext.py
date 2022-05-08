from typing import Union, Optional, Callable, Any, Iterable
import discord
from discord.ext import commands
import asyncio

class CustomContext(commands.Context):
    async def ask(self, question: Union[str, discord.Embed, None] = None,
            check: Callable = None, timeout: int = 120, delQuestion: bool = True,
            delAnswer: bool = True) -> Union[Optional[str], Any]:

        if question:
            match_question = {
                str: "content",
                discord.Embed: "embed"
            }
            question = await self.send(**{match_question[type(question)]: question})
        if not check:
            check = lambda m: m.author == self.author and m.channel == self.channel

        reply = None
        try:
            reply = await self.bot.wait_for("message", check=check, timeout=timeout)
        except asyncio.TimeoutError:
            pass

        if delQuestion:
            await question.delete()

        if not reply:
            return None

        if delAnswer:
            await reply.delete()

        return reply

    async def send_view(self, view, *args, **kwargs):
        m = await self.send(view=view, *args, **kwargs)
        setattr(view, "message", m)

    async def send_paginator(self, view):
        page = view.book.pages[0].content
        table = {
            discord.Embed: "embed",
            str: "content"
        }
        m = await self.send(**{table[type(page)]: page}, view=view)
        setattr(view, "message", m)