import camera
import detector
import subprocess
from monitor import performance

"""
	Encapsulate some convenient interface operations and provide convenient global calls for programs. 
	At present, most of them are used in the module <net>. 
	The reason why this module is not directly put in the net module is that 
	future development considers the development of GUI, 
	and programming the operation into a separate module is conducive to the interactive call of GUI.
"""


def shutdown():
	subprocess.run('halt')


def restart():
	subprocess.run('reboot')


def intruder_detect(status, sourcer=0, show=False):
	camera_detector = camera.get_camera()
	if status:
		camera_detector.start(sourcer)
		camera_detector.enable_detector(detector.IntruderDetector())
		if show:
			camera_detector.show()
	else:
		camera_detector.stop_show()
		camera_detector.stop()


def performance_monitor(status):
	monitor = performance.get_performance_monitor()
	if status:
		monitor.start()
	else:
		monitor.stop()





