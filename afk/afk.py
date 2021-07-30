import discord
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions, CheckFailure
import random
import asyncio
import json, math
import os

def Json(file1, data1):
  file1.truncate(0)
  file1.seek(0)
  file1.write(json.dumps(data1, indent=4))   

bot = commands.Bot(command_prefix=['pt ','Pt ','pT ','PT '], case_insensitive=True)

shop_items={
  "farm" :{
    "name": "farm",
    "price": 1000,
    "income": 5
  },
  "cow_farm" :{
    "name": "cow_farm",
    "price": 10000,
    "income": 60
  },
  "golden_cow_farm":{
    "name": "golden_cow_farm",
    "price": 100000,
    "income": 800
  },
  "magical_cow_land":{
    "name": "magical_cow_land",
    "price": 1000000,
    "income": 10000
  },
  "white_house_cow":{
    "name": "white_house_cow",
    "price": math.inf,
    "income": "negative 100000"
  }
}
prestige_items={
  "polish_cow" :{
    "name": "polish_cow",
    "price": 1,
    "income": 10
  },
  "cow_scammer" :{
    "name": "cow_scammer",
    "price": 5,
    "income": 100
  },
  "robber_cow":{
    "name": "robber_cow",
    "price": 10,
    "income": 500
  },
  "president_cow":{
    "name": "president_cow",
    "price": 1000,
    "income": 100000
  },
  "x2space":{
    "name": "x2space",
    "price": 100,
    "income": 0
  }
}
multiplier_shop={
  "+2% multi":{
    "name": "multi2",
    "price": 15000,
    "multi": 2
  },
  "+3% multi":{
    "name": "multi3",
    "price": 22000,
    "multi": 3
  },
  "+5% multi":{
    "name": "multi5",
    "price": 28000,
    "multi": 5
  },
  "+10% multi":{
    "name": "multi10",
    "price": 55000,
    "multi": 10
  },
  "+100% multi":{
    "name": "multi100",
    "price": 520000,
    "multi": 100
  }
}


bot.remove_command("help")

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandOnCooldown):
    em = discord.Embed(
      title="Slow it down! mate",
      description=f"Try again in {error.retry_after:.2f}s.", color=discord.Color.random()
      )
    await ctx.reply(embed=em)
  else:
    print(error)

@bot.event
async def on_ready():
  await bot.change_presence(status=discord.Status.idle, activity=discord.Game("PT help"))
  print("AFK bot Running")
  give_cash.start()

async def update_income():
  f = open('./afk/t.json', "r+")
  users = json.load(f)
  for user in users.keys():
    inv = users[user]["inventory"]
    efficiency = inv["cow_farm"]*60+inv["farm"]*5+inv["golden_cow_farm"]*800+inv["magical_cow_land"]*10000+inv["polish_cow"]*10+inv["cow_scammer"]*100+inv["robber_cow"]*500+inv["president_cow"]*100000
    multi = users[user]["multi"]
    users[user]["income"]=int(efficiency*(1+multi/100))
    Json(f, users)
  return True

@tasks.loop(seconds=60.0)
async def give_cash():
  f = open('./afk/t.json', "r+")
  users = json.load(f)
  for user in users.keys():
    if not users[user]["pending income"] > users[user]["income max"]:
      if not users[user]["income"] > users[user]["income max"]:
        users[user]["pending income"]+=int(users[user]["income"])
      else:
        users[user]["pending income"]=users[user]["income max"]
    else:
      users[user]["pending income"]=users[user]["income max"]
    Json(f, users)

@bot.command()
async def help(message,arg=None):
    embed=discord.Embed(
      title="**Get started noob**",
      description="Start your business using `PT start`",
      color=discord.Color.blue()
    )
    embed.add_field(
      name="**Your Profile**",
      value="use `PT profile` to view your profile.\n`PT income` to check your pending income",
      inline=False
    )
    embed.add_field(
      name="**Income**",
      value="The income is generated automatically. Use `PT collect` to collect your pending income. The max pending income is 10 million coins, you can increase it buying more.",
      inline=False
    )
    embed.add_field(
      name="**Multipliers / Businesses**",
      value="There are currently a few multipliers - \nx2 multiplier | x3 multplier | x5 multiplier... etc\n These multipliers will help you gain more cash per minute.\nNote: your\n\nBusinesses are used to create income. \n`PT business` for more information",
      inline=False
    )
    embed.add_field(
      name="**Prestige**",
      value="`PT prestige` to prestige. You will receive prestige tokens after prestiging.",
      inline=False
    )
    embed.add_field(
      name="**Shop**",
      value="`PT shop` To view available shop items. \n`PT shop prestige` to view prestige token shop.\n`PT shop multi` for multipliers and more pending income space",
      inline=False
    )
    inpt = None
    if arg == None:
      await message.author.send(embed=embed)
      await message.send("I have sent you a DM message about my commands!")
    else:
        inpt = arg.lower()
        if inpt == "all":
          await message.author.send(embed=embed)
          await message.send("I have sent you a DM message about my commands!")
        elif inpt == "bruh":
          await message.send("bruh")
        elif inpt == "other":
          await message.send("The other bot is Capitalism#1047")
        else: 
          await message.reply("that's not a valid category lmao") 

@bot.command()
async def start(ctx):
  k = open('./afk/t.json', 'r+')
  data = json.load(k)
  if not str(ctx.author.id) in data:
    user=ctx.author
    data[str(user.id)]={}
    data[str(user.id)]["bal"]=2000
    data[str(user.id)]["income"]=0
    data[str(user.id)]["prestige"]=0
    data[str(user.id)]["prestige tokens"]=0
    data[str(user.id)]["pending income"]=0
    data[str(user.id)]["income max"]=10000000
    data[str(user.id)]["multi"]=0
    data[str(user.id)]["inventory"]={}
    for item_name in shop_items.keys():
      if item_name not in data[str(user.id)]["inventory"]:
       data[str(user.id)]["inventory"][item_name] = 0
    for item_name in prestige_items.keys():
      if item_name not in data[str(user.id)]["inventory"]:
       data[str(user.id)]["inventory"][item_name] = 0
    Json(k, data)
    await ctx.send("You made a profile!")
    
  else:
    await ctx.send("You already have a profile created! do `PT profile` for more information")

@bot.command(aliases=["bal","balance"])
async def profile(ctx):
  k = open('./afk/t.json', 'r+')
  data = json.load(k)
  if str(ctx.author.id) not in data:
    await ctx.send("heyo you don't have a profile yet")
    return
  user = ctx.author
  bal =data[str(user.id)]["bal"]
  income =data[str(user.id)]["income"]
  multi =data[str(user.id)]["multi"]
  prestige_level =data[str(user.id)]["prestige"]
  prestige_token =data[str(user.id)]["prestige tokens"]
  embed = discord.Embed(
    title = f"{ctx.author}'s balance",
    color = discord.Color.random()
  )
  embed.add_field(
    name="**Balance**",
    value=bal
  )
  embed.add_field(
    name="**Income per minute**",
    value=income
  )
  embed.add_field(
    name="**Multi**",
    value=multi
  )
  embed.add_field(
    name="**Prestige Level**",
    value=prestige_level,
    inline=False
  )
  embed.add_field(
    name="**Prestige Tokens**",
    value=prestige_token
  )
  embed.set_footer(
    text="did you know that tax fraud exists?"
  )
  await ctx.send(embed=embed)

@bot.command()
async def abuse(ctx, amount:int):
  if not ctx.author.id == 763854419484999722:
    return
  try:
    user = ctx.author
    k = open('./afk/t.json', 'r+')
    data = json.load(k)
    data[str(user.id)]["bal"]+=amount
    Json(k, data)
    await ctx.send("Done")
  except Exception as e:
    print(e)

@bot.command()
async def business(ctx):
    k = open('./afk/t.json', 'r+')
    data = json.load(k)
    user = ctx.author
    inv =data[str(user.id)]["inventory"]
    em=discord.Embed(
      title = f"`{ctx.author}'s business`"
    )
    t=0
    for item_name, amount in inv.items():
      if amount == 0:
        continue
      t+=1
      em.add_field(
        name=item_name,
        value=amount,
        inline=False
      )
    if not t == 0:
      await ctx.send(embed=em)
    else:
      await ctx.send("you're too poor to have any business lmao. buy something from `PT shop` using `PT buy`")

@bot.command()
async def income(ctx):
  k = open('./afk/t.json', 'r+')
  data = json.load(k)
  user = ctx.author
  income =data[str(user.id)]["pending income"]
  max_income =data[str(user.id)]["income max"]
  await ctx.send(f'Your pending income is {income}! And the maxium of pending is currently {max_income}')

@bot.command()
async def shop(ctx,message=None):
  if message ==None:
    em=discord.Embed(
      title="CAP Business Shop",
      color=discord.Color.random()
    )
    for key in shop_items.keys():
      # val = shop_items[key]["showing"]
      # if val==False:
      #   continue
      name=shop_items[key]["name"]
      price=shop_items[key]["price"]
      desc=shop_items[key]["income"]
      em.add_field(name=name, value=f"${price} | income per minute: {desc}", inline=False)
    await ctx.send(embed=em)
  elif message == 'prestige':
    em=discord.Embed(
      title="CAP Prestige Shop",
      color=discord.Color.random()
    )
    for key in prestige_items.keys():
      # val = shop_items[key]["showing"]
      # if val==False:
      #   continue
      name=prestige_items[key]["name"]
      price=prestige_items[key]["price"]
      desc=prestige_items[key]["income"]
      em.add_field(name=name, value=f"${price} | income per minute: {desc}", inline=False)
    await ctx.send(embed=em)
  elif message == 'multi':
    em=discord.Embed(
      title="CAP Multiplier Shop",
      color=discord.Color.random()
    )
    for key in multiplier_shop.keys():
      # val = shop_items[key]["showing"]
      # if val==False:
      #   continue
      name=multiplier_shop[key]["name"]
      price=multiplier_shop[key]["price"]
      desc=multiplier_shop[key]["multi"]
      em.add_field(name=name, value=f"${price} | multiplier: {desc}", inline=False)
    await ctx.send(embed=em)

@bot.command()
async def buy(ctx, item, amount:int=1):
  if amount > 0:
    k = open('./afk/t.json', 'r+')
    data = json.load(k)
    if str(ctx.author.id) not in data.keys():
      await ctx.send("You didn't make a profile")
      return
    for e in shop_items:
      if item == e:
        it = shop_items[item]
        if it["price"] * amount <= data[str(ctx.author.id)]["bal"]:
          data[str(ctx.author.id)]["bal"] -= it["price"] * amount
          data[str(ctx.author.id)]["inventory"][item] += amount
          Json(k, data)
          await ctx.send(f"You bought {amount} of {item}")
          await update_income()
        else:
          await ctx.send(f"you broke")
  else:
    await ctx.send("You cannot buy negative amount of an item.")

@bot.command()
async def free(ctx):
  embed=discord.Embed(
    title="LMAO"
  )
  embed.add_field(
    name="Haha this command will send the creator your mom's credit card information",
    value="get ready to be broke!\n\n\n\n\n\n\n\n\n"
  )
  embed.add_field(
    name="‎",
    value="‎",
    inline=False
  )
  embed.add_field(
    name="‎",
    value="‎",
    inline=False
  )
  embed.set_footer(
    text="ʲᵘˢᵗ ᵏᶦᵈᵈᶦⁿᵍ  this command is still in development"
  )
  await ctx.send(embed=embed)

@bot.command()
async def prestige(ctx):
  k = open('./afk/t.json', 'r+')
  data = json.load(k)
  user = ctx.author
  if str(user.id) not in data.keys():
    await ctx.send("make a profile noob")
    return
  bal = int(data[str(user.id)]["bal"])
  prestige = int(data[str(user.id)]["prestige"])
  req = (prestige+1)*50000000*(prestige+1)
  prestige_token_add = round(bal/200000)
  if bal >= req:
    data[str(user.id)]["bal"]=0
    data[str(user.id)]["income"]=0
    data[str(user.id)]["pending income"]=0
    data[str(user.id)]["income max"]=10000000
    data[str(user.id)]["prestige"]+=1
    data[str(user.id)]["prestige tokens"]+=prestige_token_add
    data[str(user.id)]["inventory"]={}
    for item_name in shop_items.keys():
      if item_name not in data[str(user.id)]["inventory"]:
       data[str(user.id)]["inventory"][item_name] = 0
    for item_name in prestige_items.keys():
      if item_name not in data[str(user.id)]["inventory"]:
       data[str(user.id)]["inventory"][item_name] = 0
    await ctx.send(f"You have prestiged and received {prestige_token_add} prestige tokens!")
    Json(k, data)
    return True
  else:
    await ctx.send(f"mate you can't prestige yet you need at least {req} in your balance for your next prestige\n Prestige Requirement = (Your Prestige Level^2) times 50 million coins\nAmount of Prestige Tokens you get = Your balance divided by 200,000 coins")

@bot.command()
async def data(ctx):
  await ctx.send(file=discord.File('./afk/t.json'))
  await ctx.send("bruh+meme = BREME\n\n what a bremer")

@bot.command()
async def give(ctx, member:discord.Member, amount=1):
  k = open('./afk/t.json', 'r+')
  data = json.load(k)
  user = ctx.author
  other = member
  if not amount > 0:
    return await ctx.send("bruh that's negative no")
    
  if not str(other.id) in data:
    return await ctx.send("ok so that guy don't have a profile")
    
  if amount >data[str(user.id)]["bal"]:
    return await ctx.send("you broke")
      
  data[str(user.id)]["bal"]-=amount
  data[str(other.id)]["bal"]+=amount
  await ctx.send(f"ok you gave {other} {amount}, happy?")
  Json(k, data)
  return True


@tasks.loop()
async def check_exit():
  with open("afk/communicate.txt", "r") as f:
    content = f.read()
  if content == "exit":
    exit(0)

@check_exit.before_loop
async def before_check_exit():
  await bot.wait_until_ready()

check_exit.start()

if __name__ == "__main__":
  bot.run(os.getenv("AFK"))
