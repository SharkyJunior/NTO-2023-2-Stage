import cv2
import numpy as np
from detect_colors import detect_colors
import time
import tkinter as tk
# cv2.WITH_QT=True




flag = False

    # Функция для обработки щелчка на кнопке
def on_button_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 150 < x < 300 and 100 < y < 200:  # Проверяем, был ли щелчок внутри прямоугольной области кнопки
            print("Кнопка 'Start' была нажата!")
            global flag
            flag = True


# Создаем пустое изображение
image = np.zeros((480, 640, 3), dtype=np.uint8)

# Задаем массив кругов (цвет и радиус)
circles_1 = [
    {'color': (0, 255, 0), 'x': 100, 'y': 500, 'radius': 30},
    {'color': (0, 0, 255), 'x': 200, 'y': 200, 'radius': 20},
    {'color': (255, 0, 0), 'x': 300, 'y': 100, 'radius': 40}
]




vid = cv2.VideoCapture(1)
font = cv2.FONT_HERSHEY_COMPLEX
window = cv2.namedWindow("Display_Image", cv2.WINDOW_NORMAL)
cv2.setMouseCallback('Display_Image', on_button_click)

# cv2.createButton("Back", back, None, cv2.QT_PUSH_BUTTON, 1)





def get_color_at_point(image, x, y, radius):

    # Получаем область вокруг точки.
    roi = image[int(y - radius):int(y + radius),
                int(x - radius):int(x + radius)]
    # Конвертируем область в цветовое пространство HSV.

    # Возвращаем среднее значение цвета.
    b, g, r, smth = cv2.mean(roi)
    return (b, g, r)

circles1 = [
    {'color': (0, 255, 0), 'x': 100, 'y': 0, 'radius': 30},
    {'color': (0, 0, 255), 'x': 200, 'y': 0, 'radius': 20},
    {'color': (255, 0, 0), 'x': 300, 'y': 0, 'radius': 40}
]



while True:
    time.sleep(1 / 24)

    ret, frame = vid.read()
    output = frame.copy()

    # Рисуем прямоугольную область-кнопку на изображении
    cv2.rectangle(output, (150, 100), (300, 200), (200, 200, 200), -1)

    # Добавляем текст "Start" в кнопку
    cv2.putText(output, 'Start', (180, 160), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

    # Показываем окно с изображением и добавляем обработчик для щелчка мыши на кнопке



    # формируем ч/б картинку с размытием для ускорения определения кругов
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    gray = cv2.medianBlur(gray, 5)

    # распознаем круги
    circles = cv2.HoughCircles(
        gray, cv2.HOUGH_GRADIENT, 1, minDist=100, param1=60, param2=50, minRadius=50, maxRadius=200)

    # Применяем адаптивный пороговый фильтр
    thresh = cv2.adaptiveThreshold(
        gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 11, 2)

    # Находим контуры
    contours, _ = cv2.findContours(
        thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    # Ищем квадраты в контурах
    rectangles = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
        x, y, w, h = cv2.boundingRect(approx)

        # Проверяем, что контур соответствует прямоугольнику и имеет нужные пропорции
        # aspect_ratio = float(w)/h
        # and 0.9 < aspect_ratio < 1.1
        if len(approx) == 4 and cv2.contourArea(contour) > 2500 and w > 100 and h > 100 and w < 1000 and h < 1000:
            rectangles.append(approx)

    if len(rectangles) > 0:
        rectangles = [rectangles[0]]
        # print(rectangles)
        # Отрисовываем найденные квадраты
        cv2.drawContours(output, rectangles, -1, (200, 50, 100), 3)

    borders = []
    # Выводим координаты вершин квадрата
    # print("point coords:", end=' ')
    for square in rectangles:
        # cv2.fillPoly(output, [square], (0,255,0))
        for point in square:
            # print(point[0], end=' ')
            borders.append(point[0])
        # print()

    if circles is not None and len(circles) < 15:
        # print(gray.shape)
        # print(frame.shape)
        circles = np.round(circles[0, :]).astype("int")

        # отрисовываем каждый круг и пишем рядом с ним цвет для него
        for (x, y, r) in circles:
            color = get_color_at_point(frame, x, y, r / 2)
            # print(color)
            # "обводим" круг
            cv2.circle(output, (x, y), r, color, -1)
            temp = np.array(borders)
            if len(temp) > 0 and len(temp) > 0 and min(temp[:, 0]) < x < max(temp[:, 0]) and min(temp[:, 1]) < y < max(temp[:, 1]):
                cv2.putText(output, f'color: {detect_colors(color)}, inside',
                            (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font,
                            1, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                cv2.putText(output, f'color: {detect_colors(color)}, not inside',
                            (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font,
                            1, (255, 255, 255), 1, cv2.LINE_AA)

        # пишем общее количество найденных кругов
        cv2.putText(output, f'Circle count: {len(circles)}, Rectangle count: {len(rectangles)}',
                    (int(frame.shape[1] * 0.65), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
        

        cv2.putText(output, 'Press "S" to Start basket simulation',
                    (int(frame.shape[1] * 0.65), int(frame.shape[0] * 0.2)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # чтобы предотвратить "подвисание" программы при слишком большом количестве кругов, при
    # большом количестве кругов прекращаем отрисовку
    elif circles is not None and len(circles) >= 15:
        cv2.putText(output, 'Cannot distinquish circles, make them more clear or remove excess items',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
    # если нет никаких кругов, пишем соответствующее сообщение
    else:
        cv2.putText(output, 'No circles detected',
                    (int(frame.shape[1] * 0.8), int(frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)



    if flag:
            # Обновляем положение кругов
        for circle in circles1:
            circle['y'] += 5  # Изменяем положение круга, чтобы он двигался вниз

            # Рисуем круги на изображении
            cv2.circle(output, (circle['x'], circle['y']), circle['radius'], circle['color'], -1)




    # выводим кадр на экран
    cv2.imshow('Display_Image', output)
    # обрабатываем клавишу выхода из программы
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Деверь, шурин, золовка, невестка, свекр, кумовья, крестник, падчерица, отчим, дядья, сватья, кузина, сноха
