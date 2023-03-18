import json
import threading
import time
import websocket


g_WEBSOCKET_CLIENT = None


def get_websocket_client():
    global g_WEBSOCKET_CLIENT
    if not g_WEBSOCKET_CLIENT:
        g_WEBSOCKET_CLIENT = AsyncWebsocketClient()
    return g_WEBSOCKET_CLIENT


def websock_send(message, message_type):
    if not get_websocket_client().get_status():
        raise RuntimeError('Please start websocket client first')
    get_websocket_client().send(message, message_type)


class AsyncWebsocketClient:
    def __init__(self):
        self._websocket_obj = None
        self.url = ''
        self._running = False
        self.connected = False
        self.reconnect_interval = 5
        self._thread = None
        self._thread_lock = threading.Lock()

    def on_message(self, ws_obj, message):
        self.connected = True
        print("AsyncWebsocketClient: Received message：{}".format(message))

    def on_error(self, ws_obj, error):
        self.connected = False
        if isinstance(error, ConnectionRefusedError) or isinstance(error, websocket.WebSocketConnectionClosedException):
            print("AsyncWebsocketClient: - Connection Error:{}".format(error))
        else:
            print("AsyncWebsocketClient: - Other Error:{}".format(error))

    def on_open(self, ws_obj):
        self.connected = True
        print('AsyncWebsocketClient: Successfully connected!')

    def on_close(self, ws_obj, close_status_code, close_msg):
        self.connected = False
        self.reconnect()
        print('AsyncWebsocketClient: Connection closed, close code:{}, close message:{}'.format(close_status_code,
                                                                                                close_msg))

    def get_status(self):
        return self._running

    def stop(self):
        self._websocket_obj.close()
        if self._thread:
            self._thread.join()
            self._thread = None

    def start(self, url):
        self._websocket_obj = websocket.WebSocketApp(
            url=url,
            on_error=self.on_error,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close)

        self.url = url
        self._running = True
        self._thread = threading.Thread(target=self._websocket_obj.run_forever)
        self._thread.daemon = True
        self._thread.start()

    def send(self, message, message_type):
        data = {'message': message,
                'message_type': message_type}
        if self.connected:
            try:
                self._websocket_obj.send(json.dumps(data))
            except websocket.WebSocketConnectionClosedException:
                print('AsyncWebsocketClient: Send messages failed, connection is closed')

    def reconnect(self):
        self._websocket_obj.close()
        time.sleep(self.reconnect_interval)
        print("AsyncWebsocketClient: Reconnect ....")
        self.start(self.url)


class AsyncHttpClient:
    def __init__(self, device_key):
        self.m_device_key = device_key

    @staticmethod
    def get_timestamp():
        millis = int(round(time.time() * 1000))
        return millis

    # TODO: HTTP client is still developing
    def send(self):
        pass

