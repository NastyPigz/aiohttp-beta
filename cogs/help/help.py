from discord.ext import commands
import discord
import asyncio

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
    button = discord.ui.Button(
      style=discord.ButtonStyle.green,
      label="            ACCEPT            ",
      custom_id="accept"
    )
    view = discord.ui.View()
    view.add_item(button)
    mainMessage = await ctx.send(embed=embed, view=view)
    interaction = await self.bot.wait_for('interaction')
    await interaction.followup.send(content="https://tenor.com/view/dance-moves-dancing-singer-groovy-gif-17029825", ephemeral=True)
    embed=discord.Embed(
      title="Nitro",
      description="Hmm, it seems like someone\nalready claimed this gift."
    )
    embed.set_author(name="A WILD GIFT APPEARS!       ⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀")
    embed.set_thumbnail(url="https://media.discordapp.net/attachments/764113682598723584/854854416108355614/EmSIbDzXYAAb4R7.png?width=216&height=216")
    buttons = discord.ui.Button(
        style=discord.ButtonStyle.gray,
        label="            ACCEPT            ",
        custom_id="accept",
        disabled=True
      )
    view = discord.ui.View()
    view.add_item(buttons)
    await interaction.edit_original_message(embed=embed, view=view)

def setup(bot):
    bot.add_cog(Help(bot))