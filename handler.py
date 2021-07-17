import random

async def ch(prefix, author, bot, content:str=None):
  #category handler here
  content=content
  tips = [
    f'Did you know that you could remove your data?\nUse `{prefix}help data` for more information!~',
    f'Have you checked out our currency system yet?\nUse `{prefix}help currency` for more information!~',
    f'Do you want to get rich in our currency?\nUse `{prefix}vote` to get 2-3 coin bags without running any commands!~ Then use `{prefix}use` to use the coin bags, it will give you coins.',
    f'Support us by voting!\nUse `{prefix}vote` to support us and get rewards too!',
    f'Have trouble using the bot? Commands not functioning?\nJoin our support server! `{prefix}support`',
    f'Want this bot in your own server?\nUse `{prefix}invite` to get the authorization link!',
    f'Check out our website!\nUse `{prefix}web` for the URL.',
    f'Did you know about CapitalismTheAFKGod?\nIt is a bot in our support server! Join support server to experience it ({prefix}support)',
    'Dont have slash commands in your server?\nTry inviting the bot again with application.commands scope!'
  ]
  try:
    if bot.usersdb[str(author.id)]["commands"]<=50:
      if random.randint(0, 3) == 2:
        if content is None:
          content=""
        content+=f"\n\n{random.choice(tips)}"
  except:
    if random.randint(0, 3) == 2:
        if content is None:
          content=""
        content+=f"\n\n{random.choice(tips)}"
  return content
