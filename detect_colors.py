def detect_colors(bgr: tuple) -> str:
    b, g, r = map(int, bgr)
    if b <= 35 and g <= 35 and r >= 60:
        return 'red'
    elif b >= 90 and g <= 90 and r <= 60:
        return 'blue'
    elif b <= 30 and g >= 30 and r <= 20:
        return 'green'
    elif b <= 60 and g >= 100 and r >= 100:
        return 'yellow'
    elif b <= 20 and g <= 20 and r <= 20:
        return 'black'
    else:
        return 'unknown'
