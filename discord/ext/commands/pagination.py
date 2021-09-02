import discord, asyncio
from typing import List, Union

from discord import abc
from discord.ui.button import button

class Paginate(discord.ui.View):
    """Creates a paginator for embeds that is navigated with buttons.
    
    Parameters
    ------------
    send_to: :class:`discord.abc.Messageable`
    embed: List[:class:`discord.Embed`]
    """

    def __init__(self, send_to, embeds: List[discord.Embed]):
        super().__init__()
        self.send_to = send_to
        self.embeds = embeds
        self.current_page = 1

    @discord.ui.button(label = "<", style = discord.ButtonStyle.green, disabled=True)
    async def previous(self, button: discord.ui.Button, interaction = discord.Interaction):
        page_count = len(self.embeds)

        if not self.current_page:
            self.current_page = 1
        else:
            self.current_page -= 1

        if self.current_page == 1:
            button.disabled = True
            self.children[1].disabled = False

        await interaction.response.edit_message(embed = self.embeds[self.current_page-1], view = self)

    @discord.ui.button(label = '>', style=discord.ButtonStyle.green)
    async def forward(self, button: discord.ui.Button, interaction = discord.Interaction):
        page_count = len(self.embeds)
        self.children[0].disabled = False

        if not self.current_page:
            self.current_page = 1
        else:
            self.current_page += 1

        if self.current_page == page_count:
            button.disabled = True

        await interaction.response.edit_message(embed = self.embeds[self.current_page-1], view = self)

    async def send(self):
        """Sends a message with the paginated embeds."""
        if len(self.embeds) == 1:
            self.children[1].disabled = True
        if not isinstance(self.send_to, abc.Messageable):
            raise TypeError("send_to is not a messageable object")
        await self.send_to.send(embed = self.embeds[0], view = self)
