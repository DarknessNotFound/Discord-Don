import discord
from discord.ext import commands
import random
from database import *
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
            
            role_name = args[0]

            if len(args) >= 1:
                team_name = args[1]
            
            if len(args) >= 2:
                is_killing_str = args[2]

                if is_killing_str.isdigit():
                    is_killing_int = int(is_killing_str)
                    if is_killing_int != 1 and is_killing_int != 0:
                        is_killing = False
                        await ctx.send(f"Warning: \"Killing Role\" arguement is \"{is_killing_str}\" couldn't be parsed. Please input either a \"0\" for not a killing role or a \"1\" as a killing role. Defaulting to not a killing role.")
                    else:
                        if is_killing_int == 0:
                            is_killing = False
                        elif is_killing_int == 1:
                            is_killing = True
                        else:
                            raise Exception("Shouldn't ever get here, please fix your code.")
                else:
                    is_killing = 0
                    await ctx.send(f"Warning: \"Killing Role\" arguement is \"{is_killing_str}\" couldn't be parsed. Please input either a \"0\" for not a killing role or a \"1\" as a killing role. Defaulting to not a killing role.")
            else:
                is_killing = False

            if len(args) >= 3:
                is_flex_str = args[3]

                if is_flex_str.isdigit():
                    is_flex_int = int(is_flex_str)
                    if is_flex_int != 1 and is_flex_int != 0:
                        is_flex = False
                        await ctx.send(f"Warning: \"Killing Role\" arguement is \"{is_killing_str}\" couldn't be parsed. Please input either a \"0\" for not a killing role or a \"1\" as a killing role.")
                    else:
                        if is_flex_int == 0:
                            is_flex = False
                        elif is_flex_int == 1:
                            is_flex = True
                        else:
                            raise Exception("Shouldn't ever get here, please fix your code.")
            else:
                is_flex = False

            if len(args) > 4:
                role_description = " ".join(args[4:])
            else:
                role_description = ""
            
            role = RoleDB(
                id=None,
                server_id=str(ServerId),
                team_name=team_name,
                role_name=role_name,
                role_description=role_description,
                is_killing=is_killing,
                is_flex=is_flex,
            )

            id = UPSERT_ROLE(role)
            print(f"Upserted id: {id}")
            await ctx.send(f"Inserted role: {role.role_name}")
        except Exception as ex:
            print(f"ERROR -- RoleManagement -- addRole -- {ex}")


    @commands.command(name='allRoles', help='Displays all the roles. Use the \"-l\" flag to see the long form of all the roles.')
    async def allRoles(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """        
        ServerId = ctx.message.guild.id
        roles = SELECT_ROLES(ServerId)

        if len(roles) == 0:
            await ctx.send("No Roles found.")

        shorthand = True
        if len(args) >= 1:
            if args[0] == "-l":
                shorthand = False
        
        if shorthand:
            num_roles = 0
            msg = ""
            for r in roles:
                msg += r.shorthand_str() + "\n"
                num_roles += 1
                if num_roles == 20:
                    await ctx.send(msg)
                    num_roles = 0
                    msg = ""
            if num_roles != 0:
                await ctx.send(msg)
        else:
            for r in roles:
                await ctx.send(r.longhand_str())


    @commands.command(name='role', help='Reads a specific role, -l flag for longform: >>role id [-l]')
    async def readRole(self, ctx, *args):
        """Reads the specific role.
        """
        ServerId = ctx.message.guild.id

        if len(args) >= 1:
            id_str = args[0]
            if id_str.isdigit():
                id = int(id_str)
            else:
                await ctx.send(f"Id needs to be an integer, found \"{args[0]}\"")
                return

        shorthand = True
        if len(args) >= 2:
            if args[1] == "-l":
                shorthand = False
        
        r = SELECT_ROLE(id, ServerId)
        if r is None:
            await ctx.send("Role of id \"{}\" not found.")
        else:
            if shorthand:
                await ctx.send(r.shorthand_str())
            else:
                await ctx.send(r.longhand_str())


    @commands.command(name='updateRole', help='Updates the role.')
    async def updateRole(self, ctx, *args):
        """Updates the role.

        Args:
            ctx (_type_): _description_
        """        
        await ctx.send("Not implamented yet. Just delete the current one and add a new one!")


    @commands.command(name='deleteRole', help='Soft deletes the role.')
    async def deleteRole(self, ctx, *args):
        """Soft deletes the role.

        Args:
            ctx (_type_): _description_
        """
        UserDiscordId = ctx.author.id
        ServerId = ctx.message.guild.id

        if not IsAdmin(UserDiscordId, ServerId):
            await ctx.send("Only admins can delete a role.")
            return

        if len(args) >= 1:
            id_str = args[0]
            if id_str.isdigit():
                id = int(id_str)
            else:
                await ctx.send(f"Id needs to be an integer, found \"{args[0]}\"")
                return
        if DELETE_ROLE(id, ServerId):
            await ctx.send(f"Deleted role with id of {id}")
        else:
            await ctx.send(f"Failed to delete role with id of {id}")


async def setup(client):
    await client.add_cog(RoleMangaement(client))
