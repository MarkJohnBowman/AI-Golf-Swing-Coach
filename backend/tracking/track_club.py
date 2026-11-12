import sys

import cv2


def ask_for_tracker():
    print("Welcome! What Tracker API would you like to use?")
    print("Enter 0 for BOOSTING: ")
    print("Enter 1 for MIL: ")
    print("Enter 2 for KCF: ")
    print("Enter 3 for TLD: ")
    print("Enter 4 for MEDIANFLOW: ")
    print("Enter 5 for CSRT: ")
    choice = input("Please select your tracker: ")

    if choice == "0":
        tracker = cv2.legacy.TrackerBoosting_create()
        tracker_name = "BOOSTING"
    if choice == "1":
        tracker = cv2.TrackerMIL_create()
        tracker_name = "MIL"
    if choice == "2":
        tracker = cv2.TrackerKCF_create()
        tracker_name = "KCF"
    if choice == "3":
        tracker = cv2.legacy.TrackerTLD_create()
        tracker_name = "TLD"
    if choice == "4":
        tracker = cv2.legacy.TrackerMedianFlow_create()
        tracker_name = "MEDIANFLOW"
    if choice == "5":
        tracker = cv2.TrackerCSRT_create()
        tracker_name = "CSRT"

    return tracker, tracker_name


tracker, tracker_name = ask_for_tracker()

cap = cv2.VideoCapture(sys.argv[1])

# Read first frame
ret, frame = cap.read()
frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

# Special function allows us to draw on the very first frame our desired ROI
roi = cv2.selectROI(frame, False)

# Initialize tracker with first frame and bounding box
tracker.init(frame, roi)

while True:
    # Read a new frame
    ret, frame = cap.read()

    if ret == False:
        break

    frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)

    # Update tracker
    success, roi = tracker.update(frame)

    # roi variable is a tuple of 4 floats
    # We need each value and we need them as integers
    (x, y, w, h) = tuple(map(int, roi))

    # Draw Rectangle as Tracker moves
    if success:
        # Tracking success
        p1 = (x, y)
        p2 = (x + w, y + h)
        cv2.rectangle(frame, p1, p2, (0, 255, 0), 3)
    else:
        # Tracking failure
        cv2.putText(frame, "Failure to Detect Tracking!!", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

    # Display tracker type on frame
    cv2.putText(frame, tracker_name, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3)

    # Display result
    cv2.imshow(tracker_name, frame)

    # Exit if ESC pressed
    k = cv2.waitKey(30) & 0xFF
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()