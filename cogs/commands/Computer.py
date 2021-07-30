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
    self.selector_check_1.start()
    self.hidden=True
    select = create_select(
      options=[
        create_select_option(
        label='Me',
        value="Me" 
        ),
        create_select_option(
        label='You',
        value="You" 
        ), 
      ],
      min_values=1, 
      max_values=1
    )
    self.select_template_one=manage_components.create_actionrow(select)
  
  @commands.command()
  async def computer(self, ctx):
    buttons = [
      manage_components.create_button(
          style=ButtonStyle.green,
          label="chat",
          custom_id="chat"
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
          await interaction.send("Who do you want to chat with", components=[self.select_template_one], hidden=True)
          # if interaction.author != ctx.author:
          #   await interaction.defer(edit_origin=True)
          #   continue
      except asyncio.TimeoutError:
        break
  
  @tasks.loop()
  async def selector_check_1(self):
    interaction: ComponentContext = await manage_components.wait_for_component(
      self.bot,
      components=self.select_template_one,
      timeout = 30.0,
    )
    await interaction.defer(hidden=True)
    await interaction.send(str(interaction.selected_options).rstrip("]").lstrip("["), hidden=True)
    if "Me" in interaction.selected_options:
      await interaction.author.send("Hi!")
    else:
      await interaction.send("Well... talk to yourself then!", hidden=True)

def setup(bot):
  bot.add_cog(Computer(bot))