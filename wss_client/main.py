# WSS client
import communicate
import performance
import cv2.cv2 as cv2
import camera

API_KEY = ''
WEBSOCKET_URL = "wss://wssweb.net/ws/device/{api_key}"

# websocket_client = communicate.get_websocket_client()
# websocket_client.start(WEBSOCKET_URL.format(api_key=API_KEY))

# monitor = performance.get_performance_monitor()
# monitor.start() 

csi_camera = camera.get_csi_camera(0)
csi_camera.open('dataset/TownCentreXVID.mp4')
csi_camera.start()

# Your other logic
while True:
    grabbed, frame = csi_camera.read()
    cv2.imshow('frame', frame)

