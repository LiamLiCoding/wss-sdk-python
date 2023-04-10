import abc


class BaseCameraDetector(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.frame = None
        self.result = None
        self.event = None
        self._callback = []

        self.width = 0
        self.height = 0
        self.fps = 0

    def register_callback(self, func):
        self._callback.append(func)

    @abc.abstractmethod
    def detect(self, frame):
        self.on_result_change()

    def set_video_param(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

    @staticmethod
    def get_frame_area(frame):
        height, width, channels = frame.shape
        return height * width

    def on_result_change(self):
        if self._callback:
            for each_func in self._callback:
                each_func(self.result)
