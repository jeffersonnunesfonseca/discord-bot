import os
from datetime import datetime

from discord.ext import commands, tasks


class Dates(commands.Cog):
    """Work with dates"""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()

    @tasks.loop(minutes=1)
    async def current_time(self):
        now = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
        msg = f"Horário atual - {now}"
        channel_id = int(os.getenv("GENERAL_CHANNEL_ID"))
        channel = self.bot.get_channel(channel_id)
        await channel.send(msg)


def setup(bot):
    bot.add_cog(Dates(bot))