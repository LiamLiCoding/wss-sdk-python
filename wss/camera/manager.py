#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/10 17:44
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import cv2
import numpy as np

from wss.camera.base import CameraBase
from wss.camera.expections import CameraDostNotExist, CameraRunningModeError


class CameraManager:
	"""
	Important! In macOS or Linux, CameraManager should be run in main thread.
	"""

	MODE_PULLING = 1
	MODE_PARALLEL = 2

	def __init__(self):
		# Camera Objects
		self._cameras = []
		self.activated_cameras = []

		# Camera manager running mode
		self._running_mode = self.MODE_PULLING
		
		# Camera show
		self._show_status = False
		self._show_thread = None
		
	def _camera_init(self, camera_id):
		camera = CameraBase(camera_id)
		self._cameras.append(camera)
		print("Camera manager - Init camera: id {}".format(camera_id))

	def init_cameras(self, number):
		for camera_id in range(number):
			self._camera_init(camera_id)

	def start_all(self):
		for camera in self._cameras:
			camera.start(camera.camera_id)
			print("Camera manager - Start camera: id {}".format(camera.camera_id))

	def get_camera_by_id(self, camera_id):
		for camera in self._cameras:
			if camera.camera_id == camera_id:
				return camera
		raise CameraDostNotExist('Camera id {} does not exist'.format(camera_id))

	def get_all_cameras(self):
		return self._cameras

	def start_camera(self, camera_id):
		pass

	def get_mode(self):
		return self._running_mode

	def switch_mode(self, mode):
		print("Camera Manager - Change running mode: from mode{} to mode {}".format(self._running_mode, mode))
		self._running_mode = mode

	def switch_camera(self, camera_id):
		if self._running_mode != self.MODE_PULLING:
			raise CameraRunningModeError("Switch camera should be running in pulling mode!")
		camera = self.get_camera_by_id(camera_id)
		camera.start()
		self.activated_cameras.append(camera)

	def show(self, camera_id, show_time=False, show_fps=False):
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

	def show_all(self, show_time=False, show_fps=False):
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

	def set_detector(self, detector):
		pass


if __name__ == '__main__':
	camera_manager = CameraManager()
	camera_manager.init_cameras(2)
	camera_manager.start_all()
	camera_manager.show_all()
