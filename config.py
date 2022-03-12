import discord
"""
type 0 = text, 2 = voice 
ref: https://discord.com/developers/docs/resources/channel#channel-object-channel-types
permissions= readonly, all
"""

CATEGORIES_WITH_CHANNELS = {
    '🏁Entrada🏁':[
        {'name':'boas-vindas','type':0,'permission':'readonly'},
        {'name':'sistema-de-apostas','type':0,'permission':'readonly'},
        {'name':'regras','type':0,'permission':'readonly'},
    ],
    'Apostas emulador':[
        {'name':'x4-emulador-3','type':0,'permission':'all'},
        {'name':'x4-emulador-5','type':0,'permission':'all'},
        {'name':'x4-emulador-10','type':0,'permission':'all'},
        {'name':'x3-emulador-3','type':0,'permission':'all'},
        {'name':'x3-emulador-5','type':0,'permission':'all'},
        {'name':'x3-emulador-10','type':0,'permission':'all'},
        {'name':'x2-emulador-3','type':0,'permission':'all'},
        {'name':'x2-emulador-5','type':0,'permission':'all'},
        {'name':'x2-emulador-10','type':0,'permission':'all'},
        {'name':'x1-emulador-3','type':0,'permission':'all'},
        {'name':'x1-emulador-5','type':0,'permission':'all'},
        {'name':'x1-emulador-10','type':0,'permission':'all'},
        {'name':'apostas-emu-acima-de-10','type':0,'permission':'all'},

    ],
    'Apostas mobile':[
        {'name':'x4-mob-3','type':0,'permission':'all'},
        {'name':'x4-mob-5','type':0,'permission':'all'},
        {'name':'x4-mob-10','type':0,'permission':'all'},
        {'name':'x3-mob-3','type':0,'permission':'all'},
        {'name':'x3-mob-5','type':0,'permission':'all'},
        {'name':'x3-mob-10','type':0,'permission':'all'},
        {'name':'x2-mob-3','type':0,'permission':'all'},
        {'name':'x2-mob-5','type':0,'permission':'all'},
        {'name':'x2-mob-10','type':0,'permission':'all'},
        {'name':'x1-mob-3','type':0,'permission':'all'},
        {'name':'x1-mob-5','type':0,'permission':'all'},
        {'name':'x1-mob-10','type':0,'permission':'all'},
        {'name':'apostas-mob-acima-de-10','type':0,'permission':'all'},
    ],
    'Apostas mistas':[
        {'name':'x4-misto-5','type':0,'permission':'all'},
        {'name':'x4-misto-3','type':0,'permission':'all'},
        {'name':'x4-misto-10','type':0,'permission':'all'},
        {'name':'x3-misto-3','type':0,'permission':'all'},
        {'name':'x3-misto-5','type':0,'permission':'all'},
        {'name':'x3-misto-10','type':0,'permission':'all'},
        {'name':'x2-misto-3','type':0,'permission':'all'},
        {'name':'x2-misto-5','type':0,'permission':'all'},
        {'name':'x2-misto-10','type':0,'permission':'all'},
        {'name':'x1-misto-3','type':0,'permission':'all'},
        {'name':'x1-misto-5','type':0,'permission':'all'},
        {'name':'x1-misto-10','type':0,'permission':'all'},
        {'name':'apostas-misto-acima-de-10','type':0,'permission':'all'},
    ],

    'Analises de xit':[
        {'name':'ANALISE 1','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 2','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 3','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 4','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 5','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 6','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 7','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 8','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 9','type':2,'user_limit':5,'permission':'all'},
        {'name':'ANALISE 10','type':2,'user_limit':5,'permission':'all'},
    ]
}

ROLES = [
    {
        'name':'COMANDO',
        'color':discord.Colour.dark_red(),
        'permissions':discord.Permissions(
            read_messages=True,
            manage_channels=True,
            create_instant_invite=True,
            ban_members=True,
            send_messages=True,
            embed_links=True,
            add_reactions=True,
            external_emojis=True,
            use_external_emojis=True,
            attach_files=True,
            mention_everyone=True,
            read_message_history=True,
            use_slash_commands=True,
            stream=True,
            connect=True,
            speak=True,
            mute_members=True,
            deafen_members=True,
            move_members=True,
            use_voice_activation=True,
            request_to_speak=True,
            priority_speaker=True,
        )
    },
    {
        "name":"MASTER",
        'color':discord.Colour.dark_gold(),
        "permissions":discord.Permissions(administrator=True)
    }
]
