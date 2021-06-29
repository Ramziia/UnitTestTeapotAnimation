

def barycentric(xy, points):
    # Находим максимальные и минимальные значение x и y среди трех вершин
    maxx = max(xy[0][points[0]], xy[0][points[1]], xy[0][points[2]])
    maxy = max(xy[1][points[0]], xy[1][points[1]], xy[1][points[2]])
    minx = min(xy[0][points[0]], xy[0][points[1]], xy[0][points[2]])
    miny = min(xy[1][points[0]], xy[1][points[1]], xy[1][points[2]])
    # Проходимся по прямоугольнику, в котором находится треугольник
    for x in range(minx, maxx + 1):
        for y in range(miny, maxy + 1):
            a = (xy[0][points[0]] - x) * (xy[1][points[1]] - xy[1][points[0]]) - (xy[0][points[1]] - xy[0][points[0]]) * (xy[1][points[0]] - y)
            b = (xy[0][points[1]] - x) * (xy[1][points[2]] - xy[1][points[1]]) - (xy[0][points[2]] - xy[0][points[1]]) * (xy[1][points[1]] - y)
            c = (xy[0][points[2]] - x) * (xy[1][points[0]] - xy[1][points[2]]) - (xy[0][points[0]] - xy[0][points[2]]) * (xy[1][points[2]] - y)
            # Условие принадлежности треугольнику
            if a >= 0 and b >= 0 and c >= 0:
                xy[0].append(x)
                xy[1].append(y)
    return xy

# triangles_points хранит строки, в которых записани вершины треугольников
def Color(xy, triangles_points):
    xy = list(xy)
    xy[0] = list(xy[0])
    xy[1] = list(xy[1])
    for i in range(len(triangles_points)):
        xy = barycentric(xy, triangles_points[i])
    return xy