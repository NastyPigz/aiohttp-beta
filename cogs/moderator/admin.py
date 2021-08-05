from discord.ext import commands
from other.mongo import cluster
import discord, asyncio, os, sys, subprocess

class Admin(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.maindb = bot.maindb
    self.botbanned = bot.botbanned
    self.hidden=True

  @commands.command(name="bot_ban")
  async def ban(self, ctx, member, *, reason=None):
    try:
      member = int(member)
    except:
      await ctx.send("The argument has to be an integer")
      return
    users = self.maindb
    try:
      admin = users[str(ctx.author.id)]["badges"]["admin"]
    except:
      return
    if admin == 0:
      await ctx.send("You're not an admin")
      return
    data = self.botbanned
    try:
      person = await self.bot.fetch_user(member)
      try:
        data[str(person.id)]["bot_banned"]=True
      except:
        data[str(person.id)]={}
        data[str(person.id)]["_id"]=str(person.id)
        data[str(person.id)]["spam_banned"]=False
        data[str(person.id)]["bot_banned"]=True
        
      try:
        await person.send(f"You have been bot banned by a Bot Moderator for: {reason}\nIf you believe this is in error or would like to provide context, you can appeal at https://discord.gg/capitalism")
      except:
        await ctx.send("That person's DMs weren't open so I couldn't DM them!")
      channel = await self.bot.fetch_channel(853288563352404058)
      await channel.send(f"{ctx.author} banned {person.name}, id {member}, reason is {reason}")
    except Exception as e:
      print(e)
      await ctx.send("Invalid member id")
      return
    await ctx.send("he is now bot banned")

  @commands.command(name="bot_unban")
  async def unban(self, ctx, member, *, reason=None):
    try:
      member = int(member)
    except:
      await ctx.send("The argument has to be an integer")
      return
    users = self.maindb
    admin = users[str(ctx.author.id)]["badges"]["admin"]
    if admin == 0:
      await ctx.send("You're not an admin")
      return False
    data = self.botbanned
    try:
      person = await self.bot.fetch_user(member)
      spam=False
      if data[str(member)]["spam_banned"]:
        data[str(member)]["spam_banned"]=False
        spam=True
      elif data[str(member)]["bot_banned"]:
        data[str(member)]["bot_banned"]=False
      else:
        await ctx.send("They were never bot banned or spam banned.")
        return
      try:
        await person.send(f"You have been unbanned by a Bot Moderator for: {reason}. No further action is required.")
      except:
        await ctx.send("That person's DMs weren't open so I couldn't DM them!")
      channel = await self.bot.fetch_channel(853288563352404058)
      await channel.send(f"{ctx.author} unbanned {person.name}, id {member}, spam={spam}, reason={reason}")
    except Exception as e:
      print(e)
      await ctx.send("Invalid member id")
      return
    await ctx.send("he is now bot unbanned")
    return True
  
  @discord.ext.commands.cooldown(1, 600, commands.BucketType.user)
  @commands.command()
  async def shutdown(self, ctx):
    if ctx.message.author.id == 763854419484999722:
      #put something here
      self.bot.loadng=True
      await asyncio.sleep(5)
      await self.bot.aiohttp_session.close()
      await self.bot.close()
      await asyncio.sleep(55)
      exit(0)
    else:
      await ctx.reply("This command is creator only", mention_author=False)
  
  @commands.command(aliases=["restart", "nuke_bot"])
  async def reboot(self, ctx):
    if ctx.author.id == 763854419484999722:
      await ctx.send("rebooting the bot...")
      with open("afk/communicate.txt", "w") as f:
        f.write("exit")
      subprocess.run("clear", shell=True)
      os.execv(sys.executable, ['python'] + sys.argv)
    else:
      await ctx.send("You cannot reboot the bot.")
  
  @commands.command()
  async def say(self, ctx, *,message):
    if ctx.author.id == 763854419484999722:
      pass
    else:
      await ctx.send('this command is disabled')
      return
    for i in range(5):
      await ctx.send(message)

def setup(bot):
    bot.add_cog(Admin(bot))