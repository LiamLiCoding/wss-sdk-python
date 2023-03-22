import cv2
import numpy as np
import imutils
import camera
import detector
import threading

camera_detector = camera.get_camera()
camera_detector.enable_detector(detector.LongDistanceIntruderDetector())
camera_detector.start('dataset/crosswalk.avi')
camera_detector.show(show_fps=True)