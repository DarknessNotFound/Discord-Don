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

class GameManagement(commands.Cog):

    GI = None

    def __init__(self, bot):
        self.bot = bot
    
    #Creates a GameInstance object if none exist, 
    @commands.command(name='create_game', help='Creates a new game if one is not already active.')
    async def create_game(self, ctx):
        if (self.GI):
            await ctx.send("A game has already been created for this Discord.")
        else:
            self.GI = Game_CoreLoop.GameInstance
            self.GI.AddPlayer(ctx.author.user.name)
            await ctx.send("A game has been created.")

    
    #Starts game provided the GI exists, and the caller is one of the players.
    @commands.command(name='start_game', help='Starts a new game if one is not already active.')
    async def start_game(self, ctx):
        if (self.GI): #Check if we have a valid GameInstance to join.
            if(ctx.name in self.GI.Players): #Check that the caller is actually in said game.
                await ctx.send("Game starting! You should recieve your roles shortly.")
                self.GI.StartGame()
            else:
                await ctx.send("You are currently not in the current game. Use >>join_game to hop in!")
        else:
            await ctx.send("Use create_game to create a lobby that other players can join, then start the game when you're ready!")

    # Allows players to join a active game or waiting lobby
    @commands.command(name='join_game', help='Join the active game.')
    async def join_game(self, ctx):
        if (self.GI): #check if GI is valid
            if (ctx.name in self.GI.Players): #Check if join is duplicate
                await ctx.send("You've already joined the game.")
            else:
                self.GI.AddPlayer(ctx.author)
                await ctx.send(f"{ctx.author} has joined the game.")                
                if (self.GI.GameStarted): #check if GI has started.
                    self.GI.KillPlayer(ctx.author)
                    await ctx.send("Game in progress, you will respawn next game. Sit tight!")

    # Allows players to leave the game
    @commands.command(name='leave_game', help='Leave the current game.')
    async def leave_game(self, ctx):
        if(self.GI):
            if(ctx.author in self.GI.Players):
                self.GI.RemovePlayer(ctx.author)
                await ctx.send(f"{ctx.author} has left the game.")
                if(not self.GI.Players.len()):
                    self.break_lobby()
            else:
                await ctx.send("You aren't in an active game.")
        else:
            await ctx.send("There isn't an active game running.")
    
    #Player can report that they are dead to the bot
    @commands.command(name = 'dead', help = 'Report your death to the GM. \n Use this if you are sent to the ghost box.')
    async def kill_player(self, ctx):
        if (self.GI): #check if GI is valid
            if (ctx.author in self.GI.Players): #Check if player exists in player roster.
                self.GI.KillPlayer(ctx.author)
                await ctx.send(f"The uhhh.... \"{ctx.author}\" has been killed.")
            else:
                await ctx.send(f"You aren't in this game dummy.")
            

    # Ends the game, and clears the players and roles.
    @commands.command(name='end_game', help='Ends the current game.')
    async def end_game(self, ctx):
        if not self.GI and self.GI.GameStarted:
            await ctx.send("No game is currently active.")
        else:
            self.GI.EndGame()
            await ctx.send(self.GI.EchoStats())

    #Mainly for testing, allow user to display the lobby names.
    @commands.command(name='show_lobby', help = 'Displays all players currently joined to this game.')
    async def show_lobby(self, ctx):
        if self.GI:
            lobbymsg = "Current Players: \n"
            for player in self.GI.Players:
                lobbymsg = lobbymsg + player.PlayerName + "\n"
            await ctx.send(lobbymsg)
    
    #Breaks lobby, completely disbanding the group and erasing the GameInstance.
    @commands.command(name= 'break_lobby', help = 'Disbands lobby for all players. Lobbies will automatically disband, \n following all players leaving.')
    async def break_lobby(self, ctx):
        self.GI = None
        await ctx.send("Lobby be broke.")
    
    # Thanks the user, spread the love!
    @commands.command(name='thanks', help='Thank the bot and receive a response!')
    async def thanks(self, ctx):
        await ctx.send(f"You're welcome, {ctx.author.mention}! :D. I'm here to help!") 

async def setup(bot):
    await bot.add_cog(GameManagement(bot))
