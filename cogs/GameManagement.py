# GameManagement.py
import discord
from discord.ext import commands
import Game_CoreLoop
from roles import RoleDB
from random import shuffle

# Temporary roles for Thursday's test.
townie_role_tmp = RoleDB(role_name="Townie", role_description="Trying to survive and vote out all killing roles")
mafia_role_tmp = RoleDB(role_name="Mafia", role_description="Trying to kill all players that aren't mafia.")
sheriff_role_tmp = RoleDB(role_name="Sheriff", role_description="Has a gun with a single bullet that can be shot at any time. If the guy shot was a killing role, then you survive. If the guy shot was innocent, you die as well.")

FILE_NAME = "GameManagement.py"

class GameManagement(commands.Cog):

    GI = None

    def __init__(self, bot):
        self.bot = bot
    
    #Creates a GameInstance object if none exist, 
    @commands.command(name='create_game', help='Creates a new game if one is not already active.')
    async def create_game(self, ctx):
        try:
            if (self.GI):
                await ctx.send("A game has already been created for this Discord.")
            else:
                self.GI = Game_CoreLoop.GameInstance()
                self.GI.AddAuthor(ctx.author)
                await ctx.send("A game has been created.")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- create_game -- {ex}")


    #Starts game provided the GI exists, and the caller is one of the players.
    @commands.command(name='start', help='Starts a new game if one is not already active.')
    async def start(self, ctx):
        try:
            if (self.GI): #Check if we have a valid GameInstance to join.
                if self.GI.IsPlayerJoined(ctx.author): #Check that the caller is actually in said game.
                    await ctx.send("Game starting! You should recieve your roles shortly.")
                    lok = self.GI.StartGame()
                    await ctx.send(f"There are {lok} last of kind.")
                    
                    mafia_team = []
                    for player in self.GI.Players:
                        if player.PlayerRole.RoleName == "Mafia":
                            mafia_team.append(player.DisplayName)
                        if player.PlayerRole.RoleName == "Janitor":
                            mafia_team.append(f"Janitor({player.DisplayName})")

                    for player in self.GI.Players:
                        discord_id = player.DiscordId
                        user = await self.bot.fetch_user(discord_id)
                        msg = player.PlayerRole.msg()
                        if player.PlayerRole.RoleName == "Mafia":
                            msg += "\nMafia Team: "
                            for m in mafia_team:
                                msg += f"{m}, "
                        await user.send(msg)
                    
                    await ctx.send("All Roles have been sent, you can begin.")

                else:
                    await ctx.send("You are currently not in the current game. Use >>join_game to hop in!")
            else:
                await ctx.send("Use create_game to create a lobby that other players can join, then start the game when you're ready!")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- start_game -- {ex}")


    # Allows players to join a active game or waiting lobby
    @commands.command(name='join', help='Join the active game.')
    async def join(self, ctx):
        try:
            if (self.GI): #check if GI is valid
                if self.GI.IsPlayerJoined(ctx.author): #Check that the caller is actually in said game.
                    await ctx.send("You've already joined the game.")
                else:
                    self.GI.AddAuthor(ctx.author)
                    await ctx.send(f"{ctx.author.mention} has joined the game.")              
                    if (self.GI.GameStarted): #check if GI has started.
                        await ctx.send("Game in progress, you will respawn next game. Sit tight!")
            else:
                await ctx.send("Game has not be created yet, please sit tight.")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- join -- {ex}")


    # Allows players to leave the game
    @commands.command(name='leave', help='Leave the current game.')
    async def leave(self, ctx):
        try:
            if(self.GI):
                if self.GI.IsPlayerJoined(ctx.author): #Check that the caller is actually in said game.
                    self.GI.RemovePlayer(ctx.author)
                    await ctx.send(f"{ctx.author.mention} has left the game.")
                    if len(self.GI.Players) == 0:
                        await self.break_lobby(ctx)
                else:
                    await ctx.send("You aren't in an active game.")
            else:
                await ctx.send("There isn't an active game running.")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- leave -- {ex}")

    #Player can report that they are dead to the bot
    @commands.command(name = 'dead', help = 'Report your death to the GM. \n Use this if you are sent to the ghost box.')
    async def kill_player(self, ctx):
        try:
            if (self.GI): #check if GI is valid
                if self.GI.IsPlayerJoined(ctx.author): #Check that the caller is actually in said game.
                    self.GI.KillPlayer(ctx.author)
                    await ctx.send(f"The uhhh.... \"{ctx.author.mention}\" has been killed.")
                    if self.GI.CheckTeamCounts() == 1:
                        await self.end_game(ctx)
                else:
                    await ctx.send(f"You aren't in this game dummy.")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- kill_player -- {ex}")

    # Ends the game, and clears the players and roles.
    @commands.command(name='end', help='Ends the current game.')
    async def end(self, ctx):
        try:
            if not self.GI and self.GI.GameStarted:
                await ctx.send("No game is currently active.")
            else:
                self.GI.EndGame("Winners winner chicken dinner")
                await ctx.send(self.GI.EchoStats("TODO"))
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- end_game -- {ex}")

    #Mainly for testing, allow user to display the lobby names.
    @commands.command(name='lobby', help = 'Displays all players currently joined to this game.')
    async def lobby(self, ctx):
        try:
            if self.GI:
                lobbymsg = f"Current Players: {len(self.GI.Players)}\n"
                for player in self.GI.Players:
                    lobbymsg = lobbymsg + player.DisplayName + "\n"
                await ctx.send(lobbymsg)
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- lobby -- {ex}")
    
    #Breaks lobby, completely disbanding the group and erasing the GameInstance.
    @commands.command(name= 'break_lobby', help = 'Disbands lobby for all players. Lobbies will automatically disband, \n following all players leaving.')
    async def break_lobby(self, ctx):
        try:
            self.GI = None
            await ctx.send("Lobby be broke.")
        except Exception as ex:
            print(f"ERROR -- {FILE_NAME} -- break_lobby -- {ex}")
    
    # Thanks the user, spread the love!
    @commands.command(name='thanks', help='Thank the bot and receive a response!')
    async def thanks(self, ctx):
        await ctx.send(f"You're welcome, {ctx.author.mention}! :D. I'm here to help!") 

async def setup(bot):
    await bot.add_cog(GameManagement(bot))
