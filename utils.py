import discord
from config import MSG_RULES

def check_master_role_permission(ctx):
    roles = [x.name.lower() for x in ctx.author.roles]
    return "master" in roles or ctx.guild.owner.id == ctx.author.id

def check_comando_role_permission(ctx):
    roles = [x.name.lower() for x in ctx.author.roles]
    return "comando" in roles or ctx.guild.owner.id == ctx.author.id

def embed_rules_message(ctx,bot):
    embed = discord.Embed(
        title=f"Regras {ctx.guild.name}!",
        description=f"{MSG_RULES}",
        color=0x0000FF,
    )

    embed.set_author(
        name=bot.user.name, icon_url=bot.user.avatar_url
    )

    embed.set_footer(
        text="Feito por " + bot.user.name, icon_url=bot.user.avatar_url
    )
    return embed