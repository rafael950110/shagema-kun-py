# This example requires the 'message_content' intent.

import discord, os, requests, json, datetime

from discord.ext import tasks, commands
from dotenv import load_dotenv
from urllib.request import Request, urlopen
from flask import Flask
import threading


load_dotenv()
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN")
DISCORD_TESTBOT_TOKEN = os.getenv("DISCORD_TESTBOT_TOKEN")

intents = discord.Intents.all()
intents.message_content = True

# client = discord.Client(intents=intents)
bot = commands.Bot(intents=intents, command_prefix="/")

app = Flask(__name__)

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

morningTaskStartTime = datetime.time(hour=4, minute=30, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))
morningTaskEndTime   = datetime.time(hour=8, minute=30, tzinfo=datetime.timezone(datetime.timedelta(hours=9)))


@bot.event
async def on_ready():
    shagemaGuild = discord.utils.find(lambda g: g.id == guildID_SHAGEMA, bot.guilds)
    print(f'{shagemaGuild}: logged in as {bot.user}')
    emojis = { emoji.name.lower(): emoji.id for emoji in shagemaGuild.emojis }
    roles = { role.name.lower(): role.id for role in shagemaGuild.roles }
    # vc = {  for ch in shagemaGuild. }
    # print( [ (ek, ek in roles.keys()) for ek, ev in emojis.items()] )
    # print(roles.keys())
    # print(emojis)
    permission = {
        shagemaGuild.default_role: discord.PermissionOverwrite(read_messages=False),
        shagemaGuild.me: discord.PermissionOverwrite(read_messages=True)
    }
    createMorningTaskChannel.start()
    removeMorningTaskChannel.start()


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

@bot.event
async def on_raw_reaction_remove(payload):
    if guildID_SHAGEMA != payload.guild_id : return
    if roleControleMessageID == payload.message_id :
        guild = bot.get_guild(payload.guild_id)
        role = discord.utils.find(lambda m: m.name.lower() == payload.emoji.name, guild.roles)
        member = discord.utils.find(lambda m: m.id == payload.user_id, guild.members)
        await member.remove_roles(role)
        print(f'{guild}: {member.nick if member.nick else member.display_name} remove {payload.emoji.name}')

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
    await asakatsu.delete()
    print(f'{asakatsu}を削除しました')

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

if __name__ == "__main__":
    # app.run(debug=True)
    bot.run(DISCORD_TESTBOT_TOKEN)