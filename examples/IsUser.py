from dpy_toolbox import Bot
import discord

bot = Bot(command_prefix='!', intents=discord.Intents.all())
TOKEN = ''  # BAD

@bot.command()
@bot.utils.permissions.is_user(784735765514158090, "837501363927646248")
async def greet(ctx, *, name="John"):
    await ctx.send(f"Hello, {name}!")

@bot.event
async def on_ready():
    print(f'Running as {bot.user}')

bot.run(TOKEN)