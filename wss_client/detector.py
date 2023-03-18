import abc
import cv2
import event


class BaseCameraDetector(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.result = None
        self.event = None
        self.create_event()

    @abc.abstractmethod
    def create_event(self):
        pass

    @abc.abstractmethod
    def detect(self, frame):
        self.event.set_value(self.result)
        pass


class IntruderDetector(BaseCameraDetector):
    def __init__(self) -> None:
        super().__init__()
        self.frame = None
        self.result = 0
        self.benchmark_frame = None
        self.bg_sub_obj = cv2.createBackgroundSubtractorMOG2()

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', int)

    def detect(self, frame):
        foreground = cv2.blur(frame, (10, 10))
        foreground = self.bg_sub_obj.apply(foreground)
        foreground = cv2.GaussianBlur(foreground, (7, 7), 0)

        contours, hierarchy = cv2.findContours(foreground, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 40 and h > 90:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
                mid_point = (int(x + w / 2.0), int(y + h / 2.0))
                cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)
        if self.event:
            self.event.set_value(self.result)
        self.frame = frame
        return self.frame
