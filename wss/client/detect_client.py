import base64
from camera import CSICamera
from camera.detector import IntruderDetector
from net import AsyncWebsocketClient


__all__ = ['IntruderDetectClient']


class IntruderDetectClient(AsyncWebsocketClient):
    def __init__(self, url):
        AsyncWebsocketClient.__init__(self, url)

        self.camera = CSICamera(0)
        self.camera_detector = IntruderDetector(save_path='output')
        self.camera_detector.register_callback(self.on_detect_event_change)
        self.camera.enable_detector(self.camera_detector)

        self.register_message_callback(self.on_receive_message)

    def start_detect(self, source):
        self.camera.start(source=source)
        # self.camera.show()

    def on_receive_message(self, message):
        print(message)

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


if __name__ == '__main__':
    API_KEY = 'CxqDJRwGyIyinon2CnivyD3Pd-9Qy4GZF4sW9Xb2ADg'
    WEBSOCKET_URL = "ws://127.0.0.1:8000/ws/device/{api_key}"
    client = IntruderDetectClient(url=WEBSOCKET_URL.format(api_key=API_KEY))
    client.connect()
    client.start_detect("../dataset/crosswalk.avi")
