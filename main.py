import cv2
import numpy as np
from detect_colors import detect_colors
import time


vid = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX

def get_color_at_point(image, x, y, radius):
  
    # Получаем область вокруг точки.
    roi = image[int(y - radius):int(y + radius), int(x - radius):int(x + radius)]
    # Конвертируем область в цветовое пространство HSV.

    # Возвращаем среднее значение цвета.
    b, g, r, smth = cv2.mean(roi)
    return (b, g, r)

while True:
    time.sleep(1 / 24)

    ret, frame = vid.read()
    output = frame.copy()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=60, param2=50, minRadius=50, maxRadius=200)

    if circles is not None and len(circles) < 10:
        print(gray.shape)
        print(frame.shape)
        circles = np.round(circles[0, :]).astype("int")
        c = 0
        for (x, y, r) in circles:
            color = get_color_at_point(frame, x, y, r / 2)
            print(color)
            cv2.circle(output, (x, y), r, color, 4)
            cv2.rectangle(output, (x - 5, y - 5),
                          (x + 5, y + 5), (0, 200, 250), -1)
            cv2.putText(output, f'circle{c}, color: {detect_colors(color)}, ({color[0]}, {color[1]}, {color[2]})',
                        (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)
            c += 1
        cv2.putText(output, f'Circle count: {len(circles)}',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    elif circles is not None and len(circles) >= 10:
        cv2.putText(output, 'Cannot distinquish circles, make them more clear or remove excess items',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    else:
        cv2.putText(output, 'No circles detected',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.imshow('frame', output)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()

