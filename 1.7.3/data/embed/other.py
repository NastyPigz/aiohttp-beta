import discord

embed_Other = discord.Embed(
    color=discord.Color.random()
)
embed_Other.set_author(name="Other")
embed_Other.add_field(
    name="Other Commands",
    value="`guess`,`8ball`, `ping`, `choose`, `gstart`, `gcreate`, `reroll`, `pograte`"
)
