import discord
from discord.ext import commands
import random

class GameMangaement(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.players = [] 
        self.roles = {} #Dict that stores roles by player

    # commands to start the game, join the game, leave the game, 
    # (randomly?) assign roles, check your roles
