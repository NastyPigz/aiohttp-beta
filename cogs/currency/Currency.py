import discord
from discord.ext import commands, tasks
from other.mongo import cluster
import time
import random
import asyncio
from data.json.badge import badge_items
from data.json.shop import shop_items
from data.json.jobs import jobs
import datetime
from typing import Optional, Union
from handler import CapitalismConverter
from custom_methods import pint

class Currency(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.randomList = ["WeDemBois","Puppy Plop","Capitalism", "Jason", "Kirk","Donald Trump","Joe Exotic","Fat Sandwich" ,"That one guy that ate 100 burgers in 1 hour" ,"CapitalismTheTrueGaymer" ,"Jason's bot" ,"Hi Watsup","decayedspirits", "RandomN00bson","DynaBestYT","MrAwesome","A cute kitty (*￣▽￣*)ブ","Shrek","Horrorse", "Horrorse's horse","CAPnitro","Expensive Penguin","An alpha tester"]
    self.item_usable_list = ["bank_space","coin_bag","beef","cursed_beef", "horrorse_celery"]
    self.db = {}
    self.printer.start()
    self.maindb = bot.maindb
    self.bitcoin = bot.bitcoin
    self.usersdb = bot.usersdb
    self.hidden=False

  async def profile_detect(self, ctx):
    if not str(ctx.author.id) in self.maindb.keys():
      await ctx.reply(f"You do not have a profile yet! Use `{ctx.prefix}register` to make a currency profile", mention_author=False, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
      ctx.command.reset_cooldown(ctx)
      return True
    else:
      return False

  @tasks.loop(seconds=1.0)
  async def printer(self):
    today = datetime.datetime.utcnow()
    try:
      ttime=datetime.datetime(year=today.year, month=today.month, day=today.day + 1, hour=0, minute=0,second=0, microsecond=0)
    except:
      try:
        ttime=datetime.datetime(year=today.year, month=today.month+1, day=1, hour=0, minute=0,second=0, microsecond=0)
      except:
        ttime=datetime.datetime(year=today.year+1, month=1, day=1, hour=0, minute=0,second=0, microsecond=0)
    await discord.utils.sleep_until(ttime)
    self.db={}

  @commands.command()
  async def wall(self, ctx, arg=None):
    if not arg == None and arg.lower() == "trump":
      await ctx.send("TRUMP is building the wall!")
      return
    else:
      users = self.maindb[str(ctx.author.id)]
      try:
        wallet_amt = users["wallet"]
        if wallet_amt > 999:
          users["wallet"]-=1000
          self.maindb[str(ctx.author.id)]=users
          await ctx.send("You successfully donated 1000 coins to build the wall!")
        else:
          await ctx.send("You need 1000 coins to help build the wall!")
      except:
        await ctx.send("You don't have a profile yet so you can't donate to build the wall.")

  @discord.ext.commands.cooldown(1,3,commands.BucketType.user)
  @commands.command(aliases=["btc","bit","stocks"])
  async def bitcoin(self, ctx, message: Optional[Union[discord.Member, str]]=None, amount=1):
    data = self.bitcoin
    exchange_rate = data["exchange_rate"]
    try:
      message = str(message.id)
    except:
      pass
    if await self.profile_detect(ctx):
      return
    if amount < 1:
      embed=discord.Embed(
        title="Stop trying to buy/sell nothing!"
      )
      await ctx.send(embed=embed)
    if message ==None:
      user = ctx.author
      users = self.maindb[str(user.id)]
      em=discord.Embed(
        title=f"{user}'s Bitcoin status",
        color=discord.Color.gold()
      )
      em.add_field(
        name="BTC amount",
        value=f'You have {pint(users["bitcoin"])} bitcoins, stonks!'
      )
      em.set_footer(
        text=f"{ctx.prefix}btc view | {ctx.prefix}btc buy 1 | {ctx.prefix}btc sell 1 | More commands coming soon..."
      )
      await ctx.send(embed=em)
    elif message.lower() == "view":
      em=discord.Embed(
        title="Bitcoin Exchange rate",
        description=f"**${pint(exchange_rate)} --- 1 BTC**"
      )
      await ctx.send(embed=em)
    elif message.lower() == "buy":
      user = ctx.author
      users = self.maindb[str(user.id)]
      wallet_amt = users["wallet"]
      if int(amount*exchange_rate) <= int(wallet_amt):
        old_amt = wallet_amt
        new_amt = old_amt - exchange_rate*amount
        users["wallet"]=new_amt
        users["bitcoin"]+=int(amount)
        embed=discord.Embed(
          title="Transcation Successful",
          description=f"Bought {amount} bitcoins for {exchange_rate*amount}"
        )
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(
          title="omG!1! you'Re gEttin BitCoins!1",
          description="but you're broke."
        )
        await ctx.send(embed=embed)
    elif message.lower() == "sell":
      user = ctx.author
      users = self.maindb[str(user.id)]
      wallet_amt = users["wallet"]
      bitcoin_amt = users["bitcoin"]
      if bitcoin_amt >= amount:
        old_amt = wallet_amt
        new_amt = old_amt + exchange_rate*amount
        users["wallet"]=new_amt
        users["bitcoin"]-=amount
        embed=discord.Embed(
          title="Transcation Successful",
          description=f"Sold {pint(amount)} bitcoins for {pint(exchange_rate*amount)}"
        )
        await ctx.send(embed=embed)
      else:
        embed=discord.Embed(
          title="omG!1! iNstanT riChnesS?",
          description="but you don't have enough bitcoins!"
        )
        await ctx.send(embed=embed)
    elif message.lower() == "reset":
      if ctx.author.id == 763854419484999722:
          data = self.bitcoin
          data["exchange_rate"]=50000
      else:
        embed=discord.Embed(
          title="This command is creator only.",
          description="How did you find this command anyways..?"
        )
        await ctx.send(embed=embed)
    else:
      try:
        member = message
        if not member in self.maindb.keys():
          await ctx.send("He never registered.")
          return
        user = self.bot.get_user(int(member))
        users = self.maindb
        em=discord.Embed(
          title=f"{user}'s Bitcoin status",
          color=discord.Color.gold()
        )
        em.add_field(
          name="BTC amount",
          value=pint(users[str(user.id)]["bitcoin"])
        )
        await ctx.send(embed=em)
      except:
        embed=discord.Embed(
          title="Invalid Input Given!"
        )
        await ctx.send(embed=embed)

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command(aliases=["bal","balance"])
  async def coins(self, ctx, member: discord.Member=None):
    if member ==None:
      if await self.profile_detect(ctx):
        return
      user=ctx.author
      users = self.maindb
      users[str(user.id)]["wallet"]=round(int(users[str(user.id)]["wallet"]))
      users[str(user.id)]["bank"]=round(int(users[str(user.id)]["bank"]))
      wallet_amt=users[str(user.id)]["wallet"]
      bank_amt=users[str(user.id)]["bank"]
      bank_max=users[str(user.id)]["bank_max"]
      embed_Balance = discord.Embed(
        title=f"{ctx.author.name}'s balance",
        color=discord.Color.default()
      )
      embed_Balance.add_field(
        name="Wallet",
        value = "{:,}".format(wallet_amt)
      )
      embed_Balance.add_field(
        name="Bank",
        value = "{:,} / {:,}".format(bank_amt, bank_max)
      )
      await ctx.send(embed = embed_Balance)
      return True
    else:
      user=member
      users = self.maindb
      if not str(user.id) in self.maindb.keys():
        await ctx.send("He never registered.")
        return
      users[str(user.id)]["wallet"]=round(int(users[str(user.id)]["wallet"]))
      users[str(user.id)]["bank"]=round(int(users[str(user.id)]["bank"]))
      wallet_amt=users[str(user.id)]["wallet"]
      bank_amt=users[str(user.id)]["bank"]
      bank_max=users[str(user.id)]["bank_max"]

      embed_Balance = discord.Embed(
        title=f"{member.name}'s balance",
        color=discord.Color.default()
      )
      embed_Balance.add_field(
        name="Wallet",
        value = "{:,}".format(wallet_amt)
      )
      embed_Balance.add_field(
        name="Bank",
        value = "{:,} / {:,}".format(bank_amt, bank_max)
      )
      await ctx.send(embed = embed_Balance)
      return True

  @discord.ext.commands.cooldown(1, 3600, commands.BucketType.user)
  @commands.command()
  async def work(self, ctx, job=None):
    if await self.profile_detect(ctx):
      return
    user = ctx.author
    users = self.maindb
    if job == None:
      job = users[str(user.id)]["job"]
      if job == None:
        embed=discord.Embed(
          title="You're unemployed noob!",
          description=f"Use `{ctx.prefix}work list` to receive a list of jobs!"
        )
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)
      else:
        question = random.choice(jobs[job]["tasks"])
        await ctx.send(question["question"])
        def check(m):
          return m.channel==ctx.channel and m.author==ctx.author
        try:
          msg = await self.bot.wait_for('message', timeout=60.0, check=check)
          if msg.content.lower() in question["response"]:
            await ctx.send("great job that's a valid response")
          else:
            await ctx.send("TERRIBLE! THAT'S NOT EVEN CLOSE!")
        except asyncio.TimeoutError:
          await ctx.reply("You're so slow! Terrible effort. I gave you 1 minute to do this easy job and you failed. You're not getting any money.")
        return
    elif job == "list":
      em = discord.Embed(
        title="List of Jobs",
        description="~~Smh imagine unemployed~~"
      )
      for i in jobs.keys():
        em.add_field(
          name=i,
          value="Requirement: {} commands".format(jobs[i]["req"])
        )
      await ctx.send(embed=em)
      ctx.command.reset_cooldown(ctx)
    elif job in jobs.keys():
      data = self.usersdb
      if job == users[str(user.id)]["job"]:
        await ctx.send("You already have this job.")
        return
      if not data[str(user.id)]["commands"]<jobs[job]["req"]:
        users[str(user.id)]["job"]=job
        embed=discord.Embed(
          title=f"Successfully applied for {job} job!",
          description="now you must work hard or else..."
        )
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)
      else:
        await ctx.send("You don't meet the requirements to get this job.")
        ctx.command.reset_cooldown(ctx)
    else:
      await ctx.send("Invalid job provided!")
      ctx.command.reset_cooldown(ctx)
      return

  @discord.ext.commands.cooldown(1, 60, commands.BucketType.user)
  @commands.command(aliases=["slut"])
  async def beg(self, ctx):
    if await self.profile_detect(ctx):
      return
    user=ctx.author
    users = self.maindb
    exp = users[str(user.id)]["exp"]
    level = int(exp / 100)
    if level > 999:
        level = 1000
    level_multi = int(level / 50)
    multi = users[str(user.id)]["multi"] + level_multi
    if multi > 99:
        multi = 100
    earnings = int(random.randrange(1,10)*(1+(int(multi/100))))
    who = random.choice(self.randomList)
    if random.randint(1,100) > 39:
      embed=discord.Embed(
        title=f"{who} felt bad for you!",
        description=f"You received {pint(earnings)}"
      )
      embed.set_footer(text="nice")
      await ctx.send(embed=embed)
    else:
      embed=discord.Embed(
        title=f"{who} didn't feel like it.",
        description="You get NOTHING."
      )
      embed.set_footer(text="2bad4u")
      await ctx.send(embed=embed)
      return
    users[str(user.id)]["wallet"]+=earnings

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def ads(self,ctx, member:discord.Member=None):
    if not member == None:
      try:
        users = self.maindb
        ad_price = users[str(member.id)]["ads"]
        embed = discord.Embed(
          title=f"{member}'s Advertisement Data",
          description = f"Advertisement Price: {pint(ad_price)}"
        )
        await ctx.send(embed=embed)
        return
      except:
        await ctx.send("Either that user was not valid, or didn't register the bot.")
        return
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    ad_price = users[str(ctx.author.id)]["ads"]
    embed = discord.Embed(
      title=f"{ctx.author}'s Advertisement Data",
      description = f"Advertisement Price: {pint(ad_price)}"
    )
    await ctx.send(embed=embed)
  
  @discord.ext.commands.cooldown(1, 4200, commands.BucketType.user)
  @commands.command()
  async def buyad(self, ctx, member:discord.Member=None):
    if await self.profile_detect(ctx):
      return
    if member == None:
      await ctx.send("You must give a valid member in the argument!")
      ctx.command.reset_cooldown(ctx)
      return
    if member == ctx.author:
      embed=discord.Embed(
        title="You're trying to buy your own advertisement!",
        description="You can't get yourself famous yourself."
      )
      await ctx.send(embed=embed)
      ctx.command.reset_cooldown(ctx)
      return
    if not str(member.id) in self.maindb.keys():
      await ctx.send("He never registered.")
      return
    users = self.maindb
    ad_price = users[str(member.id)]["ads"]
    wallet_amt = users[str(ctx.author.id)]["wallet"]
    if wallet_amt >= ad_price:
      users[str(ctx.author.id)]["wallet"]-=ad_price
      users[str(member.id)]["wallet"]+=ad_price
      growth = int(users[str(member.id)]["ads"]/10)
      users[str(ctx.author.id)]["ads"]+= int(users[str(member.id)]["ads"]/10)
      embed=discord.Embed(
        title="Transcation Successful!",
        description=f"You bought {member}'s ads for {pint(ad_price)}, and your advertisement price grew by {pint(growth)}"
      )
      await ctx.send(embed=embed)
    else:
      await ctx.send("You don't have enough money!!! Smh as your punishment I'm giving you a 70 minute cooldown")
  
  @discord.ext.commands.cooldown(1, 600, commands.BucketType.user)
  @commands.command(aliases=["search","mine","scout"])
  async def dive(self, ctx):
    if await self.profile_detect(ctx):
      return
    user=ctx.author
    users = self.maindb
    exp = users[str(user.id)]["exp"]
    level = int(exp / 100)
    if level > 999:
        level = 1000
    level_multi = int(level / 50)
    multi = users[str(user.id)]["multi"] + level_multi
    if multi > 99:
        multi = 100
    treasure = int(random.randrange(200,300)*(1+(int(multi/100))))
    who = random.choice(self.randomList)
    success = random.randrange(1,100)
    if int(success) > 74:
      pup = users[str(user.id)]["inventory"]["puppy_true_gaymer_pass"]
      capb=users[str(user.id)]["inventory"]["capitalism_blessing"]
      if pup==0 and capb==0:
        treasure = int(random.randrange(500,800)*(1+(int(multi/100))))
      else:
        pass
      embed=discord.Embed(
        title=f"{who} blessed you SO MUCH that you found TREASURE!",
        description=f"You sold all the jewels and got {pint(treasure)}"
      )
      await ctx.send(embed=embed)
      users[str(user.id)]["wallet"]+=treasure
    else:
      await self.death(ctx.author)
      embed=discord.Embed(
        title="You were greatly injured!",
        description="You paid a lot of money"
      )
      embed.set_footer(text="If you have insurance you don't need to pay!")
      await ctx.send(embed=embed)
  
  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command(aliases=["give"])
  async def share(self, ctx,member:discord.Member,message:Union[CapitalismConverter, str]):
    if type(message) == int:
      message = str(int(message))
    if await self.profile_detect(ctx):
      return
    if not str(member.id) in self.maindb.keys():
      await ctx.send("He never registered.")
      return
    if ctx.author.id == member.id:
      await ctx.send("Capitalism is too lazy to transfer your own money to yourself")
      return
    else:
      pass
    user=ctx.author
    users = self.maindb
    other=member
    wallet_amt=users[str(user.id)]["wallet"]
    share_amt=0
    pog=True if users[str(user.id)]["badges"]["Pog"] > 0 else False
    if not message.lower() == "max" and not message.lower() == "all":
      try:
        share_amt=int(message)
      except:
        await ctx.send("that's not a valid input!")
        return
    elif message.lower() == "max" or message.lower() == "all":
      share_amt=users[str(user.id)]["wallet"]
    if share_amt > 0:
      if not share_amt>wallet_amt:
        if not pog:
          users[str(user.id)]["wallet"]-=share_amt
          users[str(other.id)]["wallet"]+=round(share_amt*0.85)
          embed=discord.Embed(
            title="Transcation Successful!",
            description=f"You gave {member} {pint(round(share_amt*0.85))} CTC after a 15% tax rate."
          )
          embed.set_footer(text="You lost: {:,}".format(share_amt))
          await ctx.send(embed=embed)
        else:
          users[str(user.id)]["wallet"]-=share_amt
          users[str(other.id)]["wallet"]+=share_amt
          embed=discord.Embed(
            title="Transcation Successful!",
            description=f"You gave {member} {pint(share_amt)} CTC. You're pog so you get NO TAX."
          )
          embed.set_footer(text="You lost: {:,}".format(share_amt))
          await ctx.send(embed=embed)
      else:
        await ctx.send("You do not have that much amount in your wallet")
    else:
      await ctx.send("You cannot share negative amount of coins.")
  
  @discord.ext.commands.cooldown(1, 10, commands.BucketType.user)
  @commands.command(aliases=["rich","leaderboard"])
  async def lb(self, ctx):
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    rich = []
    for user in users.keys():
      # if int(user) in ctx.guild.members:
        rich.append({"user_id":int(user), "balance":users[user]["wallet"]})
    def sort_(e):
      return e["balance"]
    rich.sort(key=sort_, reverse=True)
    index = 0
    stuff = ""
    for i in range(10):
      user = rich[index]
      try:
        name = await self.bot.fetch_user(user["user_id"])
        username = name.name
      except:
        username = "Clyde#0000"
      balance = user["balance"]
      stuff+=f"`{username}` - {balance:,}\n"
      index+=1
    em = discord.Embed(
      title="Top 10 riches people",
      description=stuff
    )
    await ctx.send(embed=em)

  # @discord.ext.commands.cooldown(1, 10, commands.BucketType.user)
  # @commands.command()
  # async def lba(self, ctx):
  #   await self.open_account(ctx.author)
  #   users = await get_bank_data()
  #   rich = []
  #   for user in users.keys():
  #     # if int(user) in ctx.guild.members:
  #       if user == "_id":
  #         continue
  #       rich.append({"user_id":int(user), "balance":users[user]["wallet"]})
  #   def sort_(e):
  #     return e["balance"]
  #   rich.sort(key=sort_, reverse=True)
  #   index = 0
  #   stuff = ""
  #   for i in range(20):
  #     user = rich[index]
  #     name = await self.bot.fetch_user(user["user_id"])
  #     username = name.name
  #     balance = user["balance"]
  #     stuff+=f"`{username}` - {balance}\n"
  #     index+=1
  #   em = discord.Embed(
  #     title="Top 20 riches people",
  #     description=stuff
  #   )
  #   index = 20
  #   stuff2 = ""
  #   for i in range(20):
  #     user = rich[index]
  #     name = await self.bot.fetch_user(user["user_id"])
  #     username = name.name
  #     balance = user["balance"]
  #     stuff2+=f"`{username}` - {balance}\n"
  #     index+=1
  #   em2 = discord.Embed(
  #     title="More 20 riches people",
  #     description=stuff2
  #   )
  #   await ctx.send(embed=em)
  #   await ctx.send(embed=em2)

  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command()
  async def gift(self, ctx,member:discord.Member,message,amount=1):
    if await self.profile_detect(ctx):
      return
    if not str(member.id) in self.maindb.keys():
      await ctx.send("He never registered.")
      return
    if int(amount) < 1:
      embed=discord.Embed(
        title="You cannot send someone no-amount of an item!"
      )
      await ctx.send(embed=embed)
      return
    user=ctx.author
    users = self.maindb
    other=member
    if other.id == ctx.author.id:
      embed=discord.Embed(
        title="You cannot give yourself stuff!",
        description="you already own them smh"
      )
      await ctx.send(embed=embed)
      return
    n=message.lower()
    name_=None
    for key in shop_items.keys():
      names=shop_items[key]["name"]
      if n in names:
        name_=key
        break
    if name_ == None:
      embed=discord.Embed(
        title="That item doesn't exist!",
        description="Check our shop for all the items!"
      )
      await ctx.send(embed=embed)
    for item, amt in users[str(user.id)]["inventory"].items():
      n_=item.lower()
      if name_==n_:
        old_amt = amt
        new_amt = int(old_amt)-amount
        for item2, amt2 in users[str(other.id)]["inventory"].items():
          n_2=item2.lower()
          if n_ == n_2:
            old_amt_2 = amt2
            new_amt_2 = int(old_amt_2)+amount
            if old_amt >= int(amount):
              users[str(user.id)]["inventory"][n_]=new_amt
              users[str(other.id)]["inventory"][n_]=new_amt_2
              embed=discord.Embed(
                title="Gifting Transfer Successful",
                description=f"You gave {member} {amount} {name_}!"
              )
              await ctx.send(embed=embed)
              break
            else:
              embed=discord.Embed(title="You do not have enough amount of that item!")
              await ctx.send(embed=embed)

  @commands.command(hidden=True)
  async def gib(self, ctx,member:discord.Member,message):
    if ctx.author.id == 763854419484999722:
      if await self.profile_detect(ctx):
        return
      if not str(member.id) in self.maindb.keys():
        await ctx.send("He never registered.")
        return
      users = self.maindb
      other=member
      users[str(other.id)]["wallet"]+=int(message)
      await ctx.send(f"You added  {member} {message} CTC.")
    else:
      await ctx.send("This command is creator only.")
  
  @commands.command(hidden=True)
  async def badge(self, ctx,member:discord.Member,message):
    if ctx.author.id == 763854419484999722:
      if await self.profile_detect(ctx):
        return
      if not str(member.id) in self.maindb.keys():
        await ctx.send("He never registered.")
        return
      users = self.maindb
      other=member
      badge_item_keys = [i.lower() for i in badge_items.keys()]
      if message.lower() in badge_item_keys:
        items = [key for key in badge_items.keys()]
        item=items[badge_item_keys.index(message.lower())]
        users[str(other.id)]["badges"][item]=1
      else:
        item = None
      await ctx.send(f"You gave {member} {item} badge.")
    else:
      await ctx.send("This command is creator only.")

  @commands.command(hidden=True)
  async def removebadge(self, ctx,member:discord.Member,message):
    if ctx.author.id == 763854419484999722:
      if await self.profile_detect(ctx):
        return
      if not str(member.id) in self.maindb.keys():
        await ctx.send("He never registered")
        return
      users = self.maindb
      other=member
      badge_item_keys = [i.lower() for i in badge_items.keys()]
      if message.lower() in badge_item_keys:
        items = [key for key in badge_items.keys()]
        item=items[badge_item_keys.index(message.lower())]
        users[str(other.id)]["badges"][item]=1
      else:
        item = None
      await ctx.send(f"You removed  {member} {item} badge.")
    else:
      await ctx.send("This command is creator only.")

  @commands.command(hidden=True)
  async def remove(self, ctx,member:discord.Member,message):
    if ctx.author.id == 763854419484999722:
      if await self.profile_detect(ctx):
        return
      if not str(member.id) in self.maindb.keys():
        await ctx.send("He never registered")
        return
      users = self.maindb
      other=member
      users[str(other.id)]["wallet"]-=int(message)
      await ctx.send(f"You removed {member} {pint(message)} CTC.")
    else:
      await ctx.send("This command is creator only.")
  
  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=["gamble","bet"])
  async def roll(self, ctx, message:Union[CapitalismConverter, str]):
    if type(message)==int:
      message = str(int(message))
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    user = ctx.author
    wallet_amt=users[str(user.id)]["wallet"]
    gamble_amt=0
    if message.lower() == "max" or message.lower() == "all":
      if wallet_amt >= 500:
        gamble_amt = 500
      else:
        if gamble_amt <= 14:
          await ctx.send("Seems like you don't have 15$ or more in your wallet. haha poor")
          return
        else:
          gamble_amt=wallet_amt
    else:
      try:
        gamble_amt=int(message)
        if gamble_amt <= 14:
          await ctx.send("You must gamble 15 dollars or more. haha have fun")
          return
      except:
        await ctx.send("You can't gamble that 🤔")
        return
    if not int(wallet_amt) < int(gamble_amt):
      if not gamble_amt > 500:
          roll1=random.randrange(1,13)
          roll2=random.randrange(1,13)
          exp = users[str(user.id)]["exp"]
          level = int(exp / 100)
          if level > 999:
              level = 1000
          level_multi = int(level / 50)
          multi = users[str(user.id)]["multi"] + level_multi
          if multi > 99:
            multi = 100
          random_amt = random.randint(round(gamble_amt / 3), round(gamble_amt/2))
          win_amt = round(random_amt * (0.5+multi / 100))
          if roll1 > roll2:
            users[str(user.id)]["wallet"]+=int(win_amt)
            em=discord.Embed(
              title="You won.",
              description='Profit: {:,}'.format(int(win_amt)),
              color=discord.Color.green()
            )
            em.add_field(
              name="You",
              value=f"Rolled `{roll1}`"
            )
            em.add_field(
              name="Capitalism",
              value=f"Rolled `{roll2}`"
            )
            await ctx.send(embed=em)
          elif roll2>roll1:
            users[str(user.id)]["wallet"]-=int(gamble_amt*0.5)
            em=discord.Embed(
              title="You lost.",
              description='Loss: {:,}'.format(int(gamble_amt*0.5)),
              color=discord.Color.red()
            )
            em.add_field(
              name="You",
              value=f"Rolled `{roll1}`"
            )
            em.add_field(
              name="Capitalism",
              value=f"Rolled `{roll2}`"
            )
            await ctx.send(embed=em)
          else:
            users[str(user.id)]["wallet"]+=1
            em=discord.Embed(
              title="You tied!",
              description="You won 1 coin!"
            )
            em.add_field(
              name="You",
              value=f"Rolled `{roll1}`"
            )
            em.add_field(
              name="Capitalism",
              value=f"Rolled `{roll2}`"
            )
            await ctx.send(embed=em)
      else:
        await ctx.send("You cannot gamble more than 500 coins!")
    else:
      await ctx.send("You do not have that much money in your wallet.")
  
  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=["roul"])
  async def roulette(self, ctx, message:Union[CapitalismConverter, str], message2):
    if type(message) == int:
      message = str(int(message))
    if await self.profile_detect(ctx):
      return
    user=ctx.author
    users = self.maindb
    wallet_amt=users[str(user.id)]["wallet"]
    try:
      bet_number=int(message2)
    except:
      await ctx.send(f"Roulette example: `{ctx.prefix}roul 1000 1`")
      ctx.command.reset_cooldown(ctx)
      return
    if int(bet_number) > 12:
      await ctx.send("Don't bet bigger than 12!")
      return
    if not message.lower() == "max" and not message.lower() == "all":
      try:
        gamble_amt=int(message)
        if gamble_amt <= 19:
          await ctx.send("You must gamble at least 20 coins.")
          return
      except:
        await ctx.send("You can only gamble an amount of coins.")
        return
    elif message.lower() == "max" or message.lower() == "all":
      if wallet_amt >= 250:
        gamble_amt=250
      elif wallet_amt <= 19:
        await ctx.send("You don't have 20 coins.")
        return
      else:
        gamble_amt=wallet_amt
    else:
      await ctx.send("Invalid Input Received.")
    even = False
    odd = False
    even1 = False
    odd1 = False
    if (int(bet_number) % 2) == 0:
      even = True
    else:
      odd = True
    if not int(wallet_amt) < int(gamble_amt):
      if not int(gamble_amt) > 250:
        if not int(gamble_amt) <1:
          win_number=random.randrange(0,12)
          if (win_number % 2) == 0:
            even1=True
          else:
            odd1=True
          if win_number == int(bet_number):
            if win_number == 0:
              users[str(user.id)]["wallet"]+=int(gamble_amt*0.5)
              em=discord.Embed(
                title="You won! The win number is 0!",
                description='Profit: {:,}'.format(int(gamble_amt*0.5)),
                color=discord.Color.green()
              )
              em.add_field(
                name="Results:",
                value=f"Your bet: `{bet_number}`. Win number: `{win_number}`"
              )
              em.set_footer(
                text="Roulette will pick a random number between 0 and 12."
              )
              await ctx.send(embed=em)
            else:
              users[str(user.id)]["wallet"]+=int(gamble_amt*0.2)
              em=discord.Embed(
                title="You won! Your bet number equals the win number!",
                description=f"Profit: {int(gamble_amt*0.2)}",
                color=discord.Color.green()
              )
              em.add_field(
                name="Results:",
                value=f"Your bet: `{bet_number}`. Win number: `{win_number}`"
              )
              em.set_footer(
                text="Roulette will pick a random number between 0 and 12."
              )
              await ctx.send(embed=em)
          elif even and even1 or odd and odd1 and not int(bet_number) == 0:
            users[str(user.id)]["wallet"]+=int(gamble_amt*0.1)
            em=discord.Embed(
              title="You won! They're the same color",
              description=f"Profit: {int(gamble_amt*0.1)}",
              color=discord.Color.green()
            )
            em.add_field(
              name="Results:",
              value=f"Your bet: `{bet_number}`. Win number: `{win_number}`"
            )
            em.set_footer(
              text="Roulette will pick a random number between 0 and 12."
            )
            await ctx.send(embed=em)
          else:
            users[str(user.id)]["wallet"]-=int(gamble_amt*0.2)
            em=discord.Embed(
              title="You lost.",
              description=f"Loss: {int(gamble_amt*0.2)}",
              color=discord.Color.red()
            )
            em.add_field(
              name="Results:",
              value=f"Your bet: `{bet_number}`. Win number: `{win_number}`"
            )
            em.set_footer(
              text="Roulette will pick a random number between 0 and 12, if you bet anything higher than 12, you're kinda dumb"
            )
            await ctx.send(embed=em)
        else:
            await ctx.send("your number cannot be lower than 1.")
      else:
        await ctx.send("You cannot roulette more than 250 coins")
    else:
      await ctx.send('You do not have that much money in your wallet.')
    
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def shop(self, ctx, message:Optional[Union[int, str]]=None):
    if message==None or isinstance(message, int):
      em=discord.Embed(
        title="CTC SHOP",
        color=discord.Color.red()
      )
      page=1 if not isinstance(message, int) else message
      amt_ = 0
      amnt = 0
      for key in shop_items.keys():
        val = shop_items[key]["showing"]
        if val==False:
          continue
        amnt+=1
      page_total=amnt/5
      if not page_total==int(page_total):
        page_total = int(page_total)+1
      else:
        page_total = int(page_total)
      if page > page_total:
        await ctx.send("that page doesn't exist!")
        return
      for key in shop_items.keys():
        val = shop_items[key]["showing"]
        if val==False:
          continue
        amt_+=1
        if amt_ > page*5:
          break
        if amt_ <= page*5-5:
          continue
        name=shop_items[key]["display"]
        price=shop_items[key]["price"]
        desc=shop_items[key]["description"]
        em.add_field(name=name, value=f"${price} | {desc}", inline=False)
      em.set_footer(text="page {} of {}".format(page, page_total))
      await ctx.send(embed=em)
    else:
      item=None
      t=0
      for thing in shop_items.keys():
        names = shop_items[thing]["name"]
        msg = message.lower()
        if msg in names:
          t+=1
          item = thing
          break
      if t == 0:
        await ctx.send("That item doesn't exist what are you doing")
      else:
        em=discord.Embed(
          title = shop_items[item]["display"],
          description = shop_items[item]["description"],
          color = discord.Color.red()
        )
        em.set_thumbnail(
            url = shop_items[item]["thumbnail"]
        )
        em.add_field(
          name = "Price",
          value = shop_items[item]["price"]
        )
        em.add_field(
          name = "Showing in shop",
          value = shop_items[item]["showing"],
        )
        em.add_field(
          name= "Purchasable",
          value = shop_items[item]["purchasable"],
          inline=False
        )
        em.add_field(
          name= "Sellable",
          value = "{} \n__Note:__ sell price is half".format(shop_items[item]["sellable"]),
          inline=False
        )
        em.add_field(
          name= "Usable",
          value = shop_items[item]["usable"]
        )
        ids_ = str(shop_items[item]["name"]).lstrip("[").rstrip("]")
        em.add_field(
          name="IDs for buy/sell/use/shop",
          value=f"`{ids_}`",
          inline=False
        )
        await ctx.send(embed=em)
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def buy(self, ctx, item, amount:Optional[Union[CapitalismConverter, str]]=1):
    if await self.profile_detect(ctx):
      return
    if isinstance(amount, str) or amount > 0:
      res= await self.buy_item(ctx.author,item, amount)
      if not res[0]:
        if res[1]==1:
          await ctx.send("that item isn't in the shop what are you doing")
          return
        if res[1]==2:
          await ctx.send("You do not have money lol.")
          return
      await ctx.send(f"You bought {amount} {res[1]}")
    else:
      await ctx.send("You cannot buy negative amount of an item.")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def use(self, ctx, item,amount:Optional[Union[CapitalismConverter, str, None]]=None):
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    if item == "bank_space" and users[str(ctx.author.id)]["bank_color"]==None:
      await ctx.send("You cannot get more bankspace with default bank!")
      return
    res= await self.use_item(ctx.author,item,amount)
    if not res[0]:
        if res[1]==1:
          await ctx.send("that item doesn't exist in your inventory what are you doing")
          return
        if res[1]==2:
          await ctx.send("You do not have that amount of that item bruh")
          return
        if res[1]==3:
          await ctx.send("You do not have that item bruh")
          return
        if res[1]==4:
          await ctx.send("You cannot use that item.")
          return
        if res[1]==5:
          await ctx.send("dude that's an invalid input for amount")
          return
    if res[1] =="curse":
      await ctx.send("Who do you want to curse? You have one minute to respond. (you have to post their user id (don't ping them)and remember it's 40% fail)")
      def check(author):
        def inner_check(message):
          if message.author != author:
            return False
          try:
            int(message.content)
            return True
          except ValueError:
            return False
        return inner_check
      user = ctx.author
      await self.open_account(user)
      try:
        msg = await self.bot.wait_for('message', timeout=60, check = check(ctx.author))
        response = msg.content
      except asyncio.TimeoutError:
        await ctx.send("Imagine not answering in time")
        return
      try:
        other_user = await self.bot.fetch_user(response)
      except:
        await ctx.send("The member was invalid!")
      await self.open_account(other_user)
      success = random.randint(1,100)
      if success > 59:
        await self.add_multi(ctx.author,-5)
        response = "yourself"
        who = "author"
      else:
        await self.add_multi(other_user, -5)
        response = other_user.name
        who = "user"
      await ctx.send(f"You cursed {response} with -5 multiplier.")
      await asyncio.sleep(1800)
      if who == "author":
        await self.add_multi(ctx.author,5)
      elif who == "user":
        await self.add_multi(other_user,5)
      return True
    if not res[4]:
      await ctx.send(f"You used {res[3]} {res[1]}, and {res[2]}")
    else:
      await self.add_multi(ctx.author,res[4])
      await ctx.send(f"You used {res[3]} {res[1]}, and {res[2]}")
      await asyncio.sleep(int(res[5])*60)
      negative = int(int(res[4])*-1)
      await self.add_multi(ctx.author,negative)
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def sell(self, ctx, item, amount:Optional[Union[CapitalismConverter, str]]=1):
    if await self.profile_detect(ctx):
      return
    if amount > 0:
      res= await self.sell_item(ctx.author,item,amount)
      if not res[0]:
        if res[1]==1:
          await ctx.send("that item isn't sellable what are you doing")
          return
        if res[1]==2:
          await ctx.send("You do not have that amount of that item lol.")
          return
        if res[1]==3:
          await ctx.send("You do not have that item lol.")
          return
      await ctx.send(f"You sold {amount} {res[1]}")
    else:
      await ctx.send("You cannot sell negative amount of items.")

  async def buy_item(self, user,item_name,amount):
    item_name = item_name.lower()
    name_=None
    for key in shop_items.keys():
      names=shop_items[key]["name"]
      buyable=shop_items[key]["purchasable"]
      if item_name in names:
        if buyable == False:
          return [False,1]
        name_=key
        price=shop_items[key]["price"]
        break
    if name_ == None:
      return [False,1]
    cost = int(price)*amount
    users = self.maindb
    bal=await self.update_bal(user)
    if bal[0]<cost:
      return [False, 2]
    index=0
    for thing, amt in users[str(user.id)]["inventory"].items():
      n=thing
      if n ==name_:
        old_amt=int(amt)
        new_amt=old_amt+amount
        users[str(user.id)]["inventory"][n]=new_amt
        break
      index+=1
    await self.update_bal(user,cost*-1,"wallet")
    return[True, name_]
  
  async def sell_item(self, user,item_name,amount, price=None):
    item_name = item_name.lower()
    name_=None
    for item in shop_items.keys():
      names=shop_items[item]["name"]
      sellable = shop_items[item]["sellable"]
      price_ = shop_items[item]["price"]
      if item_name in names:
        if sellable == False:
          return [False,1]
        name_=item
        if price==None:
          price=0.5*int(price_)
        break
    if name_ == None:
      return [False,1]
    cost = price*amount
    users = self.maindb
    try:
      index=0
      t=None
      for item, amt in users[str(user.id)]["inventory"].items():
        n=item
        if n ==name_:
          old_amt=amt
          new_amt=old_amt-amount
          if new_amt<0:
            return [False,2]
          users[str(user.id)]["inventory"][n]=new_amt
          t=1
          break
        index+=1
      if t ==None:
        return [False,3]
    except:
      return [False, 3]
    await self.update_bal(user,int(cost),"wallet")
    return[True, name_]

  async def use_item(self, user,item_name,amount,price=None):
      users = self.maindb
      itemname = item_name.lower()
      name_=None
      amnt=0
      for item in shop_items.keys():
        names=shop_items[item]["name"]
        if itemname in names:
          itemname=item
      inv = users[str(user.id)]["inventory"]
      for item, amt in inv.items():
        name=item
        if name ==itemname:
          if shop_items[itemname]["usable"]==False:
            return [False,4]
          name_=name
      if name_ == None:
        return [False,1]
      try:
        index=0
        t=None
        for thing, amt in users[str(user.id)]["inventory"].items():
          n=thing
          if n ==itemname:
            old_amt=amt
            if not itemname == "cursed_beef":
              if itemname == "beef":
                if not amount == None:
                  if not amount.lower() == "max" and not amount.lower() == "all":
                    if int(amount) > 99:
                      amount=100
                    amnt = amount
                  elif amount.lower() == "max" or amount.lower() == "all":
                    if int(old_amt) > 99:
                      old_amt=100
                    amnt = old_amt
                  else:
                    return [False,5]
                else:
                  amnt = 1
                if int(amnt) + int(users[str(user.id)]["multi"]) > 100:
                  return [False, 5]
              elif itemname == "horrorse_celery":
                if not amount == None:
                  if not amount.lower() == "max" and not amount.lower() == "all":
                    if int(amount) > 0:
                      amount=1
                    amnt = amount
                  elif amount.lower() == "max" or amount.lower() == "all":
                    if int(old_amt) > 0:
                      old_amt=1
                    amnt = old_amt
                  else:
                    return [False,5]
                  if 100 + int(users[str(user.id)]["multi"]) > 150:
                    return [False, 5]
                else:
                  amnt=1
              elif not amount==None:
                if not amount.lower() == "max" and not amount.lower() == "all":
                  amnt = amount
                elif amount.lower() == "max" or amount.lower() == "all":
                  amnt = old_amt
                else:
                  return [False,5]
              else:
                amnt = 1
            else:
              amnt = 1
            new_amt=int(old_amt)-int(amnt)
            if int(amnt)<0:
              return [False,2]
            if new_amt<0:
              return [False,2]
            users[str(user.id)]["inventory"][n]=new_amt
            t=1
            break
          index+=1
        if t ==None:
          return [False, 3]
      except Exception as e:
        print(e)
        return [False, 3]
      result = await self.find_use(itemname)
      if not result == "unusable":
          if result == "bank":
            users = self.maindb
            increase_amount=int(random.randrange(10,20))*int(amnt)
            users[str(user.id)]["bank_max"]+=increase_amount
            return [True, itemname, f"{increase_amount} has been increased to your bank space!",amnt, False]
          elif result == "bag":
            users = self.maindb
            increase_amount=int(random.randrange(100,150))*int(amnt)
            users[str(user.id)]["wallet"]+=increase_amount
            return [True, itemname, f"You got {increase_amount} coins from the coin bag.", amnt, False]
          elif result == "beef":
            users = self.maindb
            return [True, itemname, f"You got {amnt} multiplier", amnt, amnt, 1]
          elif result == "curse":
            return [True, "curse"]
          elif result == "horse":
            return [True, itemname, f"You got 100% multiplier for 3 hours", 1, 100, 180]
      else:
          return [False,4]

  async def update_bal(self, user,change=0,mode="wallet"):
    users = self.maindb
    users[str(user.id)][mode]+=change
    bal = [users[str(user.id)]["wallet"],users[str(user.id)]["bank"]]
    return bal

  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command(aliases=["multiplier"])
  async def multi(self, ctx):
      if await self.profile_detect(ctx):
        return
      user=ctx.author
      users = self.maindb
      multi=users[str(user.id)]["multi"]
      em = discord.Embed(
          title = f"{user}'s Multipliers",
      )
      em.add_field(
          name = "Multiplier",
          value = multi
      )
      em.set_footer(
          text = "Eat beef or gain reputation to get multiplier"
      )
      await ctx.send(embed=em)
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command(aliases=["inventory"])
  async def inv(self, ctx, args:Optional[Union[discord.User, int]]=None, page:int=None):
    if await self.profile_detect(ctx):
      return
    if args == None:
      user = ctx.author
      users = self.maindb
      inv = users[str(user.id)]["inventory"]
      total_items = 0
      for inv_item, value in inv.items():
        if not value == 0:
          total_items+=1
      em=discord.Embed(
        title = f"`{ctx.author}'s inventory`"
      )
      page_total = total_items/5
      if not page_total==int(page_total):
        page_total = int(page_total)+1
      else:
        page_total = int(page_total)
      em.set_footer(text=f"page 1 of {page_total}")
      t=0
      items = 0
      for item_name, amount in inv.items():
        if items >= 5:
          break
        if amount == 0:
          continue
        t+=1
        display_name = shop_items[item_name]["display"]
        if len(shop_items[item_name]["name"])>2:
          names = "[`{}`, `{}`, `{}` ...]".format(shop_items[item_name]["name"][0], shop_items[item_name]["name"][1], shop_items[item_name]["name"][2])
        elif len(shop_items[item_name]["name"])==2:
          names="[`{}`, `{}`]".format(shop_items[item_name]["name"][0], shop_items[item_name]["name"][1])
        else:
          names="[`{}`]".format(shop_items[item_name]["name"][0])
        names = str(names).lstrip("[").rstrip("]")
        em.add_field(
          name=f"{display_name} ─ {amount:,} owned",
          value=f"*ID* {names}",
          inline=False
        )
        items+=1
      if not t == 0:
        await ctx.send(embed=em)
        return
      else:
        await ctx.send("you're too poor to have anything")
        return
    elif type(args) == int:
      page = int(args)
      user = ctx.author
    else:
      if not page == None:
        page = int(page)
      else:
        page = 1
      user = args
      if not str(user.id) in self.maindb.keys():
        await ctx.send("He never registered.")
        return
    users = self.maindb
    inv = users[str(user.id)]["inventory"]
    total_items = 0
    for inv_item, amount in inv.items():
      if not amount == 0:
        total_items+=1
    em=discord.Embed(
      title = f"`{user}'s inventory`"
    )
    page_total = total_items/5
    if not page_total==int(page_total):
      page_total = int(page_total)+1
    else:
      page_total = int(page_total)
    em.set_footer(text=f'page {page} of {page_total}')
    t=0
    items = 0
    for item_name, amount in inv.items():
      if amount == 0:
        continue
      if (page-1)*5 > items:
        items+=1
        continue
      display_name = shop_items[item_name]["display"]
      if len(shop_items[item_name]["name"])>2:
        names = "[`{}`, `{}`, `{}` ...]".format(shop_items[item_name]["name"][0], shop_items[item_name]["name"][1], shop_items[item_name]["name"][2])
      elif len(shop_items[item_name]["name"])==2:
        names="[`{}`, `{}`]".format(shop_items[item_name]["name"][0], shop_items[item_name]["name"][1])
      else:
        names="[`{}`]".format(shop_items[item_name]["name"][0])
      names = str(names).lstrip("[").rstrip("]")
      em.add_field(
        name=f"{display_name} ─ {amount} owned",
        value=f"*ID* {names}",
        inline=False
      )
      t=1
      items+=1
      if items / page == 5:
        break
    if not t == 0:
      await ctx.send(embed=em)
    elif items == 0:
      await ctx.send(f"{user} is too poor to have anything")
    else:
      await ctx.send("That page cannot be reached")

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command(aliases=["dep"])
  async def deposit(self, ctx, message):
      if await self.profile_detect(ctx):
        return
      user=ctx.author
      users = self.maindb
      wallet_amt=users[str(user.id)]["wallet"]
      bank_amt=users[str(user.id)]["bank"]
      bank_max=users[str(user.id)]["bank_max"]
      bank_left = bank_max-bank_amt
      deposit_number = 0
      if not message.lower() == "max" and not message.lower() == "all":
        try:
          deposit_number = int(message)
        except:
          await ctx.send("Bruh that's not a valid input")
          ctx.command.reset_cooldown(ctx)
          return
      elif message.lower() == "max" or message.lower() == "all":
        if wallet_amt > bank_left:
          deposit_number = bank_left
        else:
          deposit_number = wallet_amt
      if users[str(user.id)]["bank_color"] == "red":
        if deposit_number > 200:
          deposit_number = 200
      elif users[str(user.id)]["bank_color"] == "purple":
        if deposit_number < 2500:
          await ctx.send("You cannot deposit less than 2500 coins with Royal Bank.")
          return
      elif users[str(user.id)]["bank_color"] == "white":
        deposit_number = round(deposit_number/2)
      if deposit_number > 0:
        if not int(wallet_amt) < deposit_number:
          if int(bank_max)-int(bank_amt)>=deposit_number:
            users[str(user.id)]["wallet"]-=deposit_number
            if users[str(user.id)]["bank_color"] == "green":
              if random.randint(1,100) > 94:
                await ctx.send("memers just stole your money! RIP.")
              else:
                users[str(user.id)]["bank"]+=deposit_number
            else:
              users[str(user.id)]["bank"]+=deposit_number
            if users[str(user.id)]["bank_color"] == "green":
              users[str(user.id)]["bank"]+=deposit_number*0.5
            await ctx.send(f"{deposit_number} deposited.")
            return True
          else:
            await ctx.send("You cannot hold that much money.")
        else:
          await ctx.send("You do not have that much money inside your wallet.")
      else:
        await ctx.send("You cannot deposit no coins.")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command(aliases=["with"])
  async def withdraw(self, ctx, message):
      if await self.profile_detect(ctx):
        return
      user=ctx.author
      users = self.maindb
      bank_amt=users[str(user.id)]["bank"]
      withdraw_number = 0
      if not message.lower() == "max" and not message.lower() == "all":
        withdraw_number = int(message)
      elif message.lower() == "max" or message.lower() == "all":
        withdraw_number = bank_amt
      else:
        await ctx.send("that's not a valid input lmao")
      if withdraw_number >0:
        if not int(bank_amt) < withdraw_number:
          users[str(user.id)]["wallet"]+=withdraw_number
          users[str(user.id)]["bank"]-=withdraw_number
          await ctx.send(f"{withdraw_number} withdrawed.")
          return True
        else:
          await ctx.send("You do not have that much money inside your bank.")
      else:
        await ctx.send("You cannot withdraw no amount of money.")
  
  @discord.ext.commands.cooldown(1,1,commands.BucketType.user)
  @commands.command()
  async def vote(self, ctx):
      em = discord.Embed(
          title = "Capitalism Vote Rewards",
          description = "Reward Claims are automatic"
      )
      em.add_field(
          name = "Discord Bot List",
          value = "https://discordbotlist.com/bots/capitalism\n **The Reward: Coin_Bag x1**",
          inline=False
      )
      em.add_field(
          name="Top.gg",
          value = "https://top.gg/bot/823699570147065876/vote\n **The Reward: Coin_Bag x1**\n\nVoting Top.gg on weekends for DOUBLE REWARDS!"
      )
      view = discord.ui.View()
      view.add_item(
        discord.ui.Button(
          style=discord.ButtonStyle.link,
          label="DiscordBotList",
          url="https://discordbotlist.com/bots/capitalism/upvote"
        )
      )
      view.add_item(
        discord.ui.Button(
          style=discord.ButtonStyle.link,
          label="Top.gg",
          url="https://top.gg/bot/823699570147065876/vote"
        )
      )
      await ctx.send(embed=em, 
      view=view)
  
  @discord.ext.commands.cooldown(1,5, commands.BucketType.user)
  @commands.command()
  async def profile(self, ctx,member:discord.Member=None):
    if member==None:
      if await self.profile_detect(ctx):
        return
      user = ctx.author
    else:
      if str(member.id) not in self.maindb.keys():
        await ctx.send("He never registered.")
        return
      user = member
    users = self.maindb
    data = self.usersdb
    exp = users[str(user.id)]["exp"]
    level = int(exp/100)
    if level > 999:
        level = 1000
    level_multi =int(level/50)
    multi = users[str(user.id)]["multi"]+level_multi
    badges = users[str(user.id)]["badges"]
    badge_amt=0
    for thing, amt in badges.items():
        if amt ==1:
          badge_amt+=1
    if multi > 99:
        users[str(user.id)]["multi"] = 100
    embed=discord.Embed(
      title=f"{user}'s Profile",
      color=discord.Color.red()
    )
    embed.add_field(
        name="Badge count",
        value=f"{badge_amt} (Use {ctx.prefix}badges to check badges)",
        inline=False
    )
    embed.add_field(
      name="Level",
      value=level
    )
    embed.add_field(
      name="Experience",
      value="{:,}".format(exp)
    )
    embed.add_field(
      name="Multi",
      value=multi
    )
    try:
      embed.add_field(
        name='Commands Issued',
        value="{:,}".format(data[str(user.id)]["commands"]),
        inline=False
      )
    except:
      embed.add_field(
        name='Commands Issued',
        value="N/A",
        inline=False
      )
    embed.set_footer(
      text="exp can be gained through using commands"
    )
    await ctx.send(embed=embed)
  
  @commands.command()
  async def badges(self, ctx):
      if await self.profile_detect(ctx):
        return
      users = self.maindb
      user = ctx.author
      em = discord.Embed(
          title = f"{ctx.author}'s Badges"
      )
      for item,amt in users[str(user.id)]["badges"].items():
          if amt ==0:
              continue
          for thing in badge_items.keys():
              if thing == item:
                  description = badge_items[thing]["description"]
                  emoji = badge_items[thing]["thumbnail"]
                  em.add_field(name=emoji+item, value=description,inline=False)
                  continue
      await ctx.send(embed=em)
  
  async def get_bank_color(self, arg):
    if arg == None:
      color = discord.Color.default()
    elif arg == "red":
      color = discord.Color.red()
    elif arg == "purple":
      color = discord.Color.purple()
    elif arg == "green":
      color = discord.Color.green()
    elif arg == "white":
      color = discord.Color.gold()
    return color
  
  async def get_bank_name(self, arg):
    if arg == None:
      color = "Default"
    elif arg == "red":
      color = "Premium"
    elif arg == "purple":
      color = "Royal"
    elif arg == "green":
      color = "Meme"
    elif arg == "white":
      color = "USSR"
    return color

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def banks(self, ctx, arg=None):
    if arg == None:
      embed = discord.Embed(
        title="Banks",
        description="`default`, `premium`, `royal`, `meme`, `USSR`"
      )
      await ctx.send(embed=embed)
    elif arg.lower() == "default":
      embed = discord.Embed(
        title="Default bank",
        description="Free of charge but you cannot get more space."
      )
      await ctx.send(embed=embed)
    elif arg.lower() == "premium":
      embed = discord.Embed(
        title="Premium Bank",
        description="Pay 5,000 to unlock. Every deposit will me lower than 200."
      )
      await ctx.send(embed=embed)
    elif arg.lower() == "royal":
      embed = discord.Embed(
        title="Royal Bank",
        description="Pay 25,000 to unlock. Every deposit and withdraw must be higher than 2500"
      )
      await ctx.send(embed=embed)
    elif arg.lower() == "meme":
      embed = discord.Embed(
        title="Meme Bank",
        description="Pay 20,000 to unlock. Every deposit there's a 5% chance you will get trolled and lose those money"
      )
      await ctx.send(embed=embed)
    elif arg.lower() == "ussr":
      embed = discord.Embed(
        title="USSR Bank",
        description="Free of charge, but you share half of your money each deposit"
      )
      await ctx.send(embed=embed)

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def buybank(self, ctx, arg):
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    user = ctx.author
    if arg.lower() == "premium":
      if users[str(user.id)]["bank_color"]=="red":
        await ctx.send("You already have this bank!")
      if users[str(user.id)]["wallet"] >= 5000:
        users[str(user.id)]["wallet"]-=5000
        users[str(user.id)]["bank_color"]="red"
        await ctx.send("You applied for premium bank with 5000 coins!")
      else:
        await ctx.send("You dont have enough money you need 5000")
        return
    elif arg.lower() == "royal":
      if users[str(user.id)]["bank_color"]=="purple":
        await ctx.send("You already have this bank!")
      if users[str(user.id)]["wallet"] >= 25000:
        users[str(user.id)]["wallet"]-=25000
        users[str(user.id)]["bank_color"]="purple"
        await ctx.send("You applied for royal bank with 25000 coins!")
      else:
        await ctx.send("You dont have enough money you need 25000")
        return
    elif arg.lower() == "meme":
      if users[str(user.id)]["bank_color"]=="green":
        await ctx.send("You already have this bank!")
      if users[str(user.id)]["wallet"] >= 2000:
        users[str(user.id)]["wallet"]-=20000
        users[str(user.id)]["bank_color"]="green"
        await ctx.send("You applied for meme bank with 20000 coins!")
      else:
        await ctx.send("You dont have enough money you need 20000")
        return
    elif arg.lower() == "ussr":
      if users[str(user.id)]["bank_color"]=="white":
        await ctx.send("You already have this bank!")
      if users[str(user.id)]["wallet"] >= 1:
        users[str(user.id)]["bank_color"]="white"
        await ctx.send("You applied for USSR bank with 0 coins!")
      else:
        await ctx.send("You need at least 1 coin to become a comrade")
        return
    else:
      await ctx.send("That is not a purchasable bank bro!")
      ctx.command.reset_cooldown(ctx)
      return

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def bank(self, ctx, arg=None):
    if await self.profile_detect(ctx):
      return
    user=ctx.author
    users = self.maindb
    if arg == None:
      try:
        bank = users[str(user.id)]["bank"]
        bank_max = users[str(user.id)]["bank_max"]
        bank_color = users[str(user.id)]["bank_color"]
        bank_comp = await self.get_bank_name(bank_color)
        bank_color = await self.get_bank_color(bank_color)
        em = discord.Embed(
          title=f"{ctx.author}'s bank data",
          description=f"{bank} | {bank_max}\nBank Company: {bank_comp}",
          color = bank_color
        )
        em.set_footer(text=f"Use {ctx.prefix}interest to get some more bank space!")
        await ctx.send(embed=em)
      except Exception as e:
        print(e)
    else:
      try:
        try:
          user = arg.split("!")
          user = user[1]
          user = user[:-1]
          user = await self.bot.fetch_user(int(user))
          bank = users[str(user.id)]["bank"]
          bank_max = users[str(user.id)]["bank_max"]
          em = discord.Embed(
            title=f"{user.name}'s bank data",
            description=f"{bank} | {bank_max}"
          )
          await ctx.send(embed=em)
        except:
          user = await self.bot.fetch_user(arg)
          bank = users[str(user.id)]["bank"]
          bank_max = users[str(user.id)]["bank_max"]
          em = discord.Embed(
            title=f"{user.name}'s bank data",
            description=f"{bank} | {bank_max}"
          )
          await ctx.send(embed=em)
      except:
        await ctx.send("That was not a valid user!")
  
  @discord.ext.commands.cooldown(1, 1800, commands.BucketType.user)
  @commands.command()
  async def interest(self, ctx):
    if await self.profile_detect(ctx):
      return
    users = self.maindb
    user = ctx.author
    if users[str(user.id)]["bank_color"]==None:
      await ctx.send("Your bank is the default bank! You cannot get bank interest.")
      return
    exp = users[str(user.id)]["exp"]
    level = int(exp / 100)
    if level > 999:
        level = 1000
    level_multi = int(level / 50)
    multi = users[str(user.id)]["multi"] + level_multi
    if multi > 99:
        multi = 100
    if users[str(user.id)]["bank"]>=10000:
      increase_amount=int(random.randrange(100,150)*(1+(int(multi/100))))
    else:
      await ctx.reply("You do not have enough money in your bank to apply for interest.", mention_author=False)
      ctx.command.reset_cooldown(ctx)
      return
    users[str(user.id)]["bank_max"]+=increase_amount
    await ctx.reply(f"{increase_amount} has been increased to your bank! Great job keeping up your reputation.", mention_author=False)

  @discord.ext.commands.cooldown(1, 60000, commands.BucketType.user)
  @commands.command()
  async def register(self,ctx):
    user = ctx.author
    users = self.maindb
    if str(user.id) in users.keys():
      await ctx.send("You already registered!")
      return
    users[str(user.id)]={}
    users[str(user.id)]["_id"]=str(user.id)
    users[str(user.id)]["wallet"]=0
    users[str(user.id)]["bank"]=0
    users[str(user.id)]["bank_max"]=5000
    users[str(user.id)]["inventory"]={key: 0 for (key, val) in shop_items.items()}
    users[str(user.id)]["bitcoin"]=0
    users[str(user.id)]["exp"]=0
    users[str(user.id)]["multi"]=0
    users[str(user.id)]["bank_color"]=None
    users[str(user.id)]["ads"]=1000
    users[str(user.id)]["job"]=None
    users[str(user.id)]["badges"]={key: 0 for (key, val) in badge_items.items()}
    await ctx.send(f"You are now registered! Check `{ctx.prefix}bal` for you balance!", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    return
  

  @commands.command()
  async def dm(self, ctx, member:discord.Member):
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    await ctx.send("What will be the message?")
    msg = await self.bot.wait_for('message', timeout=60.0, check=check)
    await member.send(f"{msg.content}\n\nSent by {ctx.author}")
    await ctx.send("message sent.")

  @commands.command()
  async def streak(self, ctx):
    try:
      if str(ctx.author.id) in self.db.keys():
        embed=discord.Embed(
          title="You already claimed your daily gift.",
          description="Try again on UTC 0:00"
        )
        await ctx.send(embed=embed)
      else:
        self.db[str(ctx.author.id)]=1
        if await self.profile_detect(ctx):
          return
        users = self.maindb
        random_num = random.randint(1,250)
        claimed = ""
        if random_num == 107:
          users[str(ctx.author.id)]["inventory"]["noob_trophy"]+=1
          claimed+="noob_trophy x1, "
        if random_num < 50:
          users[str(ctx.author.id)]["wallet"]+=100
          claimed+="100 coins, "
        elif random_num < 100:
          users[str(ctx.author.id)]["wallet"]+=50
          claimed+="50 coins, "
        if random_num > 200:
          users[str(ctx.author.id)]["inventory"]["capitalism_blessing"]+=1
          claimed+="capitalism_blessing x1, "
        if random_num > 99 and random_num < 201:
          users[str(ctx.author.id)]["inventory"]["beef"]+=1
          claimed+="beef x1, "
        else:
          users[str(ctx.author.id)]["wallet"]+=20
          claimed+="20 coins, "
        if random_num < 5:
          users[str(ctx.author.id)]["inventory"]["kirk_juice"]+=1
          claimed+="kirk_juice x1"
        embed=discord.Embed(
          title="You claimed:",
          description=f"{claimed} and air"
        )
        await ctx.send(embed=embed)
    except Exception as e:
      raise e


  async def death(self, user):
    users = self.maindb
    index=0
    for thing, amt in users[str(user.id)]["inventory"].items():
        n=thing
        if n == "capitalism_blessing":
          if users[str(user.id)]["inventory"]["puppy_true_gaymer_pass"] < 1:
            old_amt=amt
            if int(old_amt) > 0:
              new_amt=int(old_amt)-1
              users[str(user.id)]["inventory"][n]=new_amt
              break
            else:
              wallet_amt = users[str(user.id)]["wallet"]
              if not wallet_amt < 500:
                delete_amt = random.randint(100,500)
              else:
                delete_amt = wallet_amt
              users[str(user.id)]["wallet"]-=delete_amt
              break
          else:
            break
        index+=1
    return True

  async def find_use(self, item):
    if item in self.item_usable_list:
      if item == "bank_space":
        return "bank"
      elif item == "coin_bag":
        return "bag"
      elif item == "beef":
        return "beef"
      elif item == "cursed_beef":
        return "curse"
      elif item == "horrorse_celery":
        return "horse"
      else:
        return "unusable"
    else:
      return "unusable"
  
  async def add_multi(self, user, amount=1):
    users = self.maindb
    users[str(user.id)]["multi"]+=int(amount)
    multi = users[str(user.id)]["multi"]+int(amount)
    if multi > 99:
        users[str(user.id)]["multi"] = 100
    return True


def setup(bot):
  bot.add_cog(Currency(bot))