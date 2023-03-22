import abc
import cv2
import event


__all__ = ['CloseRangeIntruderDetector', 'LongDistanceIntruderDetector']


class BaseCameraDetector(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.frame = None
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
        self.benchmark_frame = None
        self.bg_sub = cv2.createBackgroundSubtractorMOG2(history=200, detectShadows=False)

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', dict)

    def detect(self, frame):
        self.ori_frame = frame
        # frame = cv2.blur(frame, (10, 10))
        foreground_mask = self.bg_sub.apply(frame)
        foreground_mask = cv2.GaussianBlur(foreground_mask, (7, 7), 0)
        contours, hierarchy = cv2.findContours(foreground_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            x, y, w, h = cv2.boundingRect(contour)
            if w > 40 and h > 90:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
                mid_point = (int(x + w / 2.0), int(y + h / 2.0))
                cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

        if self.event:
            self.event.set_value({'event_id': 1})
        self.frame = frame
        return foreground_mask


class LongDistanceIntruderDetector(BaseCameraDetector):
    INTRUDER_EVENT1 = 1
    INTRUDER_EVENT2 = 2
    INTRUDER_EVENT3 = 3
    INTRUDER_EVENT4 = 4

    def __init__(self) -> None:
        super().__init__()
        self.ori_frame = None
        self.benchmark_frame = None
        self.bg_sub = None
        self.hog = None
        self.prev_area = 0
        self.frame_counter = 0
        self.init_detector()
    
    def init_detector(self):
        self.bg_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=30, detectShadows=False)
        self.hog = cv2.HOGDescriptor()
        self.hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', dict)

    def detect(self, frame):
        self.frame_counter += 1
        frame_copy = frame.copy()
        frame_copy = cv2.GaussianBlur(frame_copy, (11, 11), 0)
        foreground_mask = self.bg_sub.apply(frame_copy)

        # Apply a threshold to the foreground mask to create a binary image
        _, thresh = cv2.threshold(foreground_mask, 127, 255, cv2.THRESH_BINARY)

        cleaned = cv2.GaussianBlur(thresh, (9, 9), 0)
        contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) < 1200:
            return frame

        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
        mid_point = (int(x + w / 2.0), int(y + h / 2.0))
        cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

        area = w * h
        if self.prev_area and not self.frame_counter % 25:

            print(self.frame_counter, area, self.prev_area)
            print(int((area - self.prev_area) / self.prev_area * 100))
        # if area > self.prev_area:
        #     approaching = True
        # else:
        #     approaching = False

        if not self.frame_counter % 26:
            self.prev_area = area

        if self.event:
            self.event.set_value({'event_id': self.INTRUDER_EVENT1, 'data': None})
        self.frame = frame
        return frame
