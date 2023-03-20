import cv2
import copy
import threading
import datetime


CAMERAS = []


def get_camera(index=0):
    global CAMERAS
    if not index or not len(CAMERAS) or index < len(CAMERAS) - 1:
        camera = Camera()
        CAMERAS.append(camera)
        return camera
    else:
        return CAMERAS[index]


class Camera:
    def __init__(self) -> None:
        self.video_capture = None
        self.frame = None
        self.grabbed = False
        self.detectors = []

        self._thread = None
        self._thread_lock = threading.Lock()
        self.keep_running = False

    def open(self, source=0):
        self.video_capture = cv2.VideoCapture(source)

        if self.video_capture and self.get_open_status():
            self.grabbed, self.frame = self.video_capture.read()
            return self.grabbed
        else:
            self.video_capture = None
            self.frame = None
            self.grabbed = False
            raise RuntimeError("Unable to open csi_camera or video source")

    def start(self, source=0):
        self.open(source)
        if self.keep_running:
            print('Video capturing is already running')
            return

        if self.video_capture:
            self.keep_running = True
            self._thread = threading.Thread(target=self.update)
            self._thread.daemon = True
            self._thread.start()
        else:
            print("Please open camera first")

    def stop(self):
        self.keep_running = False
        if self._thread:
            self._thread.join()
        self._thread = None

    def get_open_status(self):
        return self.video_capture.isOpened()

    def get_video_capture(self):
        return self.video_capture

    def update(self):
        while self.keep_running:
            try:
                grabbed, frame = self.video_capture.read()
                if self.detectors:
                    for detector in self.detectors:
                        frame = detector.detect(frame)
                with self._thread_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")

    def read(self, show_time=False):
        frame = []
        if self.grabbed:
            with self._thread_lock:
                frame = copy.deepcopy(self.frame)
            if show_time:
                cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
        return self.grabbed, frame

    def release(self):
        self.stop()
        if self.video_capture:
            self.video_capture.release()
            self.video_capture = None
    
    def enable_detector(self, detector):
        self.detectors.append(detector)


