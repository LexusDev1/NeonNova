import nextcord
from nextcord.ext import commands
import nekos

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def kiss(self, ctx, member: nextcord.Member):
        try:
            embed = nextcord.Embed(title=f'{ctx.author} kisses {member}')
            embed.set_image(url=nekos.img('kiss'))
            await ctx.send(embed=embed)
        except:
            ctx.send('An error occured')

    @commands.command()
    async def hug(self, ctx, member: nextcord.Member):
        try:
            embed = nextcord.Embed(title=f'{ctx.author} hugs {member}')
            embed.set_image(url=nekos.img('hug'))
            await ctx.send(embed=embed)
        except:
            ctx.send('An error occured')

    @commands.command()
    async def slap(self, ctx, member: nextcord.Member):
        try:
            embed = nextcord.Embed(title=f'{ctx.author} slaps {member}')
            embed.set_image(url=nekos.img('slap'))
            await ctx.send(embed=embed)
        except:
            ctx.send('An error occured')

    @commands.command()
    async def tickle(self, ctx, member: nextcord.Member):
        try:
            embed = nextcord.Embed(title=f'{ctx.author} tickles {member}')
            embed.set_image(url=nekos.img('tickle'))
            await ctx.send(embed=embed)
        except:
            ctx.send('An error occured')

    @commands.command()
    async def feed(self, ctx, member: nextcord.Member):
        try:
            embed = nextcord.Embed(title=f'{ctx.author} feeds {member}')
            embed.set_image(url=nekos.img('feed'))
            await ctx.send(embed=embed)
        except:
            ctx.send('An error occured')

def setup(client):
    client.add_cog(Fun(client))