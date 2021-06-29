import draw_file.Bresenham

# Соединяем вершины с помощью 3 линий, 3 раза выхываем функцию Брезенхема
def create_lines(triangles_points, xy):
    # Для возможности добавления, перенесем в лист
    xy = list(xy)
    xy[0] = list(xy[0])
    xy[1] = list(xy[1])
    for points in triangles_points:
        xy = draw_file.Bresenham.line(xy, xy[0][points[0]], xy[1][points[0]], xy[0][points[1]], xy[1][points[1]])
        xy = draw_file.Bresenham.line(xy, xy[0][points[1]], xy[1][points[1]], xy[0][points[2]], xy[1][points[2]])
        xy = draw_file.Bresenham.line(xy, xy[0][points[0]], xy[1][points[0]], xy[0][points[2]], xy[1][points[2]])
    return xy