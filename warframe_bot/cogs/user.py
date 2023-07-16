import disnake
from disnake import ui
from disnake.ext import commands


class UserCog(commands.Cog):
    """Cog of getting info"""

    def __init__(self, bot: commands.InteractionBot):
        self.bot = bot

    async def get_buttons(self):
        buttons = [
            disnake.ui.Button(label='Full', style=disnake.ButtonStyle.primary, custom_id='full'),
            disnake.ui.Button(label='Cycles', style=disnake.ButtonStyle.primary, custom_id='cycles'),
            disnake.ui.Button(label='Baro Ki\'teer', style=disnake.ButtonStyle.primary, custom_id='void_trader'),
            disnake.ui.Button(label='Fissures of Void', style=disnake.ButtonStyle.primary, custom_id='fissures'),
        ]
        return buttons

    @commands.slash_command(
        name='get_info',
        description='Get short info about world of Warframe.',
    )
    async def get_info(self, inter: disnake.ApplicationCommandInteraction):
        """Get short info about world of Warframe."""
        components = await self.get_buttons()
        await inter.send(ephemeral=True, components=components)

    @commands.Cog.listener('on_button_click')
    async def answer_on_button_click(self, inter: disnake.MessageInteraction):
        if inter.component.custom_id == 'full':
            embed = disnake.Embed(title='All info about world of Warframe')
            embed.add_field(
                name='Location with cycles.',
                value='Earth, Cetus, Fortune, Cambion Drift, Zariman',
            )
            embed.add_field(
                name='Baro Ki\'teer',
                value='Location, left time',
            )
            embed.add_field(
                name='Fissures of Void',
                value='mission_location, mission_name, mission_type, mission_enemy, tier'
            )
            await inter.send(embed=embed, ephemeral=True)
        elif inter.component.custom_id == 'cycles':
            embed = disnake.Embed(
                title='Cycles of Warframe',
                description='Earth, Cetus, Fortune, Cambion Drift, Zariman'
            )
            await inter.send(embed=embed, ephemeral=True)
        elif inter.component.custom_id == 'void_trader':
            embed = disnake.Embed(
                title='Baro Ki\'teer',
                description='Location, left time'
            )
            await inter.send(embed=embed, ephemeral=True)
        elif inter.component.custom_id == 'fissures':
            embed = disnake.Embed(
                title='Fissures of Void',
                description='mission_location, mission_name, mission_type, mission_enemy, tier'
            )
            await inter.send(embed=embed, ephemeral=True)


def setup(bot: commands.InteractionBot):
    bot.add_cog(UserCog(bot))
