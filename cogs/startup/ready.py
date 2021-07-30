import discord, datetime, concurrent, subprocess
from discord.ext import commands
from other.mongo import cluster, func_bitcoin
from data.json.shop import shop_items
from data.json.badge import badge_items
import asyncio
from discord_slash.utils.manage_components import create_select, create_select_option
from discord_slash.utils import manage_components

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
    options=[]
    d = self.bot.cogs
    paginationList = [None]
    for key in d.keys():
      try:
        if d[key].hidden:
          continue
      except:
        continue
      paginationList.append(key.lower())
    for i in paginationList:
      if i is None:
        options.append(create_select_option(
          label="All", 
          value="All"
        ))
        continue
      options.append(create_select_option(
      label=i, 
      value=i
      ))
    select = create_select(options=options, min_values=1, max_values=1, custom_id="help_select")
    action_row3=manage_components.create_actionrow(select)
    self.bot.selector = action_row3
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
      if "degree" not in document:
        db[id]["degree"]=[]
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
    await self.bot.change_presence(status=discord.Status.idle, activity=discord.Game("CAPhelp | c/help"))
    self.bot.loadng=False
    print("Running")
    with open("afk/communicate.txt", "w") as f:
      f.write("")
    self.bot.uptime=datetime.datetime.utcnow()
    async def task1():
      with concurrent.futures.ThreadPoolExecutor() as pool:
        def run():
          subprocess.run("python afk/afk.py", shell=True)
        await self.bot.loop.run_in_executor(pool, run)
    await self.bot.loop.create_task(task1())
    await func_bitcoin(self)

def setup(bot):
    bot.add_cog(StartUp(bot))