import roblox
import nextcord
from nextcord.ext import commands

class Roblox(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.roblox = roblox.Client()
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandError):
            await ctx.send(f"❌ An error occurred: `{error}`")
    
    @nextcord.slash_command(description="Search a user on Roblox")
    async def usrsearch(self, interaction: nextcord.Interaction, user: str = None):
        try:
            if user is None:
                await interaction.response.send_message("Please provide a username to search.")
                return
            
            users = self.roblox.user_search(user, max_items=None)
            
            embed = nextcord.Embed(title=f"Search Results for '{user}'")
            
            async for user in users:
                embed.add_field(name="NAME", value=f"```{user.name}```")
                embed.add_field(name="ID", value=user.id)
                embed.add_field(name="DISPLAY NAME", value=f"```{user.display_name}```")
            
            await interaction.response.send_message(embed=embed)
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: `{e}`")
  
    @nextcord.slash_command(description="Sends the group information")
    async def group(self, interaction: nextcord.Interaction, group: int = None):
        if group is None:
            await interaction.response.send_message("Please provide a valid group ID.")
            return

        try:
            group_data = await self.roblox.get_group(group)
        
            if group_data:
                embed = nextcord.Embed(title=f"Group Information: {group_data.name}")
                embed.add_field(name="ID", value=group_data.id)
                embed.add_field(name="MEMBERS", value=group_data.member_count)
                embed.add_field(name="OWNER", value=group_data.owner.display_name)
                
                if group_data.shout:
                    shout = group_data.shout
                    embed.add_field(name="CREATED", value=group_data.shout.created.strftime("%m/%d/%Y, %H:%M:%S"))
                    embed.add_field(name="BODY", value=f"{group_data.shout.body!r}")
                    embed.add_field(name="POSTER", value=group_data.shout.poster.display_name)

                await interaction.response.send_message(embed=embed)
            else:
                await interaction.response.send_message("Group not found.")
        except Exception as e:
            await interaction.response.send_message(f"❌ An error occurred: `{e}`")
            
    @nextcord.slash_command(description="Looks for the user information")
    async def rblxuser(self, interaction: nextcord.Interaction, *, userNames: str):
        users = await self.roblox.get_users_by_usernames(userNames, expand=True)
        for user in users:
            status = await self.roblox.get_status()
            embed = nextcord.Embed(title=f"Information for {userNames}")
            embed.add_field(name="NAME", value=user.name)
            embed.add_field(name="ID", value=user.id)
            embed.add_field(name="DISPLAY NAME", value=user.display_name)
            embed.add_field(name="CREATED", value=user.created.strftime("%m/%d/%Y, %H:%M:%S"))
            embed.add_field(name="STATUS", value=f"{status!r}")
            embed.add_field(name="DESCRIPTION", value=f"{user.description!r}")
            await interaction.response.send_message(embed=embed)

def setup(client):
    client.add_cog(Roblox(client))
