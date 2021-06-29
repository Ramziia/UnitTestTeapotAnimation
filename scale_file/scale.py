import numpy as np

# Масштабирование: переводим координаты в отрезок от 0 до 1, затем перевод в координаты m x m,
# с учетом соотношения между координатами
def alt(m, xy):
    # Перевожу списки в np.array
    xy = np.array(xy)
    minx = min(xy[0])
    miny = min(xy[1])
    maxx = max(xy[0])
    maxy = max(xy[1])
    d = (maxy - miny) / (maxx - minx)
    if d < 1:
        xy[1, :] = (xy[1, :] - miny) / (maxy - miny) * (m-1) * d
        xy[0, :] = (xy[0, :] - minx) / (maxx - minx) * (m-1)
    else:
        xy[1, :] = (xy[1, :] - miny) / (maxy - miny) * (m - 1)
        xy[0, :] = (xy[0, :] - minx) / (maxx - minx) * (m - 1) / d
    xy = np.array(xy).astype(int)
    print(type(xy[0][0]))
    return xy