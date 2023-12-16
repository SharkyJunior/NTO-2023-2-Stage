import cv2
import numpy as np
from detect_colors import detect_colors
import time


vid = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX


def get_color_at_point(image, x, y, radius):

    # Получаем область вокруг точки.
    roi = image[int(y - radius):int(y + radius),
                int(x - radius):int(x + radius)]
    # Конвертируем область в цветовое пространство HSV.

    # Возвращаем среднее значение цвета.
    b, g, r, smth = cv2.mean(roi)
    return (b, g, r)


while True:
    time.sleep(1 / 24)

    ret, frame = vid.read()
    output = frame.copy()

    # формируем ч/б картинку с размытием для ускорения определения кругов
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    # распознаем круги
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=60, param2=50, minRadius=50, maxRadius=200)



    

    # Применяем адаптивный пороговый фильтр
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Находим контуры
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Ищем квадраты в контурах
    rectangles = []
    
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)

        # Проверяем, что контур соответствует прямоугольнику и имеет нужные пропорции
        # aspect_ratio = float(w)/h  
        # and 0.9 < aspect_ratio < 1.1
        if len(approx) == 4 and cv2.contourArea(contour) > 1000 and w > 100 and h > 100 and w < 700 and h < 700:
            rectangles.append(approx)

    rectangles = [rectangles[0]]
    # Отрисовываем найденные квадраты
    cv2.drawContours(output, rectangles, -1, (200, 50, 100), 3)

    # Выводим координаты вершин квадрата
    print("point coords:", end=' ')
    for square in rectangles:
        # cv2.fillPoly(output, [square], (0,255,0))
        for point in square:
            print(point[0], end=' ')
        print()


    if circles is not None and len(circles) < 15:
        print(gray.shape)
        print(frame.shape)
        circles = np.round(circles[0, :]).astype("int")

        # отрисовываем каждый круг и пишем рядом с ним цвет для него
        for (x, y, r) in circles:
            color = get_color_at_point(frame, x, y, r / 2)
            print(color)
            # "обводим" круг
            cv2.circle(output, (x, y), r, color, 4)

        # пишем общее количество найденных кругов
        cv2.putText(output, f'Circle count: {len(circles)}, Rectangle count: {len(rectangles)}',
                    (int(frame.shape[1] * 0.65), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # чтобы предотвратить "подвисание" программы при слишком большом количестве кругов, при
    # большом количестве кругов прекращаем отрисовку
    elif circles is not None and len(circles) >= 15:
        cv2.putText(output, 'Cannot distinquish circles, make them more clear or remove excess items',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    # если нет никаких кругов, пишем соответствующее сообщение
    else:
        cv2.putText(output, 'No circles detected',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)


    # выводим кадр на экран
    cv2.imshow('frame', output)
    # обрабатываем клавишу выхода из программы
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Деверь, шурин, золовка, невестка, свекр, кумовья, крестник, падчерица, отчим, дядья, сватья, кузина, сноха