from dpy_toolbox import Bot, permissions  #import permissions from dpy-toolbox
import discord

bot = Bot(command_prefix='!', intents=discord.Intents.all())
TOKEN = ''  #Check example bot.py for how to use token from environment 

@bot.command()  #if you want to pass many users make a list of users like list=[1,2,3,4,5] then do "@permissions.is_user(*list)"
@permissions.is_user(784735765514158090, "837501363927646248") #Enter user-id of the person whom you want to be able to use this command as either string or integer
async def greet(ctx, *, name="John"): # Do \@Person in chat to get <@user-id> 
    await ctx.send(f"Hello, {name}!")

@bot.event
async def on_ready():
    print(f'Running as {bot.user}')

bot.run(TOKEN)
