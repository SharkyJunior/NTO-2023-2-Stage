import cv2
import numpy as np

def detect_colors(bgr: tuple) -> str:
    hsv_color = cv2.cvtColor(np.uint8([[bgr]]), cv2.COLOR_BGR2HSV)[0][0]
    b, g, r = map(int, bgr)
    
    # Определяем цвет по оттенку
    hue = hsv_color[0]

    if b <= 20 and g <= 20 and r <= 20:
        return "black"
    elif hue <= 10 or hue > 160:
        return "red"
    elif 10 < hue <= 45:
        return "yellow"
    elif 100 < hue <= 130:
        return "blue"
    elif 45 < hue <= 70:
        return "green"
    else:
        return "unknown"


