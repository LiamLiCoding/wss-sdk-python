import cv2
import copy
import threading
import datetime
import time
import platform


__all__ = ['CameraBase']


class CameraBase:
	def __init__(self, camera_id) -> None:
		self.camera_id = camera_id
		self.video_capture = None
		self.frame = None
		self.grabbed = False

		self.detectors = []

		self._thread = None
		self._thread_lock = threading.Lock()
		self._show_thread = None

		self.keep_running = False
		self.frame_counter = 0
		self.start_time = None

		self.show_time = False
		self.show_fps = False

	def open(self, source=0):
		self.video_capture = cv2.VideoCapture(source)
		self.set_detector_video_param()

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
			self.start_time = time.time()
		else:
			print("Please open camera first")

	def stop(self):
		self.keep_running = False
		if self._thread:
			self._thread.join()
		self._thread = None

	def set_detector_video_param(self):
		if self.detectors and self.video_capture:
			for detector in self.detectors:
				detector.set_video_param(width=int(self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)),
				                         height=int(self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)),
				                         fps=int(self.video_capture.get(cv2.CAP_PROP_FPS)))

	def get_open_status(self):
		return self.video_capture.isOpened()

	def get_video_capture(self):
		return self.video_capture

	def update(self):
		while self.keep_running:
			try:
				grabbed, frame = self.video_capture.read()
				if not grabbed:
					print("Video source reached its end.")
					self.stop()
					return
				self.frame_counter += 1
				if self.detectors:
					for detector in self.detectors:
						frame = detector.detect(frame)
				with self._thread_lock:
					self.grabbed = grabbed
					self.frame = frame
			except RuntimeError:
				print("Could not read image from camera")

	def read(self, show_time=False, show_fps=False):
		frame = []
		if self.grabbed:
			with self._thread_lock:
				frame = copy.deepcopy(self.frame)
			if show_time:
				time_text = datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S")
				cv2.putText(frame, time_text, (10, 50),
				            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=1)
			if show_fps:
				fps_text = "FPS {:.1f}".format(self.frame_counter / (time.time() - self.start_time))
				cv2.putText(frame, fps_text, (10, frame.shape[0] - 10),
				            cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), thickness=1)
		return self.grabbed, frame

	def release(self):
		self.stop()
		if self.video_capture:
			self.video_capture.release()
			self.video_capture = None

	def enable_detector(self, detector):
		self.detectors.append(detector)

	def show(self, show_time=False, show_fps=False):
		if platform.system() in ('Darwin', 'Linux'):
			print("Show should be in main thread")
			return
		self._show_thread = threading.Thread(target=self._show_result, args=(show_time, show_fps))
		self._show_thread.start()

	def _show_result(self, show_time, show_fps):
		while self.keep_running:
			_, frame = self.read(show_time, show_fps)
			cv2.imshow('Camera {}'.format(self.camera_id), frame)
			key = cv2.waitKey(1) & 0xff
			if key == 27:  # Esc
				break

	def stop_show(self):
		self._show_thread.join()
		self._show_thread = None


