import os
import discord
from discord.ext import commands
class Channels(commands.Cog):
    """Talks with user"""

    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="create-private-channel", help="Cria um canal privado (nome)")
    async def create_private_channel(self, ctx, name):
        has_permission = False 
        for role in ctx.author.roles:
            if int(os.getenv("ADM_ROLE_ID")) == role.id:
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



def setup(bot):
    bot.add_cog(Channels(bot))