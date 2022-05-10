from discord.ext import commands
from dpy_toolbox.errors import NotAllowed

def is_user(*args):
    user_ids = [int(x) for x in args]

    async def predicate(ctx: commands.Context) -> bool:
        if ctx.author.id not in user_ids:
            raise NotAllowed(f"{ctx.author.id} is not allowed to use {ctx.invoked_with}")
        return True

    return commands.core.check(predicate)