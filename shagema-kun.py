import discord, os, requests, json, datetime

from discord.ext import tasks, commands
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from flask import Flask
import threading
import requests

load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_TESTBOT_TOKEN = os.getenv("DISCORD_TESTBOT_TOKEN")
LINE_NOTIFY_TOKEN = os.getenv("LINE_NOTIFY_TOKEN")

intents = discord.Intents.all()
intents.messages = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(intents=intents, command_prefix="/")

roleControleMessageID = 963477173962940496
guildID_SHAGEMA = 840571302674956288

rolemoji = {    "health"         : 963477480105185330,
                "apex"           : 936216691501858846,
                "rocketleague"   : 985517883272601600,
                "yugioh"         : 985517923638575114,
                "dbd"            : 985517992408395826,
                "smashbros"      : 985518069709418556,
                "minecraft"      : 985518188919930890,
                "splatoon"       : 985518223808151622,
                "trpg"           : 985518259338109048,
                "garticphone"    : 985518316678426725,
                "humanfallflat"  : 985518382696775752,
                "bga"            : 985518436459364357,
                "escape"         : 985518483053883442,
                "mj"             : 990991250641535016
            }

privatech = [ 'admin',
              'chibunny',
              '最後のコボラー達',
              'ⓢⓒⓟ', 
              'ⓑⓐⓒⓚⓡⓞⓞⓜⓢ', 
              'フタリソウサ', 
              'ワンルーム・ディスコン', 
              'ueda-chat', 
              '小杉誕生祝い', 
              'アイデア帳', 
              '落書き帳', 
              '創作物' ]

line_messages = { '朝活' : 'が朝活を始めました', 
                  'RocketLeague-Chibnunny' : 'がロケリを始めました'}

morningTaskStartTime = datetime.time(hour=4, minute=30, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
morningTaskEndTime   = datetime.time(hour=8, minute=30, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))

# 起動時
@bot.event
async def on_ready():
    shagemaGuild = discord.utils.find(lambda g: g.id == guildID_SHAGEMA, bot.guilds)
    print(f'{shagemaGuild}: logged in as {bot.user}')
    emojis = { emoji.name.lower(): emoji.id for emoji in shagemaGuild.emojis }
    roles = { role.name.lower(): role.id for role in shagemaGuild.roles }
    permission = {
        shagemaGuild.default_role: discord.PermissionOverwrite(read_messages=False),
        shagemaGuild.me: discord.PermissionOverwrite(read_messages=True)
    }
    removeMorningTaskChannel()
    createMorningTaskChannel.start()
    removeMorningTaskChannel.start()

# リアクションの追加
@bot.event
async def on_raw_reaction_add(payload):
    if guildID_SHAGEMA != payload.guild_id : return
    if roleControleMessageID == payload.message_id :
        guild = bot.get_guild(payload.guild_id)
        # role  = guild.get_role(payload.emoji.name)
        role = discord.utils.find(lambda m: m.name.lower() == payload.emoji.name, guild.roles)
        print(role, role.id)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        print(f'{guild}: {member.nick if member.nick else member.display_name} add {payload.emoji.name}')

# リアクションの削除
@bot.event
async def on_raw_reaction_remove(payload):
    if guildID_SHAGEMA != payload.guild_id : return
    if roleControleMessageID == payload.message_id :
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.find(lambda m: m.name.lower() == payload.emoji.name, guild.roles)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        await member.remove_roles(role)
        print(f'{guild}: {member.nick if member.nick else member.display_name} remove {payload.emoji.name}')

# ボイチャの状態変化
@bot.event
async def on_voice_state_update(member, before, after):
    if before.channel != after.channel:
        author = member.nick if member.nick else member.display_name
        print(f'Author : {author}:')
        print(f'  Before : {before.channel}')
        print(f'  After  : {after.channel}')
        print(f'  Time   : {datetime.datetime.now().now()}')
        if not after.channel is None and after.channel.name in line_messages.keys():
            api_url = 'https://notify-api.line.me/api/notify'
            headers = {
                'Authorization': 'Bearer' + ' ' + LINE_NOTIFY_TOKEN
            } 
            messages = {
                'message': f'{author}{line_messages[after.channel.name]}'
            }
            requests.post(api_url, headers=headers, data=messages)

# テキストチャット送信
@bot.event
async def on_message(message):
    if message.author.bot : 
        if message.author.name == 'Minecraft ログイン/ログアウト通知' :
            print(f'MINECRFT: {message.author.nick}: {message.content.split()[0]}')
    else :
        print(f'Author : {message.author.nick if message.author.nick else message.author.display_name}')
        print(f'  Content : {message.content}')
        # print(f'  Guild   : {message.guild}')
        print(f'  Channel : {message.channel}')
        print(f'  Type    : {message.channel.type}')
        print(f'  URL     : {message.channel.jump_url}')

        webhook_url  = 'https://discord.com/api/webhooks/991592846593376336/qVYzwxZYHStcDq2PIH-LfjycNVonkPcHa18lu1Z3rqaW37yv1QYXhiRKV8wbBmdkiory'
        main_content = {
            'username'   : message.author.nick if message.author.nick else message.author.display_name,
            'avatar_url' : message.author.avatar.url,
            'content'    : f'{message.content}\n[{message.channel}]({message.channel.jump_url})'
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent"  : "DiscordBot (private use) Python-urllib/3.10",
        }

        if message.attachments:
            for attachment in message.attachments:
                save_file_name = f'{main_content["username"]}_{message.channel}_{attachment.filename}'
                print(f'  Attachment')
                print(f'    filename     : {attachment.filename}')
                print(f'    url          : {attachment.url}')
                print(f'    content_type : {attachment.content_type}')
                print(f'    created_at   : {message.created_at} ')
                await attachment.save(f'./images/{save_file_name}')
        else:
            res = requests.post(webhook_url, json.dumps(main_content).encode(), headers=headers)

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

@tasks.loop(time=morningTaskStartTime)
async def createMorningTaskChannel():
    shagemaGuild = discord.utils.find(lambda g: g.id == guildID_SHAGEMA, bot.guilds)
    category = shagemaGuild.get_channel(942305484252254258)
    ch = await category.create_voice_channel(name='朝活')
    print(f'{ch.mention}を作成しました')

@tasks.loop(time=morningTaskEndTime)
async def removeMorningTaskChannel():
    shagemaGuild = discord.utils.find(lambda g: g.id == guildID_SHAGEMA, bot.guilds)
    asakatsu = discord.utils.find(lambda ch: ch.name == '朝活', shagemaGuild.voice_channels)
    print(asakatsu.members)
    # await asakatsu.delete()
    # print(f'{asakatsu}を削除しました')

if __name__ == "__main__":
    bot.run(DISCORD_BOT_TOKEN)