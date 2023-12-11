import cv2
import numpy as np

vid = cv2.VideoCapture(0)

while True:

    # Capture the video frame
    # by frame
    ret, frame = vid.read()
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower = np.array([0, 170, 120], dtype="uint8")
    upper = np.array([359, 255, 255], dtype="uint8")
    mask = cv2.inRange(image, lower, upper)

    cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    for c in cnts:
        (x, y), radius = cv2.minEnclosingCircle(c)
        cv2.circle(frame, (int(x), int(y), radius))
        perimeter = cv2.arcLength(c, True)
        approx = cv2.approxPolyDP(c, 0.04 * perimeter, True)
        if len(approx) > 5:
            cv2.drawContours(frame, [c], -1, (36, 255, 12), -1)

    # circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, 1,
    #                            200, param1=30, param2=45, minRadius=0, maxRadius=200)

    # if circles is not None:
    #     frame2 = frame
    #     circles = np.round(circles[0, :]).astype("int")
    #     for (x, y, r) in circles[:5]:
    #         cv2.circle(frame, (x, y), r, (0, 255, 0), 4)
    #         cv2.rectangle(frame, (x - 5, y - 5),
    #                       (x + 5, y + 5), (0, 128, 255), -1)

    cv2.imshow('mask', mask)
    cv2.imshow('contour', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
