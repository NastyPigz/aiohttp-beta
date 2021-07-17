import discord, datetime
from discord.ext import commands
from other.mongo import cluster, func_bitcoin
from data.json.shop import shop_items
from data.json.badge import badge_items
import asyncio
import json

class StartUp(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.data = bot.data
    self.loop = asyncio.get_event_loop()
    self.hidden=True
  
  @commands.Cog.listener()
  async def on_ready(self):
    self.bot.loadng=True
    self.bot.remove_command("jsk")
    db = self.bot.maindb
    for id, document in db.items():
      if "_id" not in document:
        db[id]["_id"]=id
      if "wallet" not in document:
        db[id]["wallet"]=0
      if "bank" not in document:
        db[id]["bank"]=0
      if "bank_max" not in document:
        db[id]["bank_max"]=5000
      if "bank_color" not in document:
        db[id]["bank_color"]=None
      if "job" not in document:
        db[id]["job"]=None
      if "ads" not in document:
        db[id]["ads"]=1000
      if "exp" not in document:
        db[id]["exp"]=0
      if "bitcoin" not in document:
        db[id]["bitcoin"]=0
      db[id]["multi"]=0
      if "inventory" not in document:
        db[id]["inventory"]={key: 0 async for (key, val) in shop_items.items()}
      for item_name in shop_items.keys():
        if item_name not in db[id]["inventory"].keys():
          db[id]["inventory"][item_name] = 0
      if "badges" not in document:
        db[id]["badges"]={key: 0 async for (key, val) in badge_items.items()}
      for item_name in badge_items.keys():
        if item_name not in db[id]["badges"].keys():
            db[id]["badges"][item_name] = 0

    #discord.utils.wait_until() #the next minute but all seconds are 0, or do it inside func_bitcoin
    #maybe change some stuff in func_bitcoin, like put amount+=1 each api call
    await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("CAPhelp | c/help"))
    self.bot.loadng=False
    print("Running")
    self.bot.uptime=datetime.datetime.utcnow()
    await func_bitcoin(self)

  # async def setup(self):
  #   f1 = self.loop.create_task(func_bitcoin(self))
  #   f2 = self.loop.create_task(self.func_data())
  #   await asyncio.wait([f1, f2])

  # async def func_data(self):
  #   while True:
  #     with open("data/json/data.json", "w") as f:
  #       json.dump(self.data, f)
  #     await asyncio.sleep(1)

def setup(bot):
    bot.add_cog(StartUp(bot))