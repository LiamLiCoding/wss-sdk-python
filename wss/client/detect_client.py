import cv2
import base64
import time

from device import profiler
from camera import CameraManager
from detector import IntruderDetector
from net import AsyncWebsocketClient


__all__ = ['IntruderDetectClient']


class IntruderDetectClient(AsyncWebsocketClient):
    def __init__(self, url):
        AsyncWebsocketClient.__init__(self, url)
        self.profiler = None
        self.camera_manager = None
        self.camera_detector = None
        self._accept_operation_command = False

        self.init_profiler()
        self.init_net_callback()
        self.init_cameras()

    def init_cameras(self):
        self.camera_manager = CameraManager()
        self.camera_manager.initialize_cameras(1)

        self.camera_detector = IntruderDetector(save_path='output')
        self.camera_detector.register_callback(self.on_detect_event_change)
        self.camera_manager.set_detector(self.camera_detector)

        self.camera_manager.start_all()
        # self.camera_manager.show_all(show_time=True, show_fps=True)

    def init_profiler(self):
        self.profiler = profiler.Profiler()
        self.profiler.register_callback(self.on_profiler_update)

    def init_net_callback(self):
        self.register_message_callback(self.on_receive_message)

    def enable_detection(self, operation, feedback=True):
        if operation == 'enable':
            self.camera_manager.start_all()
        else:
            self.camera_manager.stop_all()

        print(operation + ' detection')
        if feedback:
            self.send({'operation_type': 'intruder_detection', 'operation': operation}, message_type='operation_feedback')

    def enable_profiler(self, operation, feedback=True):
        if operation == 'enable':
            self.profiler.start()
        else:
            self.profiler.stop()

        print(operation + ' profiler')
        if feedback:
            self.send({'operation_type': 'profiler', 'operation': operation}, message_type='operation_feedback')

    def on_receive_message(self, data):
        message = data.get('message', '')
        message_type = data.get('message_type', '')

        if message_type == 'init':
            self.on_init_message(message)
        elif message_type == 'operation':
            self.on_operation_message(message)

    def on_profiler_update(self, data):
        self.send(data, 'profiler')

    def on_detect_event_change(self, data):
        path = data.get('path', '')
        intruder_type = data.get('intruder_type', 0)

        if path and intruder_type:
            message = {'intruder_type': intruder_type, 'data_type': 'image',
                       'data_file': None, 'data_file_name': path.replace('output/', '')}
            with open(path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")
                message['data_file'] = image_data
            self.send(message=message, message_type='detect_event')

    def on_init_message(self, message):
        operation = message.get('operation', '')
        operation_type = message.get('operation_type', '')

        if operation_type == 'profiler':
            self.enable_profiler(operation, feedback=False)
        elif operation_type == 'intruder_detection':
            print("!!")
            # self.enable_detection(operation, feedback=False)

    def on_operation_message(self, message):
        if not self._accept_operation_command:
            return

        operation = message.get('operation', '')
        operation_type = message.get('operation_type', '')

        if operation_type == 'profiler':
            self.enable_profiler(operation)
        elif operation_type == 'intruder_detection':
            self.enable_detection(operation)
        elif operation_type == 'restart':
            self.restart()

    def restart(self):
        print("Received restart message")
        self.send({'operation_type': 'restart', 'operation': ''}, message_type='operation_feedback')


if __name__ == '__main__':
    API_KEY = 'Ff30WhLcvwASASpPWvrV8ZU2E-K_WLkGJeJWy0_3VRw'
    WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/device/{api_key}"
    client = IntruderDetectClient(url=WEBSOCKET_URL.format(api_key=API_KEY))
    client.connect()
