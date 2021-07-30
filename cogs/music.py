import discord
from discord.ext import commands, tasks

class Music(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden = True

def setup(bot):
  bot.add_cog(Music(bot))