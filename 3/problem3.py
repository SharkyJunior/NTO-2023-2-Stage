import cv2
import numpy as np
import time
import tkinter as tk
import random
# cv2.WITH_QT=True


# отдельный метод для классификации цвета по цветовым каналам
def detect_colors(bgr: tuple) -> str:
    b, g, r = map(int, bgr)

    # используем отношения значений цветовых каналов для определения цвета
    if r >= 3*b and r >= 3*g:
        return 'red'
    elif b >= 4*r and g >= 2*r:
        return 'blue'
    elif g >= 1.5*b and g >= 2*r:
        return 'green'
    elif g >= 2.5*b and r >= 2.5*b and (0.85*g <= r <= 1.15*g):
        return 'yellow'
    elif g >= 1.5*b and r >= 10*b and 1.4*g <= r < 2*g:
        return 'orange'
    elif b <= 30 and g <= 30 and r <= 30:
        return 'black'
    elif b >= 175 and g >= 175 and r >= 175:
        return 'white'
    elif r >= 1.3*g and r >= 2*b:
        return 'brown'
    else:
        return "unknown"


flag = False

circles1 = []

# Функция для обработки щелчка на кнопке


def on_button_click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        if 150 < x < 300 and 100 < y < 200:  # Проверяем, был ли щелчок внутри прямоугольной области кнопки
            print("Кнопка 'Start' была нажата!")
            global flag
            global circles1
            flag = True
            circles1 = []


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


while True:
    time.sleep(1 / 24)

    ret, frame = vid.read()
    output = frame.copy()

    # Рисуем прямоугольную область-кнопку на изображении
    cv2.rectangle(output, (150, 100), (300, 200), (200, 200, 200), -1)

    # Добавляем текст "Start" в кнопку
    cv2.putText(output, 'Start', (180, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2, cv2.LINE_AA)

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
                if flag:
                    circles1.append(
                        {'color': color, 'x': 300 + random.randint(0, 900), 'y': -100, 'radius': r})
                cv2.putText(output, f'color: {detect_colors(color)}, inside',
                            (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font,
                            1, (255, 255, 255), 1, cv2.LINE_AA)
            else:
                cv2.putText(output, f'color: {detect_colors(color)}, not inside',
                            (int(x+(r**0.5))+100, int(y + (r**0.5))+100), font,
                            1, (255, 255, 255), 1, cv2.LINE_AA)
        flag = False
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

    height, width, channels = output.shape
    # Обновляем положение кругов
    for circle in circles1:
        circle['y'] += 30  # Изменяем положение круга, чтобы он двигался вниз
        if circle['y'] >= height + 200:
            circles1 = []
        # Рисуем круги на изображении
        cv2.circle(output, (circle['x'], circle['y']),
                   circle['radius'], circle['color'], -1)

    # выводим кадр на экран
    cv2.imshow('Display_Image', output)
    # обрабатываем клавишу выхода из программы
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# Деверь, шурин, золовка, невестка, свекр, кумовья, крестник, падчерица, отчим, дядья, сватья, кузина, сноха
