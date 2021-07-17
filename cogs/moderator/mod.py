from discord.ext import commands
from discord.ext.commands import has_permissions
import discord
import asyncio

class Mod(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.logsdb = bot.logsdb
    self.hidden=False
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  @commands.has_permissions(ban_members = True)
  async def unban(self, ctx,*,member,reason=None):
    try:
        banned_users = await ctx.guild.bans()
        id_ = None
        try:
            int(member)
            id_ = True
        except:
            id_ = False
        if not id_ == True:
            member_name, member_discriminator = member.split('#')
        else:
            mem="discord#0000"
            member_name, member_discriminator = mem.split('#')
        async for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f"{user} has been unbanned by {ctx.author}.")
            elif int(user.id) == int(member):
                await ctx.guild.unban(user)
                await ctx.send(f"{user} has been unbanned by {ctx.author}.")
    except:
      await ctx.reply("This pog person isn't banned.", mention_author=False)

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  @commands.has_permissions(kick_members = True)
  async def kick(self, ctx, member: discord.Member, *, reason=None):
      try:
          await member.kick(reason=reason)
          await ctx.reply(f'User {member} has been kicked.', mention_author=False)
      except:
          await ctx.reply("You cannot kick this pog person.", mention_author=False)

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  @has_permissions(ban_members = True)
  async def ban(self, ctx, *arg):
    try:
      member = arg[0]
    except:
      await ctx.send("heyoo dude fill in the arguments")
      return
    try:
        int(member)
    except:
        member = member.split("!")
        member = member[1]
        member = member.split(">")
        member = member[0]
    try:
        reason=arg[1]
    except:
        reason=None
    try:
      user = await self.bot.fetch_user(member)
      await ctx.guild.ban(user, reason = reason)
      await ctx.reply(f'User {user} has been banned.', mention_author=False)
    except:
      await ctx.reply("You cannot ban this pog person.", mention_author=False)

  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  @has_permissions(administrator=True)
  async def prefix(self, ctx, *, arg=None):
    data = self.logsdb
    if arg == None:
      try:
        data[str(ctx.guild.id)]
      except:
        data[str(ctx.guild.id)]={"_id":str(ctx.guild.id)}
      try:
        data[str(ctx.guild.id)]["prefix"]=""
        await ctx.send(f"The prefix for this server has been set to NOTHING",  allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
        return
      except:
        await ctx.send("The prefix couldn't be set because it wasn't in a valid format")
        return
    try:
      arg = arg.split()
      # if len(list_) > 1:
      #   try:
      #     arg = list(arg)
      #   except:
      #     await ctx.send("Hey you can't include spaces in the prefix.")
      #     return
      if len(arg) > 5:
        await ctx.send("Hey a single server can't have more than 5 prefixes or else my memory usage will be 50 TB in a day")
        return
    except:
      pass
    try:
      data[str(ctx.guild.id)]
    except:
      data[str(ctx.guild.id)]={"_id":str(ctx.guild.id)}
    try:
      try:
        arg[0]
        prefix = str(arg).lstrip('[').rstrip(']')
      except:
        pass
      data[str(ctx.guild.id)]["prefix"]=arg
      await ctx.send(f"The prefix for this server has been set to {prefix}!",  allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except:
      await ctx.send("The prefix couldn't be set because it wasn't in a valid format")
      return
    

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  @has_permissions(administrator=True)
  async def purge(self, ctx, num: int):
      await ctx.channel.purge(limit = num + 1)

  @commands.Cog.listener()
  async def on_member_join(self, member):
    data = self.logsdb
    if str(member.guild.id) in data.keys():
      try:
        channel_id = data[str(member.guild.id)]["channel"]
      except:
        return
      channel = await self.bot.fetch_channel(channel_id)
      await channel.send(f"{member.mention} just joined the server! Welcome!", allowed_mentions=discord.AllowedMentions.none())
    else:
      return
  
  @discord.ext.commands.cooldown(1,2,commands.BucketType.user)
  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def setchannel(self, ctx, channel: discord.TextChannel):
    data = self.logsdb
    try:
      try:
        data[str(ctx.guild.id)]
      except:
        data[str(ctx.guild.id)]={"_id":str(ctx.guild.id)}
      data[str(ctx.guild.id)]["channel"]=channel.id
      await ctx.send(f"The default WELCOME channel has been set to {channel.mention}!")
    except:
      await ctx.send("Channel not found")

  @discord.ext.commands.cooldown(1,5,commands.BucketType.guild)
  @commands.command()
  @has_permissions(manage_guild=True)
  async def enable(self, ctx, cmd):
      logs = self.logsdb
      cmd = cmd.lower()
      if self.bot.get_command(cmd)==None:
        await ctx.send("Command not found.")
        return
      else:
        cmd = self.bot.get_command(cmd)
        cmd = cmd.name
      try:
        logs[str(ctx.guild.id)]["disabled"]
        index = logs[str(ctx.guild.id)]["disabled"].index(cmd)
        logs[str(ctx.guild.id)]["disabled"].pop(index)
      except:
        await ctx.send("Hey dude you never disabled the command.")
        return
      await ctx.send(f"{cmd} enabled!")

  @discord.ext.commands.cooldown(1,5,commands.BucketType.guild)
  @commands.command()
  @has_permissions(manage_guild=True)
  async def disable(self, ctx, cmd):
      if cmd.lower() == "disable" or cmd.lower() == "enable":
        await ctx.send("Disable and enable command cannot be disabled.")
        return
      logs = self.logsdb
      cmd = cmd.lower()
      if self.bot.get_command(cmd)==None:
        await ctx.send("Command not found.")
        return
      else:
        cmd = self.bot.get_command(cmd)
        cmd = cmd.name
      try:
        logs[str(ctx.guild.id)]
        try:
          logs[str(ctx.guild.id)]["disabled"].append(cmd)
        except:
          logs[str(ctx.guild.id)]["disabled"]=[]
          logs[str(ctx.guild.id)]["disabled"].append(cmd)
      except:
        logs[str(ctx.guild.id)]={"_id":str(ctx.guild.id)}
        logs[str(ctx.guild.id)]["disabled"]=[]
        logs[str(ctx.guild.id)]["disabled"].append(cmd)
      await ctx.send(f"{cmd} Command disabled.")


def setup(bot):
    bot.add_cog(Mod(bot))