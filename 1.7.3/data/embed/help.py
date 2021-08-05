import discord

async def embed_(ctx):
  em = discord.Embed(
          title="Help",
          url="https://www.google.com",
          description="Here are all the categories.",
          color=discord.Color.random()
      )
  return em