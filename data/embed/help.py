import discord

async def embed_(ctx):
  try:
    prefix = ctx.prefix
  except:
    prefix = "/"
  em = discord.Embed(
          title="Help",
          url="https://www.google.com",
          description="Here are all the categories.",
          color=discord.Color.random()
      ).add_field(
          name="General",
          value=f"`{prefix}help general`"
      ).add_field(
          name="Moderation",
          value=f"`{prefix}help moderation`"
      ).add_field(
          name="Other",
          value=f"`{prefix}help other`"
      ).add_field(
          name="Emoji",
          value=f"`{prefix}help emoji`"
      ).add_field(
          name="Currency",
          value=f"`{prefix}help currency`"
      ).add_field(
        name="data",
        value = f"`{prefix}help data`"
      ).set_footer(
          text=f"{prefix}donate coming soon 👀 I will make it p2w (jk)"
  )
  return em