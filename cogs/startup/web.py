from aiohttp import web
from discord.ext import commands, tasks
import discord
import os
import aiohttp

app = web.Application()
routes = web.RouteTableDef()

def setup(bot):
    bot.add_cog(Webserver(bot))

class Webserver(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.web_server.start()
        self.maindb = bot.maindb
        self.hidden=True

        @routes.get('/')
        async def welcome(request):
            return web.Response(text="Running")
        
        @routes.get('/vote')
        async def votewebhook(request):
          #remember to switch and edit in website.
          try:
            user = request.headers.get('user')
            website = request.headers.get('website')
            double_vote = request.headers.get('double_vote')
          except Exception as e:
            print(e)
            return web.Response(text='{"status": 404}\n')
          try:
            user_ = await self.bot.fetch_user(user)
          except:
            return web.Response(text='{"status": 404}\n')
          try:
            await user_.send(f"Thanks for voting for me on {website}!")
            if double_vote:
              self.maindb[str(user)]["inventory"]["coin_bag"]+=2
            else:
              self.maindb[str(user)]["inventory"]["coin_bag"]+=1
          except:
            pass
          return web.Response(text='{"status": 200}\n')
        
        @routes.get('/api')
        async def api(request):
          try:
            user = request.headers.get('user')
            data = request.headers.get('data')
            help_ = request.headers.get('help')
            if help_:
              return web.Response(text='{"status": 200, "message":"TO INCLUDE USER PLEASE USE ARGUMENT #USER# EXAMPLE: URL/API/V1?user=USER_ID TO INCLUDE DATA PLEASE USE ARGUMENT #DATA# EXAMPLE: URL/API/V1?user=USER_ID&DATA=STRING FOR DATA SUPPORT PLEASE ASK FOR SUPPORT IN DISCORD.GG/CAPITALISM"}\n')
          except:
            return web.Response(text='{"status": 404, "message":"One of the arguments were not satisfied."}\n')
          if user == None:
            return web.Response(text='{"status": 404, "message":"One of the arguments were not satisfied."}\n')
          if not str(user) in self.maindb.keys():
            return web.Response(text='{"status": 404, "message":"The user did not have a profile"}\n')
          else:
            try:
              if data == None:
                data_ = self.maindb[str(user)]
                text={"status":200, "message":data_}
                return web.json_response(text)
              data_ = self.maindb[str(user)][str(data)]
              text={"status": 200, "message":data_}
              return web.json_response(text)
            except:
              return web.Response(text='{"status": 404, "message":"The data provided was not valid"}\n')

        self.webserver_port = os.environ.get('PORT', 5000)
        app.add_routes(routes)

    @tasks.loop()
    async def web_server(self):
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, host='0.0.0.0', port=self.webserver_port)
        await site.start()

    @web_server.before_loop
    async def web_server_before_loop(self):
        await self.bot.wait_until_ready()