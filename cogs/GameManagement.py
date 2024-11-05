# GameManagement.py
import discord
from discord.ext import commands

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
    
    # Thanks the user, spread the love!
    @commands.command(name='thanks', help='Thank the bot and receive a response!')
    async def thanks(self, ctx):
        await ctx.send(f"You're welcome, {ctx.author.mention}! :D. I'm here to help!") 

async def setup(bot):
    await bot.add_cog(GameManagement(bot))
