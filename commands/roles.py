import os
import discord
from discord.ext import commands
from discord.utils import get
import utils

class Roles(commands.Cog):
    """ Work with roles"""

    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="addcargo", help="Adiciona cargo a uma pessoa. Args:user nome_cargo, nome do usuario")
    async def add_role(self, ctx, role_name, username):
        if not utils.check_master_role_permission(ctx):
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.name}, você não tem permissão!")            
        else:
            role = get(ctx.guild.roles, name=role_name.upper())
            if not role:
                msg = f"cargo não encontrado, favor verificar novamente o cargo."
                await ctx.send(msg)
                return

            user = None
            for member in ctx.guild.members:
                if username.lower() == member.name.lower():
                    user = member
                    break    

            if user:
                msg = f"Cargo **{role.name.upper()}** adicionado ao usuário **{member.name}**"
                await member.add_roles(role)    
                await ctx.send(msg)
            else:
                msg = f"não foi possivel adicionar o cargo **{role.name.upper()}** ao usuário desejado, favor verificar o **NOME** do usuario"
                await ctx.send(msg)


def setup(bot):
    bot.add_cog(Roles(bot))