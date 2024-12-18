# Author: Grant "DarknessNotFound" Albright
# Github: DarknessNotFound

# I don't recommend changing anything in this file, as it just sets up
# the cogs and runs the bot and itself.

import os
import asyncio
import discord
from dotenv import load_dotenv
from discord.ext import commands
from database import CREATE_DATABASE

print("Discord-Don application started.")

# Needed for lists of members
intents = discord.Intents.all()
intents.members = True
intents.message_content = True

# Load Enviroment variables
load_dotenv()
TOKEN = os.getenv('TOKEN')

# Bot and client settings.
client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix='!', intents=intents, case_insensitive=True)
# Prints a message to say it connected successfully
# NOTE: Sometimes takes a second to trigger and send msg

print("Creating the Database")
CREATE_DATABASE()

@bot.event
async def on_ready():
    print("Connected successfully.")


@bot.command()
async def load(ctx, extension):
    bot.load_extension(f'cogs.{extension}')


@bot.command()
async def unload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')


@bot.command()
async def reload(ctx, extension):
    bot.unload_extension(f'cogs.{extension}')
    bot.load_extension(f'cogs.{extension}')


# This searches for all cogs in the cog file and loads the functions for use
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')


# Functions that starts the bot.
async def main():
    async with bot:
        await load_extensions()
        await bot.start(TOKEN)


asyncio.run(main())
