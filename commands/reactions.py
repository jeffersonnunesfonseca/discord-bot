import os
from discord.ext import commands

class Reactions(commands.Cog):
    """Work with Reactions"""

    def __init__(self, bot):
        self.bot = bot

    # events => commands.Cog.listener()
    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, user):
        print(reaction.emoji)


def setup(bot):
    bot.add_cog(Reactions(bot))