import cv2
import copy
import threading


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
        self.m_video_capture = None
        self.m_frame = None
        self.m_grabbed = False

        self.m_thread = None
        self.m_thread_lock = threading.Lock()
        self.m_running = False

    def open(self, source=0):
        self.m_video_capture = cv2.VideoCapture(source)

        if self.m_video_capture and self.get_open_status():
            self.m_grabbed, self.m_frame = self.m_video_capture.read()
        else:
            self.m_video_capture = None
            self.m_frame = None
            self.m_grabbed = False
            raise RuntimeError("Unable to open csi_camera or video source")

    def start(self):
        if self.m_running:
            print('Video capturing is already running')
            return

        if self.m_video_capture:
            self.m_running = True
            self.m_thread = threading.Thread(target=self.update)
            self.m_thread.start()

    def stop(self):
        self.m_running = False
        if self.m_thread:
            self.m_thread.join()
        self.m_thread = None

    def get_open_status(self):
        return self.m_video_capture.isOpened()

    def get_video_capture(self):
        return self.m_video_capture

    def update(self):
        while self.m_running:
            try:
                grabbed, frame = self.m_video_capture.read()
                with self.m_thread_lock:
                    self.m_grabbed = grabbed
                    self.m_frame = frame
            except RuntimeError:
                print("Could not read image from camera")

    def read(self):
        with self.m_thread_lock:
            frame = copy.deepcopy(self.m_frame)
            grabbed = self.m_grabbed
        return grabbed, frame

    def release(self):
        self.stop()
        if self.m_video_capture:
            self.m_video_capture.release()
            self.m_video_capture = None


