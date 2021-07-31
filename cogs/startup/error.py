from discord.ext import commands
from cogs.moderator.admin import Admin
from data.json.help import help_menu
import discord
import traceback

class ErrorHandler(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.maindb = bot.maindb
    self.botbanned = bot.botbanned
    self.hidden=True

  def convert(self,t:int):
    if t < 60:
      return "{:0.2f}s".format(t)
    elif t<3600:
      return "{:0.2f}m".format(t/60)
    else:
      return "{:0.2f}h".format(t/3600)

  @commands.Cog.listener()
  async def on_command_error(self, ctx, error):
    print(error)
    try:
      if str(ctx.command) == "bot_unban":
        result = await Admin.unban(self,ctx, ctx.author.id)
        if result:
          return
      banned = self.bot.botbanned
      try:
        if banned[str(ctx.author.id)]["bot_banned"]:
          await ctx.send("You're bot banned! Join support server to appeal. ~~bad boy!~~")
          return
        elif banned[str(ctx.author.id)]["spam_banned"]:
          return
      except:
        pass
      if ctx.guild == None:
        await ctx.send("Sorry but we've disabled DM commands")
        return
      else:
        pass
      if isinstance(error, commands.CommandOnCooldown):
        the_time=self.convert(error.retry_after)
        #error.retry_after:.2f
        em = discord.Embed(
        title="Slow it down, mate",
        description=f"Try again in {the_time}.",
        color=discord.Color.random()
        )
        await ctx.reply(embed=em, mention_author=False)
        return
      elif isinstance(error, discord.Forbidden):
        em=discord.Embed(
          title="I tried to dm...",
          description="But I failed! Check if you/they blocked me or closed dms."
        )
        await ctx.send(embed=em)
        return
      elif isinstance(error, commands.BadArgument):
        em=discord.Embed(
          title="Invalid/Bad Argument",
          description="Are you sure you followed the format?"
        )
        await ctx.reply(embed=em, mention_author=False)
        ctx.command.reset_cooldown(ctx)
        return
      elif isinstance(error, commands.MissingRequiredArgument):
        string_ = '%s%s %s' % (
          ctx.prefix, 
          ctx.command.qualified_name, 
          ctx.command.signature
        )
        embed=discord.Embed(title="You are missing required arguments for the command!", description=f"Format: `{string_}`")
        await ctx.send(embed=embed)
        ctx.command.reset_cooldown(ctx)
        return
      elif isinstance(error, commands.CommandNotFound):
        return
      elif isinstance(error, commands.BotMissingPermissions):
        content_string=""
        for i in error.missing_perms:
          content_string+="`{}`, ".format(i)
        await ctx.send("I am missing permissions!\n{}".format(content_string.rstrip(", ")))
        ctx.command.reset_cooldown(ctx)
        return
      elif isinstance(error, commands.MissingPermissions):
        content_string=""
        for i in error.missing_perms:
          content_string+="`{}`, ".format(i)
        await ctx.send("You are missing required permissions!\n{}".format(content_string.rstrip(", ")))
        ctx.command.reset_cooldown(ctx)
        return
      elif isinstance(error, commands.CheckFailure):
        return
      elif isinstance(error, commands.CommandInvokeError):
        if str(error.original) == "403 Forbidden (error code: 50007): Cannot send messages to this user":
          await ctx.send("I failed send message! The user must have blocked me or closed their dms.")
          return
        elif str(error.original)=="404 Not Found (error code: 10008): Unknown Message":
          await ctx.send("I tried to delete, edit or fetch a message but it couldn't be reached. Please stop deleting my messages that are working in progress. Get some help.")
          return
        else:
          try:
            if error.original.code == 50013:
              await ctx.send("Hmm looks like the floor here is made out of floor! I am missing permissions. To do one of the tasks.")
              return
          except:
            pass
          traceb = ""
          traceblist = traceback.format_exception(type(error), error, error.__traceback__)
          for i in traceblist:
            traceb+=i
          await ctx.send(f"```py\n{traceb}```")
      else:
        ctx.command.reset_cooldown(ctx)
        traceb = ""
        traceblist = traceback.format_exception(type(error), error, error.__traceback__)
        for i in traceblist:
          traceb+=i
        await ctx.send(f"```py\n{traceb}```")
        return
    except Exception as e:
      print(e)
      return

def setup(bot):
    bot.add_cog(ErrorHandler(bot))