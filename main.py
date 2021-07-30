# exit(0)
import discord, aiohttp, sys
from discord.ext import commands, tasks
discord.http.Route.BASE = 'https://discord.com/api/v9'
async def get_gateway(self, *, encoding: str = 'json', zlib: bool = True) -> str:
    return "wss://gateway.discord.gg?encoding=json&v=9&compress=zlib-stream"
discord.http.HTTPClient.get_gateway = get_gateway
class _Overwrites:
    __slots__ = ('id', 'allow', 'deny', 'type')

    def __init__(self, **kwargs):
        self.id = kwargs.pop('id')
        self.allow = int(kwargs.pop('allow_new', 0))
        self.deny = int(kwargs.pop('deny_new', 0))
        self.type = sys.intern(str(kwargs.pop('type')))

    def _asdict(self):
        return {
            'id': self.id,
            'allow': str(self.allow),
            'deny': str(self.deny),
            'type': self.type,
        }
discord.abc._Overwrites = _Overwrites
from discord.ext.commands.bot import BotBase
class Bot(BotBase, discord.Client):
  pass
commands.Bot = Bot
import random, asyncio, re, time, datetime, logging, os, json
from data.profanity import swearwords
from asyncio.tasks import Task
from other.mongo import cluster
from data.json.shop import shop_items
from data.json.slash import help_slash
from data.json.badge import badge_items
import smtplib
from cogs.startup.ready import StartUp
from discord_slash import SlashCommand, SlashContext
from data.embed.general import embed_General
from data.embed.help import embed_
from data.embed.mod import embed_Moderation
from data.embed.emoji import embed_Emoji
from data.embed.currency import embed_Currency
from data.embed.other import embed_Other
from data.json.help import help_menu
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
import logging
from discord_slash.utils.manage_components import create_select, create_select_option
from handler import ch

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log',
                              encoding='utf-8',
                              mode='w')
handler.setFormatter(
    logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


#number value, not string. This stores a list important to a part of the help command subclass
# 600034099918536718 is _WeDemBois_. The most pog dev in history
admins = [
  763854419484999722,
  725081836874760224,
  521347381636104212,
  600034099918536718,
]


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
  fallback = os.urandom(32).hex()
  prefixes = prefix
  try:
    comp = re.compile("^(" + "|".join(map(re.escape, prefixes)) + ").*", flags=re.I)
    match = comp.match(message.content)
    if match is not None:
      return match.group(1)
    return fallback
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
        components=None,
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
      return await super().send(content=content, embed=embed,file=file, files=files, delete_after=delete_after, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False), components=components)
    # except discord.HTTPException:
    except Exception as e:
      print(e)
      pass

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
        components=None,
        chb=True):
    try:
      if chb:
        content = await ch(self.prefix, self.author, self.bot, content, self.command.cog)
      else:
        pass
      return await super().reply(content=content, embed=embed, file=file, files=files, delete_after=delete_after, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False, replied_user=False), components=components)
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
client.selector = None
client.smdata = None

@tasks.loop()
async def selector_help():
  await client.wait_until_ready()
  embed = discord.Embed(
    title="Help", 
    url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
    description="Here are all the categories.",
    color=discord.Colour.random()
    )
  d = client.cogs
  for key in d.keys():
    try:
      if d[key].hidden:
        continue
    except:
      continue
    embed.add_field(
      name=key.capitalize(),
      value="`{}`".format("<prefix>"+'help '+key.lower()), 
      inline=True
    )
  if not client.selector == None:
    interaction: ComponentContext = await manage_components.wait_for_component(
      client,
      components=client.selector
    )
    if "All" in interaction.selected_options:
      embed=embed
    else:
      embed = await CustomHelp.get_cog_help(None, client.get_cog(interaction.selected_options[0]))
    await interaction.edit_origin(embed=embed)

selector_help.start()

class CustomHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (
      self.context.clean_prefix, 
      command.qualified_name, 
      command.signature
    )

  async def send_bot_help(self, mapping):
    embed = discord.Embed(
      title="Help", 
      url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
      description="Here are all the categories.",
      color=discord.Colour.random()
      )
    d = client.cogs
    paginationList = [None]
    continue_=None
    for key in d.keys():
      try:
        if not self.context.author.id in admins:
          if d[key].hidden:
            continue
        elif continue_:
          if d[key].hidden:
            continue
        elif continue_ == False:
          pass
        else:
          def check(m):
            return m.author == self.context.author and m.channel == self.context.channel
          await self.context.send("say r or n")
          msg = await self.context.bot.wait_for('message', check=check)
          if not msg.content.lower() == "r":
            continue_ = True
            continue
          else:
            continue_ = False
            pass
      except:
        continue
      embed.add_field(
        name=key.capitalize(),
        value="`{}`".format(self.context.prefix+'help '+key.lower()), 
        inline=True
      )
      paginationList.append(key.lower())
    current = 0
    buttons = [
          manage_components.create_button(
              style=ButtonStyle.URL,
              label="Invite me",
              url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
          ),
          manage_components.create_button(
              style=ButtonStyle.URL,
              label="Support Server",
              url="https://discord.gg/capitalism",
          ),
        ]
    action_row = manage_components.create_actionrow(*buttons)
    buttons2 = [
          manage_components.create_button(
              style=ButtonStyle.green,
              label="⬅️",
              custom_id="back",
          ),
          manage_components.create_button(
              style=ButtonStyle.grey,
              label=f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
              disabled=True
          ),
          manage_components.create_button(
              style=ButtonStyle.green,
              label="➡️",
              custom_id="front"
          )
        ]
    action_row2 = manage_components.create_actionrow(*buttons2)
    mainMessage = await self.context.reply(
      embed = embed,
      components=[action_row2, action_row],
      mention_author=False
    )
    while True:
      try:
          interaction: ComponentContext = await manage_components.wait_for_component(
            self.context.bot,
            components=action_row2,
            messages=mainMessage,
            timeout = 30.0,
          )
          if interaction.origin_message_id != mainMessage.id:
            await interaction.defer(edit_origin=True)
            continue
          if interaction.author != self.context.author:
            the_num = paginationList[current+1]
            if the_num is None:
              embed_edited=embed
            else:
              embed_edited = await self.get_cog_help(self.context.bot.get_cog(the_num))
            await interaction.send(
              embed = embed_edited,
              components = [client.selector, action_row],
              hidden=True
            )
            continue
          if interaction.custom_id == "back":
              current -= 1
          elif interaction.custom_id == "front":
              current += 1
          if current == len(paginationList):
              current = 0
          elif current < 0:
              current = len(paginationList) - 1
          buttons = [
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Invite me",
                url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
            ),
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Support Server",
                url="https://discord.gg/capitalism",
            ),
          ]
          action_row = manage_components.create_actionrow(*buttons)
          buttons2 = [
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="⬅️",
                    custom_id = "back"
                ),
                manage_components.create_button(
                    style=ButtonStyle.grey,
                    label=f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                    custom_id = "cur",
                    disabled=True
                ),
                manage_components.create_button(
                    style=ButtonStyle.green,
                    label="➡️",
                    custom_id = "front"
                )
              ]
          action_row2 = manage_components.create_actionrow(*buttons2)
          the_num = paginationList[current]
          if the_num is None:
            embed_edited=embed
          else:
            embed_edited = await self.get_cog_help(self.context.bot.get_cog(the_num))
          await interaction.edit_origin(
              embed = embed_edited,
              components = [action_row2, action_row]
          )
      except asyncio.TimeoutError:
          buttons = [
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Invite me",
                url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands"
            ),
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Support Server",
                url="https://discord.gg/capitalism"
            ),
            manage_components.create_button(
                style=ButtonStyle.red,
                label="Timeout",
                disabled=True
            ),
          ]
          action_row = manage_components.create_actionrow(*buttons)
          await mainMessage.edit(
              components = [
                  action_row
              ]
          )
          break

  async def get_cog_help(self, cog):
    try:
      if cog.qualified_name.lower()=="jishaku":
        return
      else:
        try:
          if cog.hidden:
            return
        except:
          return
      cmd=[]
      for commandd in cog.walk_commands():
        if (commandd.hidden==True):
          continue
        cmd.append(commandd)
      command = ''
      for cc in cmd:
        command += f'`{cc.name}`, '
      embed = discord.Embed(
        title=cog.qualified_name, 
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQm", 
        description=command,
        color=discord.Colour.random()
        )
      return embed
    except Exception as e:
      print(e)

  async def send_cog_help(self, cog):
    if cog.qualified_name.lower()=="jishaku":
      return
    else:
      try:
        if cog.hidden:
          return
      except:
        return
    cmd=[]
    for commandd in cog.walk_commands():
      if (commandd.hidden==True):
        continue
      cmd.append(commandd)
    command = ''
    for cc in cmd:
      command += f'`{cc.name}`, '
    embed = discord.Embed(
      title=cog.qualified_name, 
      url="https://www.youtube.com/watch?v=dQw4w9WgXcQm", 
      description=command,
      color=discord.Colour.random()
      )
    await self.context.send(embed=embed)

  async def send_group_help(self, group):
    if not self.context.author.id in admins:
      return await self.context.message.add_reaction(":think:825452368128376843")
    content=""
    for command in group.commands:
      content+="`{}`, ".format(command.name)
    await self.context.send(content)

  async def send_command_help(self, command):
    if not isinstance(command, commands.core.Command):
      clss = client.get_commands(command)
    else:
      clss = command
    if not clss.cog == None:
      if ((clss.hidden == True) and (self.context.author.id not in admins)) or ((clss.cog.hidden == True) and (self.context.author.id not in admins)):
        return await self.context.message.add_reaction(":think:825452368128376843")
    else:
      return await self.context.message.add_reaction(":think:825452368128376843")
    embed = discord.Embed(
      title=command,
      color=discord.Colour.random()
    )
    embed.add_field(
        name='Usage:',
        value=self.get_command_signature(command),
        inline=False
    )
    if len(clss.aliases) == 0:
      embed.add_field(
        name='Aliases:',
        # value='None, like 0. Zip, Natta, None.',
        value='None',
        inline=False
      )
    else:
      embed.add_field(
        name='Aliases:',
        value=', '.join(clss.aliases),
        inline=False
      )
    if not clss._buckets._cooldown == None:
      rate = clss._buckets._cooldown.rate
      embed.add_field(
        name='Cooldown:',
        value="{} seconds every {} {}".format(clss._buckets._cooldown.per, rate, "commands" if rate > 1 else "command"),
        inline=False
      )
    else:
      embed.add_field(
        name='Cooldown:',
        value="None",
        inline=False
      )
    embed.add_field(
      name='Description:',
      value=clss.help,
      inline=False
    )

    embed.set_footer(text="\"< >\" stands for a required argument and \"[ ]\" stands for a optional argument")

    await self.context.send(embed=embed)
           

help_attr={
   'name': "help",
  #  'cooldown': commands.cooldown(1, 2, commands.BucketType.user)
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


with open("data/json/data.json", "r") as f:
	dat = json.load(f)
client.data = dat
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

extensions = [
    'cogs.moderator.admin', 'cogs.moderator.mod', 'cogs.commands.General', 'cogs.help.rules', 'cogs.startup.error',
    'cogs.startup.ready', 'cogs.currency.Currency', 'cogs.emoji.emojis',
    'cogs.commands.Data', "cogs.commands.SocialMedia", "cogs.startup.web", 'other.mongo', 'cogs.growth.growth', 'jishaku', 'cogs.commands.Evaluation',
    "cogs.debug", "cogs.commands.Computer", "cogs.experimental",
    "cogs.music"
]

@client.command()
async def check_help(ctx):
	content = ""
	async for command in client.commands:
		if str(command.name) not in help_menu.keys():
			content += f"{command.name} "
	await ctx.send(content=content)

@client.check
async def check_cmds(ctx):
  if not client.is_ready():
    await ctx.channel.send("I am just starting!")
    return False
  if client.loadng:
    await ctx.channel.send("The developers are loading commands, try again later.")
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
  if ctx.guild == None:
    dm_channel = True
  else:
    dm_channel = False
  logs = client.logsdb
  try:
    cmds = logs[str(ctx.guild.id)]["disabled"]
    if str(ctx.command) in cmds:
      await ctx.channel.send("This command is disabled in this server.")
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

@commands.check
async def check_commands(ctx: SlashContext):
  if not client.is_ready():
    await ctx.send("I am just starting!")
    return False
  if client.loadng:
    await ctx.send("The developers are loading commands, try again later.")
    return
  banned = client.botbanned
  if ctx.guild == None:
    dm_channel = True
  else:
    dm_channel = False
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

@client.event
async def on_slash_command(ctx: SlashContext):
	try:
		client.cmdintervals[str(ctx.author.id)]
	except:
		client.cmdintervals[str(ctx.author.id)] = []
	client.cmdintervals[str(ctx.author.id)].append(datetime.datetime.utcnow())
	author_messages = client.cmdintervals[str(ctx.author.id)]
	if len(author_messages) < 4:
		pass
	else:
		if (author_messages[-1] - author_messages[-3]).seconds < 6:
			try:
				client.cmdintervals["strikes"][str(ctx.author.id)] += 1
				if client.cmdintervals["strikes"][str(ctx.author.id)] >= 10:
					users = client.botbanned
					if str(ctx.author.id) in users.keys():
						if users[str(ctx.author.id)]["spam_banned"]:
							return
						users[str(ctx.author.id)]["spam_banned"] = True
					else:
						users[str(ctx.author.id)] = {
						    "_id": str(ctx.author.id),
						    "spam_banned": True,
						    "bot_banned": False
						}
					channel = await client.fetch_channel(853288563352404058)
					await channel.send(
					    f"The bot spam_banned {ctx.author} for spamming commands, id {ctx.author.id}"
					)
					try:
						await ctx.author.send(
						    "You are now bot banned from our bot for spamming too many commands."
						)
					except:
						await ctx.message.reply(
						    "You are now bot banned from our bot for spamming too many commands."
						)
			except:
				client.cmdintervals["strikes"][str(ctx.author.id)] = 1
			em = discord.Embed(
			    title="Stop spamming commands!",
			    description=
			    "If you continue spam commands you will be bot banned.")
			try:
				await ctx.author.send(embed=em)
			except:
				await ctx.send(embed=em)

@client.event
async def on_slash_command_error(ctx: SlashContext, er):
  print(er)
  if ctx.guild == None:
    await ctx.send("You cannot use slash commands in DMs.", hidden=True)
  banned = client.botbanned
  try:
    if banned[str(ctx.author.id)]["bot_banned"]:
      await ctx.send(
			    "You're bot banned! Join support server to appeal. ~~bad boy!~~",
			    hidden=True)
      return
    if banned[str(ctx.author.id)]["spam_banned"]:
      await ctx.send(
			    "You were banned for spamming too many commands. \nAppeal here: discord.gg/capitalism (If you are banned from the server, there's no way you can get unbanned.)",
			    hidden=True)
  except:
    print(er)
    return

@client.command()
async def calc(ctx, arg):
	pass

@client.command()
async def test(ctx):
	print(client.data)

@client.command()
async def reload(ctx, *, arg):
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


# @discord.ext.commands.cooldown(1, 40, commands.BucketType.user)
# @client.command()
# async def rob(ctx, member: discord.Member):
#     if await find_ban(ctx.author.id)==True:
#       await ctx.send("You are bot banned.")
#       return
#     await open_account(ctx.author)
#     await open_account(member)
#     user=ctx.author
#     target=member
#     users = await get_bank_data()
#     wallet_amt=users[str(user.id)]["wallet"]
#     wallet_amt_target=users[str(target.id)]["wallet"]
#     success = int(random.randrange(1,100))
#     if not int(wallet_amt) < 500:
#       if not int(wallet_amt_target) < 100:
#         if int(success) > 69:
#           stolen_amount=int(random.randrange(round(int(wallet_amt_target)/100),int(wallet_amt_target)/10))
#           users[str(user.id)]["wallet"]+=stolen_amount
#           users[str(target.id)]["wallet"]-=stolen_amount
#           await ctx.send(f"You robbed {stolen_amount}!")
#           with open("data.json","w") as f:
#             json.dump(users,f, sort_keys=True, indent=4)
#           return True
#         else:
#           users[str(user.id)]["wallet"]-=500
#           users[str(target.id)]["wallet"]+=500
#           await ctx.send("You failed to rob this guy and paid him 500 coins.")
#           with open("data.json","w") as f:
#             json.dump(users,f, sort_keys=True, indent=4)
#           return True
#       else:
#         await ctx.send("They're too poor to be robbed.")
#     else:
#       await ctx.send("you need at least 500 coins to rob someone.")

slash = SlashCommand(client, sync_commands=True)

options = [{
"name": "argument",
"description": "input for command or category",
"required": False,
"type": 3
}]
  
@slash.slash(name="Prefix", description="Gives you the bot prefix", options=[])
@check_commands
async def _prefix(ctx: SlashContext):
  prefix = client.logsdb
  try:
    prefix = prefix[str(ctx.guild.id)]["prefix"]
    prefix = str(prefix).lstrip('[').rstrip(']')
    await ctx.send(f"Hi! My prefix is {prefix}!")
  except:
    await ctx.send("Hi! My prefix is 'CAP' or 'c/'!")


@slash.slash(name="Help", description="Run this command for help!", options=options)
@check_commands
async def _help(ctx: SlashContext, argument=None):
  embed = await embed_(ctx)
  embed.color = discord.Color.random()
  embed_General.color = discord.Color.random()
  embed_Moderation.color = discord.Color.random()
  embed_Other.color = discord.Color.random()
  embed_Emoji.color = discord.Color.random()
  embed_Currency.color = discord.Color.random()
  inpt = None
  if argument == None:
    buttons = [
      manage_components.create_button(
          style=ButtonStyle.URL,
          label="Invite me",
          url=
          "https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands"
      ),
      manage_components.create_button(
          style=ButtonStyle.URL,
          label="Support Server",
          url="https://discord.gg/capitalism"),
    ]  
    action_row = manage_components.create_actionrow(*buttons)
    embed.add_field(name="Slash", value="`/help slash`")
    await ctx.send(embed=embed, components=[action_row])
  else:
    inpt = argument.lower()
    if inpt == "all":
      embed.add_field(name="Slash", value="`/help slash`")
      buttons = [
        manage_components.create_button(
            style=ButtonStyle.URL,
            label="Invite me",
            url=
            "https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands"
        ),
        manage_components.create_button(
            style=ButtonStyle.URL,
            label="Support Server",
            url="https://discord.gg/capitalism"),
      ]
      action_row = manage_components.create_actionrow(*buttons)
      await ctx.send(embed=embed, components=[action_row])
    elif inpt == "moderation":
      await ctx.send(embed=embed_Moderation)
    elif inpt == "other":
      await ctx.send(embed=embed_Other)
    elif inpt == "emoji":
      await ctx.send(embed=embed_Emoji)
    elif inpt == "currency":
      await ctx.send(embed=embed_Currency)
    elif inpt == "general":
      await ctx.send(embed=embed_General)
    elif inpt == "slash":
      embed_Slash = discord.Embed(
        title="All Slash Commmands",
        description=
        "`communism`, `prefix`, `help`, `invite`, `support`, `website`, `pograte`, `think`"
    )
      await ctx.send(embed=embed_Slash)
    elif inpt == "data":
      embed_Data = discord.Embed(color=discord.Color.random()) 
      embed_Data.add_field(
        name="Data Type Commands",
        value="`removedata`, `removelogs`, `removeall`")
      await ctx.send(embed=embed_Data)
    else:
      try:
        if inpt in slash.commands.keys():
          try:
            desc = help_slash[inpt]["use"]
            footer = help_slash[inpt]["footer"]
            em = discord.Embed(
              title=inpt,
              description=f"__**Description**__: {desc}")
            em.set_footer(text=f"Command format --- {footer}")
            await ctx.send(embed=em)
          except:
            await ctx.send(
              f"{inpt} is a valid command but no help source was found."
            )
        else:
          command = client.get_command(inpt)
          inpt = command.name
          try:
            desc = help_menu[inpt]["use"]
            cooldown = help_menu[inpt]["cooldown"]
            alias = help_menu[inpt]["aliases"]
            footer = help_menu[inpt]["footer"]
            em = discord.Embed(
              title=inpt,
              description=
              f"__**Description**__: {desc} \n __**Cooldown**__: {cooldown} seconds \n __**Aliases**__: {alias}"
            )
            em.set_footer(text=f"Command format --- {footer}")
            await ctx.send(embed=em)
          except:
            await ctx.send(
              f"{command.name} is a valid command but no help source was found."
            )
      except:
        await ctx.send("that is not a valid category or command!")


@slash.slash(name="Communism", description="Will ban you", options=[])
@check_commands
async def _communism(ctx: SlashContext):
  await ctx.send("Capitalism is better", hidden=True)


@slash.slash(name="Invite", description="Posts the invite link", options=[])
@check_commands
async def _invite(ctx: SlashContext):
  await ctx.send(
    "[Click me for the invite](<https://discord.com/api/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands>)",
    hidden=True)


@slash.slash(name="Support",
            description="Posts the support server",
            options=[])
@check_commands
async def _support(ctx: SlashContext):
  await ctx.send("https://discord.gg/capitalism", hidden=True)


@slash.slash(name="pograte", description="POG RATE", options=[])
@check_commands
async def _pograte(ctx: SlashContext):
  number = random.randint(1, 100)
  embedPog = discord.Embed(
    title="POG RATE MACHINE",
    description="You are {}% pog <:littlepog:825452143657353226>".format(
        number),
    color=discord.Color.random())
  await ctx.send(embed=embedPog, hidden=True)


@slash.slash(name="website", description="Posts website", options=[])
@check_commands
async def _website(ctx: SlashContext):
  await ctx.send("https://discord.capitalismbot.repl.co", hidden=True)


options_think = [{
  "name": "seconds",
  "description": "How long should I think? (In seconds)",
  "required": False,
  "type": 4
}]


@slash.slash(name="think",
            description="I will think a lot",
            options=options_think)
async def _think(ctx: SlashContext, seconds=1):
  await ctx.defer()
  if seconds > 840:
    await ctx.send("Sorry, I cannot think more than 14 minutes.")
  await asyncio.sleep(seconds)
  await ctx.send(
    f"I thought for {seconds} seconds, but still don't know how intelligent you are."
)

for extension in extensions:
	client.load_extension(extension)

client.run(os.getenv("TOKEN"))