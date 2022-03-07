import os

def check_master_role_permission(ctx):
    has_permission = False 
    for role in ctx.author.roles:
        if int(os.getenv("MASTER_ROLE_ID")) == role.id:
            has_permission = True
            break
    return has_permission

def check_comando_role_permission(ctx):
    has_permission = False 
    for role in ctx.author.roles:
        if int(os.getenv("COMANDO_ROLE_ID")) == role.id:
            has_permission = True
            break
    return has_permission
