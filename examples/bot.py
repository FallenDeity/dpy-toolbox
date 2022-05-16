from dpy_toolbox import Bot #pip install dpy-toolbox
import discord #install dpy 2.0 pip install -U git+https://github.com/Rapptz/discord.py@rewrite#egg=discord.py[voice] Note: You need PyNaCl for voice support.
TOKEN = ''  #Just for example purposes. Please put the token in an .env file and use "token=os.environ['TOKEN']".

bot = Bot(command_prefix='!', intents=discord.Intents.all()) #Enable Intents in your bot page.

@bot.event 
async def on_ready():
    print(f'Running as {bot.user}') #prints bot name when up and running.

bot.run(TOKEN) #add your token fetched from environment.
