import abc
import cv2
import event
import datetime

__all__ = ['IntruderDetector']


class BaseCameraDetector(metaclass=abc.ABCMeta):
    def __init__(self) -> None:
        self.frame = None
        self.result = None
        self.event = None

        self.width = 0
        self.height = 0
        self.fps = 0

        self.create_event()

    @abc.abstractmethod
    def create_event(self):
        pass

    @abc.abstractmethod
    def detect(self, frame):
        self.event.set_value(self.result)
        pass

    def set_video_param(self, width, height, fps):
        self.width = width
        self.height = height
        self.fps = fps

    @staticmethod
    def get_frame_area(frame):
        height, width, channels = frame.shape
        return height * width


class IntruderDetector(BaseCameraDetector):
    INTRUDER_EVENT1 = 1
    INTRUDER_EVENT2 = 2
    INTRUDER_EVENT3 = 3
    INTRUDER_EVENT4 = 4

    def __init__(self) -> None:
        super().__init__()
        self.ori_frame = None
        self.benchmark_frame = None

        self.bg_sub = cv2.createBackgroundSubtractorMOG2(history=700, varThreshold=30, detectShadows=False)

        self.prev_roi_area = 0
        self.frame_counter = 0
        self.detect_counter = 0
        self.not_detect_counter = 0
        self.video_output_writer = None
        self.video_output_path = ''
        self.event_data = None
        self.status = self.INTRUDER_EVENT1

    def create_event(self):
        self.event = event.get_event_controller().create_event('intruder', dict)

    def detect(self, frame):
        self.frame_counter += 1
        frame_copy = frame.copy()
        frame_copy = cv2.GaussianBlur(frame_copy, (11, 11), 0)
        foreground_mask = self.bg_sub.apply(frame_copy)

        _, thresh = cv2.threshold(foreground_mask, 127, 255, cv2.THRESH_BINARY)

        cleaned = cv2.GaussianBlur(thresh, (9, 9), 0)
        contours, hierarchy = cv2.findContours(cleaned, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        max_contour = max(contours, key=cv2.contourArea)

        if cv2.contourArea(max_contour) < 1200 or (cv2.contourArea(max_contour) / self.get_frame_area(frame)) > 0.6:
            self.not_detect_counter += 1
            if self.not_detect_counter > self.fps * 5:
                self.set_event(self.INTRUDER_EVENT1, frame)
            return frame

        x, y, w, h = cv2.boundingRect(max_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2, lineType=cv2.LINE_AA)
        mid_point = (int(x + w / 2.0), int(y + h / 2.0))
        cv2.circle(frame, mid_point, 3, (255, 0, 255), 6)

        if self.status == self.INTRUDER_EVENT1:
            self.set_event(self.INTRUDER_EVENT2, frame)

        roi_area = w * h
        if self.prev_roi_area and not self.frame_counter % self.fps:  # Detect per second
            if int((roi_area - self.prev_roi_area) / self.prev_roi_area * 100) > 10:
                self.detect_counter += 1

        if self.detect_counter > 2 and self.status == self.INTRUDER_EVENT2:  # At lease last for 2 seconds
            self.set_event(self.INTRUDER_EVENT3, frame)

        if self.detect_counter > 5:  # At lease last for 5 seconds
            self.set_event(self.INTRUDER_EVENT4, frame)

        if not self.frame_counter % (self.fps + 1):
            self.prev_roi_area = roi_area

        cv2.putText(frame, 'Event {}'.format(self.status), (10, 100), cv2.FONT_HERSHEY_PLAIN, 3,
                    (0, 0, 255), thickness=2)

        self.frame = frame
        return frame
    
    def set_event(self, event_type, frame):
        if event_type == self.INTRUDER_EVENT1:
            if self.status == self.INTRUDER_EVENT4:
                self.event.set_value({'event_id': self.INTRUDER_EVENT4, 'data': self.video_output_path})
                self.video_output_writer.release()
                self.video_output_writer = None
                self.detect_counter = 0
                self.not_detect_counter = 0

        if event_type == self.INTRUDER_EVENT2:
            output_path = 'output/event2_{}.jpg'.format(datetime.datetime.now().strftime("%I-%M-%S"))
            cv2.imwrite(output_path, frame)
            self.event.set_value({'event_id': self.INTRUDER_EVENT1, 'data': output_path})
            
        elif event_type == self.INTRUDER_EVENT3:
            output_path = 'output/event3_{}.jpg'.format(datetime.datetime.now().strftime("%I-%M-%S"))
            cv2.imwrite(output_path, frame)
            self.event.set_value({'event_id': self.INTRUDER_EVENT1, 'data': output_path})
            
        elif event_type == self.INTRUDER_EVENT4:
            self.video_output_path = 'output/event4_{}.avi'.format(datetime.datetime.now().strftime("%I-%M-%S"))
            if not self.video_output_writer:
                self.video_output_writer = cv2.VideoWriter(self.video_output_path, cv2.VideoWriter_fourcc(*'XVID'),
                                                           self.fps, (self.width, self.height))
            self.video_output_writer.write(frame)

        self.status = event_type

