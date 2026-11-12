import sys

import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

cap = cv2.VideoCapture(sys.argv[1])

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        results = model(frame, conf=0.05, verbose=False)
        frame = results[0].plot()

        frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("YOLO", frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()