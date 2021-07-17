import discord, asyncio, time
from discord.ext import commands, tasks

class Rules(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden=True

  @commands.command()
  async def rules(self, ctx):
      em = discord.Embed(
        title = "CapitalismTheTrueGaymer Bot Rules",
        description = "Rule 1: Be pog\nRule 2: Producing through 50k+ coins each day using while autotyping is NOT allowed.\nRule 3: Any form of scamming is not allowed. \nRule 4: When reporting a user, please provide detailed proof.\nRule 5: No abuse use of the bot. \nRule 6: You cannot trade bot currency for un-bot-related activities or currencies."
      )
      em.set_footer(
        text = "Not following these rules will get you bot banned."
      )
      await ctx.send(embed=em) 

def setup(bot):
    bot.add_cog(Rules(bot))