import disnake
from disnake.ext import commands

import settings

bot = commands.InteractionBot(intents=disnake.Intents.all())


@bot.event
async def on_ready():
    print('Bot is ready!')


if __name__ == '__main__':
    bot.run(settings.BOT_TOKEN)
