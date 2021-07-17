import discord
from discord.ext import commands
import asyncio

class Data(commands.Cog):
  def __init__(self, bot):
    self.hidden=False
    self.bot = bot
    self.maindb = bot.maindb
    self.logsdb = bot.logsdb
    self.usersdb = bot.usersdb  

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def removedata(self,ctx):
    users = self.maindb
    try:
      users[str(ctx.author.id)]
      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
      await ctx.send("Are you sure you want to remove your data ENTIRELY? Meaning you will lose all your progress. Say `Y` or `y` for yes.")
      try:
        msg = await self.bot.wait_for('message', timeout=60, check = check)
        if msg.content.lower() == "y":
          users.pop(str(ctx.author.id))
          await ctx.send("All your currency data has been fully wiped.")
        else:
          await ctx.send("alright, nothing has been changed.")
          return
      except asyncio.TimeoutError:
        await ctx.send("alright, nothing has been changed.")
        return
    except:
      await ctx.send("You never had any data in our currency system")

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def removelogs(self, ctx):
    if not ctx.author.id == ctx.guild.owner_id:
      await ctx.send("You're not the owner of this guild!")
      return
    users = self.logsdb
    try:
      users[str(ctx.guild.id)]
      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
      await ctx.send("Are you sure you want to remove your guild data ENTIRELY? Meaning you will lose all your logs. Say `Y` or `y` for yes.")
      msg = await self.bot.wait_for('message', timeout=60, check = check)
      if msg.content.lower() == "y":
        users.pop(str(ctx.guild.id))
        await ctx.send("All the moderation logs of this server/guild has been wiped.")
      else:
        await ctx.send("alright, nothing has been changed.")
        return
    except Exception:
      await ctx.send("Your guild never had any data in our moderation system")

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def removeall(self,ctx):
    users = self.usersdb
    try:
      users[str(ctx.author.id)]
      data = self.maindb
      try:
        data[str(ctx.author.id)]  
      except:
        pass
      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
      await ctx.send("Are you sure you want to remove your data ENTIRELY? Meaning you will lose all your currency and bot usage. Say `Y` or `y` for yes. **NOTE: THIS WILL NOT WIPE YOUR LOGS**")
      msg = await self.bot.wait_for('message', timeout=60, check = check)
      if msg.content.lower() == "y":
        users.pop(str(ctx.author.id))
        try:
          data.pop(str(ctx.author.id))
        except:
          pass
        await ctx.send("All your currency data and usage data has been wiped.")
      else:
        await ctx.send("alright, nothing has been changed.")
        return
    except:
      await ctx.send("You never had any data in our system")

def setup(bot):
    bot.add_cog(Data(bot))