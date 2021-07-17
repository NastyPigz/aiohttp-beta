from discord.ext import commands
import discord
import asyncio
from data.embed.general import embed_General
from data.embed.help import embed
from data.embed.mod import embed_Moderation
from data.embed.emoji import embed_Emoji
from data.embed.currency import embed_Currency
from data.embed.other import embed_Other
from data.json.help import help_menu
from discord_slash.utils import manage_components
from discord_slash.model import ButtonStyle
from discord_slash.context import ComponentContext

class Help(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.hidden=True

  def em(self, ctx):
    return embed(ctx)

  @commands.command()
  async def help(self, ctx,arg=None):
    embed=self.em(ctx)
    embed.color=discord.Color.random()
    embed_General.color = discord.Color.random()
    embed_Moderation.color = discord.Color.random()
    embed_Other.color = discord.Color.random()
    embed_Emoji.color = discord.Color.random()
    embed_Currency.color = discord.Color.random()
    # embed.add_field(name="REPLIT", value="REPLIT")
    inpt = None
    if arg == None:
      paginationList = [embed, embed_General, embed_Moderation, embed_Other, embed_Emoji, embed_Currency]
      current = 0
      buttons = [
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Invite me",
                url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
            ),
            manage_components.create_button(
                style=ButtonStyle.URL,
                label="Support Server",
                url="https://discord.gg/capitalism",
            ),
          ]
      action_row = manage_components.create_actionrow(*buttons)
      buttons2 = [
            manage_components.create_button(
                style=ButtonStyle.green,
                label="⬅️",
                custom_id="back",
            ),
            manage_components.create_button(
                style=ButtonStyle.grey,
                label=f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                disabled=True
            ),
            manage_components.create_button(
                style=ButtonStyle.green,
                label="➡️",
                custom_id="front"
            )
          ]
      action_row2 = manage_components.create_actionrow(*buttons2)
      mainMessage = await ctx.reply(
        embed = paginationList[current],
        # components = [
        #     action_row, action_row2
        # ],
        components=[action_row2, action_row],
        mention_author=False
      )
      while True:
        try:
            interaction: ComponentContext = await manage_components.wait_for_component(
              self.bot,
              components=action_row2,
              messages=mainMessage,
              timeout = 30.0,
            )
            if interaction.origin_message_id != mainMessage.id:
              await interaction.defer(edit_origin=True)
              continue
            if interaction.author != ctx.author:
              await interaction.defer(edit_origin=True)
              continue
            if interaction.custom_id == "back":
                current -= 1
            elif interaction.custom_id == "front":
                current += 1
            if current == len(paginationList):
                current = 0
            elif current < 0:
                current = len(paginationList) - 1
            buttons = [
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Invite me",
                  url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
              ),
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Support Server",
                  url="https://discord.gg/capitalism",
              ),
            ]
            action_row = manage_components.create_actionrow(*buttons)
            buttons2 = [
                  manage_components.create_button(
                      style=ButtonStyle.green,
                      label="⬅️",
                      custom_id = "back"
                  ),
                  manage_components.create_button(
                      style=ButtonStyle.grey,
                      label=f"Page {int(paginationList.index(paginationList[current])) + 1}/{len(paginationList)}",
                      custom_id = "cur",
                      disabled=True
                  ),
                  manage_components.create_button(
                      style=ButtonStyle.green,
                      label="➡️",
                      custom_id = "front"
                  )
                ]
            action_row2 = manage_components.create_actionrow(*buttons2)
            await interaction.edit_origin(
                embed = paginationList[current],
                components = [action_row2, action_row]
            )
        except asyncio.TimeoutError:
            buttons = [
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Invite me",
                  url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands"
              ),
              manage_components.create_button(
                  style=ButtonStyle.URL,
                  label="Support Server",
                  url="https://discord.gg/capitalism"
              ),
              manage_components.create_button(
                  style=ButtonStyle.red,
                  label="Timeout",
                  disabled=True
              ),
            ]
            action_row = manage_components.create_actionrow(*buttons)
            await mainMessage.edit(
                components = [
                    action_row
                ]
            )
            break
    else:
      inpt = arg.lower()
      if inpt == "all":
        await ctx.reply(embed=embed, mention_author=False)
      elif inpt == "moderation":
        await ctx.reply(embed=embed_Moderation, mention_author=False)
      elif inpt == "other":
        await ctx.reply(embed = embed_Other, mention_author=False)
      elif inpt == "emoji":
        await ctx.reply(embed = embed_Emoji, mention_author=False)
      elif inpt == "currency":
        await ctx.reply(embed = embed_Currency, mention_author=False)
      elif inpt == "general":
        await ctx.reply(embed=embed_General, mention_author=False)
      elif inpt == "data":
        embed_Data = discord.Embed(
          color = discord.Color.random()
        )
        embed_Data.add_field(
          name = "`Data Type Commands`",
          value = "`removedata`, `removelogs`, `removeall`"
        )
        await ctx.reply(embed=embed_Data, mention_author=False)
      else:
        try:
          command = self.bot.get_command(inpt)
          inpt = command.name.lower()
          try:
            desc = help_menu[inpt]["use"]
            cooldown = help_menu[inpt]["cooldown"]
            alias = help_menu[inpt]["aliases"]
            footer = help_menu[inpt]["footer"]
            em = discord.Embed(
              title = inpt,
              description = f"__**Description**__: {desc} \n __**Cooldown**__: {cooldown} seconds \n __**Aliases**__: {alias}"
            )
            em.set_footer(text=f"Command format with CAP as prefix--- {footer}")
            await ctx.reply(embed=em, mention_author=False)
          except:
            await ctx.reply(f"{command.name} is a valid command but no help source was found.", mention_author=False)
        except:
          await ctx.reply("that is not a valid category or command!", mention_author=False)
  
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