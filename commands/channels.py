from multiprocessing.connection import wait
import os
import time

import discord

from discord.ext import commands
from discord_components import Button
from discord.errors import HTTPException,NotFound
from asyncio.exceptions import TimeoutError

import utils


class Channels(commands.Cog):
    """Talks with user"""
    _USERS_ACCEPT_INTERCTION = [] # armazena estrutura com usuarios e interações para que seja validado
    _LIMIT_USER_IN_BET = 2 # limite de usuario por aposta
    
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
            
            btn_accept =  Button(label = f"Entrar na fila [0/{self._LIMIT_USER_IN_BET}]", custom_id = "btn_accept",style=1,emoji="✅")
            btn_reject =  Button(label = "Sair da fila", custom_id = "btn_reject", style=4, emoji="❎")


            msg = await ctx.send(embed=embed, components = [[btn_accept,btn_reject]])
            await self._btn_interaction(ctx,msg,btn_accept,btn_reject)


    async def _btn_interaction(self,ctx, msg, btn_accept, btn_reject):
        """ cuida da interação com o botao de aceito """
        while True:
            try:
                # this_user_has_interation = False
                interaction_accept_btn = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "btn_accept" or inter.custom_id == "btn_reject",timeout=60)

                user_id = interaction_accept_btn.user.id
                message_id = interaction_accept_btn.message.id
                
                print(f"clique {interaction_accept_btn.user.name} - {interaction_accept_btn.user.id}")               
                print(f"message.id {message_id}")

                if "sair" in interaction_accept_btn.component.label.lower():
                    # TODO logica do botao sair ... 
                    await ctx.send("clicou em sair - implementar regras ...")
                else:
                    await ctx.send("clicou em entrar")
                    is_accepted,total = self._resolve_bets_accepted(message_id=message_id,user_id=user_id)
                    if is_accepted:
                        btn_accept.set_disabled(False)  # força disable False 
                        if total == 2:
                            btn_accept.set_disabled(True)  

                        btn_accept.set_label(f"Entrar na fila [{total}/{self._LIMIT_USER_IN_BET}]")
                        await interaction_accept_btn.respond(type = 7, components = [[btn_accept, btn_reject]])

                    else:
                        # await ctx.send(f"**{ctx.author.name}** você já esta participando de uma aposta.")
                        await interaction_accept_btn.respond(type = 7)

            except TimeoutError as e:
                print(f"TimeoutError {e}")
                if self._USERS_ACCEPT_INTERCTION:
                    for index, inter in enumerate(self._USERS_ACCEPT_INTERCTION):
                        if int(inter["message_id"]) == msg.id:
                            self._USERS_ACCEPT_INTERCTION.pop(index)
                
                if msg:
                    await msg.delete()
                    await ctx.send(f"Aposta cancelada por falta de jogadores ... ")
            except HTTPException as e:
                print(f"HTTPException {e}")

            except Exception as e:
                print(f"sem mensagem {e}")
                break


            # try:
            #     # this_user_has_interation = False
            #     interaction_accept_btn = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "btn_reject",timeout=60)
            #     # import ipdb; ipdb.set_trace()
            #     user_id = interaction_accept_btn.user.id
            #     message_id = interaction_accept_btn.message.id
                
            #     print(f"clique {interaction_accept_btn.user.name} - {interaction_accept_btn.user.id}")               
            #     print(f"message.id {message_id}")

                
            #     is_accepted,total = self._resolve_bets_accepted(message_id=message_id,user_id=user_id)
            #     print(is_accepted)
            #     print(total)
            #     print(self._USERS_ACCEPT_INTERCTION)
            #     if is_accepted:
            #         btn_accept.set_disabled(False)  # força disable False 
            #         if total == 2:
            #             btn_accept.set_disabled(True)  


            #         btn_accept.set_label(f"Entrar na fila [{total}/{self._LIMIT_USER_IN_BET}]")
            #         await interaction_accept_btn.respond(type = 7, components = [[btn_accept, btn_reject]])

            #     else:
            #         # await ctx.send(f"**{ctx.author.name}** você já esta participando de uma aposta.")
            #         await interaction_accept_btn.respond(type = 7)

            # except TimeoutError as e:
            #     print(f"TimeoutError {e}")
            #     if self._USERS_ACCEPT_INTERCTION:
            #         for index, inter in enumerate(self._USERS_ACCEPT_INTERCTION):
            #             if int(inter["message_id"]) == msg.id:
            #                 self._USERS_ACCEPT_INTERCTION.pop(index)
                
            #     if msg:
            #         await msg.delete()
            #         await ctx.send(f"Aposta cancelada por falta de jogadores ... ")
            # except HTTPException as e:
            #     print(f"HTTPException {e}")

            # except Exception as e:
            #     print(f"sem mensagem {e}")
            #     break

    
    def _resolve_bets_accepted(self,**kwargs):     
        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se o usuario ja esta em alguma interação
        if not self._USERS_ACCEPT_INTERCTION:
            print("[1] Interação NAO existe, adicionando o user")
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":1
            }
            self._USERS_ACCEPT_INTERCTION.append(interaction)

            return True,1,

        for inter in self._USERS_ACCEPT_INTERCTION:
            if user_id in  inter["users_id"]:
                print(f"[2] usuário ja esta em uma aposta {inter}")
                return False,inter['total'],
        
        interaction_exists = False
        total_users = 0

        # verifica se ja existe a interação e se existir adiciona o usuario nela, se nao cria e adiciona usuario
        for inter in self._USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id:
                total_users = len(inter["users_id"])
                if total_users >= self._LIMIT_USER_IN_BET:
                    print(f"[3] Aposta já contem limite de usuarios {inter}")
                    return False, total_users,
                    
                print("[4] Interação ja existe, adicionando o user")
                inter["users_id"].append(user_id)
                total_users = len(inter["users_id"])
                inter["total"] = total_users
                interaction_exists = True
                break
        
        if not interaction_exists:
            print("[5] Interação NAO existe, adicionando o user")
            total_users = 1
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":total_users
            }
            self._USERS_ACCEPT_INTERCTION.append(interaction)

        return True,total_users,


def setup(bot):
    bot.add_cog(Channels(bot))
    