import json
import time
import queue
import threading
import websocket

from wss.core.exception import ConnectionException


__all__ = ['AsyncWebsocketClient']


class AsyncWebsocketClient:
    def __init__(self, url):
        self.url = url
        self.connected = False
        self.reconnect_interval = 5

        self._ws = None
        self._message_callback = None
        self._running = False

        self._message_queue = queue.Queue()
        self._message_thread = None

        self._thread = None
        self._thread_lock = threading.Lock()

    def on_open(self, ws_obj):
        self.connected = True
        print('AsyncWebsocketClient: Successfully connected!')

    def on_close(self, ws_obj, close_status_code, close_msg):
        self.connected = False
        self.reconnect()
        print('AsyncWebsocketClient: Connection closed, close code:{}, close message:{}'.format(close_status_code,
                                                                                                close_msg))

    def on_message(self, ws_obj, message):
        print("AsyncWebsocketClient: Received message：{}".format(message))
        self.connected = True
        if self._message_callback:
            self._message_callback(json.loads(message))

    def on_error(self, ws_obj, error):
        self.connected = False
        if isinstance(error, ConnectionRefusedError) or isinstance(error, websocket.WebSocketConnectionClosedException):
            print("AsyncWebsocketClient: - Connection Error:{}".format(error))
        else:
            print("AsyncWebsocketClient: - Other Error:{}".format(error))

    def register_message_callback(self, func):
        self._message_callback = func

    def get_status(self):
        return self._running

    def disconnect(self):
        self._ws.close()
        if self._thread:
            self._thread.join()
            self._thread = None

        if self._message_thread:
            self._message_thread.join()
            self._message_thread = None

    def connect(self):
        self._ws = websocket.WebSocketApp(
            url=self.url,
            on_error=self.on_error,
            on_open=self.on_open,
            on_message=self.on_message,
            on_close=self.on_close)

        self._running = True

        self._thread = threading.Thread(target=self._ws.run_forever)
        self._thread.start()

        self._message_thread = threading.Thread(target=self._async_send_message)
        self._message_thread.start()

    def reconnect(self):
        self._ws.close()
        time.sleep(self.reconnect_interval)
        print("AsyncWebsocketClient: Reconnect ....")
        self.connect()

    def send(self, message, message_type):
        if not self.connected:
            raise ConnectionException('AsyncWebsocketClient - connection is closed')

        data = {'message': message,
                'message_type': message_type}

        self._message_queue.put(json.dumps(data))

    def _async_send_message(self):
        while True:
            message = self._message_queue.get()
            try:
                self._ws.send(message)
                print('AsyncWebsocketClient - Send message')
            except websocket.WebSocketConnectionClosedException:
                print('AsyncWebsocketClient: Send messages failed, connection is closed')
            except Exception as ee:
                print('Other exception, detail:{}'.format(ee))




