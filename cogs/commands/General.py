import discord, requests, os, aiohttp, time, qrcode, image
from discord.ext import commands, tasks
from discord.ext.commands import has_permissions
from data.profanity import swearwords
from cogs.moderator.admin import Admin
import random, asyncio, smtplib, re, datetime, asyncio, os, sys
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from data.json.help import help_menu
from discord_slash.utils.manage_components import create_select, create_select_option
from discord_slash.utils.manage_components import wait_for_component
from discord_slash.context import ComponentContext
from data.json.jobs import jobs
from other.mongo import cluster
import concurrent, io
import functools
from pathlib import Path

class General(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.usage = bot.usage
    self.data = bot.data
    self.maindb = bot.maindb
    self.logsdb = bot.logsdb
    self.usersdb = bot.usersdb
    self.botbanned = bot.botbanned
    self.session = bot.aiohttp_session
    self.servers = {}
    self.calling = []
    self.intervals = bot.intervals
    self.cmdintervals = {"strikes":{}}
    self.hidden=False

  def make_qr(self, arg:str):
    img=qrcode.make(arg)
    path_name=""
    for i in range(10):
      path_name+=str(random.randint(0,9))
    if Path(f"cogs/commands/{path_name}.png").exists():
      while Path(f"cogs/commands/{path_name}.png").exists():
        path_name+=str(random.randint(0,9))
    img.save(f"cogs/commands/{path_name}.png")
    return path_name

  # @commands.bot_has_permissions(attach_files=True)
  @commands.command(name="qr", aliases=["qrcode"])
  async def qrcode(self, ctx, arg):
    loop = asyncio.get_running_loop()
    with concurrent.futures.ThreadPoolExecutor() as pool:
      result = await loop.run_in_executor(pool, self.make_qr, arg)
    try:
      file_=discord.File(f"cogs/commands/{result}.png", filename="qrcode.png")
      embed = discord.Embed(title="Be aware of QRcodes!", description="People can put IP grabbers, cookies loggers or NSFW stuff that would create awkward scenes.")
      embed.set_image(url="attachment://qrcode.png")
      embed.set_footer(text="to scan the QR code search \"QR code scanner\" on google")
      await ctx.send(embed=embed, file=file_)
      Path(f"cogs/commands/{result}.png").unlink()
    except Exception as e:
      raise e

  @commands.command(name="uptime")
  async def uptime_(self, ctx):
    try:
      tim_e = datetime.datetime.utcnow()-self.bot.uptime
      await ctx.send(str(tim_e))
    except Exception as e:
      print(e)

  # @commands.bot_has_permissions(attach_files=True)
  @commands.command()
  async def cat(self, ctx, code:int):
    response = await self.session.get(f"https://http.cat/{code}.jpg")
    rb = await response.read()
    bytes_ = io.BytesIO(rb)
    await ctx.send(file=discord.File(fp=bytes_, filename=f"http{code}.jpg"))


  # @commands.bot_has_permissions(attach_files=True)
  @commands.command()
  async def screenshot(self, ctx, url):
    if not ctx.channel.nsfw:
      # if not ctx.author.id == 763854419484999722:
        return await ctx.send("WOAH! NSFW not allowed here! This command can only be used in NSFW channels due to some websites having explicit content on their main page. I don't wanna be banned for sending what you told me to send.")
    try:
      r= await self.bot.aiohttp_session.post(
        "https://api.deepai.org/api/nsfw-detector",
        data={
            'image': f"https://image.thum.io/get/http://{url}",
        },
        headers={'api-key': 'aa97b2c1-4e45-4c71-994c-05b50e93bbb1'}
      )
    except Exception as e:
      print(e)
    try:
      dict1 = await r.json()
      if dict1["output"]["nsfw_score"] > 0.4:
        await ctx.send("Hey, looks like the NSFW score for this website is going off the charts! Do you want to proceed? `y` or `Y`")
        def check(m):
          return m.author == ctx.author and m.channel == ctx.channel
        try:
          msg = await self.bot.wait_for('message', check=check, timeout=10.0)
          if not msg.content.lower() == "y":
            return
        except asyncio.TimeoutError:
          return
    except:
      await ctx.send("The NSFW detector website is down, do you want to continue?")
      def check(m):
        return m.author == ctx.author and m.channel == ctx.channel
      try:
        msg = await self.bot.wait_for('message', check=check, timeout=10.0)
        decline_list = ["yes", "oui", "ye", "why not", "y not", "ye!", "y", "y!", "yes!", "yus"]
        if not any([True if i in msg.content.lower() else False for i in decline_list]):
          return
      except asyncio.TimeoutError:
        return
    embed=discord.Embed(
    )
    embed.set_image(url=f"https://image.thum.io/get/auth/53268-Bot/https://{url}")
    await ctx.send(embed=embed)

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def ping(self, ctx):
      before = time.monotonic()
      message = await ctx.reply("Pong!", mention_author=False, chb=False)
      ping = (time.monotonic() - before) * 1000
      await message.edit(content=f"Pong!  `{int(ping)}ms`", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False, replied_user=False))
      #print(f'Ping {int(ping)}ms')
  
  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command(aliases=["websocket", "ws"])
  async def latency(self, ctx):
    await ctx.send(f"`{round(self.bot.latency*1000)}ms`")
  
  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def db(self, ctx):
    if not ctx.author.id == 763854419484999722:
      await ctx.send("You cannot view database speed.")
      return
    before = time.monotonic()
    collection = cluster["CapBot"]["bitcoin"]
    for i in collection.find({}):
      users = i
    collection.replace_one({"_id":1}, users)
    after = time.mofpnotonic() - before
    await ctx.send(f"`{round(after*1000)}ms`")

  @commands.command()
  async def timenow(self, ctx):
    dt = datetime.datetime.utcnow()
    timestamp = int(dt.timestamp())
    await ctx.send(f"<t:{timestamp}>")

  # @commands.bot_has_permissions(embed_links=True)
  @commands.command()
  async def insult(self, ctx, member:discord.Member):
    with open ("cogs/commands/insults.txt", "r") as f:
      insults = f.readlines()
    insult = random.choice(insults)
    embed=discord.Embed(
      description=member.mention
    )
    embed.set_image(url=str(insult))
    embed.set_footer(text=f"Insult requested by {ctx.author}")
    await ctx.send(embed=embed)

  @commands.command()
  async def choice(self, ctx, job:str):
    try:
      the_q = random.choice(jobs[job]["tasks"])
      questions = the_q["response"]
      if len(questions) > 24:
        que_holder=[]
        for i in range(25):
          que_holder.append(random.choice(questions))
        questions = que_holder
      if any([True if len(i) > 24 else False for i in questions]):
        que_holder=[]
        for i in questions:
          if not len(i) > 24:
            que_holder.append(i)
        questions=que_holder
      questions_clone = questions.copy()
      right_answers = []
      for i in range(int(len(questions)/2)):
        stuff = random.choice(questions_clone)
        right_answers.append(stuff)
        questions_clone.pop(questions_clone.index(stuff))
      options = []
      for i in questions:
        options.append(create_select_option(label=questions[questions.index(i)], value=questions[questions.index(i)]))
      select = create_select(options=options, min_values=1, max_values=1)
      action_row=manage_components.create_actionrow(select)
      messageMain = await ctx.send(content=the_q["question"], components=[action_row])
      while True:
        try:
          select_ctx: ComponentContext = await wait_for_component(self.bot, components=action_row, timeout=30.0)
          options = select_ctx.selected_options
          content = ""
          for i in options:
            content+=f"{i}"
          is_right = True if str(content) in right_answers else False
          salary = jobs[job]["salary"] if is_right else jobs[job]["fail"]
          try:
            number_of_degrees = len(self.maindb[str(ctx.author.id)]["degree"])
          except:
            number_of_degrees=0
          if number_of_degrees > 0:
            salary=int(salary*(number_of_degrees*0.2+1))
          await select_ctx.send(f"Selected options: {content}, right={True if str(content) in right_answers else False}, Salary = {salary}")
        except asyncio.TimeoutError:
          await messageMain.edit(content="Choice test timeout", components=[])
    except Exception as e:
      print(e)
  
  @commands.command()
  async def used(self, ctx):
    try:
      embed=discord.Embed(
        title=f"{ctx.author}'s bot usage data'",
        description="__commands__: {:,}".format(self.usersdb[str(ctx.author.id)]["commands"])
      )
      await ctx.send(embed=embed)
    except:
      await ctx.send("Hey, for some reason I cannot find any data.")

  @commands.command(aliases=["commands"])
  async def command(self, ctx):
    try:
      command_=""
      for command in help_menu.keys():
        command_+=f"`{command}`, "
      await ctx.author.send(command_)
    except:
      await ctx.send("Hey I couldn't DM you!")

  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command()
  async def userphone(self, ctx):
    if len(self.servers)==0:
      self.servers[str(ctx.guild.id)]=ctx.channel.id
      if not ctx.guild.id in self.calling:
        await ctx.send("Waiting for a server to call...")
        return
      else:
        await ctx.send("There's already a call inside this server!")
        return
    else:
      for server in self.servers.keys():
        guild_id = int(server)
        if guild_id == ctx.guild.id:
          await ctx.send("Call cancelled.")
          self.servers.pop(str(server))
          return
        channel_id = self.servers[str(server)]
        self.servers.pop(str(server))
        break
      guild = self.bot.get_guild(guild_id)
      channel = None
      for chan in guild.text_channels:
        if chan.id == channel_id:
          channel = chan
      if channel == None:
        await ctx.send("Their text channel was deleted during the wait process.")
      await channel.send("Connected! say -h to hangup.")
      await ctx.send("Connected! say -h to hangup.")
      self.calling.append(channel.guild.id)
      self.calling.append(ctx.guild.id)
    def check(m):
      urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', m.content.lower())
      invites = re.findall("discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})", m.content.lower())
      if urls or invites:
        return False
      if m.author.id == 823699570147065876:
        return False
      return m.channel == ctx.channel or m.channel == channel
    while True:
      try:
        msg = await self.bot.wait_for('message', timeout=30.0, check=check)
        try:
          self.intervals[str(msg.channel.id)]
        except:
          self.intervals[str(msg.channel.id)]={}
        try:
          self.intervals[str(msg.channel.id)][str(msg.author.id)]
        except:
          self.intervals[str(msg.channel.id)][str(msg.author.id)]=[]
        self.intervals[str(msg.channel.id)][str(msg.author.id)].append(msg.created_at)
        author_messages = self.intervals[str(msg.channel.id)][str(msg.author.id)]  
        if len(author_messages) == 1:
          pass
        else:
          if (author_messages[-1]-author_messages[-2]).seconds == 0:
            if (author_messages[-1]-author_messages[-2]).microseconds < 300000:
              await msg.channel.send("Heyo stop spamming!")
              await ctx.send("Disconnected due to spam.")
              await channel.send("Disconnected due to spam.")
              break
        if msg.content.lower() == "-hangup" or msg.content.lower() == "-h":
          await ctx.send("Disconnected by hanging up.")
          await channel.send("Disconnected by hanging up.")
          break
        if msg.channel == ctx.channel:
          await channel.send(f"**{msg.author}:** {msg.content}", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
        else:
          await ctx.send(f"**{msg.author}:** {msg.content}", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
      except asyncio.TimeoutError:
        await ctx.send("Disconnected.")
        await channel.send("Disconnected.")
        break
    try:
      self.calling.pop(ctx.guild.id)
    except:
      pass
    try:
      self.calling.pop(channel.guild.id)
    except:
      return

  @commands.Cog.listener()
  async def on_command_completion(self, ctx):
    try:
      list_ = ["bruh","nice","meme","bruhmeme"]
      string_ = random.choice(list_)+random.choice(list_)+random.choice(list_)
      self.data[string_] = 1
      result = await self.detc_user(ctx.author)
      if result:
        embed = discord.Embed(
          title="Hey there I see you're new to CapitalismDiscordBot.\nIf you experience any difficulty or bugs, or even anything that should be improved, Please join our support server and reply there.\nHave fun with my features!",
          color=discord.Color.gold()
        )
        embed.set_author(name="CapitalismBot", url="https://discord.capitalismbot.repl.co/dashboard", icon_url="https://i.redd.it/ay9oenzf2vb21.png")
        embed.set_thumbnail(url="https://www.pngkey.com/png/detail/395-3958678_where-the-a-is-a-common-symbol-for.png")
        embed.set_footer(text="Capitalism Discord Bot", icon_url="https://i.dlpng.com/static/png/6312530-what-capitalism-symbol-the-of-is-symbol-symbol-capitalism-capitalism-symbol-820_703_preview.png")
        buttons = [
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Invite me",
                  url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands"
              ),
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Support Server",
                  url="https://discord.gg/capitalism"
              ),
          ]
        action_row = manage_components.create_actionrow(*buttons)
        try:
          await ctx.author.send(embed=embed,
            components=[
              action_row
            ]
          )
        except:
          await ctx.message.reply(embed=embed,
            components=[
              action_row
            ],
            mention_author=False
          )
      user = ctx.author
      users = self.maindb
      try:
        users[str(user.id)]["exp"]+=1
      except:
        pass
      users = self.usersdb
      try:
        users[str(user.id)]["commands"]+=1
        return
      except:
        return
    except:
      return

  async def detc_user(self, user):
    users = self.usersdb
    if str(user.id) in users:
      return False
    else:
      users[str(user.id)]={"_id":str(user.id), "commands":0}
    return True

  @discord.ext.commands.cooldown(1, 60, commands.BucketType.user)
  @commands.command()
  async def email(self, ctx):
      EMAIL_ADDRESS = 'capitalismdiscordbot@gmail.com'
      EMAIL_PASSWORD = str(os.getenv("EMAIL_PASSWORD"))
      await ctx.send("who will be the email receiver?")
      def check(author):
        def inner_check(message):
          if message.author != author:
            return False
          try:
            return True
          except ValueError:
            return False
        return inner_check
      try:
        msg = await self.bot.wait_for('message', timeout=30, check = check(ctx.author))
        RECEIVER = msg.content
        subject = 'Support Capitalism, Deny Communism.'
        await ctx.send("what will be the body? (if it's too short google will mark it as spam)")
        try:
          msg = await self.bot.wait_for('message', timeout=30, check = check(ctx.author))
          body = f'{msg.content} \n\n\nsent by {ctx.author} from discord'
          message = f'Subject: {subject}\n\n{body}'
          server = smtplib.SMTP('smtp.gmail.com', 587)
          server.ehlo()
          server.starttls()
          server.ehlo()
          try:
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
          except Exception as e:
            print(e)
            await ctx.send("Cannot log into Bot Email due to Google being annoying (or gmail having issues)")
            return
          try:
            server.sendmail(EMAIL_ADDRESS, RECEIVER, message)
            server.quit()
            await ctx.send("Email success. Note: if this is an invalid email, it can still say this message")
          except Exception as e:
            print(e)
            await ctx.send("failed to email, are you sure that's the right information?")
        except asyncio.TimeoutError:
          await ctx.send('imagine not replying in time mate')
      except asyncio.TimeoutError:
        await ctx.send("imagine not replying in time mate")

  @commands.Cog.listener()
  async def on_command(self, ctx):
    if ctx.author.id == 763854419484999722:
      ctx.command.reset_cooldown(ctx)
    else:
      try:
        if self.maindb[str(ctx.author.id)]["badges"]["admin"]>0:
          ctx.command.reset_cooldown(ctx)
      except:
        pass
    try:
      self.cmdintervals[str(ctx.author.id)]
    except:
      self.cmdintervals[str(ctx.author.id)]=[]
    self.cmdintervals[str(ctx.author.id)].append(ctx.message.created_at)
    author_messages = self.cmdintervals[str(ctx.author.id)]  
    if len(author_messages) < 6:
      pass
    else:
      time_spent=author_messages[-1]-author_messages[-5]
      if time_spent.seconds < 3:
        try:
          self.cmdintervals["strikes"][str(ctx.author.id)]+=1
          if self.cmdintervals["strikes"][str(ctx.author.id)] >= 10:
            users = self.botbanned
            if str(ctx.author.id) in users.keys():
              if users[str(ctx.author.id)]["spam_banned"]:
                return
              users[str(ctx.author.id)]["spam_banned"]=True
            else:
              users[str(ctx.author.id)]={"_id":str(ctx.author.id), "spam_banned":True, "bot_banned":False}
            channel = await self.bot.fetch_channel(853288563352404058)
            await channel.send(f"The bot spam_banned {ctx.author} for spamming commands, id {ctx.author.id}")
            try:
              await ctx.author.send("You are now bot banned from our bot for spamming too many commands.")
            except:
              await ctx.message.reply("You are now bot banned from our bot for spamming too many commands.")
        except:
          self.cmdintervals["strikes"][str(ctx.author.id)]=1
        em = discord.Embed(title="Stop spamming commands!", description="If you continue spam commands you will be bot banned.")
        try:
          await ctx.author.send(embed=em)
        except:
          await ctx.message.reply(embed=em)

  @commands.Cog.listener()
  async def on_message(self, message):
    try:
      channel = await self.bot.fetch_channel(message.channel.id)
      if isinstance(channel, discord.channel.DMChannel):
        return
    except:
      return
    if message.author == self.bot.user:
      if not str(message.guild.id) in self.logsdb.keys():
        self.logsdb[str(message.guild.id)]={"_id": str(message.guild.id)}
        self.logsdb[str(message.guild.id)]["lm"]=int(message.created_at.timestamp())
      else:
        self.logsdb[str(message.guild.id)]["lm"]=int(message.created_at.timestamp())
      return
    if f"<@{self.bot.user.id}>" in message.content or f"<@!{self.bot.user.id}>" in message.content:
      users = self.botbanned
      if str(message.author.id) in users.keys():
        if users[str(message.author.id)]["spam_banned"] or users[str(message.author.id)]["bot_banned"]:
          return
      prefix = self.logsdb
      try:
        prefix = prefix[str(message.guild.id)]["prefix"]
        prefix = str(prefix).lstrip('[').rstrip(']')
        await message.reply(f"Hi! My prefix is {prefix}!", mention_author=False)
      except:
        await message.reply("Hi! My prefix is 'CAP' or 'c/'!", mention_author=False)

  @commands.command()
  async def lm(self, ctx):
    try:
      await ctx.send("Last message sent by me in this server is created at <t:{}>".format(self.logsdb[str(ctx.guild.id)]["lm"]), allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except:
      return

  @commands.command()
  async def getElementById(self, ctx, id_:int):
    try:
      message = await ctx.channel.fetch_message(id_)
      await ctx.send(f"The content of that message was: \n```\n{message.content}```", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except:
      await ctx.send("Hey that message weren't sent inside this channel!")
      return

  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command()
  async def msg(self, ctx, *, message):
    if "`" in message:
      await ctx.send('sorry bud, you can\'t send ` in your message')
    else:
      urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message.lower())
      invites = re.findall("discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})", message.lower())
      if not urls and not invites:
        var1 = message.lower()
        words = var1.split()
        repeat = int(len(words))
        repeat_times = 0
        for i in words:
          if not i in swearwords:
              if repeat_times == repeat or repeat_times == repeat-1:
                author = ctx.message.author
                await ctx.send(content=f'`{message}`\n\n- {author}',allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
                try:
                  await ctx.message.delete()
                except:
                  pass
                break
              else:
                repeat_times+=1
          else:
            try:
              await ctx.message.delete()
            except:
              pass
            await ctx.send("You cannot send blacklisted words. Sorry but we've blacklisted 835 words that are either swears or close to swears. You can still manually speak most of them.")
            break
      else:
        try:
          await ctx.message.delete()
        except:
          pass
        await ctx.send("You cannot send links")
  
  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command()
  async def info(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("This bot sucks and this command is discontinued due to the owner's laziness")
  
  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command()
  async def suggestion(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("https://discord.gg/capitalism\nPost your suggestions in #suggestions channel!")
  
  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def amIright(self, ctx):
    response = ["yes","no","hmm idk"]
    await ctx.send(random.choice(response))
  
  @discord.ext.commands.cooldown(1, 3, commands.BucketType.user)
  @commands.command()
  async def choose(self, ctx, *, arg=None):
    if not arg==None:
      if "`" in arg:
        await ctx.send("I'm not choosing with options that has ` in them.")
      listrandom = arg.split()
      if len(listrandom) == 1:
        await ctx.send("that's only 1 choice bruh you need at least 2")
      else:
        for i in listrandom:
          urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', i.lower())
          invites = re.findall("discord(?:\.com|app\.com|\.gg)[\/invite\/]?(?:[a-zA-Z0-9\-]{2,32})", i.lower())
          if urls or invites:
            await ctx.send("You cannot choose between links.")
            return
        await ctx.send("`"+random.choice(listrandom)+"`",allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    else:
      await ctx.send(f"You need give at least 2 choices nerd. Format is {ctx.prefix}choose (1)  (2) ... (n)",discord.AllowedMentions(roles=False, users=False, everyone=False))
    
  @discord.ext.commands.cooldown(1, 2, commands.BucketType.user)
  @commands.command(name="8ball")
  async def _8ball(self, ctx):
      await ctx.reply("What question do you want to ask? :8ball:", mention_author=False)
      def check(author):
        def inner_check(message):
          if message.author != author:
              return False
          try:
              return True
          except ValueError:
              return False
        return inner_check
      try:
        msg = await self.bot.wait_for('message', timeout=30, check = check(ctx.author))
        if msg:
          await ctx.send("Ok, lemme think for a sec...")
          await asyncio.sleep(2)
          response = ["Yes.","Nah","I wouldn't care less.","maybe?idk","Certainly","Think about the results.","Hell nah"]
          await ctx.send(random.choice(response))
      except asyncio.TimeoutError:
        await ctx.reply("Imagine not answering", mention_author=False)
  
  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command(aliases=["link"])
  async def invite(self, ctx):
    await ctx.send("<https://discord.com/api/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands>")
  
  @discord.ext.commands.cooldown(1, 15, commands.BucketType.user)
  @commands.command()
  async def support(self, ctx):
    try:
      await ctx.message.delete()
    except:
      pass
    await ctx.send("https://discord.gg/capitalism")
  
  @commands.command()
  async def web(self, ctx):
    await ctx.send("https://discord.capitalismbot.repl.co")
  
  @discord.ext.commands.cooldown(1, 1, commands.BucketType.user)
  @commands.command(aliases=["howpog"])
  async def pograte(self, ctx,arg=None):
    number = random.randint(1,100)
    if arg ==None:
      embedPog = discord.Embed(
      title="POG RATE MACHINE",
      description="You are {}% pog <:littlepog:825452143657353226>".format(number),
      color=discord.Color.random()
      )
      await ctx.send(embed=embedPog)
    else:
      embedPog = discord.Embed(
      title="POG RATE MACHINE",
      description="{} is {}% pog <:littlepog:825452143657353226>".format(arg, number),
      color=discord.Color.random()
      )
      await ctx.send(embed=embedPog)

  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def guess(self, ctx):
    number = random.randint(1,100000)
    await ctx.reply("Guess a number between 1 and 100,000", mention_author=False)
    def check(author):
      def inner_check(message):
        if message.author != author:
            return False
        try:
            int(message.content)
            return True
        except ValueError:
            return False
      return inner_check
    try:
      msg = await self.bot.wait_for('message', timeout=30, check = check(ctx.author))
      attempt = int(msg.content)
      if msg:
        if not attempt<=0:
          if not attempt>=100001:
            if attempt == number:
              await msg.reply("Nice job! You got it correct. Screenshot this and post it in support server.", mention_author=False)
            else:
              await msg.reply(f"You're so bad smh you didn't get it right. The correct number was {number}", mention_author=False)
          else:
            await msg.reply("Dude that wasn't even in range 1-100,000", mention_author=False)
        else:
          await msg.reply("Dude that wasn't even in range 1-100,000", mention_author=False)
    except asyncio.TimeoutError:
      await ctx.reply("Imagine not answering", mention_author=False)
    
  @discord.ext.commands.cooldown(1,5,commands.BucketType.user)
  @commands.command()
  async def gcreate(self, ctx):
    await ctx. send("Starting a giveaway. Answer within 30 seconds for the following questions.")
    questions = ["Which channel should the giveaway be posted in?", "How long should it last? Use (s|m|h|d)", "What is the prize of the giveaway?"]
    answers=[]
    def check(m):
      return m.author == ctx.author and m.channel == ctx.channel
    for i in questions:
      await ctx.send(i)
      try:
        msg=await self.bot.wait_for('message', timeout=30.0, check=check)
      except asyncio.TimeoutError:
        await ctx.send("imagine not answering in time")
        return
      else:
        answers.append(msg.content)
    try:
      c_id=int(answers[0][2:-1])
    except:
      await ctx.send("That's not a valid channel id lmao")
      return
    channel=self.bot.get_channel(c_id)
    if channel == None:
      await ctx.send("Hey I could not find the channel to post the giveaway in.")
      return
    time_=self.convert(answers[1])
    if time_ == -1:
      await ctx.send("use (s|m|h|d) for time! Example: 10s for 10 seconds, 1h for 1 hour.")
      return
    elif time_ ==-2:
      await ctx.send("Time has to be a valid time integer+(s|m|h|d) ya idiot")
      return
    prize = answers[2]
    await ctx.send(f"Alright, the giveaway will be in {channel.mention} and will last {answers[1]} seconds!")
    em=discord.Embed(
      title="Capitalist's Giveaway!",
      description=f"**Prize:** {prize} (React with tada to enter)",
      color=discord.Color.random()
    )
    em.add_field(
      name="host by:",
      value =ctx.author.mention,
      inline=False
    )
    end = datetime.datetime.utcnow()+datetime.timedelta(seconds=time_)
    em.add_field(
      name="Ends at:",
      value=f"{end} UTC",
  )
    em.set_footer(
      text=f"Ends in {answers[1]} from when it started."
    )
    try:
      my_msg=await channel.send(embed=em)
    except:
      await ctx.send("Something went wrong, check if the channel was a text channel I have permissions to send messages in.")
      return
    await my_msg.add_reaction("<a:tadagif:827221672193032192>")
    await asyncio.sleep(time_)
    new_msg = await channel.fetch_message(my_msg.id)
    try:
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner=random.choice(users)
        await channel.send(f"Congrats to {winner.mention} winning {prize}!", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except:
        await channel.send(f"I could not determine a winner for the '*prize:* {prize}'' giveaway",allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
  
  def convert(self, time):
    pos = ["s","m","h","d"]
    time_dict = {"s":1,"m":60,"h":3600,"d":3600*24}
    unit=time[-1]
    if unit not in pos:
      return -1
    try:
      val = int(time[:-1])
    except:
      return -2
    return val*time_dict[unit]
  
  @commands.command(aliases=["gend"])
  async def reroll(self, ctx, channel:discord.TextChannel, id_:int):
    try:
      new_msg = await channel.fetch_message(id_)
    except:
      await channel.send("The message id was incorrect.")
    try:
      users=await new_msg.reactions[0].users().flatten()
      users.pop(users.index(self.bot.user))
      winner = random.choice(users)
      await channel.send(f"The new winner is {winner.mention}!")
    except:
      await channel.send("Something went wrong, are you sure anyone participated in the giveaway at all?")
  
  @discord.ext.commands.cooldown(1, 5, commands.BucketType.user)
  @commands.command()
  async def reminder(self, ctx):
    await ctx.send("Settings a reminder!\nWhat message would you like the bot to dm you?")
    def check(m):
      return m.channel == ctx.channel and m.author == ctx.author
    try:
      msg = await self.bot.wait_for('message', timeout=60.0, check=check)
      dm_msg = msg.content
      await ctx.send(f"Please state when you want to receive a DM reminder. (Use UTC)\nThe UTC time is currently {datetime.datetime.utcnow()}")
      try:
        msg = await self.bot.wait_for('message', timeout=60.0, check=check)
        try:
          time_ = datetime.datetime.fromisoformat(msg.content)
          await ctx.send(f"Alright, I'll remind you at {time_}", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
          await discord.utils.sleep_until(datetime.datetime.fromisoformat(msg.content))
          await ctx.author.send(f"You set a reminder: {dm_msg}")
        except Exception as e:
          print(e)
          await ctx.send("Invalid time provided.")
          ctx.command.reset_cooldown(ctx)
          return
      except asyncio.TimeoutError:
        await ctx.send("You did not reply in time.")
    except asyncio.TimeoutError:
      await ctx.send("You did not reply in time.")

  @commands.command()
  async def gstart(self, ctx, sec:str,*,prize:str):
    em=discord.Embed(
      title="Capitalist's Giveaway!",
      description=f"**Prize:** {prize} (React with tada to join)",
      color =discord.Color.random()
    )
    em.add_field(
      name="host by:",
      value =ctx.author.mention,
      inline=False
    )
    sec = self.convert(sec)
    end = datetime.datetime.utcnow()+datetime.timedelta(seconds=sec)
    em.add_field(
      name="Ends at:",
      value=f"{end} UTC",
    )
    em.set_footer(
      text=f"Ends {sec} seconds from start"
    )
    my_msg=await ctx.send(embed=em)
    await my_msg.add_reaction("<a:tadagif:827221672193032192>")
    await asyncio.sleep(sec)
    new_msg = await ctx.channel.fetch_message(my_msg.id)
    try:
        users = await new_msg.reactions[0].users().flatten()
        users.pop(users.index(self.bot.user))
        winner = random.choice(users)
        await ctx.send(f"Congrats to {winner.mention} winning {prize}!", allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    except:
        await ctx.send(f"I could not determine a winner for the '*prize:* {prize}' giveaway.",allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

  @commands.command(aliases=["tictactoe"])
  async def ttt(self, ctx, member:discord.Member):
    if member.id == 823933438079795260:
      await ctx.send("You cannot play with me because I'm too good at the game")
      return
    turns = 0
    options = ["a1", "a2","a3","b1","b2","b3","c1","c2","c3"]
    a1 = "⬛"
    a2 = "⬛"
    a3 = "⬛"
    b1 = "⬛"
    b2 = "⬛"
    b3 = "⬛"
    c1 = "⬛"
    c2 = "⬛"
    c3 = "⬛"
    def check(m):
      if m.author.id == member.id:
        if m.channel == ctx.channel:
          return True
    def check2(m):
      if m.author.id == ctx.author.id:
        if m.channel == ctx.channel:
          return True
    game_end = False
    mem=True
    autho=False
    while not game_end:
      if game_end:
        break
      if a1 == a2 and a1 == a3:
        if not a1 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif a1 == b2 and a1 == c3:
        if not a1 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif a1 == b1 and a1 == c1:
        if not a1 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif b1 == b2 and b1 == b3:
        if not b1 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif c1 == c2 and c1 == c3:
        if not c1 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif a2 == b2 and a2 == c2:
        if not a2 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif a3 == b3 and a3 == c3:
        if not a3 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      elif a3 == b2 and a3 == c1:
        if not a3 == "⬛":
          await ctx.send(f"{ctx.author.mention} won.")
          break
      embed = discord.Embed(
        title = "Tic Tac Toe Game",
        description = "`a1-a3`, `b1-b3`, `c1-c3` to place. letter = rows, numbers = columns\ntype `end` to end the game"
      )
      embed.add_field(
        name = "board",
        value = f"{a1}{a2}{a3}\n{b1}{b2}{b3}\n{c1}{c2}{c3}"
      )
      turns+=1
      while mem:
        await ctx.send(content=f"{member.mention} hey {ctx.author} wants to play tictactoe", embed=embed)
        try:
          option = await self.bot.wait_for('message', timeout=60.0, check=check)
        except asyncio.TimeoutError:
          await ctx.send("imagine not replying on time")
          game_end=True
          autho=False
          mem=False
          break
        option = option.content
        if option.lower() == "end":
          await ctx.send("game ends.")
          mem=False
          autho=False
          game_end=True
          break
        if not option in options:
          await ctx.send("that's not a valid option bruh")
          continue
        else:
          emoji = "❎"
          if option == "a1":
            if not a1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a1 = emoji
          elif option == "a2":
            if not a2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a2 = emoji
          elif option == "a3":
            if not a3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a3 = emoji
          elif option == "b1":
            if not b1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b1 = emoji
          elif option == "b2":
            if not b2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b2 = emoji
          elif option == "b3":
            if not b3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b3 = emoji
          elif option == "c1":
            if not c1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c1 = emoji
          elif option == "c2":
            if not c2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c2 = emoji
          elif option == "c3":
            if not c3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c3 = emoji
          mem=False
          autho=True
          break
      embed = discord.Embed(
        title = "Tic Tac Toe Game",
        description = "`a1-a3`, `b1-b3`, `c1-c3` to place. letter = rows, numbers = columns\ntype `end` to end the game"
      )
      embed.add_field(
        name = "board",
        value = f"{a1}{a2}{a3}\n{b1}{b2}{b3}\n{c1}{c2}{c3}"
      )
      if a1 == a2 and a1 == a3:
        if not a1 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif a1 == b2 and a1 == c3:
        if not a1 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif a1 == b1 and a1 == c1:
        if not a1 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif b1 == b2 and b1 == b3:
        if not b1 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif c1 == c2 and c1 == c3:
        if not c1 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif a2 == b2 and a2 == c2:
        if not a2 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif a3 == b3 and a3 == c3:
        if not a3 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      elif a3 == b2 and a3 == c1:
        if not a3 == "⬛":
          await ctx.send(f"{member.mention} won.")
          break
      turns+=1
      if turns == 10:
        await ctx.send(content = "Draw! you both suck", embed=embed)
        break
      while autho:
        await ctx.send(content=f"{ctx.author.mention} hey {member} wants to play tictactoe", embed=embed)
        try:
          option = await self.bot.wait_for('message', timeout=60.0, check=check2)
        except asyncio.TimeoutError:
          await ctx.send("imagine not replying on time")
          game_end=True
          mem=False
          autho=False
          break
        option = option.content
        if option.lower() == "end":
          await ctx.send("game ends.")
          mem=False
          autho=False
          game_end=True
          break
        if not option in options:
          await ctx.send("that's not a valid option bruh")
          continue
        else:
          emoji = "🔴"
          if option == "a1":
            if not a1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a1 = emoji
          elif option == "a2":
            if not a2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a2 = emoji
          elif option == "a3":
            if not a3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            a3 = emoji
          elif option == "b1":
            if not b1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b1 = emoji
          elif option == "b2":
            if not b2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b2 = emoji
          elif option == "b3":
            if not b3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            b3 = emoji
          elif option == "c1":
            if not c1 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c1 = emoji
          elif option == "c2":
            if not c2 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c2 = emoji
          elif option == "c3":
            if not c3 == "⬛":
              await ctx.send("that block is already taken!")
              continue
            c3 = emoji
          mem=True
          autho=False
          break
  
  # @commands.bot_has_permissions(manage_webhooks=True)
  @commands.command(aliases=["imp"])
  async def impersonate(self, ctx, user:discord.User, *, words):
    webhooks = await ctx.guild.webhooks()
    if user.id == 763854419484999722:
      await ctx.send(content="Hey server, this low life tried to impersonate the owner!\n<a:youtried:857689614259978290>")
      return
    webh=None
    for webhook in webhooks:
      if webhook.channel == ctx.channel and webhook.user == self.bot.user:
        webh = webhook
        break
    if webh == None:
      try:
        webh = await ctx.channel.create_webhook(name="NQN")
      except Exception as e:
        if isinstance(e, discord.HTTPException):
          await ctx.send("Well... this is awkward. But the webhook limit reached for this channel!")
          return
        print(e)
        return
    await webh.send(content=words, username=user.name, avatar_url=user.avatar_url, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))

  # @commands.bot_has_permissions(manage_webhooks=True)
  @commands.command()
  async def nqn(self, ctx, emoji):
    try:
      emoji = int(emoji)
      emoji = self.bot.get_emoji(emoji)
    except:
      try:
        emoji = emoji.split(":")
        emoji = emoji[-1].rstrip(">")
        emoji = self.bot.get_emoji(int(emoji))
      except:
        await ctx.send("Given input not in valid format")
        return
    if emoji == None:
      await ctx.send("Unable to get emoji, are you sure that emoji is from a server in our mutual servers?")
      return
    webhooks = await ctx.guild.webhooks()
    webh=None
    for webhook in webhooks:
      if webhook.channel == ctx.channel and webhook.user == self.bot.user:
        webh = webhook
        break
    if webh == None:
      try:
        webh = await ctx.channel.create_webhook(name="NQN")
      except:
        await ctx.send("I need `manage_webhook` permissions.")
    await webh.send(content=emoji, username=ctx.author.name, avatar_url=ctx.author.avatar_url)

def setup(bot):
    bot.add_cog(General(bot))