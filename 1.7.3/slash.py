import subprocess

subprocess.run("pip install discord-py-slash-command", shell=True)

import discord, os, datetime, random, asyncio
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from dotenv import load_dotenv
from pymongo import MongoClient
from data.json.slash import help_slash
from data.embed.help import embed_
from data.json.help import help_menu
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle

def get_cluster():
  load_dotenv()
  cluster = MongoClient(os.getenv("MONGO"))
  return cluster

cluster = get_cluster()

client = commands.Bot(command_prefix=str(os.urandom(2000)))
client.loadng = False
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


@commands.check
async def check_commands(ctx):
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
async def on_slash_command(ctx):
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
			    title="Hey, slow down with the slash commands!",
			    description=
			    "Please don't use slash commands too fast as I will be rate limited!")
			try:
				await ctx.author.send(embed=em)
			except:
				await ctx.send(embed=em)

@client.event
async def on_slash_command_error(ctx, er):
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

@client.listen()
async def on_message(message):
  if message.author.id == 763854419484999722 and "reboot" in message.content:
    await client.close()
    print("Slash client closed.")

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

@client.event
async def on_ready():
  await client.change_presence(status=discord.Status.idle, activity=discord.Game("CAPhelp | c/help"))
  print(f"Slash Client is Ready CTRL+R {datetime.datetime.utcnow()}")

client.run(os.getenv("TOKEN"))