import cv2
import random

# vid = cv2.VideoCapture(1)
# ret, frame = vid.read()
# output = frame.copy()


class Circle:
    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y
        self.r = r
        self.color = color


def rand_comb(circles, output, frame, font):
    n = len(circles)
    test = list(range(n))
    a = []
    for (x, y, r) in circles:
        temp = Circle(x, y, r, detect_colors(
            get_color_at_point(frame, x, y, r / 2)))
        a.append(temp)
    res_n = n // 2
    res = random.choices(test, k=res_n)
    output_dict = {}
    for x in res:
        if x.color in output_dict:
            output_dict[x.color] += 1
        else:
            output_dict[x.color] = 1
    output_text = 'Put '
    for key, value in output_dict:
        output_text += str(value) + ' ' + key + ', '
    output_text = output_text[:-2]
    output_text += 'circles into a bаsket'
    cv2.putText(output, output_text, (int(frame.shape[1] * 0.8), int(
        frame.shape[0] * 0.1)), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
