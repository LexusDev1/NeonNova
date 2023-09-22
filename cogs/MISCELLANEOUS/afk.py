import nextcord
from nextcord.ext import commands
import aiosqlite

class Afk(commands.Cog):
    def __init__(self, client):
        self.client = client
  
    @commands.Cog.listener()
    async def on_ready(self):
        setattr(self.client, "db", await aiosqlite.connect("./storage/db/main.db"))
        async with self.client.db.cursor() as cursor:
            await cursor.execute("CREATE TABLE IF NOT EXISTS afk (user INTEGER, guild INTEGER, reason TEXT)")
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id))
            data = await cursor.fetchone()
            if data:
                await message.channel.send(f"{message.author.mention}: Welcome back :tada:", delete_after=10)
                await cursor.execute("DELETE FROM afk WHERE user = ? AND guild = ?", (message.author.id, message.guild.id))
            if message.mentions:
                for mention in message.mentions:
                    await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (mention.id, message.guild.id))
                    data2 = await cursor.fetchone()
                    if data2 and mention.id != message.author.id:
                        await message.channel.send(f"```{mention.display_name} is currently AFK! Reason: {data2[0]}```", delete_after=10)
        await self.client.db.commit()
        await self.client.process_commands(message)
    
    @nextcord.slash_command(description="Afk command")
    async def afk(self, interaction: nextcord.Interaction, *, reason=None):
        if reason is None:
            reason = "No reason provided"
        async with self.client.db.cursor() as cursor:
            await cursor.execute("SELECT reason FROM afk WHERE user = ? AND guild = ?", (interaction.user.id, interaction.guild.id))
            data = await cursor.fetchone()
            if data:
                if data[0] == reason:
                    return await interaction.response.send_message("```You're already afk```")
                await cursor.execute("UPDATE afk SET reason = ? WHERE user = ? AND guild = ?", (reason, interaction.user.id, interaction.guild.id,))
            else:
                await cursor.execute("INSERT INTO afk (user, guild, reason) VALUES (?, ?, ?)", (interaction.user.id, interaction.guild.id, reason,))
                await interaction.response.send_message(f"```You're now afk for the reason {reason}```")
        await self.client.db.commit()

def setup(client):
    client.add_cog(Afk(client))
