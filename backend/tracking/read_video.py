import sys
import cv2

cap = cv2.VideoCapture(sys.argv[1])

if cap.isOpened() == False:
    print("ERROR FILE NOT FOUND OR WRONG CODEC USED!")

print("Frame rate:", cap.get(cv2.CAP_PROP_FPS))
print("Number of frames:", int(cap.get(cv2.CAP_PROP_FRAME_COUNT)))

while cap.isOpened():

    ret, frame = cap.read()

    if ret == True:

        frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3)
        cv2.imshow("frame", frame)

        if cv2.waitKey(0) & 0xFF == ord("q"):
            break

    else:
        break

cap.release()
cv2.destroyAllWindows()