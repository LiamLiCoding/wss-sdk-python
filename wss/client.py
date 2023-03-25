import net

API_KEY = ''
WEBSOCKET_URL = "wss://wssweb.net/ws/device/{api_key}"

websocket_client = net.get_websocket_client()
websocket_client.start(WEBSOCKET_URL.format(api_key=API_KEY))

def main():
    pass


while True:
    pass
