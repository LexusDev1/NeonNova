import nextcord
from nextcord.ext import commands

class Purge(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description="Deletes messages based on the interval")
    @commands.has_permissions(administrator=True)
    async def purge(self, interaction: nextcord.Interaction, frequency: int = None):
        if frequency is None:
            await interaction.response.send_message("Please provide a valid frequency value.", ephemeral=True)
            return
        
        frequency = min(frequency + 1, 10000000000000000000000)
        if frequency > 90000000000000000000000:
            embed = nextcord.Embed(
                description="Purge amount exceeded 90000000000000000000000",
                color=nextcord.Color.red()
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.channel.purge(limit=frequency)
            await interaction.response.send_message(f"Successfully purged {frequency} messages.", ephemeral=True)

def setup(client):
    client.add_cog(Purge(client))
