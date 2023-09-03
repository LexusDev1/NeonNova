import nextcord
from nextcord.ext import commands
import yaml
import os
import asyncio
import aiosqlite
import roblox

os.environ['PYTHONDONTWRITEBYTECODE'] = '1'

with open("./storage/yaml/configs.yaml", "r") as f:
    CONFIG = yaml.safe_load(f)

TOKEN = CONFIG['Discord']['TOKEN']

async def getprefix(client, message):
    async with aiosqlite.connect("./storage/db/prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (message.guild.id,))
            data = await cursor.fetchone()
            if data:
                return data
            else:
                try:
                    await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', (prefix, message.guild.id,))
                    await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (message.guild.id,))
                    data = await cursor.fetchone()
                    if data:
                        await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, message.guild.id,))
                except Exception:
                    return 'dsb?'
            
intents = nextcord.Intents.default()
intents.typing = False
intents.presences = False
intents.message_content = True
intents.members = True

roblox = roblox.Client()
client = commands.Bot(
    shard_count=10,
    command_prefix=getprefix,
    intents=intents,
    case_insensitive=False
)

async def load():
    for folder in os.listdir("./cogs"):
        if os.path.isdir(os.path.join("./cogs", folder)):
            for filename in os.listdir(os.path.join("./cogs", folder)):
                if filename.endswith(".py"):
                    cog_name = f"cogs.{folder}.{filename[:-3]}"
                    client.load_extension(cog_name)
                    print(f"Loaded Cog: {cog_name}")

async def main():
    await load()
    print("Hello")
    async with aiosqlite.connect("./storage/db/prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('CREATE TABLE IF NOT EXISTS prefixes (prefix TEXT, guild ID)')
        await db.commit()
    await client.start(TOKEN)

@client.event 
async def on_guild_join(guild):
    async with aiosqlite.connect("./storage/db/prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', ('dsb?', guild.id,))
        await db.commit()

@client.event 
async def on_guild_remove(guild):
    async with aiosqlite.connect("./storage/db/prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('DELETE FROM prefixes WHERE guild = ?', (guild.id,))
        await db.commit()
          
@client.slash_command(description="Sets the prefix")
async def setprefix(interaction: nextcord.Interaction, prefix=None):
    if prefix is None:
        return

    async with aiosqlite.connect("./storage/db/prefixes.db") as db:
        async with db.cursor() as cursor:
            await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (interaction.guild.id,))
            data = await cursor.fetchone()
            if data:
                await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, interaction.guild.id,))
                await interaction.response.send_message(content=f"Updated prefix to ```{prefix}```")
            else:
                await cursor.execute('INSERT INTO prefixes (prefix, guild) VALUES (?, ?)', (prefix, interaction.guild.id,))
                await cursor.execute('SELECT prefix FROM prefixes WHERE guild = ?', (interaction.guild.id,))
                data = await cursor.fetchone()
                if data:
                    await cursor.execute('UPDATE prefixes SET prefix = ? WHERE guild = ?', (prefix, interaction.guild.id,))
                    await interaction.response.send_message(content=f"Updated prefix to ```{prefix}```")
                else:
                    return
            await db.commit()

loop = asyncio.get_event_loop()
loop.run_until_complete(main())
