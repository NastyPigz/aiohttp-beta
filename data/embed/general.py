import discord

embed_General = discord.Embed(
    color=discord.Color.random()
)
embed_General.set_author(name = "General")
embed_General.add_field(
    name="General Commands:",
    value="`amIright`, `bruh`, `msg`, `info`, `support`, `link`, `suggestion`,`rules`,`vote`"
)