import discord
from discord.ext import commands

class Emojis(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden=False
  
  @discord.ext.commands.cooldown(1, 2, commands.BucketType.user)
  @commands.command()
  async def bruh(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<:bruh:823937997036453938>")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def pog(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<:littlepog:825452143657353226>")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def WeDemBois(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<a:WeDemBois:823730867201376296>")

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def sad(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<a:pensiveGIF:826168776503459871>")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def think(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<:think:825452368128376843>")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def raged(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("<:re:826170479613313054>")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def thinker(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    message = list(await ctx.channel.history(limit=1).flatten())[-1]
    await message.add_reaction(":think:825452368128376843")

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def pogger(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    message = list(await ctx.channel.history(limit=1).flatten())[-1]
    await message.add_reaction(":littlepog:825452143657353226")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def bruher(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    message = list(await ctx.channel.history(limit=1).flatten())[-1]
    await message.add_reaction(":bruh:823937997036453938")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def agree(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    message = list(await ctx.channel.history(limit=1).flatten())[-1]
    await message.add_reaction(":YES:825426606188527677")
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def disagree(self, ctx):
      try:
        await ctx.message.delete()
      except:
        pass
      message = list(await ctx.channel.history(limit=1).flatten())[-1]
      await message.add_reaction(":NO:825426696621654016")

def setup(bot):
  bot.add_cog(Emojis(bot))