import numpy as np
import re

# Считывание вершин треугольников
# triangles - матрица 3 * кол-во треугольников. triangles хранит только номера строчек, в которых записаны вершины треугольников
def coord_f(f):
    f.seek(0)
    triangles = []
    for line in f.readlines():
        # В файле small_teapot вершины треугольников разделены /0/0, поэтому до split(), удаляем
        line = re.sub('/0/0', ' ', line)
        words = line.split()
        if len(words) != 0:
            if words[0] == 'f':
                triangles.append(words[1:4])
    triangles = np.array(triangles).astype(int) - 1
    return triangles

# Считывание вершин из файла и запись в список xy, состоящий из списков x, y. Работаю со списками для возможности добавления
# Возвращаю список, состоящий из двух списков
def coord_v(f):
    xy = [[], []]
    for line in f.readlines():
        words = line.split()
        if len(words) != 0:
            if words[1] == 'f':
                break
            if words[0] == 'v':
                xy[0].append(float(words[1]))
                xy[1].append(float(words[2]))
    return xy







