# AdminTest.py
import discord
from discord.ext import commands

FILE_NAME = "AdminTest"
class AdminTest(commands.Cog):
    def __init__(self, client):
        self.client = client

    # Commands
    @commands.command(name='echo', help='Echos what user said.')
    async def echo(self, ctx, *args):
        """Echos what was inputed.

        Args:
            ctx (_type_): _description_
        """        
        await ctx.send(' '.join(args))

async def setup(client):
    await client.add_cog(AdminTest(client))
