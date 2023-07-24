import disnake
from disnake.ext import commands


class AdminCogs(commands.Cog):
    """Work above cogs"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    @commands.slash_command(
        name='load_cog',
        description='Load cog into bot.',

    )
    @commands.is_owner()
    async def load_cog(self, inter: disnake.ApplicationCommandInteraction, cog: str):
        """Load cog into bot"""
        try:
            name = f'cogs.{cog}'
            self.bot.load_extension(name)
            await inter.send(f'{cog} was loaded.', ephemeral=True)
        except (commands.ExtensionAlreadyLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)

    @commands.slash_command(
        name='unload_cog',
        description='Unload cog from bot.'
    )
    @commands.is_owner()
    async def unload_cog(self, inter: disnake.ApplicationCommandInteraction, cog: str):
        """Unload cog from bot"""
        try:
            name = f'cogs.{cog}'
            self.bot.unload_extension(name)
            await inter.send(f'{cog} was unloaded.', ephemeral=True)
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)

    @commands.slash_command(
        name='reload_cog',
        description='Reload cog from bot.'
    )
    @commands.is_owner()
    async def reload_cog(self, inter: disnake.ApplicationCommandInteraction, cog: str):
        """Reload cog from bot"""
        try:
            name = f'cogs.{cog}'
            self.bot.reload_extension(name)
            await inter.send(f'{cog} was reloaded.', ephemeral=True)
        except (commands.ExtensionNotLoaded, commands.ExtensionNotFound) as e:
            await inter.send(f'Error: {e}', ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(AdminCogs(bot))
