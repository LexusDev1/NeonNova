import nextcord
from nextcord.ext import commands

class Lock(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description="Locks the channel")
    async def lock(
        self,
        interaction: nextcord.Interaction,
        channel: nextcord.TextChannel = None,
        settings=None
    ):
        if settings == "--server":
            for channel in interaction.guild.channels:
                await channel.set_permissions(
                    interaction.guild.default_role,
                    reason=f"{interaction.user.name} Locked the channel {channel.name} with ```--server```",
                    send_messages=False
                )
            await interaction.response.send_message("Locked channels down", ephemeral=True)
        if channel is None:
            channel = interaction.message.channel
        await channel.set_permissions(
            interaction.guild.default_role,
            reason=f"{interaction.user.name} Locked the channel {channel.name}",
            send_messages=False
        )
        await interaction.response.send_message("Locked the channel", ephemeral=True)

def setup(client):
    client.add_cog(Lock(client))
