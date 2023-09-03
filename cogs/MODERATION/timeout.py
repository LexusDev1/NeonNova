from nextcord.ext import commands
import nextcord
import datetime
import humanfriendly

class Timeout(commands.Cog):
    def __init__(self, client):
        self.client = client

    @nextcord.slash_command(description="Timeouts a member")
    @commands.has_role("Operator")
    async def timeout(self, interaction: nextcord.Interaction, member: nextcord.Member, time, *, reason=None):
        time = humanfriendly.parse_timespan(time)
        guild = interaction.guild
        member = guild.get_member(member.id)  # Retrieve the member from the guild
        
        try:
            await member.edit(timeout=datetime.timedelta(minutes=time))
            embed = nextcord.Embed(description=f"<@{member.id}> has been timed out.", color=nextcord.Color.blue())
            await interaction.response.send_message(embed=embed)
        except nextcord.Forbidden:
            embed = nextcord.Embed(description="I don't have permission to perform this action.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        except nextcord.HTTPException as e:
            embed = nextcord.Embed(description=f"An error occurred: {e}", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
            
    @nextcord.slash_command(description="Removes the timeout from the user")
    @commands.has_role("Operator")
    async def untimeout(self, interaction: nextcord.Interaction, member: nextcord.Member = None, *, reason=None):
        guild = interaction.guild
        member = guild.get_member(member.id)
        try:
            await member.edit(timeout=None)
        except nextcord.Forbidden:
            embed = nextcord.Embed(description="I don't have permission to perform this action.", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)
        except nextcord.HTTPException as e:
            embed = nextcord.Embed(description=f"An error occurred: {e}", color=nextcord.Color.red())
            await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Timeout(client))
