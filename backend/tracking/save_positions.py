import csv
import sys

import cv2
from ultralytics import YOLO

model = YOLO("best.pt")

cap = cv2.VideoCapture(sys.argv[1])

frame_number = 0
found = 0
rows = []

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        results = model(frame, conf=0.1, verbose=False)
        boxes = results[0].boxes

        if len(boxes) > 0:
            # Take the box the model is most sure about
            best = boxes.conf.argmax()
            x, y, w, h = boxes.xywh[best].tolist()
            rows.append([frame_number, int(x), int(y)])
            found = found + 1
        else:
            # Club head not found, leave x and y empty
            rows.append([frame_number, "", ""])

        frame_number = frame_number + 1

    else:
        break

cap.release()

with open("club_positions.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["frame", "x", "y"])
    writer.writerows(rows)

print("Frames:", frame_number)
print("Club head found in:", found)