from dpy_toolbox import Bot, ButtonDisplay, ButtonReact
import discord
TOKEN = ''  # BAD

bot = Bot(command_prefix='!', intents=discord.Intents.all())

async def rect_callback(inter: discord.Interaction):
    await inter.response.send_message(f"{inter.user} interacted with me!")

@bot.command()
async def rect(ctx):
    myView = ButtonReact()
    myView.add(rect_callback, ButtonDisplay(label="Text"))
    await ctx.send("Hello", view=myView)


@bot.event
async def on_ready():
    print(f'Running as {bot.user}')

bot.run(TOKEN)