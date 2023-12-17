
# отдельный метод для классификации цвета по цветовым каналам
def detect_colors(bgr: tuple) -> str:
    b, g, r = map(int, bgr)

    # используем отношения значений цветовых каналов для определения цвета
    if r >= 3*b and r >= 3*g:
        return 'red'
    elif b >= 1.5*r and g <= 1.5*r:
        return 'blue'
    elif g >= 1.5*b and g >= 2*r:
        return 'green'
    elif g >= 2.5*b and r >= 2.5*b and (0.85*g <= r <= 1.15*g):
        return 'yellow'
    elif g >= 1.5*b and r >= 1.5*b and r >= 1.4*g:
        return 'orange'
    elif b <= 30 and g <= 30 and r <= 30:
        return 'black'
    elif b >= 175 and g >= 175 and r >= 175:
        return 'white'
    else:
        return "unknown"
