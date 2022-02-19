import discord, aiohttp
from discord.ext import commands, tasks
import random, asyncio, re, datetime, logging, os
from other.mongo import cluster
from data.json.slash import help_slash
from data.embed.general import embed_General
from data.embed.help import embed_
from data.embed.mod import embed_Moderation
from data.embed.emoji import embed_Emoji
from data.embed.currency import embed_Currency
from data.embed.other import embed_Other
from data.json.help import help_menu
from handler import ch
from help import CustomHelp
from other.mongo import cluster
from dotenv import load_dotenv

load_dotenv()

extensions = [
  'cogs.commands.General',
  'cogs.help.rules',
  'cogs.moderator.admin',
  'cogs.moderator.mod',
  'cogs.startup.ready',
  'cogs.currency.Currency',
  'cogs.emoji.emojis',
  'cogs.startup.error',
  'cogs.commands.Data',
  "cogs.commands.SocialMedia",
  "cogs.startup.web",
  'other.mongo',
  'cogs.growth.growth',
  'jishaku',
  'cogs.commands.Evaluation',
  "cogs.debug",
  "cogs.commands.Computer",
  "cogs.experimental",
  "cogs.music",
  "cogs.help.help"
]

os.system("clear")
# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log',
#                               encoding='utf-8',
#                               mode='w')
# handler.setFormatter(
#     logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

async def get_pre(bot, message):
  data = client.logsdb
  try:
    if str(message.guild.id) in data.keys():
      prefix = data[str(message.guild.id)]["prefix"]
    else:
      return [
			    'CAP', 'cap', 'cAp', "caP", "Cap", "CAp", "CaP", "cAP", "c/",
			    "C/"
			]
  except:
    return [
		    'CAP', 'cap', 'cAp', "caP", "Cap", "CAp", "CaP", "cAP", "c/", "C/"
		]
  prefixes = prefix
  try:
    comp = re.compile("^(" + "|".join(map(re.escape, prefixes)) + ").*", flags=re.I)
    match = comp.match(message.content)
    if match is not None:
      return str(match.group(1))
    return str(os.urandom(4000))
  except:
    return ""

intents = discord.Intents.all()
intents.presences = False

class MyContext(commands.Context):
  async def send(self, content=None,
        *,
        tts=None,
        embed=None,
        embeds=None,
        file=None,
        files=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        reference=None,
        view=None,
        stickers=None,
        chb=True
      ):
    try:
      if self.command.name.lower() == "help":
        cog_ = "help"
      elif self.command.name.lower() in ["calc", "test", "reload", "check_help"]:
        cog_ = "main_file_commands"
      else:
        cog_ = self.command.cog.qualified_name.lower()
      if chb:
        content = await ch(self.prefix, self.author, self.bot, content, cog_)
      else:
        pass
      allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False)
      return await super().send(content=content, embed=embed, embeds=embeds, file=file, files=files, delete_after=delete_after, allowed_mentions=allowed_mentions, view=view, stickers=stickers)
    # except discord.HTTPException:
    except Exception as e:
      print(e)

  async def reply(self, content=None,
        *,
        tts=None,
        embed=None,
        embeds=None,
        file=None,
        files=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        reference=None,
        mention_author=None,
        view=None,
        chb=True):
    try:
      if chb:
        content = await ch(self.prefix, self.author, self.bot, content, self.command.cog)
      else:
        pass
      return await super().reply(content=content, embed=embed, file=file, files=files, delete_after=delete_after, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False, replied_user=False), view=view)
    # except discord.HTTPException:
    except Exception as e:
      print(e)
      pass

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        usable_list = [725081836874760224,763854419484999722]
        if user.id in usable_list:
            return True
        return await super().is_owner(user)

    async def get_context(self, message, *, cls=MyContext):
        return await super().get_context(message, cls=cls)

client = MyBot(case_insensitive=True,
command_prefix=get_pre,
strip_after_prefix=True,
intents=intents)
client.smdata = None

help_attr={
    'name': "help",
    'aliases': ['h']
  }

commands.cooldown(1, 5)(client.get_command('help'))
help_cmd = CustomHelp(
  command_attrs=help_attr
)

client._BotBase__cogs = commands.core._CaseInsensitiveDict()
client.help_command=help_cmd
client.uptime=None

client.loadng = False

def convert_mongo():
  db = cluster["CapBot"]
  collection = db["main"]
  cursor = collection.find({})
  for document in cursor:
    users = document
  for user in users.keys():
    if user == "_id":
      continue
    client.maindb[user]={k:v for k, v in users[user].values()}
    client.maindb[user]["_id"]=user
  db = cluster["CapBot"]
  collection = db["logs"]
  cursor = collection.find({})
  for document in cursor:
    users = document
  for user in users.keys():
    if user == "_id":
      continue
    client.logsdb[user]={k:v for k, v in users[user].values()}
    client.logsdb[user]["_id"]=user
  db = cluster["CapBot"]
  collection = db["users"]
  cursor = collection.find({})
  for document in cursor:
    users = document
  for user in users.keys():
    if user == "_id":
      continue
    client.usersdb[user]={k:v for k, v in users[user].values()}
    client.usersdb[user]["_id"]=user

client.intervals = {}
db = cluster["CapBot"]
collection = db["main"]
cursor = collection.find({})
client.maindb = {}
for document in cursor:
	client.maindb[document["_id"]] = document
collection = db["logs"]
cursor = collection.find({})
client.logsdb = {}
for document in cursor:
	client.logsdb[document["_id"]] = document
collection = db["users"]
cursor = collection.find({})
client.usersdb = {}
for document in cursor:
	client.usersdb[document["_id"]] = document
collection = db["bot_banned"]
client.botbanned = {}
cursor = collection.find({})
for document in cursor:
	client.botbanned[document["_id"]] = document
collection = db["bitcoin"]
client.bitcoin = {"_id": 1}
cursor = collection.find({"_id": 1})
for document in cursor:
	client.bitcoin["exchange_rate"] = document["exchange_rate"]
client.cmdintervals = {"strikes": {}}
client.usage = {}
client.aiohttp_session = aiohttp.ClientSession()

@client.command()
async def check_help(ctx):
	content = ""
	for command in client.commands:
		if str(command.name) not in help_menu.keys():
			content += f"{command.name} "
	await ctx.send(content=content)

@client.check
async def check_cmds(ctx):
  if not client.is_ready():
    await ctx.send("I am just starting!")
    return False
  if client.loadng:
    await ctx.send("The developers are loading commands, try again later.")
    return False
  if isinstance(ctx.me, discord.Member):
    if not ctx.me.guild_permissions.send_messages:
      return False
    if not ctx.me.guild_permissions.embed_links:
      await ctx.channel.send("Heyy so... I'm missing `embed_links` permissions. More than half of the commands in this bot responds in embeds.")
      return False
    if not ctx.me.guild_permissions.external_emojis:
      await ctx.channel.send("I need to have `external_emojis` permissions! Lots of my functions will include emojis.")
      return False
    if not ctx.me.guild_permissions.read_message_history:
      await ctx.channel.send("... I can't read message history in this channel! Please make sure I have `read_message_history` permissions.")
      return False
  banned = client.botbanned
  try:
    if isinstance(ctx.channel, discord.DMChannel):
      return False
    elif client.get_channel(ctx.channel.id) is None:
      if isinstance(await client.fetch_channel(ctx.channel.id), discord.DMChannel):
        return False
    dm_channel=False
  except:
    dm_channel=False
  logs = client.logsdb
  try:
    cmds = logs[str(ctx.guild.id)]["disabled"]
    if str(ctx.command) in cmds:
      await ctx.send("This command is disabled in this server.")
      return False
  except:
    pass
  try:
    if banned[str(ctx.author.id)]["bot_banned"] or banned[str(
        ctx.author.id)]["spam_banned"] or dm_channel:
      return False
    else:
      return True
  except:
    if dm_channel:
      return False
    return True
  # return not ((ctx.author.id in await get_bot_banned()) or (ctx.guild == None) or (ctx.author.id in await get_spam_banned()) or client.loadng or (str(ctx.command) in (await get_log_data()).get(str(ctx.guild.id), {}).get("disabled", [])))

@client.command()
async def calc(ctx, arg):
	pass

@client.command()
async def test(ctx):
	print(client.data)

@client.command()
async def reload(ctx, *, arg=None):
  if arg is None:
    client.loadng = True
    for extension in extensions:
      client.reload_extension(extension)
    await ctx.send("Reloaded all.")
    client.loadng=False
    return
  try:
    devs = [763854419484999722, 583745403598405632]
    if not ctx.author.id in devs:
      return
    client.loadng = True
    argument = ""
    for i in arg:
      argument += i
    try:
      client.reload_extension(argument)
    except Exception as e:
      print(e)
    await ctx.send("Reloaded.")
    client.loadng = False
  except Exception as e:
    print(e)

for extension in extensions:
	client.load_extension(extension)

client.run("ODIzOTMzNDM4MDc5Nzk1MjYw.YFoBzw.HxYegdHARAz4zmsmWXllKOlcuTc")
