import disnake
from disnake.ext import commands

from . import config

bot = commands.InteractionBot(intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')


if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)
