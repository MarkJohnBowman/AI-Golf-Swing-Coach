import csv
import sys

import cv2

# Read the filled positions, None means still missing
positions = []
with open("club_positions_filled.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        if row["x"] == "":
            positions.append(None)
        else:
            positions.append((int(row["x"]), int(row["y"])))

cap = cv2.VideoCapture(sys.argv[1])
fps = cap.get(cv2.CAP_PROP_FPS)

writer = None
frame_number = 0

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True and frame_number < len(positions):

        # Draw the path so far, skipping gaps that are still missing
        for k in range(1, frame_number + 1):
            if positions[k - 1] is not None and positions[k] is not None:
                cv2.line(frame, positions[k - 1], positions[k], (0, 255, 0), 4)

        # Make the video writer on the first frame, so it's the same size
        if writer is None:
            height, width = frame.shape[:2]
            fourcc = cv2.VideoWriter_fourcc(*"mp4v")
            writer = cv2.VideoWriter("club_path.mp4", fourcc, fps, (width, height))

        writer.write(frame)

        frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("Club path", frame)

        if cv2.waitKey(30) & 0xFF == ord("q"):
            break

        frame_number = frame_number + 1

    else:
        break

cap.release()
writer.release()
cv2.destroyAllWindows()