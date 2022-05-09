# Discord.py Toolbox
## Made by TheWever

### Import d.py-toolbox
```
from dpy_toolbox import Bot
```

### Instantiate the bot
```
bot = Bot(command_prefix='!')
```

### EmojiReact (example):
```
# import offical discord.py lib
import discord
# import custom bot class
from dpy_toolbox import Bot
# token to run the bot later on
TOKEN = 'OTcwMzczODU0MTM4NjMwMjA0.Ym7BEw.vb3Bjais3Z2CmqKLHrwnNnd5E0w'

# new custom bot instance
bot = Bot(command_prefix='!', intens=discord.Intents.all())

# callback (used later)
async def emoji_callback(payload: discord.RawReactionActionEvent):
    # print on update
	print('User reacted')

# declare commnad
@bot.command()
async def emoji_react(ctx, *, message="test"):
    # send message in channel
    msg = await ctx.send(message)
    # new EmojiReact instance to handle reactions
    er = bot.utils.EmojiReact()
    # add emoji and callback to listen for
    await er.add("✅", emoji_callback)
    # start listening for updates on message
    await er.listen(msg)

# run bot
bot.run(TOKEN)
```
