import cv2


def human_detect(self, frame):
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	# Detect faces in the image
	faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30),
	                                           flags=cv2.CASCADE_SCALE_IMAGE)

	if len(faces) > 0:
		print("Human detected.")
	else:
		print("No human detected.")

	# Draw rectangles around detected faces
	for (x, y, w, h) in faces:
		cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

	return frame
