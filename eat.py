import aiohttp
session = aiohttp.ClientSession()
ws = await session.ws_connect(
    'http://webscoket-server.org/endpoint')

while True:
  msg = await ws.receive()
  if msg.tp == aiohttp.MsgType.text:
      if msg.data == 'close':
          await ws.close()
          break
      else:
          ws.send_str(msg.data + '/answer')
  elif msg.tp == aiohttp.MsgType.closed:
      break
  elif msg.tp == aiohttp.MsgType.error:
      break

# import websocket
# import json
# import threading
# import time

# def send_json_request(ws, request):
#     ws.send(json.dumps(request))

# def recieve_json_response(ws):
#     response = ws.recv()
#     if response:
#         return json.loads(response)

# def heartbeat(interval, ws):
#     print('Heartbeat begin')
#     while True:
#         time.sleep(interval)
#         heartbeatJSON = {
#             "op": 1,
#             "d": "null"
#         }
#         send_json_request(ws, heartbeatJSON)
#         print("Heartbeat sent")

# ws = websocket.WebSocket()
wss://gateway.discord.gg?encoding=json&v=9&compress=zlib-stream
# ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
# event = recieve_json_response(ws)

# heartbeat_interval = event['d']['heartbeat_interval'] / 1000
# threading._start_new_thread(heartbeat, (heartbeat_interval, ws))

token = ""
payload = {
    'op': 2,
    "d": {
        "token": token,
        "properties": {
            "$os": "windows",
            "$browser": "chrome",
            "$device": 'pc'
        }
    }
}
# send_json_request(ws, payload)

# while True:
#     event = recieve_json_response(ws)

#     try:
#         print(f"{event['d']['author']['username']}: {event['d']['content']}")
#         op_code = event('op')
#         if op_code == 11:
#             print('heartbeat received')
#     except:
#         pass