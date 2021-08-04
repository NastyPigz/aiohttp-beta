import discord, typing, asyncio
from discord.ext import commands

#number value, not string. This stores a list important to a part of the help command subclass
# 600034099918536718 is _WeDemBois_. The most pog dev in history
admins = [
  763854419484999722,
  725081836874760224,
  521347381636104212,
  600034099918536718,
]

class HelpBase(discord.ui.View):
  def __init__(self, *, timeout=30.0, message):
    super().__init__(timeout=timeout)
    self.mainMessage = message

  async def on_timeout(self):
    await self.mainMessage.edit(
      view=ClosedPaginator()
    )

class HelpMenuSelect(discord.ui.Select):
  def __init__(self, embeds, **kwargs):
    super().__init__(**kwargs)
    self.things = kwargs
    self.embeds = embeds
  
  async def callback(self, interaction: discord.Interaction):
    selected_option = self.values[0]
    if selected_option.lower() == "all":
      embed = self.embeds[0]
    else:
      for embed in self.embeds:
        if embed.title.lower() == selected_option.lower():
          embed = embed
          break
    select = HelpMenuSelect(self.embeds, **self.things)
    view = discord.ui.View()
    view.add_item(select)
    await interaction.response.edit_message(
      embed=embed,
      view=view
    )

class ClosedPaginator(discord.ui.View):
  def __init__(self):
    super().__init__()
    self.add_item(discord.ui.Button(
      style=discord.ButtonStyle.link,
      label="Invite me",
      url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
      row=0
    ))
    self.add_item(discord.ui.Button(
      style=discord.ButtonStyle.link,
      label="Support Server",
      url="https://discord.gg/capitalism",
      row=0
    ))
    self.add_item(discord.ui.Button(
      style=discord.ButtonStyle.red,
      label="Timeout",
      disabled=True,
      row=0
    ))

class BackButton(discord.ui.Button):
  def __init__(self, item, **kwargs):
    super().__init__(**kwargs)
    self.thing = item

  async def callback(self, interaction: discord.Interaction):
    if interaction.user.id != self.thing.user.id:
      current = self.thing.current-1
      if current == len(self.thing.embeds):
        current = 0
      elif current < 0:
        current = len(self.thing.embeds) - 1
      await interaction.response.send_message(
        embed = self.thing.embeds[current],
        view=self.thing.selector,
        ephemeral=True
      )
    else:
      self.thing.current-=1
      if self.thing.current == len(self.thing.embeds):
        self.thing.current = 0
      elif self.thing.current < 0:
        self.thing.current = len(self.thing.embeds) - 1
      view = HelpBase(message=interaction.message)
      view.add_item(BackButton(
        self.thing, 
        style=discord.ButtonStyle.success,
        label="⬅️",
        custom_id = "back",
        row=0
      ))
      view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=f"Page {int(self.thing.current+1)}/{len(self.thing.embeds)}",
        custom_id = "cur",
        disabled=True,
        row=0
      ))
      view.add_item(FrontButton(
        self.thing, 
        style=discord.ButtonStyle.success,
        label="➡️",
        custom_id = "front",
        row=0
      ))
      view.add_item(self.thing.link1)
      view.add_item(self.thing.link2)
      await interaction.response.edit_message(
        embed=self.thing.embeds[self.thing.current],
        view=view
      )

class FrontButton(discord.ui.Button):
  def __init__(self, item, **kwargs):
    super().__init__(**kwargs)
    self.thing = item

  async def callback(self, interaction: discord.Interaction):
    if interaction.user.id != self.thing.user.id:
      current = self.thing.current+1
      if current == len(self.thing.embeds):
        current = 0
      elif current < 0:
        current = len(self.thing.embeds) -1
      await interaction.response.send_message(
        embed = self.thing.embeds[current],
        view=self.thing.selector,
        ephemeral=True
      )
    else:
      self.thing.current+=1
      if self.thing.current == len(self.thing.embeds):
        self.thing.current = 0
      elif self.thing.current < 0:
        self.thing.current = len(self.thing.embeds) -1
      view = HelpBase(message=interaction.message)
      view.add_item(BackButton(
        self.thing, 
        style=discord.ButtonStyle.success,
        label="⬅️",
        custom_id = "back",
        row=0
      ))
      view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=f"Page {int(self.thing.current+1)}/{len(self.thing.embeds)}",
        custom_id = "cur",
        disabled=True,
        row=0
      ))
      view.add_item(FrontButton(
        self.thing, 
        style=discord.ButtonStyle.success,
        label="➡️",
        custom_id = "front",
        row=0
      ))
      view.add_item(self.thing.link1)
      view.add_item(self.thing.link2)
      await interaction.response.edit_message(
        embed=self.thing.embeds[self.thing.current],
        view=view
      )

class Paginator(discord.ui.View):
  def __init__(self, *, embeds:typing.List[discord.Embed], timeout: typing.Union[float], user:typing.Union[discord.Member], selector: typing.Union[discord.ui.View]):
    super().__init__(timeout=timeout)
    self.selector=selector
    self.embeds=embeds
    self.current = 0
    self.user=user
    self.link1 = discord.ui.Button(
      style=discord.ButtonStyle.link,
      label="Invite me",
      url="https://discord.com/oauth2/authorize?client_id=823699570147065876&permissions=268823670&redirect_uri=https%3A%2F%2Fdiscord.com%2Foauth2%2Fauthorize%3Fclient_id%3DCapitalismBot&scope=bot%20applications.commands",
      row=1
    )
    self.add_item(
      self.link1
    )
    self.link2 = discord.ui.Button(
      style=discord.ButtonStyle.link,
      label="Support Server",
      url="https://discord.gg/capitalism",
      row=1
    )
    self.add_item(
      self.link2
    )

  async def on_timeout(self):
    pass

  @discord.ui.button(
    style=discord.ButtonStyle.success,
    label="⬅️",
    custom_id = "back",
    row=0
  )
  async def a_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
    if interaction.user.id != self.user.id:
      current = self.current-1
      if current == len(self.embeds):
        current = 0
      elif current < 0:
        current = len(self.embeds) - 1
      await interaction.response.send_message(
        embed = self.embeds[current],
        view=self.selector,
        ephemeral=True
      )
    else:
      self.current-=1
      if self.current == len(self.embeds):
        self.current = 0
      elif self.current < 0:
        self.current = len(self.embeds) - 1
      view = HelpBase(message=interaction.message)
      view.add_item(BackButton(
        self,
        style=discord.ButtonStyle.success,
        label="⬅️",
        custom_id = "back",
        row=0
      ))
      view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=f"Page {int(self.current+1)}/{len(self.embeds)}",
        custom_id = "cur",
        disabled=True,
        row=0
      ))
      view.add_item(FrontButton(
        self, 
        style=discord.ButtonStyle.success,
        label="➡️",
        custom_id = "front",
        row=0
      ))
      view.add_item(self.link1)
      view.add_item(self.link2)
      await interaction.response.edit_message(
        embed=self.embeds[self.current],
        view=view
      )
  
  @discord.ui.button(
    style=discord.ButtonStyle.secondary,
    label=f"Page 1/7",
    custom_id = "cur",
    disabled=True,
    row=0
  )
  async def b_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
    pass

  @discord.ui.button(
    style=discord.ButtonStyle.success,
    label="➡️",
    custom_id = "front",
    row=0
  )
  async def c_callback(self, button: discord.ui.Button, interaction: discord.Interaction):
    if interaction.user.id != self.user.id:
      current = self.current+1
      if current == len(self.embeds):
        current = 0
      elif current < 0:
        current = len(self.embeds) - 1
      await interaction.response.send_message(
        embed = self.embeds[current],
        view=self.selector,
        ephemeral=True
      )
    else:
      self.current+=1
      if self.current == len(self.embeds):
        self.current = 0
      elif self.current < 0:
        self.current = len(self.embeds) - 1
      view = HelpBase(message=interaction.message)
      view.add_item(BackButton(
        self, 
        style=discord.ButtonStyle.success,
        label="⬅️",
        custom_id = "back",
        row=0
      ))
      view.add_item(discord.ui.Button(
        style=discord.ButtonStyle.secondary,
        label=f"Page {int(self.current+1)}/{len(self.embeds)}",
        custom_id = "cur",
        disabled=True,
        row=0
      ))
      view.add_item(FrontButton(
        self,
        style=discord.ButtonStyle.success,
        label="➡️",
        custom_id = "front",
        row=0
      ))
      view.add_item(self.link1)
      view.add_item(self.link2)
      await interaction.response.edit_message(
        embed=self.embeds[self.current],
        view=view
      )

class CustomHelp(commands.HelpCommand):
  def get_command_signature(self, command):
    return '%s%s %s' % (
      self.context.clean_prefix, 
      command.qualified_name, 
      command.signature
    )

  async def send_bot_help(self, mapping):
    embed = discord.Embed(
      title="Help", 
      url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", 
      description="Here are all the categories.",
      color=discord.Colour.random()
      )
    options=[discord.SelectOption(
      label="All",
      value="All"
    )]
    d = self.context.bot.cogs
    paginationList = [None]
    continue_=None
    for key in d.keys():
      try:
        if not self.context.author.id in admins:
          if d[key].hidden:
            continue
        elif continue_:
          if d[key].hidden:
            continue
        elif continue_ == False:
          pass
        else:
          def check(m):
            return m.author == self.context.author and m.channel == self.context.channel
          await self.context.send("say r or n")
          msg = await self.context.bot.wait_for('message', check=check)
          if not msg.content.lower() == "r":
            continue_ = True
            continue
          else:
            continue_ = False
            pass
      except:
        continue
      embed.add_field(
        name=key.capitalize(),
        value="`{}`".format(self.context.prefix+'help '+key.lower()), 
        inline=True
      )
      options.append(
        discord.SelectOption(
          label=key.lower().capitalize(),
          value=key.lower().capitalize()
        )
      )
      paginationList.append(await self.get_cog_help(d[key]))
    paginationList[0]=embed
    view = discord.ui.View()
    item = HelpMenuSelect(paginationList, options=options, min_values=1, max_values=1, row=0)
    view.add_item(item)
    view = Paginator(embeds=paginationList, timeout=30.0, user=self.context.author, selector=view)
    mainMessage = await self.context.reply(
      embed = embed,
      view=view,
      mention_author=False
    )
    async def help_task(view, mainMessage, CP):
      while True:
        await view.wait()
        await mainMessage.edit(
          view=CP()
        )
        break
      return True
    await self.context.bot.loop.create_task(help_task(view, mainMessage, ClosedPaginator))

  async def get_cog_help(self, cog):
    try:
      # if cog.qualified_name.lower()=="jishaku":
      #   return
      # else:
      #   try:
      #     if cog.hidden:
      #       return
      #   except:
      #     return
      cmd=[]
      for commandd in cog.walk_commands():
        if (commandd.hidden==True):
          continue
        cmd.append(commandd)
      command = ''
      for cc in cmd:
        command += f'`{cc.name}`, '
      embed = discord.Embed(
        title=cog.qualified_name, 
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQm", 
        description=command,
        color=discord.Colour.random()
        )
      return embed
    except Exception as e:
      print(e)

  async def send_cog_help(self, cog):
    if cog.qualified_name.lower()=="jishaku":
      return
    else:
      try:
        if cog.hidden:
          return
      except:
        return
    cmd=[]
    for commandd in cog.walk_commands():
      if (commandd.hidden==True):
        continue
      cmd.append(commandd)
    command = ''
    for cc in cmd:
      command += f'`{cc.name}`, '
    embed = discord.Embed(
      title=cog.qualified_name, 
      url="https://www.youtube.com/watch?v=dQw4w9WgXcQm", 
      description=command,
      color=discord.Colour.random()
      )
    await self.context.send(embed=embed)

  async def send_group_help(self, group):
    if not self.context.author.id in admins:
      return await self.context.message.add_reaction(":think:825452368128376843")
    content=""
    for command in group.commands:
      content+="`{}`, ".format(command.name)
    await self.context.send(content)

  async def send_command_help(self, command):
    if not isinstance(command, commands.core.Command):
      clss = self.context.bot.get_commands(command)
    else:
      clss = command
    if not clss.cog == None:
      if ((clss.hidden == True) and (self.context.author.id not in admins)) or ((clss.cog.hidden == True) and (self.context.author.id not in admins)):
        return await self.context.message.add_reaction(":think:825452368128376843")
    else:
      return await self.context.message.add_reaction(":think:825452368128376843")
    embed = discord.Embed(
      title=command,
      color=discord.Colour.random()
    )
    embed.add_field(
        name='Usage:',
        value=self.get_command_signature(command),
        inline=False
    )
    if len(clss.aliases) == 0:
      embed.add_field(
        name='Aliases:',
        # value='None, like 0. Zip, Natta, None.',
        value='None',
        inline=False
      )
    else:
      embed.add_field(
        name='Aliases:',
        value=', '.join(clss.aliases),
        inline=False
      )
    if not clss._buckets._cooldown == None:
      rate = clss._buckets._cooldown.rate
      embed.add_field(
        name='Cooldown:',
        value="{} seconds every {} {}".format(clss._buckets._cooldown.per, rate, "commands" if rate > 1 else "command"),
        inline=False
      )
    else:
      embed.add_field(
        name='Cooldown:',
        value="None",
        inline=False
      )
    embed.add_field(
      name='Description:',
      value=clss.help,
      inline=False
    )

    embed.set_footer(text="\"<>\" => required | \"[]\" => optional")

    await self.context.send(embed=embed)