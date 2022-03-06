from discord.ext import commands
import discord

class Talks(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="oi", help="Envia um Oi (Não requer argumento)")
    async def send_hello(self, ctx):

        name = ctx.author.name

        response = f"Olá, {name}! Seja bem vindo."
        await ctx.send(response)

    @commands.command(
        name="segredo", help="Envia um segredo no privado. Não requer argumento"
    )
    async def secret(self, ctx):
        try:
            await ctx.author.send("Pssiuu!, Oii")

        except discord.errors.Forbidden:
            await ctx.send(
                "Não posso te contar o segredo, habilite receber mensagens de qualquer pessoa do servidor (Opções > Privacidade)"
            )

def setup(bot):
    bot.add_cog(Talks(bot))