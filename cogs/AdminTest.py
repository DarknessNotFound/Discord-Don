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
        try:
            await ctx.send(' '.join(args))
            print(ctx.author.id)
        except Exception as ex:
            print(f"ERROR -- AdminTest -- echo -- {ex}")

    @commands.command(name='dm_slide', help='Echos what user said.')
    async def dm_slide(self, ctx, *args):
        """Echos what was inputed.

        Args:
            ctx (_type_): _description_
        """        
        try:
            msg = "I just slid into your dms"
            await ctx.author.send(msg)

            if len(args) > 0:
                target = " ".join(args).split(" ")
                for t in target:
                    dis_id = t[2:-1]
                    user = await self.client.fetch_user(dis_id)
                    target_msg = f"{ctx.author.name} wanted me to slide into you dms ;)"
                    await user.send(target_msg)

        except Exception as ex:
            print(f"ERROR -- AdminTest -- dm_slide -- {ex}")

async def setup(client):
    await client.add_cog(AdminTest(client))
