import disnake
from disnake.ext import commands


class AdminCogs(commands.Cog):
    """Work above cogs"""

    PATH_COGS = 'cogs'

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command()
    @commands.is_owner()
    async def load(self, inter: disnake.ApplicationCommandInteraction, cog):
        try:
            self.bot.load_extension(f'{self.PATH_COGS}.{cog}')
            await inter.send(f"Cog '{cog}' load successfully!", ephemeral=True)
        except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)

    @commands.slash_command()
    @commands.is_owner()
    async def unload(self, inter: disnake.ApplicationCommandInteraction, cog):
        try:
            self.bot.unload_extension(f'{self.PATH_COGS}.{cog}')
            await inter.send(f"Cog '{cog}' unload successfully!", ephemeral=True)
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)

    @commands.slash_command()
    @commands.is_owner()
    async def reload(self, inter: disnake.ApplicationCommandInteraction, cog):
        try:
            self.bot.reload_extension(f'{self.PATH_COGS}.{cog}')
            await inter.send(f"Cog '{cog}' reload successfully!", ephemeral=True)
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(AdminCogs(bot))
