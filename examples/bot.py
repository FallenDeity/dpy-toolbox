from dpy_toolbox import Bot
import discord
TOKEN = ''  # lol please dont do that this is just an example / put that in a .env

bot = Bot(command_prefix='!', intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f'Running as {bot.user}')

bot.run(TOKEN)