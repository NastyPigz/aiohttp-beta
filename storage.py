# discord.http.Route.BASE = 'https://discord.com/api/v9'
# async def get_gateway(self, *, encoding: str = 'json', zlib: bool = True) -> str:
#     return "wss://gateway.discord.gg?encoding=json&v=9&compress=zlib-stream"
# discord.http.HTTPClient.get_gateway = get_gateway
# class _Overwrites:
#     __slots__ = ('id', 'allow', 'deny', 'type')

#     def __init__(self, **kwargs):
#         self.id = kwargs.pop('id')
#         self.allow = int(kwargs.pop('allow_new', 0))
#         self.deny = int(kwargs.pop('deny_new', 0))
#         self.type = sys.intern(str(kwargs.pop('type')))

#     def _asdict(self):
#         return {
#             'id': self.id,
#             'allow': str(self.allow),
#             'deny': str(self.deny),
#             'type': self.type,
#         }
# discord.abc._Overwrites = _Overwrites
# from discord.ext.commands.bot import BotBase
# class Bot(BotBase, discord.Client):
#   pass
# commands.Bot = Bot