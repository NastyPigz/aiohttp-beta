import discord
from discord.ext import commands, tasks
import asyncio
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext
from discord_slash.utils.manage_components import create_select, create_select_option

class Computer(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.selector_message_ids = []
    self.selector_check.start()
    self.hidden=True
  
  @commands.command()
  async def computer(self, ctx):
    buttons = [
      manage_components.create_button(
          style=ButtonStyle.green,
          label="pro",
          custom_id="pro"
      )
    ]
    action_row = manage_components.create_actionrow(*buttons)
    mainMessage = await ctx.send(content="ㅤ", components=[action_row])
    while True:
      try:
          interaction: ComponentContext = await manage_components.wait_for_component(
            self.bot,
            components=action_row,
            messages=mainMessage,
            timeout = 30.0,
          )
          if interaction.origin_message_id != mainMessage.id:
            await interaction.defer(edit_origin=True)
            continue
          select = create_select(
            options=[
              create_select_option(
              label='bruheurbuwihqruh',
              value="no" 
              )
            ],
            min_values=1, 
            max_values=1
          )
          action_row2=manage_components.create_actionrow(select)
          selectorMessage=await interaction.send("u a noob", components=[action_row2], hidden=True)
          print(selectorMessage)
          self.selector_message_ids.append(selectorMessage.id)
          # if interaction.author != ctx.author:
          #   await interaction.defer(edit_origin=True)
          #   continue
      except asyncio.TimeoutError:
        break
  
  @tasks.loop()
  async def selector_check(self):
    if self.selector_message_ids == []:
      return
    interaction: ComponentContext = await manage_components.wait_for_component(
      self.bot,
      messages=self.selector_message_ids,
      timeout = 30.0,
    )
    await interaction.send(interaction.selected_options)

def setup(bot):
  bot.add_cog(Computer(bot))