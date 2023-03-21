import abc
import cv2
import event


__all__ = ['CloseRangeIntruderDetector', 'LongDistanceIntruderDetector']


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


class CloseRangeIntruderDetector(BaseCameraDetector):
    def __init__(self) -> None:
        super().__init__()
        self.ori_frame = None
        self.frame = None
        self.result = {}
        self.benchmark_frame = None
        self.bg_sub_obj = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', dict)

    def detect(self, frame):
        self.ori_frame = frame
        # frame = cv2.blur(frame, (10, 10))
        foreground_mask = self.bg_sub_obj.apply(frame)
        foreground_mask = cv2.GaussianBlur(foreground_mask, (7, 7), 0)
        contours, hierarchy = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 40 and h > 90:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
                mid_point = (int(x + w / 2.0), int(y + h / 2.0))
                cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

        if self.event:
            self.event.set_value({'event_id':1})
        self.frame = frame
        return self.frame


class LongDistanceIntruderDetector(BaseCameraDetector):
    def __init__(self) -> None:
        super().__init__()
        self.ori_frame = None
        self.frame = None
        self.result = {}
        self.benchmark_frame = None
        self.bg_sub_obj = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', dict)

    def detect(self, frame):
        self.ori_frame = frame
        foreground_mask = self.bg_sub_obj.apply(frame)
        foreground_mask = cv2.GaussianBlur(foreground_mask, (7, 7), 0)
        contours, hierarchy = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 40 and h > 90:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
                mid_point = (int(x + w / 2.0), int(y + h / 2.0))
                cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

        if self.event:
            self.event.set_value({'event_id':1})
        self.frame = frame
        return self.frame
