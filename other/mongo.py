from pymongo import MongoClient
import random, asyncio
import discord, os
import copy
from discord.ext import commands, tasks
from dotenv import load_dotenv

def get_cluster():
  load_dotenv()
  cluster = MongoClient("mongodb+srv://cap:z67253635@clustercapitalism.wkr0p.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
  return cluster

cluster = get_cluster()

def setup(bot):
  bot.add_cog(Mongo(bot))

class Mongo(commands.Cog):
  def __init__(self, bot):
    self.db = cluster["CapBot"]
    self.hidden=True
    self.bot = bot
    self.maindb = bot.maindb
    self.logsdb = bot.logsdb
    self.usersdb = bot.usersdb
    self.botbanned = bot.botbanned
    self.bitcoin = bot.bitcoin
    self.amount = 0
    self.oldmain=copy.deepcopy(self.maindb)
    self.oldlogs=copy.deepcopy(self.logsdb)
    self.oldusers=copy.deepcopy(self.usersdb)
    self.oldbotb=copy.deepcopy(self.botbanned)
    self.oldbitcoin=copy.deepcopy(self.bitcoin)
    self.clear_intervals.start()
    self.mainr=False
    self.logsr=False
    self.banr=False
    self.usersr=False
    self.bitcoinr=False
    self.store_main.start()
    self.store_logs.start()
    self.store_ban.start()
    self.store_users.start()
    self.store_bitcoin.start()

  @tasks.loop(seconds=1.0)
  async def store_main(self):
    if self.bot.loadng:
      return
    if self.mainr:
      return
    if not self.oldmain == self.maindb:
      self.mainr=True
      collection = self.db["main"]
      value = {k: self.maindb[k] for k in self.maindb.keys() if k not in self.oldmain.keys() or self.maindb[k] != self.oldmain[k]}
      value2=copy.deepcopy(value)
      for id, document in value.items():
        self.amount+=1
        if self.amount > 99:
          self.oldmain.update({k: v for k, v in value2.items()})
          self.mainr=False
          return
        result = collection.find({})
        for doc in result:
          if doc["_id"] not in self.maindb.keys():
            self.amount+=1
            collection.delete_one(doc)
        self.amount+=1
        collection.replace_one({"_id":id}, document, upsert=True)
        value2.pop(id)
      self.oldmain = copy.deepcopy(self.maindb)
      self.mainr=False
  
  @tasks.loop(seconds=1.0)
  async def store_logs(self):
    if self.bot.loadng:
      return
    if self.logsr:
      return
    if not self.oldlogs == self.logsdb:
      self.logsr=True
      collection = self.db["logs"]
      value = {k: self.logsdb[k] for k in self.logsdb.keys() if k not in self.oldlogs.keys() or self.logsdb[k] != self.oldlogs[k]}
      value2=copy.deepcopy(value)
      for id, document in value.items():
        self.amount+=1
        if self.amount > 99:
          self.oldlogs.update({k: v for k, v in value2.items()})
          self.logsr=False
          return
        result = collection.find({})
        for doc in result:
          if doc["_id"] not in self.logsdb.keys():
            self.amount+=1
            collection.delete_one(doc)
        self.amount+=1
        collection.replace_one({"_id":id}, document, upsert=True)
        value2.pop(id)
      self.oldlogs = copy.deepcopy(self.logsdb)
      self.logsr=False
  
  @tasks.loop(seconds=1.0)
  async def store_ban(self):
    if self.bot.loadng:
      return
    if self.banr:
      return
    if not self.oldbotb == self.botbanned:
      self.banr=True
      collection = self.db["bot_banned"]
      value = {k: self.botbanned[k] for k in self.botbanned.keys() if k not in self.oldbotb.keys() or self.botbanned[k] != self.oldbotb[k]}
      value2=copy.deepcopy(value)
      for id, document in value.items():
        self.amount+=1
        if self.amount > 99:
          self.oldbotb.update({k: v for k, v in value2.items()})
          self.banr=False
          return
        collection.replace_one({"_id":id}, document, upsert=True)
        value2.pop(id)
      self.oldbotb = copy.deepcopy(self.botbanned)
      self.banr=False
  
  @tasks.loop(seconds=1.0)
  async def store_users(self):
    if self.bot.loadng:
      return
    if self.usersr:
      return
    if not self.oldusers == self.usersdb:
      self.usersr=True
      collection = self.db["users"]
      value = {k: self.usersdb[k] for k in self.usersdb.keys() if k not in self.oldusers.keys() or self.usersdb[k] != self.oldusers[k]}
      value2=copy.deepcopy(value)
      for id, document in value.items():
        self.amount+=1
        if self.amount > 99:
          self.oldusers.update({k: v for k, v in value2.items()})
          self.usersr=False
          return
        result = collection.find({})
        for doc in result:
          if doc["_id"] not in self.usersdb.keys():
            self.amount+=1
            collection.delete_one(doc)
        self.amount+=1
        collection.replace_one({"_id":id}, document, upsert=True)
        value2.pop(id)
      self.oldusers = copy.deepcopy(self.usersdb)
      self.usersr=False

  @tasks.loop(seconds=1.0)
  async def store_bitcoin(self):
    if self.bot.loadng:
      return
    if self.bitcoinr:
      return
    if not self.oldbitcoin == self.bitcoin:
      self.bitcoinr=True
      collection = self.db["bitcoin"]
      self.amount+=1
      if self.amount > 99:
        self.bitcoinr=False
        return
      collection.replace_one({"_id":1}, self.bitcoin)
      self.bitcoinr=False

  @tasks.loop(seconds=60.0)
  async def clear_intervals(self):
    self.amount = 0

async def func_bitcoin(self):
  """
  bitcoin exchange rate function
  """
  print("Bitcoin Functioning...")
  while True:
      users = self.bot.bitcoin
      exchange_rate = users["exchange_rate"]
      if exchange_rate < 55000:
          if exchange_rate > 45000:
              users["exchange_rate"]+=random.randint(0,500)
              users["exchange_rate"]-=random.randint(0,500)
          else:
              users["exchange_rate"]+=random.randint(1500,2000)
      else:
          users["exchange_rate"]-=random.randint(1500,2000)
      await asyncio.sleep(60)