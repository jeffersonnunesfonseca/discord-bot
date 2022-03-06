
import discord
from discord.ext import commands
from discord_components import Button

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

    @commands.command(name="teste")
    async def teste(self,ctx):
        embed = discord.Embed(
            title="Botão",
            description="Embed com botão",
            color=0x0000FF,
        )

        await ctx.send(embed=embed, components = [
            Button(label = "WOW button!", custom_id = "button1")
        ] )

        # interaction = await self.bot.wait_for("button_click", check = lambda i: i.custom_id == "button1")
        # import ipdb; ipdb.set_trace()
        # await interaction.send(content = "Button clicked!")
        button1 = Button(label = "button1", custom_id = "button1")
        button2 = Button(label = "button2", custom_id = "button2")
        button3 = Button(label = "button3", custom_id = "button3")
        button1disabled = Button(label = "button1", custom_id = "button1", disabled = True)
        button2disabled = Button(label = "button2", custom_id = "button2", disabled = True)
        button3disabled = Button(label = "button3", custom_id = "button3", disabled = True)
        msg = await ctx.send("button", components = [button1, button2, button3])
        interaction = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "button1")
        await interaction.respond(type = 7, content = msg, components = [button1disabled, button2disabled, button3disabled])
        await interaction.send(f"Disabled")
        # self.bot.buttons = Buttons(self.bot)
        # res = await self.bot.buttons.send(ctx.message.channel, "here you go", buttons=[Button("myID", "Press me", emoji="😀")])
        # url_image = "https://picsum.photos/1920/1080"


        # print(res)


def setup(bot):
    bot.add_cog(Talks(bot))