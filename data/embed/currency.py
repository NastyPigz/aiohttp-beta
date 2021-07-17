import discord

embed_Currency = discord.Embed(
    color=discord.Color.random()
)
embed_Currency.set_author(name="Currency")
embed_Currency.add_field(
    name="Currency commands",
    value="`coins`, `beg`, `work`, `inv`, `roll`, `roul`, `share`, `buy`, `sell`, `btc`, `bankspace`, `withdraw`, `deposit`, `shop`, `use`, `gift`,`mine`,`profile`, `multi`, `ads`, `buyad`, `bank`, `interest`, `banks`, `buybank`",
    inline=False
)