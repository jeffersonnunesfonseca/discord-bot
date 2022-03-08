from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument
from discord.ext import commands
from discord_components import *


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
        DiscordComponents(self.bot)
        print(f"EU SOU UM TESTE. ME CHAMO {self.bot.user}")


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

    # @client.listen('on_button_press')
    # async def on_button(btn: PressedButton, msg: ResponseMsg):
    #     await btn.respond("You pressed " + btn.content)

    # @commands.Cog.listener()
    # async def on_button_press(self, btn, message):
    #     msg = f"{btn.member.name} me clicou "
    #     await message.respond(msg)

    # await btn.respond("You pressed " + btn.content)
    # @commands.Cog.listener()
    # async def on_disconnect(self):
    #     print("Bot off.")

def setup(bot):
    bot.add_cog(Manager(bot))