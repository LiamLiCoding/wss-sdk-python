#!/usr/bin/env python 
# -*- coding:utf-8 -*-
# @Time : 2023/4/10 17:44
# @Author : Haozheng Li (Liam)
# @Email : hxl1119@case.edu

import cv2


from wss.camera.base import CameraBase
from wss.camera.expections import CameraDostNotExist


class CameraManager:
	"""
	Important! CameraManager should be run in main thread.
	"""

	MODE_PULLING = 1
	MODE_PARALLEL = 2

	def __init__(self):
		# Camera Object manage
		self._cameras = []

		# Camera manager running mode
		self._running_mode = self.MODE_PULLING
		
		# Camera show
		self._show_status = False
		self._show_thread = None
		
	def _init_camera(self, camera_id):
		camera = CameraBase(camera_id)
		self._cameras.append(camera)

	def start_cameras(self, number):
		for camera_id in range(number):
			self._init_camera(camera_id)

	def start_camera(self, camera_id):
		pass

	def start_all_camera(self, camera_id):
		if self._running_mode == self.MODE_PULLING:
			pass
		elif self._running_mode == self.MODE_PARALLEL:
			pass

	def change_running_mode(self, mode):
		print("Camera Manager - Change running mode: from mode{} to mode {}".format(self._running_mode, mode))
		self._running_mode = mode

	def get_running_mode(self):
		return self._running_mode

	def get_camera_by_id(self, camera_id):
		for camera in self._cameras:
			if camera.index == camera_id:
				return camera
		raise CameraDostNotExist('Camera id {} does not exist'.format(camera_id))

	def show_camera(self, camera_id, show_time=False, show_fps=False):
		if self._show_status:
			print("Other showing windows is running. Please close it and retry.")
			return

		camera = self.get_camera_by_id(camera_id)
		if camera:
			while self.keep_running:
				_, frame = self.read(show_time, show_fps)
				cv2.imshow('Camera {}'.format(self.camera_id), frame)
				key = cv2.waitKey(1) & 0xff
				if key == 27:  # Esc
					break

	def show_all_cameras(self, camera_id):
		pass

	def set_detector(self, detector):
		pass

