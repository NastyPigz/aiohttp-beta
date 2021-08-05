import discord

embed_Moderation = discord.Embed(
    color=discord.Color.random()
)
embed_Moderation.set_author(name="Moderation")
embed_Moderation.add_field(
    name="Moderation Commands",
    value="`ban`, `unban`, `purge`, `kick`, `prefix`"
)