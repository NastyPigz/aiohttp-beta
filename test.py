client = {}
prefixes = []

@client.event
async def on_message(message):
  content_lower = message.content.lower()
  content = message.content
  bool_list = [content.startswith(i) for i in prefixes]
  for i in bool_list:
    if i:
      prefix=i
  if any(bool_list):
    amount = len(prefix)
    args = content[amount:].split(" ")
    command = args[0].lower()
    match command:
      case "ping" | "pong":
        content = "Pong!" if command == "ping" else "Ping!"
        await message.channel.send(content+str(round(client.latency)))
      
      case "say":
        if len(args) > 0:
          await message.channel.send(' '.join(args))