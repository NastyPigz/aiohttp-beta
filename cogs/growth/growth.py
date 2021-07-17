import discord, datetime
from discord.ext import commands, tasks

def setup(bot):
  bot.add_cog(Growth_detect(bot))

class Growth_detect(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.logsdb = bot.logsdb
    self.task1_loading=False
    self.task2_loading=False
    self.check_guilds.start()
    self.hidden=True
    self.check_active.start()

  @commands.command(hidden=True)
  async def test2(self, ctx):
    num = 0
    guild = self.bot.get_guild(823890466034286642)
    for mem in guild.members:
      if mem.bot:
        num += 1
    await ctx.send(str(num))
    await ctx.send(len(guild.members))

  @tasks.loop()
  async def check_active(self):
    if self.task1_loading:
      return
    for guild in self.bot.guilds:
      self.task1_loading=True
      try:
        last_message=self.logsdb[str(guild.id)]["lm"]
        if (int(datetime.datetime.utcnow().timestamp())-last_message) > 604800:
          for channel in guild.channels():
            try:
              await channel.send("Hey, looks like the last time you used me was 1 week ago. Invite me back when you really can use me often!")
              break
            except:
              continue
          await guild.leave()
      except:
        continue
    self.task1_loading=False

  @tasks.loop()
  async def check_guilds(self):
    if self.task2_loading:
      return
    for guild in self.bot.guilds:
      self.task2_loading=True
      bots=[]
      if len(guild.members) == 1:
        continue
      for member in guild.members:
        if member.bot:
          bots.append(member)
      if len(bots)/len(guild.members) > 0.4:
        for channel in guild.channels:
          try:
            await channel.send("Hey, looks like 40% or more of the members here are bots. I do not accept joining these types of servers because it affects me from being verified. Ratio was: {}".format(len(bots)/len(guild.members)))
            break
          except:
            continue
        await guild.leave()
        break
    self.task2_loading=False

  # @check_active.before_loop
  # async def before_check_active(self):
  #   await self.bot.wait_until_ready()
  
  @check_guilds.before_loop
  async def before_check_guilds(self):
    await self.bot.wait_until_ready()

  @commands.Cog.listener()
  async def on_guild_join(self, guild):
    for channel in guild.channels:
      #for some reason it's sorted alphabetically
      try:
        await channel.send("Thank you for adding me to your server! Make sure you use me often! I will be very enjoyable, I promise!\n`Note: If you don't use me often I will eventually leave~`")
        break
      except:
        continue