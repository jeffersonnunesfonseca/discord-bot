import time

import discord
from discord.ui import Button 
from discord.ext import commands
# from discord_components import Button
from discord.errors import HTTPException
from asyncio.exceptions import TimeoutError

import utils
from config import MSG_RULES

class BtnAcceptBet(discord.ui.View):

    @discord.ui.button(label="0",custom_id='1',style=discord.ButtonStyle.green)
    async def count(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0
        if number >= 4:
            button.style = discord.ButtonStyle.red
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)

    @discord.ui.button(label="0",custom_id='2',style=discord.ButtonStyle.red)
    async def count2(self, button: discord.ui.Button, interaction: discord.Interaction):
        number = int(button.label) if button.label else 0
        if number >= 4:
            button.style = discord.ButtonStyle.green
            button.disabled = True
        button.label = str(number + 1)

        # Make sure to update the message with our updated selves
        await interaction.response.edit_message(view=self)


class Channels(commands.Cog):
    """Talks with user"""
    _USERS_ACCEPT_INTERCTION = [] # armazena estrutura com usuarios e interações para que seja validado
    _LIMIT_USER_IN_BET = 2 # limite de usuario por aposta
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="testezada")
    async def testezada(self, ctx):
        btn = BtnAcceptBet()
        await ctx.send("Press!", view=btn)

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
                name=self.bot.user.name, icon_url=self.bot.user.avatar.url
            )

            embed.add_field(name="Tipo de jogo", value=type, inline=False)
            embed.add_field(name="Formato", value=size, inline=False)
            embed.add_field(name="R$ Valor da aposta", value=price, inline=False)
            embed.set_footer(
                text="Feito por " + self.bot.user.name, icon_url=self.bot.user.avatar.url
            )

            # btn_accept =  Button(label = f"Entrar na fila [0/{self._LIMIT_USER_IN_BET}]", custom_id = "btn_accept",style=1,emoji="✅")
            # btn_reject =  Button(label = "Sair da fila", custom_id = "btn_reject", style=4, emoji="❎")

            # self.bot.add_view(BtnAcceptBet(),message_id=msg.id)
            # buttons = {
            #     'view':[BtnAcceptBet()],

            # }
            msg = await ctx.send(embed=embed,view=BtnAcceptBet())
            
            # self.bot.add_view(BtnAcceptBet(),message_id=msg.id)
            # msg = await ctx.send(embed=embed,components = [[btn_accept,btn_reject]])
            # await self._btn_interaction(ctx,msg,btn_accept,btn_reject,embed)

    async def _btn_interaction(self,ctx, msg, btn_accept, btn_reject, embed):
        """ cuida da interação com o botao de aceito """
        while True:
            try:
                interaction_accept_btn = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "btn_accept" or inter.custom_id == "btn_reject",timeout=60)

                user_id = interaction_accept_btn.user.id
                message_id = interaction_accept_btn.message.id

                print(f"[clique {interaction_accept_btn.user.name} - {interaction_accept_btn.user.id}] [message.id {message_id}]")               

                if "sair" in interaction_accept_btn.component.label.lower():
                    is_reject, total = self._reject_bet(message_id=message_id,user_id=user_id)
                    if is_reject:
                        btn_accept.set_disabled(False)  # força disable False 
                        btn_accept.set_label(f"Entrar na fila [{total}/{self._LIMIT_USER_IN_BET}]")
                        
                        await interaction_accept_btn.respond(type = 7, components = [[btn_accept, btn_reject]])
                        index_to_remove = None
                        for index,x in enumerate(embed.fields):
                            if x.value == interaction_accept_btn.user.name:
                                index_to_remove=index
                                break
                        
                        if index_to_remove:
                            embed.remove_field(index=4)
                            await msg.edit(embed=embed)

                    else:
                        await interaction_accept_btn.respond(type = 7)
                else:
                    is_accepted, total = self._accept_bet(message_id=message_id,user_id=user_id)
                    if is_accepted:

                        embed.add_field(name="Participante:", value=interaction_accept_btn.user.mention, inline=True)
                        await msg.edit(embed=embed)
                        if total < 2:
                            btn_accept.set_disabled(False)
                        else:
                            btn_accept.set_disabled(True)

                            # aqui criar um canal
                            guild = ctx.guild
                            user_1 = None
                            user_2 = None

                            # pega dados dos usuarios que estavam na fila
                            users = [users['users_id'] for users in self._USERS_ACCEPT_INTERCTION if users['message_id'] == interaction_accept_btn.message.id ]
                            user_id_1, user_id_2 = tuple(users[0])

                            user_1 = ctx.guild.get_member(user_id_1)
                            user_2 = ctx.guild.get_member(user_id_2)
                        
                            channel_bet_name = f"aposta-{user_1.name}-x-{user_2.name}".lower()
                            overwrites = {
                                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                                guild.me: discord.PermissionOverwrite(read_messages=True),
                                ctx.author: discord.PermissionOverwrite(read_messages=True),
                                user_1: discord.PermissionOverwrite(read_messages=True),
                                user_2: discord.PermissionOverwrite(read_messages=True)
                            }                    
                            channel = await guild.create_text_channel(channel_bet_name, overwrites=overwrites)
                            await channel.send(embed=utils.embed_rules_message(ctx,self.bot))
                            btn_remove_channel =  Button(label = "Remover canal", custom_id = "btn_remove_channel", style=4, emoji="❎")
                            # await channel.send(components=[btn_remove_channel])

                            self._clear_queue_by_message_id(msg.id)

                            await msg.delete()        
                            # await self._btn_close_channel_interaction(btn_remove_channel)

                            break

                        btn_accept.set_label(f"Entrar na fila [{total}/{self._LIMIT_USER_IN_BET}]")
                        await interaction_accept_btn.respond(type=7, components = [[btn_accept, btn_reject]])
                        
                    else:
                        await interaction_accept_btn.respond(type=7)

            except TimeoutError as e:
                print(f"TimeoutError {e}")
                self._clear_queue_by_message_id(msg.id)
                
                await msg.delete()
                await ctx.send(f"Aposta cancelada por falta de jogadores ...")

            except HTTPException as e:
                print(f"HTTPException {e}")

            except Exception as e:
                print(f"sem mensagem {e}")
                break
    
    def _accept_bet(self,**kwargs):     
        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se o usuario ja esta em alguma interação
        if not self._USERS_ACCEPT_INTERCTION:
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":1
            }
            self._USERS_ACCEPT_INTERCTION.append(interaction)

            return True,1,

        for inter in self._USERS_ACCEPT_INTERCTION:
            if user_id in  inter["users_id"]:
                return False,inter['total'],
        
        interaction_exists = False
        total_users = 0

        # verifica se ja existe a interação e se existir adiciona o usuario nela, se nao cria e adiciona usuario
        for inter in self._USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id:
                total_users = len(inter["users_id"])
                if total_users >= self._LIMIT_USER_IN_BET:
                    return False, total_users,
                    
                inter["users_id"].append(user_id)
                total_users = len(inter["users_id"])
                inter["total"] = total_users
                interaction_exists = True
                break
        
        if not interaction_exists:
            total_users = 1
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":total_users
            }
            self._USERS_ACCEPT_INTERCTION.append(interaction)

        return True,total_users,

    def _reject_bet(self,**kwargs): 

        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se existe alguma interação
        if not self._USERS_ACCEPT_INTERCTION:
            return False, 0,

        # verifica se existe mensagem com o id da interação e se o usuario que esta clicando esta nela
        for inter in self._USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id and user_id in inter["users_id"]:
                index = inter["users_id"].index(user_id)
                inter["users_id"].pop(index)
                total_users = len(inter["users_id"])
                return True, total_users,

        return False, 0,

    def _clear_queue_by_message_id(self,message_id):
        if self._USERS_ACCEPT_INTERCTION:
            for index, inter in enumerate(self._USERS_ACCEPT_INTERCTION):
                if int(inter["message_id"]) == message_id:
                    self._USERS_ACCEPT_INTERCTION.pop(index)    
    
    async def _btn_close_channel_interaction(self,btn):
        while True:
            interaction_btn = await self.bot.wait_for("button_click", check = lambda inter: inter.custom_id == "btn_remove_channel" ,timeout=60)

            if utils.check_comando_role_permission(interaction_btn):
                await interaction_btn.respond(type=7)
                await interaction_btn.channel.delete()
                break
            else:
                await interaction_btn.channel.send(f"{interaction_btn.author.name}, você não tem permissão para fechar o canal!")
                await interaction_btn.respond(type=7)


    
def setup(bot):
    bot.add_cog(Channels(bot))
    