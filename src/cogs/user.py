import asyncio

import disnake
from disnake.ext import commands, tasks

from objects import Manager
from utils.formatter import get_table, get_table_of_trader, get_table_fissures
from utils.translater import get_text as _

class UserCog(commands.Cog):
    """Work above cogs"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot
        self.manager = Manager()

        self.manager_loop.start()

    @commands.slash_command(
        name='info',
        description='Get short menu.'
    )
    async def get_info(self, inter: disnake.ApplicationCommandInteraction):
        """Get short menu."""
        components = [
            disnake.ui.Button(label=_('Places with Cycles'), style=disnake.ButtonStyle.primary, custom_id='places'),
            disnake.ui.Button(label=_('Void Trader'), style=disnake.ButtonStyle.primary, custom_id='void_trader'),
            disnake.ui.Button(label=_('Steel Trader'), style=disnake.ButtonStyle.primary, custom_id='steel_trader'),
            disnake.ui.Button(label=_('Void Fissures'), style=disnake.ButtonStyle.primary, custom_id='simple_fissures'),
            disnake.ui.Button(label=_('Storm Fissures'), style=disnake.ButtonStyle.primary, custom_id='storm_fissures'),
            disnake.ui.Button(label=_('Void Fissures of Steel Path'), style=disnake.ButtonStyle.primary,
                              custom_id='hard_fissures'),
            disnake.ui.Button(label=_('Requiem Fissures'), style=disnake.ButtonStyle.primary, custom_id='kuva_fissures'),
        ]
        await inter.send(ephemeral=True, components=components)

    @commands.Cog.listener('on_button_click')
    async def get_button_info(self, inter: disnake.MessageInteraction):
        match inter.component.custom_id:
            case 'places':
                embed = disnake.Embed(
                    title='',
                    description=get_table(_('Places with Cycles'), self.manager.get_info_places()),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'void_trader':
                embed = disnake.Embed(
                    title='',
                    description=get_table_of_trader(self.manager.void_trader.get_info(),
                                                    self.manager.void_trader.inventory.get_info(), _('Inventory')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'steel_trader':
                embed = disnake.Embed(
                    title='',
                    description=get_table_of_trader(self.manager.steel_trader.get_info(),
                                                    self.manager.steel_trader.inventory.get_info(), _('Offers')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'simple_fissures':
                embed = disnake.Embed(
                    title='',
                    description=get_table_fissures(_('Void Fissures'), self.manager.get_fissures_info('simple')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'storm_fissures':
                embed = disnake.Embed(
                    title='',
                    description=get_table_fissures(_('Storm Fissures'), self.manager.get_fissures_info('storm')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'hard_fissures':
                embed = disnake.Embed(
                    title='',
                    description=get_table_fissures(_('Void Fissures of Steel Path'), self.manager.get_fissures_info('hard')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case 'kuva_fissures':
                embed = disnake.Embed(
                    title='',
                    description=get_table(_('Requiem Fissures'), self.manager.get_fissures_info('kuva')),
                )
                await inter.send(embed=embed, ephemeral=True)

            case '_':
                return

    @tasks.loop(minutes=1)
    async def manager_loop(self):
        if self.manager.is_ready:
            self.manager.update()
            if self.manager.is_delete_fissures:
                asyncio.create_task(self.add_new_fissures())
                self.manager.is_delete_fissures = False
        elif not self.manager.is_ready:
            self.manager.prepare()

    async def add_new_fissures(self):
        await asyncio.sleep(180)
        self.manager.add_new_fissures()


def setup(bot: commands.InteractionBot):
    bot.add_cog(UserCog(bot))
