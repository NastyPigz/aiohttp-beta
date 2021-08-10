from discord.ext import commands, tasks
import copy

def setup(bot):
    bot.add_cog(WebRequest(bot))

class WebRequest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.vote_request.start()
        self.update_main.start()
        self.update_sm.start()
        self.maindb = bot.maindb
        self.oldmain = copy.deepcopy(bot.maindb)
        self.oldsm = copy.deepcopy(bot.smdata)
        self.hidden=True
        self.session = bot.aiohttp_session
        self.smdata = bot.smdata
        
    @tasks.loop(seconds=1.0)
    async def vote_request(self):
      response = await self.session.get("/gv")
      data = await response.json()
      user = data.get('user')
      website = data.get('website')
      double_vote = data.get('double_vote')
      user_ = self.bot.get_user(int(user))
      if user_ is None:
        print(user, "is ID, he cannot be found.")
        return
      try:
        await user_.send(f"Thanks for voting for me on {website}!")
        if double_vote:
          self.maindb[str(user)]["inventory"]["coin_bag"]+=2
        else:
          self.maindb[str(user)]["inventory"]["coin_bag"]+=1
      except:
        pass
        
    @tasks.loop(seconds=1.0)
    async def update_main(self):
      if self.oldmain != self.maindb:
        await self.session.post("/pm", json=self.maindb)
        self.oldmain = copy.deepcopy(self.maindb)
    
    @tasks.loop(seconds=1.0)
    async def update_sm(self):
      if self.oldsm != self.smdata:
        await self.session.post("/ps", json=self.smdata)
        self.oldsm = copy.deepcopy(self.smdata)
