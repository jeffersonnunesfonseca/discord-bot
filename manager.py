import asyncio
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands

# from discord_components import *

class Manager(commands.Cog):
    """Manage the bot"""

    FORBIDDEN_WORDS = [
        "porra",
        "cu",
        "fdp"
    ]

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Bot {self.bot.user} ON")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # bloqueia palavoes
        has_forbidden_word = False 
        split_message = message.content.split(" ")
        for sm in split_message:
            if sm.lower() in self.FORBIDDEN_WORDS:
                has_forbidden_word= True
                break
        
        if has_forbidden_word:
            # await message.channel.send(f"que boca suja ein {message.author.name}")
            await message.delete()
            await message.channel.send(f"mensagem apagada ... ")
        
        # força apagar mensagens de comando apos 2 minutos para evitar spam
        try:
            reaction, user = await self.bot.wait_for('on_application_command', timeout=120)
        except asyncio.TimeoutError:
            commands = list(self.bot.all_commands.keys())
            edited_commands = [f"!{res}" for res in commands]
            if message.content in edited_commands:
                await message.delete()

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument):
            await ctx.send(
                "Favor enviar todos os Argumentos. Digite !help para ver os parâmetros de cada comando"
            )
        elif isinstance(error, CommandNotFound):
            await ctx.send(
                "O comando não existe. Digite !help para ver todos os comandos"
            )
        else:
            raise error

def setup(bot):
    bot.add_cog(Manager(bot))