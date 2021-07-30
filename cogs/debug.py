import sys, discord
from discord.ext import commands
from jishaku.features.baseclass import Feature
from jishaku.cog import STANDARD_FEATURES, OPTIONAL_FEATURES

def setup(bot:commands.Bot):
  bot.add_cog(debug(bot=bot))

JISHAKU_HIDE = "True"

class debug(*OPTIONAL_FEATURES, *STANDARD_FEATURES):
    @Feature.Command(
        name="debug",
        aliases=["dbg"],
        hidden=JISHAKU_HIDE,
        invoke_without_command=True,
        ignore_extras=False,
        brief="Capitalism debugging commands",
        help="**Checks**\nBot Owner",
    )
    @commands.is_owner()
    async def jsk(self, ctx: commands.Context):
     super().jsk(ctx)