from discord.ext import commands
import discord
import asyncio
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden=True
  
  @commands.command()
  async def nitro(self, ctx):
    embed=discord.Embed(
      title="Nitro",
      description="Expires in 23 hours"
    )
    embed.set_author(name="A WILD GIFT APPEARS!       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/764113682598723584/854854416108355614/EmSIbDzXYAAb4R7.png?width=216&height=216")
    buttons = [
      manage_components.create_button(
        style=ButtonStyle.green,
        label="            ACCEPT            ",
        custom_id="accept"
      )
    ]
    action_row=manage_components.create_actionrow(*buttons)
    mainMessage = await ctx.send(embed=embed, components=[action_row])
    try:
      interaction: ComponentContext = await manage_components.wait_for_component(self.bot, components=action_row, messages=mainMessage, timeout=10.0)
      # await interaction.defer(edit_origin=True)
      await interaction.send("https://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825", hidden=True)
      embed=discord.Embed(
        title="Nitro",
        description="Hmm, it seems like someone\nalready claimed this gift."
      )
      embed.set_author(name="A WILD GIFT APPEARS!       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/764113682598723584/854854416108355614/EmSIbDzXYAAb4R7.png?width=216&height=216")
      buttons = [
        manage_components.create_button(
          style=ButtonStyle.grey,
          label="            ACCEPT            ",
          custom_id="accept",
          disabled=True
        )
      ]
      action_row=manage_components.create_actionrow(*buttons)
      await mainMessage.edit(embed=embed, components=[action_row])
    except asyncio.TimeoutError:
      embed=discord.Embed(
        title="Nitro",
        description="Hmm, it seems like someone\nalready claimed this gift."
      )
      embed.set_author(name="A WILD GIFT APPEARS!       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
      embed.set_thumbnail(url="https://media.discordapp.net/attachments/764113682598723584/854854416108355614/EmSIbDzXYAAb4R7.png?width=216&height=216")
      buttons = [
        manage_components.create_button(
          style=ButtonStyle.grey,
          label="            ACCEPT            ",
          custom_id="accept",
          disabled=True
        )
      ]
      action_row=manage_components.create_actionrow(*buttons)
      await mainMessage.edit(embed=embed, components=[action_row])

def setup(bot):
    bot.add_cog(Help(bot))