import json
import time
import threading
import websocket


__all__ = ['AsyncWebsocketClient']


class AsyncWebsocketClient:
    def __init__(self, url):
        self.url = url
        self.connected = False
        self.reconnect_interval = 5

        self._websocket_obj = None
        self._message_callback = None
        self._running = False

        self._thread = None
        self._thread_lock = threading.Lock()

    def on_message(self, ws_obj, message):
        self.connected = True
        if self._message_callback:
            self._message_callback(message)
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

    def register_message_callback(self, func):
        self._message_callback = func

    def get_status(self):
        return self._running

    def stop(self):
        self._websocket_obj.close()
        if self._thread:
            self._thread.join()
            self._thread = None

    def start(self):
        self._websocket_obj = websocket.WebSocketApp(
            url=self.url,
            on_error=self.on_error,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close)

        self._running = True
        self._thread = threading.Thread(target=self._websocket_obj.run_forever)
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
        self.start()




