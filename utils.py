import discord
from config import MSG_RULES

def check_master_role_permission(owner_guild_id,user_id,user_roles):
    roles = [x.name.lower() for x in user_roles]
    return "master" in roles or owner_guild_id == user_id

def check_comando_role_permission(owner_guild_id,user_id,user_roles):
    roles = [x.name.lower() for x in user_roles]
    return "comando" in roles or owner_guild_id == user_id

def embed_rules_message(ctx,bot):
    embed = discord.Embed(
        title=f"Regras {ctx.guild.name}!",
        description=f"{MSG_RULES}",
        color=0x0000FF,
    )

    embed.set_author(
        name=bot.user.name, icon_url=bot.user.avatar.url
    )

    embed.set_footer(
        text="Feito por " + bot.user.name, icon_url=bot.user.avatar.url
    )
    return embed