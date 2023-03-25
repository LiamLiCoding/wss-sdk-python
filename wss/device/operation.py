import camera
import detector
import subprocess

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





