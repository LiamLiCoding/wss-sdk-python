import cv2
import imutils

__all__ = ['MotionDetector', 'HumanDetector', 'DetectorManager']


class DetectorManager:
    def __init__(self):
        pass


class BaseDetector:
    frame = None

    def register_callback(self):
        pass

    def get_tagged_frame(self):
        return self.frame

    def tag_frame(self):
        return self.frame

    def detect(self, frame):
        result = False

        self.frame = frame

        return result, frame


class MotionDetector(BaseDetector):
    def __init__(self) -> None:
        self.benchmark_frame = None

    def frame_delta_detect(self, frame):
        result = False
        text = "Unoccupied"
        frame = imutils.resize(frame, width=500)

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if self.benchmark_frame is None:
            self.benchmark_frame = gray
            return False, frame

        frame_delta = cv2.absdiff(self.benchmark_frame, gray)
        thresh = cv2.threshold(frame_delta, 25, 255, cv2.THRESH_BINARY)[1]

        thresh = cv2.dilate(thresh, None, iterations=2)
        (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # 遍历轮廓
        for c in cnts:
            # 遍历轮廓
            if cv2.contourArea(c) < 500:
                continue
            # 计算轮廓的边界框，在当前帧中画出该框，并且更新标签
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            result = True
            text = "Occupied"

        cv2.putText(frame, "Room Status: {}".format(text), (10, 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

        self.frame = frame

        return result, frame


class HumanDetector(BaseDetector):
    def __init__(self) -> None:
        self.frame = None

    def detect(self, frame):
        result = False

        self.frame = frame

        return result

