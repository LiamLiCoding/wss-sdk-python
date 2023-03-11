# WSS client
import communicate
import performance

API_KEY = ''
WEBSOCKET_URL = "wss://wssweb.net/ws/device/{api_key}"

websocket_client = communicate.get_websocket_client()
websocket_client.start(WEBSOCKET_URL.format(api_key=API_KEY))

monitor = performance.get_performance_monitor()
monitor.start()

while True:
    pass

