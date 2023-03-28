from wss.client import IntruderDetectClient

API_KEY = '1111'
WEBSOCKET_URL = "wss://wssweb.net/ws/device/{api_key}"

client = IntruderDetectClient(url=WEBSOCKET_URL.format(api_key=API_KEY))
client.start()
