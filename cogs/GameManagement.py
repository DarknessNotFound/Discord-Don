# GameManagement.py
import discord
from discord.ext import commands
from roles import RoleDB
from random import shuffle

# Temporary roles for Thursday's test.
townie_role_tmp = RoleDB(role_name="Townie", role_description="Trying to survive and vote out all killing roles")
mafia_role_tmp = RoleDB(role_name="Mafia", role_description="Trying to kill all players that aren't mafia.")
sheriff_role_tmp = RoleDB(role_name="Sheriff", role_description="Has a gun with a single bullet that can be shot at any time. If the guy shot was a killing role, then you survive. If the guy shot was innocent, you die as well.")

class GameManagement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = []  # List to store players who join the game
        self.roles = {}  # Dictionary to assign roles to players
        self.game_active = False  # Flag to track if a game is active
    
    # Starts the game and allows players to join if they're not active
    @commands.command(name='start_game', help='Starts a new game if one is not already active.')
    async def start_game(self, ctx):
        if self.game_active:
            await ctx.send("A game is already in progress! :(")
        else:
            self.game_active = True
            self.players.clear()
            self.roles.clear()
            await ctx.send("The game has started! Let's have fun! Use `>>join_game` to join.")

    # Allows players to join a active game
    @commands.command(name='join_game', help='Join the active game.')
    async def join_game(self, ctx):
        if not self.game_active:
            await ctx.send("There is no active game to join. Use `>>start_game` to start one.")
        elif ctx.author in self.players:
            await ctx.send(f"{ctx.author.mention}, you are already in the game!")
        else:
            self.players.append(ctx.author)
            await ctx.send(f"{ctx.author.mention} has joined the game!")

    # Allows players tp leave the game
    @commands.command(name='leave_game', help='Leave the current game.')
    async def leave_game(self, ctx):
        if ctx.author in self.players:
            self.players.remove(ctx.author)
            await ctx.send(f"{ctx.author.mention} has left the game.")
        else:
            await ctx.send(f"{ctx.author.mention}, you are not in the game.")

    # Ends the game, and clears the players and roles.
    @commands.command(name='end_game', help='Ends the current game.')
    async def end_game(self, ctx):
        if not self.game_active:
            await ctx.send("No game is currently active.")
        else:
            self.game_active = False
            self.players.clear()
            self.roles.clear()
            await ctx.send("The game has ended. Good game friends! :)")

    # Ends the game, and clears the players and roles.
    @commands.command(name='assign_roles', help='Assigns the roles to everyone.')
    async def assign_roles(self, ctx):
        try:
            print("Assign Roles called.")
            if not self.game_active:
                await ctx.send("No game is currently active.")
            elif len(self.players) < 1:
                await ctx.send("Not enough players joined, please ")
            else:
                print("Here")
                num_mafia = len(self.players) // 6
                num_sheriff = 1
                num_players = len(self.players) - num_mafia - num_sheriff
                await ctx.send(f"Assigning roles. There will be {num_mafia} mafia, {num_sheriff} sheriff, and {num_players} townies")

                roles_list = ["M" for x in range(num_mafia)] + ["S" for x in range(num_sheriff)] + ["T" for x in range(num_players)]
                shuffle(roles_list)
                assert len(roles_list) == len(self.players), "Number of players isn't equal to the number of roles."
                for i, p in enumerate(self.players):
                    print(f"Player: {p}")
                    channel = await p.create_dm()
                    if roles_list[i] == "M":
                        role_name = mafia_role_tmp.role_name
                        role_desc = mafia_role_tmp.role_description
                    elif roles_list[i] == "S":
                        role_name = sheriff_role_tmp.role_name
                        role_desc = sheriff_role_tmp.role_description
                    elif roles_list[i] == "T":
                        role_name = townie_role_tmp.role_name
                        role_desc = townie_role_tmp.role_description
                    else:
                        print("ERROR in GameManagement -- assign_roles")
                        role_name = "Error"
                        role_desc = "Error"
                    
                    msg = f"Your role is {role_name}. {role_desc}"
                    send_msg = await channel.send(msg)
        except Exception as ex:
            print(f"ERROR -- cogs/GameManagement -- assign_roles -- {ex}")

    @commands.command(name="dm_slide", help="The bot will slide into your DMs.")
    async def dm_slide(self, ctx, *args):
        client = ctx.author
        print(client)
        channel = await client.create_dm()
        print(channel)
        await channel.send("I slid into your DMs ;)")


    # Thanks the user, spread the love!
    @commands.command(name='thanks', help='Thank the bot and receive a response!')
    async def thanks(self, ctx):
        await ctx.send(f"You're welcome, {ctx.author.mention}! :D. I'm here to help!") 

async def setup(bot):
    await bot.add_cog(GameManagement(bot))
