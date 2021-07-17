import discord, aiohttp, os
from discord.ext import commands

class Evaluation(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden=False
    self.session = bot.aiohttp_session

  @commands.command()
  async def eval(self, ctx, *, script):
    res = self.convert_code_blocks(script)
    if not res:
      await ctx.send("This is not a valid code block")
      return
    else:
      script = res
    await ctx.send("this might take a few seconds depending on the length of your code ok")
    try:
      website_ = os.getenv("EW")
      r= await self.session.get(
        f"{website_}/request?script={script}",
      )
      json_format = await r.json()
      await ctx.send("```cs\n{}```".format(json_format["output"].replace("jdoodle", "capitalismbot").replace("JDoodle", "Capitalismbot")), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except Exception as e:
      print(e)

  @commands.command()
  async def js(self, ctx, *, script):
    res = self.convert_code_blocks_(script, "js")
    if not res:
      await ctx.send("This is not a valid code block")
      return
    else:
      script = res
    await ctx.send("this might take a few seconds depending on the length of your code ok")
    try:
      website_ = os.getenv("EW")
      r= await self.session.get(
        f"{website_}/javascript?script={script}",
      )
      json_format = await r.json()
      await ctx.send("```js\n{}```".format(json_format["output"].replace("jdoodle", "capitalismbot").replace("JDoodle", "Capitalismbot")), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except Exception as e:
      print(e)
  
  @commands.command()
  async def java(self, ctx, *, script):
    res = self.convert_code_blocks_(script, "java")
    if not res:
      await ctx.send("This is not a valid code block")
      return
    else:
      script = res
    await ctx.send("this might take a few seconds depending on the length of your code ok")
    try:
      website_ = os.getenv("EW")
      r= await self.session.get(
        f"{website_}/java?script={script}",
      )
      json_format = await r.json()
      await ctx.send("```java\n{}```".format(json_format["output"].replace("jdoodle", "capitalismbot").replace("JDoodle", "Capitalismbot")), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except Exception as e:
      print(e)

  @commands.command()
  async def lua(self, ctx, *, script):
    res = self.convert_code_blocks_(script, "lua")
    if not res:
      await ctx.send("This is not a valid code block")
      return
    else:
      script = res
    await ctx.send("this might take a few seconds depending on the length of your code ok")
    try:
      website_ = os.getenv("EW")
      r= await self.session.get(
        f"{website_}/lua?script={script}",
      )
      json_format = await r.json()
      await ctx.send("```lua\n{}```".format(json_format["output"].replace("jdoodle", "capitalismbot").replace("JDoodle", "Capitalismbot")), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except Exception as e:
      print(e)

  @commands.command()
  async def py(self, ctx, *, script):
    res = self.convert_code_blocks_(script, "py")
    if not res:
      await ctx.send("This is not a valid code block")
      return
    else:
      script = res
    await ctx.send("this might take a few seconds depending on the length of your code ok")
    try:
      website_ = os.getenv("EW")
      r= await self.session.get(
        f"{website_}/python?script={script}",
      )
      json_format = await r.json()
      await ctx.send("```py\n{}```".format(json_format["output"].replace("jdoodle", "capitalismbot").replace("JDoodle", "Capitalismbot")), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except Exception as e:
      print(e)

  def convert_code_blocks_(self, ipt, lang:str):
    try:
      final = ipt.lstrip("```")
      final = final.lstrip(lang)
      final = final.rstrip("```")
      return final
    except:
      return False

  def convert_code_blocks(self, ipt):
    try:
      final = ipt.lstrip("```")
      final = final.lstrip("cs")
      final = final.rstrip("```")
      return final
    except:
      return False

def setup(bot):
    bot.add_cog(Evaluation(bot))