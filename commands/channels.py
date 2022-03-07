import os
from turtle import color

import discord

from discord.ext import commands
from discord_components import Button

import utils


class Channels(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="create-private-channel", help="Cria um canal privado (nome)")
    async def create_private_channel(self, ctx, name):
        has_permission = False 
        for role in ctx.author.roles:
            if int(os.getenv("COMANDO_ROLE_ID")) == role.id:
                has_permission = True
                break
        if not has_permission:
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.name}, você não tem permissão!")
        else:
            guild = ctx.guild
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                ctx.author: discord.PermissionOverwrite(read_messages=True), 

            }
            
            channel = await guild.create_text_channel(name, overwrites=overwrites)
            await channel.send('New channel created.')

    # bot.command => commands.command
    @commands.command(name="fila", help="Cria uma fila. Args: tipo(emu, mob),tamanho(4x4,1x1..), valor")
    async def create_queue(self, ctx,type,size,price):
        if not utils.check_comando_role_permission(ctx):
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.name}, você não tem permissão!")
            return
        else:
            await ctx.send(f"{ctx.author.name}, VCÊ TEM A PERMISSÃO CARAAA")
            
            embed = discord.Embed(
                title="Fila Criada!",
                description="escolha a opção desejada nos botões abaixo.",
                color=0x0000FF,
            )

            embed.set_author(
                name=self.bot.user.name, icon_url=self.bot.user.avatar_url
            )

            embed.add_field(name="Tipo de jogo", value=type, inline=False)
            embed.add_field(name="Formato", value=size, inline=False)
            embed.add_field(name="R$ Valor da aposta", value=price, inline=False)

            embed.set_footer(
                text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar_url
            )


            btn_accept =  Button(label = "Entrar na fila [0/2]", custom_id = "btn_accept",style=1,emoji="✅")
            btn_reject =  Button(label = "Sair da fila", custom_id = "btn_reject", style=4, emoji="❎")


            await ctx.send(embed=embed, components = [[btn_accept,btn_reject]])

            # interaction = await self.bot.wait_for("button_click", check = lambda i: i.custom_id == "button1")
            # import ipdb; ipdb.set_trace()
            # await interaction.send(content = "Button clicked!")
            # button1 = Button(label = "button1", custom_id = "button1")
            # button2 = Button(label = "button2", custom_id = "button2")
            # button3 = Button(label = "button3", custom_id = "button3")
            # button1disabled = Button(label = "button1", custom_id = "button1", disabled = True)
            # button2disabled = Button(label = "button2", custom_id = "button2", disabled = True)
            # button3disabled = Button(label = "button3", custom_id = "button3", disabled = True)
            # msg = await ctx.send("button", components = [button1, button2, button3])
            # interaction = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "button1")
            # await interaction.respond(type = 7, content = msg, components = [button1disabled, button2disabled, button3disabled])
            # await interaction.send(f"Disabled")
            # self.bot.buttons = Buttons(self.bot)
            # res = await self.bot.buttons.send(ctx.message.channel, "here you go", buttons=[Button("myID", "Press me", emoji="😀")])
            # url_image = "https://picsum.photos/1920/1080"



def setup(bot):
    bot.add_cog(Channels(bot))