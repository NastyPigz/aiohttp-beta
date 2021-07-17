from discord.ext import commands
import aiohttp, os
from discord.http import Route

def setup(bot:commands.Bot):
  bot.add_cog(experiment(bot=bot))

class experiment(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.session = bot.aiohttp_session
  
  @commands.command()
  async def activity(self, ctx, arg:int):
    if not ctx.author.voice:
      await ctx.send("be in a voice channel")
      return
    voice = ctx.author.voice
    if arg == 1:
      app_id=755600276941176913
    elif arg == 2:
      app_id=773336526917861400
    elif arg == 3:
      app_id=814288819477020702
    elif arg == 4:
      app_id=755827207812677713
    elif arg == 0:
      app_id=832012815819604009
    else:
      await ctx.send("Unsupported activity type")
      return
    r=Route('POST', '/channels/{channel_id}/invites', channel_id=voice.channel.id)
    res = await self.bot.http.request(r,
      json={
        "max_age":86400,
        "max_uses": 0,
        "target_application_id": app_id,
        "target_type": 2,
        "temporary": False,
        "validate": None,
      }
      )
    await ctx.send("https://discord.com/invite/{}".format(res["code"]))