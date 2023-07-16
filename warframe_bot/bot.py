import disnake
from disnake.ext import commands

from warframe_bot import config

bot = commands.InteractionBot(intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print(f'{bot.user.name} is ready!')


bot.load_extensions('cogs')


if __name__ == '__main__':
    bot.run(config.BOT_TOKEN)
