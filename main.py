import os
from discord.ext import commands
import discord

intents = discord.Intents().all()

bot = commands.Bot(command_prefix="!",intents=intents)


def load_cogs(bot):
    bot.load_extension("manager")
    # bot.load_extension("tasks.dates")

    for file in os.listdir("commands"):
        if file.endswith(".py"):
            cog = file[:-3]
            bot.load_extension(f"commands.{cog}")


load_cogs(bot)
token = os.getenv("BOT_TOKEN")
bot.run(token)