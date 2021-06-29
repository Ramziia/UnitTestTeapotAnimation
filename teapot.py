import reading_file.reading
import scale_file.scale
import show_img_file.show
import draw_file.create_lines_for_triangles
from core import *
import draw_file.Color

path = "task1.obj"
f = open(path)
# размеры изображения чайника
picture_size = 400
# считываем координаты вершин
xy = reading_file.reading.coord_v(f)
# triangles = матрица строк, в которых записаны вершины, начиная с 0
triangles = reading_file.reading.coord_f(f)
# Масштабирование
xy = scale_file.scale.alt(picture_size, xy)
# Раскрашиваю чайник. Не видна функция отрисовки треугольников по алгоритму Бреенхема, но она тоже работает
xy = draw_file.Color.Color(xy, triangles)
xy = draw_file.create_lines_for_triangles.create_lines(triangles, xy)
xy.append(np.ones(len(xy[0])))
xy = np.array(xy).astype(int)
img = np.zeros((picture_size, picture_size, 3), dtype=np.uint8)
color = np.array([255, 0, 0])
img[xy[0, :], xy[1, :]] = color
show_img_file.show.show_fun(img)

