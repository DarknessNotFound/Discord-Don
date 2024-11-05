import discord
from discord.ext import commands
import random
from database import UPSERT_ROLE
from roles import RoleDB
from database_players import IsAdmin

class RoleMangaement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []
        self.roles = {} #Dict that stores roles by player

    # Commands
    @commands.command(name='addRole', help='Arguements: Role Name, Team name, Is Killing (1 or 0), Is Flex Class (1 or 0), Role Description. Note, Role name and team name must not have spaces.')
    async def addRole(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """
        try:
            UserDiscordId = ctx.author.id
            ServerId = ctx.message.guild.id
            if not IsAdmin(UserDiscordId, ServerId):
                await ctx.send("Only admins can add a role.")
                return
            
            if len(args) == 0:
                await ctx.send("No arguements inputed, aborting addRole.")
            
            input = ' '.join(args)
            role_name = input[0]

            if len(input) >= 1:
                team_name = input[1]
            
            if len(input) >= 2:
                is_killing_str = input[2]

                if is_killing_str.isdigit():
                    is_killing_int = int(is_killing_str)
                    if is_killing_int != 1 and is_killing_int != 0:
                        is_killing = False
                        await ctx.send(f"Warning: \"Killing Role\" arguement is \"{is_killing_str}\" couldn't be parsed. Please input either a \"0\" for not a killing role or a \"1\" as a killing role.")
                    else:
                        if is_killing_int == 0:
                            is_killing = True
                        elif is_killing_int == 1:
                            is_killing = False
                        else:
                            raise Exception("Shouldn't ever get here, please fix your code.")
            else:
                is_killing = False

            if len(input) >= 3:
                is_flex_str = input[3]

                if is_flex_str.isdigit():
                    is_flex_int = int(is_flex_str)
                    if is_flex_int != 1 and is_flex_int != 0:
                        is_flex = False
                        await ctx.send(f"Warning: \"Killing Role\" arguement is \"{is_killing_str}\" couldn't be parsed. Please input either a \"0\" for not a killing role or a \"1\" as a killing role.")
                    else:
                        if is_flex_int == 0:
                            is_flex = True
                        elif is_flex_int == 1:
                            is_flex = False
                        else:
                            raise Exception("Shouldn't ever get here, please fix your code.")
            else:
                is_flex = False


            if len(input) > 4:
                role_description = input[2:]
            else:
                role_description = ""
            
            role = RoleDB(
                id=None,
                server_id=ServerId,
                team_name=team_name,
                role_name=role_name,
                role_description=role_description,
                is_killing=is_killing,
                is_flex=is_flex,
            )

            UPSERT_ROLE(role)
        except Exception as ex:
            print(f"ERROR -- RoleManagement -- addRole -- {ex}")


    # Commands
    @commands.command(name='readRole', help='Updates the role.')
    async def updateRole(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """        
        await ctx.send(' '.join(args))

    # Commands
    @commands.command(name='updateRole', help='Updates the role.')
    async def updateRole(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """        
        await ctx.send(' '.join(args))

    # Commands
    @commands.command(name='Role', help='Updates the role.')
    async def updateRole(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """        
        await ctx.send(' '.join(args))


async def setup(client):
    await client.add_cog(RoleMangaement(client))
