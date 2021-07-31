import discord, os
from discord.ext import commands
from pprint import pprint as pp
import functools

async def get_pre(bot, message):
  return "!#"

class MyContext(commands.Context):
  async def send(self, content=None,
        *,
        tts=None,
        embed=None,
        embeds=None,
        file=None,
        files=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        reference=None,
        view=None,
        components=None,
        chb=True
      ):
    try:
      return await super().send(content=content, embed=embed,file=file, files=files, delete_after=delete_after, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False))
    # except discord.HTTPException:
    except Exception as e:
      print(e)

  async def reply(self, content=None,
        *,
        tts=None,
        embed=None,
        embeds=None,
        file=None,
        files=None,
        delete_after=None,
        nonce=None,
        allowed_mentions=None,
        reference=None,
        mention_author=None,
        view=None,
        components=None,
        chb=True):
    try:
      return await super().reply(content=content, embed=embed, file=file, files=files, delete_after=delete_after, allowed_mentions=discord.AllowedMentions(roles=False, users=False, everyone=False, replied_user=False))
    # except discord.HTTPException:
    except Exception as e:
      print(e)
      pass

class MyBot(commands.Bot):
    async def is_owner(self, user: discord.User):
        usable_list = [725081836874760224,763854419484999722]
        if user.id in usable_list:
            return True
        return await super().is_owner(user)

    async def get_context(self, message, *, cls=MyContext):
        return await super().get_context(message, cls=cls)

intents = discord.Intents.all()
intents.presences=False
bot = MyBot(case_insensitive=True,
command_prefix=get_pre,
strip_after_prefix=True,
intents=intents, help_command=None)
# commands.cooldown(1, 5)(bot.get_command('help'))

@bot.listen()
async def on_ready():
  print("Raaannning")
  input("PLS EXIT\n")
  exit(0)

@bot.check
async def commands_check(ctx):
  return True

@bot.command()
async def help(ctx):
  await ctx.send("no help")

# @bot.event
# async def on_socket_response(data):
# # print('\n' + str(data) + '\n')
# # return
#
# data = data or {}
# d = data.get('d') or {}
# assert d is not None
# guild_id = d.get('guild_id', 0)
#
# if data['t'] == 'GUILD_CREATE':
#     print(d['name'])
#     print(d.get('threads'))
#
# if int(guild_id) == 817958268097789972:
#     print('Socket data:')
#     # print(data['t'])
#     # print(data['d'])
#     print(data)


# @bot.event
# async def on_message(msg):
#   await bot.process_commands(msg)

@bot.command()
async def bruh(ctx):
    await ctx.send('Pong!')

@bot.command()
async def ping(ctx: commands.Context):
    await ctx.send('Pong!')

bot.run(os.getenv("TOKEN"))