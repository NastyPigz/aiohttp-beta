import discord, os, sys, io
from discord.ext import commands, tasks
import asyncio, re
from discord.http import Route

json = __import__("json")

def setup(bot):
  bot.add_cog(SocialMedia(bot))

class SocialMedia(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.launched=[]
    self.botbanned = bot.botbanned
    with open("cogs/commands/data.json", "r") as f:
      self.data = json.load(f)
    self.bot.smdata = self.data
    self.wait_for_launch.start()

  @tasks.loop()
  async def wait_for_launch(self):
    def check(m):
      return m.guild == None and (m.content.lower() == "launch" or m.content.lower() == "reboot")
    msg = await self.bot.wait_for('message', check=check)
    try:
      if self.botbanned[str(msg.author.id)]["bot_banned"] or self.botbanned[str(msg.author.id)]["spam_banned"]:
        return
    except:
      pass
    if not msg.author.id in self.launched:
      if msg.content.lower() == "launch":
        loop = asyncio.get_running_loop()
        loop.create_task(self.launch_alt(msg))
      else:
        if msg.author.id == 763854419484999722:
          await msg.author.send("rebooting the bot...")
          os.execv(sys.executable, ['python'] + sys.argv)
        else:
          pass

  def Json(self, data1):
    with open("cogs/commands/data.json", "w") as file1:
      file1.truncate(0)
      file1.seek(0)
      file1.write(json.dumps(data1, indent=4))

  @commands.command()
  async def post(self, ctx):
    try:
      file = ctx.message.attachments[0]
      bytes_ = await file.read()
      bytes_ = io.BytesIO(bytes_)
      await ctx.send(file=discord.File(bytes_, filename=file.filename))
    except:
      try:
        r = r'((?:https:\/\/media\.discordapp\.net\/attachments\/)\d+\/\d+\/(\w+\.\w+))'
        matches = re.findall(r, ctx.message.content)
        r= r'((?:https:\/\/cdn\.discordapp\.com\/attachments\/)\d+\/\d+\/(\w+\.\w+))'
        matches2 = re.findall(r, ctx.message.content)
        if len(matches) == 0 and len(matches2) == 0:
          raise Exception
        else:
          if len(matches) == 0:
            matches = matches2
          else:
            matches = matches
          URL = matches[0][0]
          image = await self.bot.aiohttp_session.get(URL)
          bytes_ = await image.read()
          bytes_ = io.BytesIO(bytes_)
          await ctx.send(file=discord.File(bytes_, filename=matches[0][1]))
      except:
        embed = discord.Embed()
        url = ctx.message.content.lower().replace(str(ctx.prefix), "").replace("post", "")
        embed.set_image(url=url)
        await ctx.send("If the image doesn't load, it was invalid.", embed=embed)

  @commands.command()
  async def create(self, ctx):
    with open("cogs/commands/data.json", "r+") as f:
      data = json.load(f)
      if str(ctx.author.id) in data.keys():
        await ctx.send("You already registered for CAPcord!")
        return
      else:
        await ctx.send("Alrighty! Please provide me a 6-digit password in our DMs.")
        def check(m):
          return m.author == ctx.author and m.guild == None and len(m.content) == 6
        try:
          msg = await self.bot.wait_for('message', timeout=60.0, check=check)
          await msg.author.send("You are now registered for CAPcord!")
          self.data[str(ctx.author.id)]={}
          self.data[str(ctx.author.id)]["password"]=msg.content
          self.Json(self.data)
          return
        except asyncio.TimeoutError:
          await ctx.send("Ok, register cancelled.")
          return

  async def always_detect_message(self, ctx):
    def check(m):
      return m.author == ctx.author and m.guild == None and not m.author.id == 823933438079795260
    while True:
      try:
        msg = await self.bot.wait_for('message', timeout=300.0, check=check)
        if msg.content.lower() == "add":
          try:
            await msg.author.send("Ok, please give me their USER ID.")
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            try:
              user_id = int(msg.content)
              if user_id == ctx.author.id:
                await msg.author.send("hahaha... you can't be friends with yourself")
                continue
              user = self.bot.get_user(user_id)
              if user == None:
                raise Exception
              else:
                if str(user.id) not in self.data.keys():
                  await msg.author.send("They aren't using CAPcord, sad.")
                else:
                  try:
                    if user.id in self.data[str(ctx.author.id)]["requests"]:
                      try:
                        self.data[str(ctx.author.id)]["requests"].pop(self.data[str(ctx.author.id)]["requests"].index(user.id))
                        self.data[str(user.id)]["requests"].pop(self.data[str(user.id)]["requests"].index(ctx.author.id))
                      except:
                        pass
                      try:
                        if ctx.author.id in self.data[str(user.id)]["blocked"]:
                          await msg.author.send("Sorry, the user blocked you.")
                          self.Json(self.data)
                          continue
                      except:
                        pass
                      try:
                        self.data[str(ctx.author.id)]["friends"].append(user.id)
                      except:
                        self.data[str(ctx.author.id)]["friends"]=[user.id]
                      try:
                        self.data[str(user.id)]["friends"].append(ctx.author.id)
                      except:
                        self.data[str(user.id)]["friends"]=[ctx.author.id]
                      self.Json(self.data)
                      await msg.author.send("You have accepted their friend request!")
                      continue
                  except:
                    pass
                  try:
                    if user.id in self.data[str(ctx.author.id)]["friends"]:
                      await msg.author.send("Okay, I get it. Your guys are friends. But stop trying to add them again!")
                      continue
                  except:
                    pass
                  try:
                    if user.id in self.data[str(ctx.author.id)]["requests"]:
                      await msg.author.send("You already sent them a request! Tell them to accept it smh.")
                      continue
                  except:
                    pass
                  try:
                    if ctx.author.id in self.data[str(user.id)]["blocked"]:
                      await msg.author.send("Sorry, the user blocked you.")
                      continue
                    if user.id in self.data[str(ctx.author.id)]["blocked"]:
                      await msg.author.send("You blocked them... ")
                      continue
                  except:
                    pass
                  try:
                    setting = self.data[str(user.id)]["settings"]["friend_setting"]
                    if not setting:
                      await msg.author.send("Oop, they have friend request settings off. Must have been a famous guy!")
                      continue
                  except:
                    pass
                  try:
                    self.data[str(user.id)]["requests"].append(ctx.author.id)
                    self.Json(self.data)
                  except:
                    self.data[str(user.id)]["requests"]=[ctx.author.id]
                    self.Json(self.data)
                  await msg.author.send("Alright, sent them a request!")
            except:
              await msg.author.send("Uhh, I can't find them.")
          except asyncio.TimeoutError:
            await msg.author.send("Alright, no one was added.")
        elif msg.content.lower() == "remove":
          try:
            await msg.author.send("Ok, please give me their USER ID.")
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            try:
              user_id = int(msg.content)
              user = self.bot.get_user(user_id)
              if user == None:
                raise Exception
              else:
                if str(user.id) not in self.data.keys():
                  await msg.author.send("They aren't using CAPcord, sad.")
                else:
                  try:
                    if user.id in self.data[str(ctx.author.id)]["friends"]:
                      try:
                        self.data[str(ctx.author.id)]["friends"].pop(self.data[str(ctx.author.id)]["friends"].index(user.id))
                        self.data[str(user.id)]["friends"].pop(self.data[str(user.id)]["friends"].index(ctx.author.id))
                        self.Json(self.data)
                        await msg.author.send(f"Successfully removed {user} from your friend list.")
                      except:
                        await msg.author.send("Hmm, something went wrong. If this happens again, ask this issue in the support server")
                    else:
                      await msg.author.send("You guys aren't friends, sadly.")
                  except:
                    await msg.author.send("You don't have any friends, sad.")
            except:
              await msg.author.send("That's not a valid input.")
          except asyncio.TimeoutError:
            await ctx.send("Alright, no friends was removed.")
        elif msg.content.lower() == "close":
          self.launched.pop(self.launched.index(ctx.author.id))
          await msg.author.send("Thank you for using CAPcord. Goodbye!")
          break
        elif msg.content.lower() == "toggle":
          try:
            self.data[str(ctx.author.id)]["settings"]["friend_setting"] = False if self.data[str(ctx.author.id)]["settings"]["friend_setting"] else True
            settings = self.data[str(ctx.author.id)]["settings"]["friend_setting"]
          except:
            self.data[str(ctx.author.id)]["settings"]={}
            self.data[str(ctx.author.id)]["settings"]["friend_setting"]=False
            settings = self.data[str(ctx.author.id)]["settings"]["friend_setting"]
          self.Json(self.data)
          await msg.author.send(f"Turned friends requests ALLOWED to {settings}")
        elif msg.content.lower() == 'menu':
          try:
            friends = self.data[str(ctx.author.id)]["friends"]
            content="**Home**\n__Updates__: CAPcord v0.0.1 Release Added CONTACTS\n**Friends**\n"
            for friend_id in friends:
              friend_name = self.bot.get_user(friend_id)
              content+=f"{friend_name} ID => {friend_name.id}\n"
            if len(friends) == 0:
              content+="None\n"
            content+="\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
          except:
            content="**Home**\n__Updates__: CAPcord v0.0.0 Release Added CONTACTS\n**Friends**\n__None__\n\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
          try:
            if len(self.data[str(ctx.author.id)]["requests"]) > 0:
              string_requests=""
              for user_id in self.data[str(ctx.author.id)]["requests"]:
                ac_user = self.bot.get_user(user_id)
                string_requests+="{}#{} ID => {}\n".format(ac_user.name, ac_user.discriminator, ac_user.id)
              content+=f"\n\n**NEW FRIEND REQUESTS**\n{string_requests}\nTo accept a friend request run `add`, then their USER ID"
          except:
            pass
          await msg.author.send(content)
        elif msg.content.lower() == 'posts':
          try:
            try:
              await msg.author.send("Who's posts would you like to view? Please send their USER ID. (If you don't respond, I'll send your own posts)")
              msg = await self.bot.wait_for('message', timeout=10.0, check=check)
              try:
                user_id = int(msg.content)
                user = self.bot.get_user(user_id)
                if user == None:
                  raise Exception
                try:
                  if user.id == msg.author.id:
                    posts = self.data[str(msg.author.id)]["posts"]
                    embeds=[]
                    for post in posts:
                      if post.startswith("https"):
                        embeds.append(
                          {
                            "title":"Post {}".format(posts.index(post)),
                            "description": str(post),
                            "image":{
                              "url": post
                            }
                          }
                        )
                      else:
                        embeds.append(
                          {
                            "title":"Post {}".format(posts.index(post)),
                            "description": str(post)
                          }
                        )
                    r=Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
                    await self.bot.http.request(
                      r,
                      json={
                        "content": "Your posts:",
                        "embeds": embeds
                      }
                    )
                    continue
                  if not user.id in self.data[str(msg.author.id)]["friends"]:
                    await msg.author.send("That guy isn't your friend.")
                    continue
                  try:
                    posts = self.data[str(user.id)]["posts"]
                    embeds=[]
                    for post in posts:
                      if post.startswith("https"):
                        embeds.append(
                          {
                            "title":"Post {}".format(posts.index(post)),
                            "description": str(post),
                            "image":{
                              "url": post
                            }
                          }
                        )
                      else:
                        embeds.append(
                          {
                            "title":"Post {}".format(posts.index(post)),
                            "description": str(post)
                          }
                        )
                    r=Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
                    await self.bot.http.request(
                      r,
                      json={
                        "content": f"{user}'s Posts",
                        "embeds": embeds
                      }
                    )
                  except:
                    await msg.author.send("Hmm, they don't have any posts.")
                except Exception as e:
                  print(e)
                  await msg.author.send("You don't have any friends, sad.")
              except:
                await msg.author.send("Uhh, I cannot find that user.")
            except asyncio.TimeoutError:
              try:
                posts = self.data[str(msg.author.id)]["posts"]
                embeds=[]
                for post in posts:
                  if post.startswith("https"):
                    embeds.append(
                      {
                        "title":"Post {}".format(posts.index(post)),
                        "description": str(post),
                        "image":{
                          "url": post
                        }
                      }
                    )
                  else:
                    embeds.append(
                      {
                        "title":"Post {}".format(posts.index(post)),
                        "description": str(post)
                      }
                    )
                r=Route('POST', '/channels/{channel_id}/messages', channel_id=msg.channel.id)
                await self.bot.http.request(
                  r,
                  json={
                    "content": "Your posts:",
                    "embeds": embeds
                  }
                )
              except Exception as e:
                print(e)
                await msg.author.send("Hmm, you don't have any posts.")
          except:
            await msg.author.send("No posts were found.")
        elif 'post' in msg.content.lower():
          try:
            url = msg.attachments[0].url
            try:
              if len(self.data[str(ctx.author.id)]["posts"]) > 4:
                self.data[str(ctx.author.id)]["posts"].pop(0)
              self.data[str(ctx.author.id)]["posts"].append(url)
            except:
              self.data[str(ctx.author.id)]["posts"]=[url]
            await msg.author.send("Posted.")
          except:
            content = msg.content.lower().lstrip("post ")
            try:
              if len(self.data[str(ctx.author.id)]["posts"]) > 4:
                self.data[str(ctx.author.id)]["posts"].pop(0)
              if not content in self.data[str(ctx.author.id)]["posts"]:
                self.data[str(ctx.author.id)]["posts"].append(content)
              else:
                await msg.author.send("You cannot make the same post twice.")
                continue
            except:
              self.data[str(ctx.author.id)]["posts"]=[content]
            await msg.author.send("Posted.")
          self.Json(self.data)
        elif msg.content.lower() == 'unblock':
          try:
            await msg.author.send("Ok, please give me their USER ID.")
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            try:
              user_id = int(msg.content)
              user = self.bot.get_user(user_id)
              if user == None:
                raise Exception
              else:
                if str(user.id) not in self.data.keys():
                  await msg.author.send("They aren't using CAPcord, sad.")
                else:
                  try:
                    if user.id in self.data[str(ctx.author.id)]["blocked"]:
                      try:
                        self.data[str(ctx.author.id)]["blocked"].pop(self.data[str(ctx.author.id)]["blocked"].index(user.id))
                        self.Json(self.data)
                        await msg.author.send(f"Successfully unblocked {user} .")
                      except Exception as e:
                        print(e)
                        await msg.author.send("Hmm, something went wrong. If this happens again, ask this issue in the support server")
                    else:
                      await msg.author.send("You never blocked that poor guy.")
                  except:
                    await msg.author.send("You don't have any blocked users.")
            except:
              await msg.author.send("That's not a valid input.")
          except asyncio.TimeoutError:
            await ctx.send("Alright, no friends was removed.")
        elif msg.content.lower() == 'block':
          try:
            await msg.author.send("Ok, please give me their USER ID.")
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            try:
              user_id = int(msg.content)
              if user_id == ctx.author.id:
                await msg.author.send("hahaha... you can't block yourself")
                continue
              user = self.bot.get_user(user_id)
              if user == None:
                raise Exception
              else:
                if str(user.id) not in self.data.keys():
                  await msg.author.send("They aren't using CAPcord, sad.")
                else:
                  try:
                    if user.id in self.data[str(ctx.author.id)]["blocked"]:
                      await msg.authorl.send("How many times do u want to block them?!?! They're already blocked.")
                      continue
                  except:
                    pass
                  try:
                    if user.id in self.data[str(ctx.author.id)]["requests"]:
                      self.data[str(ctx.author.id)]["requests"].pop(self.data[str(ctx.author.id)]["requests"].index(user.id))
                  except:
                    pass
                  try:
                    if ctx.author.id in self.data[str(user.id)]["requests"]:
                      self.data[str(user.id)]["requests"].pop(self.data[str(user.id)]["requests"].index(ctx.author.id))
                  except:
                    pass
                  try:
                    if user.id in self.data[str(ctx.author.id)]["friends"]:
                      self.data[str(ctx.author.id)]["friends"].pop(self.data[str(ctx.author.id)]["friends"].index(user.id))
                  except:
                    pass
                  try:
                    if ctx.author.id in self.data[str(user.id)]["friends"]:
                      self.data[str(user.id)]["friends"].pop(self.data[str(user.id)]["friends"].index(ctx.author.id))
                  except:
                    pass
                  try:
                    self.data[str(ctx.author.id)]["blocked"].append(user.id)
                    self.Json(self.data)
                  except:
                    self.data[str(ctx.author.id)]["blocked"]=[user.id]
                    self.Json(self.data)
                  await msg.author.send("They're now BLOCKED.")
            except:
              await msg.author.send("Uhh, I can't seemed to find that user.")
          except asyncio.TimeoutError:
            await msg.author.send("Alright, no one was added.")
        elif msg.content.lower() == 'send':
          await msg.author.send("Please tell me which friend you would like to call (give USER ID )")
          try:
            msg = await self.bot.wait_for('message', timeout=10.0, check=check)
            try:
              user_id = int(msg.content)
              user = self.bot.get_user(user_id)
              if user == None:
                raise Exception
              else:
                if str(user.id) not in self.data.keys():
                  await msg.author.send("They aren't using CAPcord, sad.")
                else:
                  try:
                    if user.id in self.data[str(ctx.author.id)]["friends"]:
                      try:
                        await user.send(f"Call from {msg.author} ID => {msg.author.id}\nSay `accept`, `a` or `yes` to accept.")
                        await msg.author.send("Dialing...")
                        try:
                          def check2(m):
                            return m.guild == None and m.author == user
                          msg2 = await self.bot.wait_for('message', timeout=60.0, check=check2)
                          if msg2.content.lower() in ["accept", "a", "yes"]:
                            await msg.author.send("Connected! say `hang` to hang up.")
                            await msg2.author.send("Connected! say `hang` to hang up.")
                            while True:
                              def check3(m):
                                return (m.author == msg.author or m.author == msg2.author) and m.guild==None
                              try:
                                msg3 = await self.bot.wait_for('message', timeout=30.0, check=check3)
                                if msg3.content.lower() == "hang":
                                  await msg.author.send("Call hanged up.")
                                  await msg2.author.send("Call hanged up.")
                                  break
                                if msg3.author == msg.author:
                                  await msg2.author.send("**{}**: {}".format(msg3.author, msg3.content))
                                else:
                                  await msg.author.send("**{}**: {}".format(msg3.author, msg3.content))
                              except asyncio.TimeoutError:
                                await msg.author.send("Call disconnected.")
                                await msg2.author.send("Call disconnected.")
                                break
                          else:
                            await msg2.author.send("Call declined.")
                            await msg.author.send("Your call was declined.")
                        except asyncio.TimeoutError:
                          await msg.author.send("Call ended.")
                      except:
                        try:
                          await msg.author.send("Hmm, seems like either of you blocked me or closed DMs.")
                        except:
                          pass
                    else:
                      await msg.author.send("You guys aren't friends, sadly.")
                  except:
                    await msg.author.send("You don't have any friends, sad.")
            except:
              await msg.author.send("That's not a valid input.")
          except asyncio.TimeoutError:
            await msg.author.send("Alright, no new calls were started.")
        else:
          print(msg.content)
      except asyncio.TimeoutError:
        self.launched.pop(self.launched.index(ctx.author.id))
        await ctx.author.send("Thank you for using CAPcord. Goodbye!\n\n**TIMEOUT**")
        break
    return

  async def launch_alt(self, msg_):
    if msg_.author.id in self.launched:
      await msg_.author.send("You already launched the app!")
      return
    with open("cogs/commands/data.json","r+") as f:
      data = json.load(f)
      if not str(msg_.author.id) in data.keys():
        await msg_.author.send(f"New to CAPcord? Register now for free!\nRegistering is as easy as CAPcreate\n__Note:__ execute this in a server.")
        return
      else:
        await msg_.author.send("Please send your 6-digit password here")
        def check(m):
          return m.author == msg_.author and m.guild == None and len(m.content) == 6
        try:
          msg = await self.bot.wait_for('message', timeout=60.0, check=check)
          if not msg.content==data[str(msg.author.id)]["password"]:
            await msg.author.send("Hey hacker! Stop trying to login this guy's account.")
            return
          else:
            self.launched.append(msg_.author.id)
            try:
              friends = self.data[str(msg_.author.id)]["friends"]
              content="**Home**\n__Updates__: CAPcord v0.0.1 Release Added CONTACTS\n**Friends**\n"
              for friend_id in friends:
                friend_name = self.bot.get_user(friend_id)
                content+=f"{friend_name} ID => {friend_name.id}\n"
              content+="\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
            except:
              content="**Home**\n__Updates__: CAPcord v0.0.0 Release Added CONTACTS\n**Friends**\n__None__\n\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
            try:
              if len(self.data[str(msg_.author.id)]["requests"]) > 0:
                string_requests=""
                for user_id in self.data[str(msg_.author.id)]["requests"]:
                  ac_user = self.bot.get_user(user_id)
                  string_requests+="{}#{} ID => {}\n".format(ac_user.name, ac_user.discriminator, ac_user.id)
                content+=f"\n\n**NEW FRIEND REQUESTS**\n{string_requests}\nTo accept a friend request run `add`, then their USER ID"
            except:
              pass
            await msg.author.send(
              content
              )
            await self.always_detect_message(msg)
        except asyncio.TimeoutError:
          await msg_.channel.send("You did not provide a password. Process cancelled.")
          return

  @commands.command()
  async def launch(self, ctx):
    if ctx.author.id in self.launched:
      await ctx.send("You already launched the app!")
      return
    with open("cogs/commands/data.json","r+") as f:
      data = json.load(f)
      if not str(ctx.author.id) in data.keys():
        await ctx.send(f"New to CAPcord? Register now for free!\nRegistering is as easy as {ctx.prefix}create")
        return
      else:
        await ctx.send("Please send me your password in our DMs")
        def check(m):
          return m.author == ctx.author and m.guild == None and len(m.content) == 6
        try:
          msg = await self.bot.wait_for('message', timeout=60.0, check=check)
          if not msg.content==data[str(ctx.author.id)]["password"]:
            await msg.author.send("Hey hacker! Stop trying to login this guy's account.")
            return
          else:
            self.launched.append(ctx.author.id)
            try:
              friends = self.data[str(ctx.author.id)]["friends"]
              content="**Home**\n__Updates__: CAPcord v0.0.1 Release Added CONTACTS\n**Friends**\n"
              for friend_id in friends:
                friend_name = self.bot.get_user(friend_id)
                content+=f"{friend_name} ID => {friend_name.id}\n"
              content+="\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
            except:
              content="**Home**\n__Updates__: CAPcord v0.0.0 Release Added CONTACTS\n**Friends**\n__None__\n\n**VALID INVOKES**\n`add`, `remove`, `send`, `block`, `unblock`, `close`, `menu`, `toggle`, `posts`, `post`"
            try:
              if len(self.data[str(ctx.author.id)]["requests"]) > 0:
                string_requests=""
                for user_id in self.data[str(ctx.author.id)]["requests"]:
                  ac_user = self.bot.get_user(user_id)
                  string_requests+="{}#{} ID => {}\n".format(ac_user.name, ac_user.discriminator, ac_user.id)
                content+=f"\n\n**NEW FRIEND REQUESTS**\n{string_requests}\nTo accept a friend request run `add`, then their USER ID"
            except:
              pass
            await msg.author.send(
              content
              )
            await self.always_detect_message(ctx)
        except asyncio.TimeoutError:
          await ctx.send("You did not provide a password. Process cancelled.")
          return
