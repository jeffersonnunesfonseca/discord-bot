from turtle import color
import discord

from discord.ext import commands

import utils

from config import CATEGORIES_WITH_CHANNELS, ROLES

class Configurations(commands.Cog):
    """Works with Cryptocurrency"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="up_server_configuration", help="Sobe configurações iniciais do servidor, canais, cargos ...")
    async def up_default_channels(self,ctx):

        if utils.check_master_role_permission(ctx):            
            # create roles
            current_roles = [x.name.upper() for x in ctx.guild.roles]
            for role in ROLES:
                if not role['name'].upper() in current_roles:
                    print(f"Role {role['name'].upper()} não existe e vai ser criada")
                    await ctx.guild.create_role(name=role['name'],permissions=role['permissions'],color=role['color'])

            # cria canais se nao existir

            current_categories = [x.name.upper() for x in ctx.guild.categories]
            for category, values in CATEGORIES_WITH_CHANNELS.items():
                if not category.upper() in current_categories:
                    print(f"Categoria {category.upper()} não existe e vai ser criada")
                    new_category = await ctx.guild.create_category(category)
                    for ch in values:
                        print(f"Criando canal {ch['name']} na categoria [{new_category.id}] - {new_category.name}")
                        if not ch['type']:
                            if str(ch['permission']) == "readonly":
                                overwrites_read_only = {
                                    ctx.guild.default_role: discord.PermissionOverwrite(read_message_history=True,send_messages=False),
                                }
                                await ctx.guild.create_text_channel(str(ch['name']), category=new_category,overwrites=overwrites_read_only)
                            else:
                                await ctx.guild.create_text_channel(str(ch['name']), category=new_category)

                        if ch['type'] == 2:
                            await ctx.guild.create_voice_channel(str(ch['name']), category=new_category,user_limit=int(ch['user_limit']))
            
        else:
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.name}, você não tem permissão!")    

def setup(bot):
    bot.add_cog(Configurations(bot))