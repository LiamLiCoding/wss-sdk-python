import cv2
import copy
import threading
import datetime


CSI_CAMERAS = []


def get_csi_camera(index=0):
    global CSI_CAMERAS
    if index == 0 and not len(CSI_CAMERAS):
        camera = CSICamera()
        CSI_CAMERAS.append(camera)
        return camera
    elif index < len(CSI_CAMERAS) - 1:
        return CSI_CAMERAS[index]


class CSICamera:
    def __init__(self) -> None:
        self.video_capture = None
        self.frame = None
        self.grabbed = False
        self.detectors = []

        self.thread = None
        self.thread_lock = threading.Lock()
        self.running = False

    def open(self, source=0):
        self.video_capture = cv2.VideoCapture(source)

        if self.video_capture and self.get_open_status():
            self.grabbed, self.frame = self.video_capture.read()
        else:
            self.video_capture = None
            self.frame = None
            self.grabbed = False
            raise RuntimeError("Unable to open csi_camera or video source")

    def start(self):
        if self.running:
            print('Video capturing is already running')
            return

        if self.video_capture:
            self.running = True
            self.thread = threading.Thread(target=self.update)
            self.thread.start()

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()
        self.thread = None

    def get_open_status(self):
        return self.video_capture.isOpened()

    def get_video_capture(self):
        return self.video_capture

    def update(self):
        while self.running:
            try:
                grabbed, frame = self.video_capture.read()
                with self.thread_lock:
                    self.grabbed = grabbed
                    self.frame = frame
            except RuntimeError:
                print("Could not read image from camera")

    def read(self, show_time=False):
        frame = []
        if self.grabbed:
            with self.thread_lock:
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
    
    def register_detector(self, detector):
        self.detectors.append(detector)


