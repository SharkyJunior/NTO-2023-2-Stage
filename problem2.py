import cv2
import numpy as np
from detect_colors import detect_colors


def far_enough(p1: tuple, p2: tuple) -> bool:
    # чтобы не делать массив слишком огромным и перегружать систему, добавлять новую точку будем
    # только тогда, когда от предыдущей точки есть заметное расстояние
    return (p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2 >= 2500


def get_color_at_point(image, x, y, radius):

    # Получаем область вокруг точки.
    roi = image[int(y - radius):int(y + radius),
                int(x - radius):int(x + radius)]
    # Конвертируем область в цветовое пространство HSV.

    # Возвращаем среднее значение цвета.
    b, g, r, smth = cv2.mean(roi)
    return (b, g, r)


vid = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX

# храним траекторию в виде массива точек на экране
trajectory = []

while True:

    # получаем кадр из веб камеры
    ret, frame = vid.read()
    output = frame.copy()

    # формируем ч/б картинку с размытием для ускорения определения кругов
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    # распознаем круги
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=60, param2=50, minRadius=50, maxRadius=200)

    # если круг один, тогда рисуем для него траекторию
    if circles is not None and len(circles) == 1:
        circles = np.round(circles[0, :]).astype("int")
        # отрисовываем круг и информацию для него: номер и цвет
        for (x, y, r) in circles:
            radius = r
            color = get_color_at_point(frame, x, y, r / 2)
            print(color)
            cv2.circle(output, (x, y), r, color, 4)
            cv2.rectangle(output, (x - 5, y - 5),
                          (x + 5, y + 5), (0, 200, 250), -1)
            cv2.putText(output, f'color: {detect_colors(color)}, ({int(color[0])}, {int(color[1])}, {int(color[2])})',
                        (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font, 1, (255, 255, 255), 1, cv2.LINE_AA)

        # если круг сдвинулся на заметное расстояние, то добавляем точку в траекторию
        if len(trajectory) > 0 and far_enough(trajectory[-1], (x, y)):
            trajectory.append((x, y, r, color))
        elif len(trajectory) == 0:
            trajectory.append((x, y, r, color))

        cv2.putText(output, f'Circle count: {len(circles)}',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    # выводим сообщение, если кругов больше, чем один
    elif circles is not None and len(circles) >= 2:
        cv2.putText(output, 'Cannot distinquish single circle, make it more clear or remove excess circles',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    # если нет никаких кругов, пишем соответствующее сообщение
    else:
        cv2.putText(output, 'No circles detected',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # отрисовываем траекторию в виде кругов
    if len(trajectory) >= 2:
        for i in range(len(trajectory)):
            cv2.circle(output, trajectory[i][:2],
                       trajectory[i][2], trajectory[i][3], 2)
    # выводим кадр на экран
    cv2.imshow('frame', output)
    # обрабатываем клавишу выхода из программы
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    # обрабатываем клавишу очистки траектории
    if cv2.waitKey(1) & 0xFF == ord('c'):
        trajectory = []


vid.release()
cv2.destroyAllWindows()
