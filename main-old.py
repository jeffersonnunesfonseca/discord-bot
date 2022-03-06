import os
import requests
import discord
import logging
from datetime import datetime
from discord.ext import commands, tasks
from discord.ext.commands.errors import CommandNotFound, MissingRequiredArgument

LOGGER = logging.getLogger(__name__)

bot = commands.Bot("!")


forbidden_word = [
    "porra",
    "cu",
    "fdp"
]

@bot.event
async def on_ready():
    print(f"Estou pronto e conectado como {bot.user}")
    # current_time.start()

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    
    # bloqueia palavoes
    has_forbidden_word = False 
    split_message = message.content.split(" ")
    for sm in split_message:
        if sm in forbidden_word:
            has_forbidden_word= True
            break
    
    if has_forbidden_word:
        # await message.channel.send(f"que boca suja ein {message.author.name}")
        await message.delete()
        await message.channel.send(f"mensagem apagada ... ")

    await bot.process_commands(message)

@bot.event
async def on_reaction_add(reaction,user):
    print(reaction.emoji)
    if reaction.emoji == "👍":
        role = user.guild.get_role(os.getenv("ADM_ROLE_ID"))
        await user.add_roles(role)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error,CommandNotFound):
        await ctx.send("Comando inválido.")
    elif isinstance(error,MissingRequiredArgument):
        await ctx.send("Favor enviar todos os Argumentos.")
        
    else:
        raise error

    await ctx.send("Digite !help para ver todos os comandos.")

@bot.command(name="oi")
async def send_hello(ctx):
    name = ctx.author.name

    response = f"Olá, {name}! Seja bem vindo."
    await ctx.send(response)

@bot.command(name="calcular")
async def calculate(ctx, expression):
    response = None
    try:
        expression = expression.lower()
        if "x" in expression:
            expression = expression.replace("x","*")

        response = str(eval(expression))
    except:
        response = "Expressão inválida."
    await ctx.send(f"A resposta é : {response}")

@bot.command()
async def binance(ctx, coin, base):
    response = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}")
    data = response.json()
    price = data.get("price")

    if not price:
        await ctx.send("Ops ... algum erro")
    
    await ctx.send(f"O valor do par {coin}/{base} é {price}")

@bot.command(name="segredo")
async def send_dm(ctx):
    try:
        await ctx.author.send("Psiu, Oii")
    except discord.errors.Forbidden:
        await ctx.send(f"{ctx.author.name} não posso te contar um segredo :( habilite a opção para receber mensagens diretas")

@bot.command(name="foto", help="Envia uma foto no privado. Não requer argumento")
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080"

    embed_image = discord.Embed(
        title="Resultado da busca de imagem",
        description="PS: A busca é totalmente aleatória",
        color=0x0000FF,
    )

    embed_image.set_author(
        name=bot.user.name, icon_url=bot.user.avatar_url
    )
    embed_image.set_footer(
        text="Feito por " + bot.user.name, icon_url=bot.user.avatar_url
    )

    embed_image.add_field(name="API", value="Usamos a API do https://picsum.photos")
    embed_image.add_field(name="Parâmetros", value="{largura}/{altura}")

    embed_image.add_field(name="Exemplo", value=url_image, inline=False)

    embed_image.set_image(url=url_image)

    await ctx.send(embed=embed_image)

@tasks.loop(seconds=60)
async def current_time():
    now = datetime.now().strftime("%d/%m/%Y às %H:%M:%S")
    msg = f"Horário atual - {now}"
    channel_id = 949862745694687286
    channel = bot.get_channel(channel_id)
    await channel.send(msg)

bot.run("OTQ5ODcxMjE3OTE2MTIxMTM5.YiQqgg.mWUjpSQLnm1wjFvwoCLoOZKltkA")


