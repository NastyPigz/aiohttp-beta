from discord.ext import commands, tasks
import aiohttp, os, discord, asyncio, json
from discord.http import Route

def setup(bot:commands.Bot):
  bot.add_cog(experiment(bot=bot))

class experiment(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.session = bot.aiohttp_session
  #   token = str(os.getenv("TOKEN"))
  #   self.payload = {
  #     'op': 2,
  #     "d": {
  #       "token": token,
  #       "properties": {
  #           "$os": "windows",
  #           "$browser": "chrome",
  #           "$device": 'pc'
  #       }
  #     }
  #   }

  # @commands.Cog.listener()
  # async def on_ready(self):
  #   session = aiohttp.ClientSession()
  #   ws = await session.ws_connect('wss://gateway.discord.gg/?v=9&encording=json')
  #   msg = await ws.receive()
  #   data = msg.json()
  #   heartbeat_interval = data['d']['heartbeat_interval'] / 1000
  #   self.send_heart_beat.start(heartbeat_interval, ws)
  #   await ws.send_json(self.payload)
  #   while True:
  #     print("Loop!")
  #     msg = await ws.receive()
  #     try:
  #       print(msg.json())
  #       dict_ = msg.json()
  #       if dict_.get('t') == 'MESSAGE_CREATE':
  #         if dict_.get('d') != None:
  #           print(dict_.get('d'))
  #     except:
  #       continue

  # @tasks.loop()
  # async def send_heart_beat(self, interval, session):
  #   print(interval)
  #   await asyncio.sleep(interval)
  #   heartbeatJSON = {
  #       "op": 1,
  #       "d": "null"
  #   }
  #   await session.send_json(heartbeatJSON)

  @commands.command()
  async def embeds(self, ctx):
    with open("test.py", 'rb') as fp:
      file1 = discord.File(fp, filename="test.py")
    with open("handler.py", "rb") as fp:
      file2 = discord.File(fp, filename="handler.py")
    await ctx.send(content="re",files=[file1, file2])
    r=Route('POST', '/channels/{channel_id}/messages', channel_id=ctx.channel.id)
    res = await self.bot.http.request(
      r,
      json={
        "content": "Hello, World!",
        "tts": False,
        "embeds": [
          {
          "title": "Hello, Embed!",
          "description": "This is an embedded message."
          },
          {
            "title": "Hello, Embed!",
            "description": "This is another embedded message."
          },
          {
            "title": "Hello, Embed!",
            "description": "This is an embedded message."
          },
          {
            "title": "Hello, Embed!",
            "description": "This is an embedded message."
          },
          {
            "title": "Hello, Embed!",
            "description": "This is an embedded message."
          }
        ],
        "allowed_mentions": {
          "parse": ["users", "roles"],
          "replied_user": False
        },
        "message_reference": {
          "message_id": ctx.message.id,
          "guild_id": ctx.guild.id,
          "fail_if_not_exists": False
        }
      })
    await ctx.send(res)

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