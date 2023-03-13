# WSS client
import communicate
import performance
import cv2
import camera
import detector

API_KEY = ''
WEBSOCKET_URL = "wss://wssweb.net/ws/device/{api_key}"

# websocket_client = communicate.get_websocket_client()
# websocket_client.start(WEBSOCKET_URL.format(api_key=API_KEY))
#
# monitor = performance.get_performance_monitor()
# monitor.start()

csi_camera = camera.get_csi_camera(0)
# csi_camera.open('dataset/TownCentreXVID.mp4')
csi_camera.open(0)
csi_camera.start()

detector_obj = detector.MotionDetector()
cv2.namedWindow('image', cv2.WINDOW_NORMAL)
detect = False

while True:
    grabbed, frame = csi_camera.read(show_time=True)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("l"):
        detect = True
    if detect:
        result, result_frame = detector_obj.frame_delta_detect(frame=frame)
        if grabbed:
            cv2.imshow('Main Frame', result_frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

csi_camera.release()
cv2.destroyAllWindows()


