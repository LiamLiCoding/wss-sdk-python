#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/10 17:44
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import cv2
import numpy as np

from wss.camera.base import CameraBase
from wss.camera.expections import CameraDostNotExist, CameraRunningModeError


__all__ = ['CameraManager']


class CameraManager:
	"""
	Important! In macOS or Linux, CameraManager should be run in main thread.
	"""

	MODE_PULLING = 1
	MODE_PARALLEL = 2

	def __init__(self) -> None:
		# Camera Objects
		self._cameras = []
		self.activated_cameras = []

		# Camera manager running mode
		self._running_mode = self.MODE_PULLING
		
		# Camera show
		self._show_status = False
		self._show_thread = None

		# detector
		self.detector = None
		
	def _camera_init(self, camera_id) -> object:
		camera = CameraBase(camera_id)
		self._cameras.append(camera)
		print("Camera manager - Init camera: id {}".format(camera_id))
		return camera

	def initialize_cameras(self, number) -> None:
		for camera_id in range(number):
			self._camera_init(camera_id)

	@staticmethod
	def _stop_camera(camera_obj) -> None:
		if camera_obj:
			camera_obj.stop()
			camera_obj.release()
			print("Camera manager - Stop camera: id {}".format(camera_obj.camera_id))

	@staticmethod
	def _start_camera(camera_obj) -> None:
		if camera_obj:
			camera_obj.start('../dataset/crosswalk.avi')
			# camera_obj.start(camera_obj.get_camera_id())
			print("Camera manager - Start camera: id {}".format(camera_obj.camera_id))

	def set_camera_properties(self, width, height, codec, fps):
		for camera in self._cameras:
			camera.set_properties(width, height, codec, fps)

	def start_camera_by_id(self, camera_id):
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._start_camera(camera)

	def stop_camera_by_id(self, camera_id):
		camera = self.get_camera_by_id(camera_id)
		if camera:
			self._stop_camera(camera)

	def start_all(self) -> None:
		for camera in self._cameras:
			self._start_camera(camera)

	def stop_all(self) -> None:
		for camera in self._cameras:
			self._stop_camera(camera)

	def get_camera_by_id(self, camera_id) -> object:
		for camera in self._cameras:
			if camera.camera_id == camera_id:
				return camera
		raise CameraDostNotExist('Camera id {} does not exist'.format(camera_id))

	def get_all_cameras(self) -> list:
		return self._cameras

	def get_mode(self) -> int:
		return self._running_mode

	def switch_mode(self, mode) -> None:
		self._running_mode = mode
		print("Camera Manager - Change running mode: from mode{} to mode {}".format(self._running_mode, mode))

	def switch_camera(self, camera_id) -> None:
		if self._running_mode != self.MODE_PULLING:
			raise CameraRunningModeError("Switch camera should be running in pulling mode!")
		camera = self.get_camera_by_id(camera_id)
		camera.start()
		self.activated_cameras.append(camera)

	def show(self, camera_id, show_time=False, show_fps=False) -> None:
		"""
		!!Important!! show function will block the main thread
		"""
		if self._show_status:
			print("Other showing windows is running. Please close it and retry.")
			return

		camera = self.get_camera_by_id(camera_id)
		if camera:
			while True:
				_, frame = camera.read(show_time, show_fps)
				cv2.imshow('Camera {}'.format(camera_id), frame)
				key = cv2.waitKey(1) & 0xff
				if key == 27:  # Esc
					break

	def show_all(self, show_time=False, show_fps=False) -> None:
		"""
		!!Important!! show all function will block the main thread
		"""
		while True:
			cameras_merge_frame = None
			for index, camera in enumerate(self._cameras):
				_, frame = camera.read(show_time, show_fps)

				if not index:
					cameras_merge_frame = frame
				elif not index % 2:
					cameras_merge_frame = np.vstack((cameras_merge_frame, frame))
				else:
					cameras_merge_frame = np.hstack((cameras_merge_frame, frame))

			cv2.imshow('All Cameras', cameras_merge_frame)
			key = cv2.waitKey(1) & 0xff
			if key == 27:  # Esc
				break

	def set_detector(self, detector) -> None:
		self.detector = detector
		for camera in self._cameras:
			camera.enable_detector(detector)

		print("Camera Manager - Set detector: {}".format(detector))


if __name__ == '__main__':
	camera_manager = CameraManager()
	camera_manager.initialize_cameras(2)
	camera_manager.start_all()
	camera_manager.show_all(show_time=True, show_fps=True)
