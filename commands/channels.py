import discord
from discord.ui import Button 
from discord.ext import commands
# from discord_components import Button
from discord.errors import HTTPException
from asyncio.exceptions import TimeoutError

import utils
from config import MSG_RULES

_USERS_ACCEPT_INTERCTION = [] # armazena estrutura com usuarios e interações para que seja validado
_LIMIT_USER_IN_BET = 2 # limite de usuario por aposta

def _clear_queue_by_message_id(message_id):
    if _USERS_ACCEPT_INTERCTION:
        for index, inter in enumerate(_USERS_ACCEPT_INTERCTION):
            if int(inter["message_id"]) == message_id:
                _USERS_ACCEPT_INTERCTION.pop(index)  

class BtnClosePrivateChannel(discord.ui.View):
    message_id = None

    @discord.ui.button(label="Encerrar canal",custom_id='close_channel',style=discord.ButtonStyle.red)
    async def BtnCloseChannel(self, button: discord.ui.Button, interaction: discord.Interaction):
        if not utils.check_comando_role_permission(interaction.guild.owner_id,interaction.user.id,interaction.user.roles):
            await interaction.channel.send(f"{interaction.user.name}, você não tem permissão!")
            return

        _clear_queue_by_message_id(self.message_id)
        await interaction.channel.delete()
        await interaction.response.edit_message(view=self)

class BtnsQueue(discord.ui.View):

    bot = None

    @discord.ui.button(label=f"Entrar na fila [0/{_LIMIT_USER_IN_BET}]",custom_id='btn_accept',style=discord.ButtonStyle.primary)
    async def BtnAcceptBet(self, button: discord.ui.Button, interaction: discord.Interaction):
        author = interaction.message.author
        guild = interaction.guild
        user_id = interaction.user.id
        message_id = interaction.message.id
        is_accepted, total = self._handler_accept_bet(message_id=message_id,user_id=user_id)

        print("#################### CLICK BTN ACCEPT ##########################")
        print(f"author {author}")
        print(f"user_id {user_id}")
        print(f"message_id {message_id}")
        print(f"total na fila {total}")
        print(f"users na fila {_USERS_ACCEPT_INTERCTION}")
        print("##############################################")
        
        embed = interaction.message.embeds[0]
        if is_accepted:
            button.label = f"Entrar na fila [{total}/{_LIMIT_USER_IN_BET}]"
            embed = self._handler_message_embed(button.custom_id,interaction)

            if total < 2:
                button.disabled = False
            else:
                button.disabled = True
                overwrites,channel_bet_name = self._handler_rules_private_chat(author,guild,message_id)
                channel = await guild.create_text_channel(channel_bet_name, overwrites=overwrites)

                view_close_channel = BtnClosePrivateChannel()
                view_close_channel.message_id = message_id
                await channel.send(embed=utils.embed_rules_message(interaction,self.bot),view=view_close_channel)

        await interaction.response.edit_message(embed=embed, view=self)

    @discord.ui.button(label="Sair da fila",custom_id='btn_reject',style=discord.ButtonStyle.red)
    async def BtnRejectBet(self, button: discord.ui.Button, interaction: discord.Interaction):
        author = interaction.message.author
        guild = interaction.guild
        user_id = interaction.user.id
        message_id = interaction.message.id
        

        is_reject, total = self._handler_reject_bet(message_id=message_id,user_id=user_id)
        embed = interaction.message.embeds[0]

        print("#################### CLICK BTN REJECT ##########################")
        print(f"author {author}")
        print(f"user_id {user_id}")
        print(f"message_id {message_id}")
        print(f"total na fila {total}")
        print(f"users na fila {_USERS_ACCEPT_INTERCTION}")
        print("##############################################")

        if is_reject:
            try:
                self.BtnAcceptBet.disabled = False
                self.BtnAcceptBet.label=f"Entrar na fila [{total}/{_LIMIT_USER_IN_BET}]"
                embed = self._handler_message_embed(button.custom_id,interaction)

                # interaction.message.components[0].children[0].label='sasa'
                # btn_accept.set_disabled(False)  # força disable False 
                # btn_accept.set_label(f"Entrar na fila [{total}/{_LIMIT_USER_IN_BET}]")
                
                # await interaction_accept_btn.respond(type = 7, components = [[btn_accept, btn_reject]])
                # index_to_remove = None
                # for index,x in enumerate(embed.fields):
                #     if x.value == interaction_accept_btn.user.name:
                #         index_to_remove=index
                #         break
                
                # if index_to_remove:
                #     embed.remove_field(index=4)
                #     await msg.edit(embed=embed)
            except Exception as e:
                print(e)
                import ipdb; ipdb.set_trace()
        await interaction.response.edit_message(embed=embed, view=self)

    def _handler_accept_bet(self,**kwargs) -> tuple: 
        """ 
        verifica se existe alguma interação, 
        se existir verifica se pertence a mensagem atual, 
        se for verifica se o usuario da interação ja esta e se estiver nao faz nada
        
        se nao existir interação cria uma com a mensagem e usuario atual,
        se ja existir interação mas nao for da msg atual append mais uma interação com a mensagem atual

        assingn: kwargs message_id, user_id
        return tuple(boolean, integer)
        """
        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se o usuario ja esta em alguma interação
        if not _USERS_ACCEPT_INTERCTION:
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":1
            }
            _USERS_ACCEPT_INTERCTION.append(interaction)

            return (True,1,)

        # verifica se o usuario da interação ja esta na fila
        for inter in _USERS_ACCEPT_INTERCTION:
            if user_id in  inter["users_id"]:
                return (False,inter['total'],)
        
        interaction_exists = False
        total_users = 0

        # verifica se ja existe a interação e se existir adiciona o usuario nela, se nao cria e adiciona usuario
        for inter in _USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id:
                total_users = len(inter["users_id"])
                if total_users >= _LIMIT_USER_IN_BET:
                    return (False, total_users,)
                    
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
            _USERS_ACCEPT_INTERCTION.append(interaction)

        return (True,total_users,)

    def _handler_message_embed(self,btn_type,interaction):
        embed = interaction.message.embeds[0]
        if btn_type == 'btn_accept':
            embed.add_field(name="Participante:", value=interaction.user.mention, inline=True)
        elif btn_type == 'btn_reject':
            index_to_remove = [index for index,x in enumerate(embed.fields) if x.value == interaction.user.mention][0]
            embed.remove_field(index=index_to_remove)

        return embed

    def _handler_rules_private_chat(self,author,guild,message_id):

        id_user_1, id_user_2 = [users['users_id'] for users in _USERS_ACCEPT_INTERCTION if users['message_id'] == message_id][0]
        user_1 = guild.get_member(id_user_1)
        user_2 = guild.get_member(id_user_2)

        channel_bet_name = f"aposta-{user_1.name}-x-{user_2.name}".lower()
        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            guild.me: discord.PermissionOverwrite(read_messages=True),
            author: discord.PermissionOverwrite(read_messages=True),
            user_1: discord.PermissionOverwrite(read_messages=True),
            user_2: discord.PermissionOverwrite(read_messages=True)
        }                    

        return (overwrites,channel_bet_name,)

    def _handler_reject_bet(self,**kwargs) -> tuple:
        """ 
        verifica se o usuario que fez a interação está reservado em alguma fila e o remove
        kwargs: message_id e user_id
        o retorno é uma tuple onde o primero valor é bool (se econtrou ou nao), e o segundo é a int de user na fila atualizado
        """
        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se existe alguma interação
        if not _USERS_ACCEPT_INTERCTION:
            return (False, 0,)

        # verifica se existe mensagem com o id da interação e se o usuario que esta clicando esta nela
        for inter in _USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id and user_id in inter["users_id"]:
                # retorar a chave com base no valor encontrado no array
                index = inter["users_id"].index(user_id)
                inter["users_id"].pop(index)
                total_users = len(inter["users_id"])
                return (True, total_users,)

        return (False, 0,)

class Channels(commands.Cog):
    """Talks with user"""
    _USERS_ACCEPT_INTERCTION = [] # armazena estrutura com usuarios e interações para que seja validado
    _LIMIT_USER_IN_BET = 2 # limite de usuario por aposta
    
    def __init__(self, bot):
        self.bot = bot

    # bot.command => commands.command
    @commands.command(name="fila", help="Cria uma fila. Args: tipo(emu, mob),tamanho(4x4,1x1..), valor")
    async def create_queue(self, ctx,type,size,price):
        if not utils.check_comando_role_permission(ctx.guild.owner_id,ctx.author.id,ctx.author.roles):
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

            view = BtnsQueue()
            view.bot = self.bot

            await ctx.send(embed=embed,view=view)
            

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
                        btn_accept.set_label(f"Entrar na fila [{total}/{_LIMIT_USER_IN_BET}]")
                        
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
                            users = [users['users_id'] for users in _USERS_ACCEPT_INTERCTION if users['message_id'] == interaction_accept_btn.message.id ]
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

                            _clear_queue_by_message_id(msg.id)

                            await msg.delete()        
                            # await self._btn_close_channel_interaction(btn_remove_channel)

                            break

                        btn_accept.set_label(f"Entrar na fila [{total}/{_LIMIT_USER_IN_BET}]")
                        await interaction_accept_btn.respond(type=7, components = [[btn_accept, btn_reject]])
                        
                    else:
                        await interaction_accept_btn.respond(type=7)

            except TimeoutError as e:
                print(f"TimeoutError {e}")
                _clear_queue_by_message_id(msg.id)
                
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
        if not _USERS_ACCEPT_INTERCTION:
            interaction = {
                "message_id": message_id,
                "users_id":[user_id],
                "total":1
            }
            _USERS_ACCEPT_INTERCTION.append(interaction)

            return True,1,

        for inter in _USERS_ACCEPT_INTERCTION:
            if user_id in  inter["users_id"]:
                return False,inter['total'],
        
        interaction_exists = False
        total_users = 0

        # verifica se ja existe a interação e se existir adiciona o usuario nela, se nao cria e adiciona usuario
        for inter in _USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id:
                total_users = len(inter["users_id"])
                if total_users >= _LIMIT_USER_IN_BET:
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
            _USERS_ACCEPT_INTERCTION.append(interaction)

        return True,total_users,

    def _reject_bet(self,**kwargs): 

        message_id = int(kwargs.get("message_id"))        
        user_id = int(kwargs.get("user_id"))

        # verifica se existe alguma interação
        if not _USERS_ACCEPT_INTERCTION:
            return False, 0,

        # verifica se existe mensagem com o id da interação e se o usuario que esta clicando esta nela
        for inter in _USERS_ACCEPT_INTERCTION:
            if int(inter["message_id"]) == message_id and user_id in inter["users_id"]:
                index = inter["users_id"].index(user_id)
                inter["users_id"].pop(index)
                total_users = len(inter["users_id"])
                return True, total_users,

        return False, 0,
    
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
    