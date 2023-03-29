from camera import CSICamera
from camera.detector import IntruderDetector
from net import AsyncWebsocketClient


__all__ = ['IntruderDetectClient']


class IntruderDetectClient(AsyncWebsocketClient):
    def __init__(self, url):
        AsyncWebsocketClient.__init__(self, url)
        self.camera = CSICamera(0)
        self.camera_detector = IntruderDetector()
        self.camera_detector.register_callback(self.on_detect_event)
        self.camera.enable_detector(self.camera_detector)

        self.register_message_callback(self.on_receive_message)

    def start(self):
        super().start()
        self.camera.start(source='data')
        self.camera.show()

    def on_receive_message(self, message):
        print(message)

    def on_detect_event(self, event):
        print(event)
