import sys
from pathlib import Path

import cv2

cap = cv2.VideoCapture(sys.argv[1])

# Name of the video without .mov, used in the file names
name = Path(sys.argv[1]).stem

Path("datasets/frames").mkdir(parents=True, exist_ok=True)

frame_number = 0

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        cv2.imwrite(f"datasets/frames/{name}_{frame_number:04d}.jpg", frame)
        frame_number = frame_number + 1

    else:
        break

cap.release()

print("Frames saved:", frame_number)