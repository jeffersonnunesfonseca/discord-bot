import os

def check_master_role_permission(ctx):
    roles = [x.name.lower() for x in ctx.author.roles]
    return "master" in roles or ctx.guild.owner.id == ctx.author.id

def check_comando_role_permission(ctx):
    roles = [x.name.lower() for x in ctx.author.roles]
    return "comando" in roles or ctx.guild.owner.id == ctx.author.id

