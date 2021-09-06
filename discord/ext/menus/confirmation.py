import discord
from discord import abc
from discord.app import InteractionContext

class Confirm(discord.ui.View):
    def __init__(self, content: str, timeout: int, usercheck = True):
        super().__init__(timeout=timeout)
        self.content = content
        self.usercheck = usercheck
        self.value = None
        self.user = None

    def interaction_check(self, interaction):
        return self.user == interaction.user

    @discord.ui.button(label = "Confirm", style = discord.ButtonStyle.green)
    async def confirm_button(self, button: discord.ui.Button, interaction = discord.Interaction):

        if self.usercheck and not self.interaction_check(interaction):
            return

        self.value = True
        await self.stop()

    @discord.ui.button(label = "Deny", style = discord.ButtonStyle.red)
    async def deny_button(self, button: discord.ui.Button, interaction = discord.Interaction):

        if self.usercheck and not self.interaction_check(interaction):
            return

        self.value = False
        await self.stop()

    @property
    def confirmed(self):
        return self.value is True

    @property
    def denied(self):
        return self.value is False
        
    @property
    def timed_out(self):
        return self.value is None

    async def send(self, messageable: Union[abc.Messageable, InteractionContext], ephemeral: bool = False):
            """Sends a message with the paginated items.
            
            Parameters
            ------------

            messageable: :class:`discord.abc.Messageable`
                The messageable channel to send to.

            ephemeral: :class:`bool`
                Choose whether or not the message is ephemeral. Only works with slash commands.

            Returns
            --------

            :class:`~discord.Message`
                The message that was sent.
            """

            if not isinstance(messageable, (abc.Messageable, InteractionContext)):
                raise TypeError("messageable is not a messageable object")
            page = self.pages[0]
            if isinstance(messageable, discord.app.context.InteractionContext):
                message = await messageable.send(content = self.content , view = self, ephemeral = ephemeral)
            else:
                message = await messageable.send(content = self.content, view = self)
            await self.wait()
            return message