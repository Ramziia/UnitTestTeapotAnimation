

# Реализация целочисленного алгоритма Брезенхема
def line(XY, beginx, beginy, endx, endy):
    XLength = beginx - endx
    YLength = beginy - endy
    # TMatrix - Это матрица, которая нужна для перехода от отдих координат к другим,
    TMatrix = [0, 0, 0]
    if XLength < 0:
        XLength *= -1
        TMatrix[0] = 1
    if YLength < 0:
        YLength *= -1
        TMatrix[1] = 1
    if YLength > XLength:
        XLength, YLength = YLength, XLength
        TMatrix[2] = 1
    e = 2 * YLength - XLength
    eS = 2 * YLength
    eD = 2 * YLength - 2 * XLength
    x = 0
    y = 0
    while x <= XLength:
        a = x
        b = y
        if TMatrix[2] == 1:
            a, b = b, a
        if TMatrix[1] == 1:
            b *= -1
        if TMatrix[0] == 1:
            a *= -1
        a = endx + a
        b = endy + b
        XY[0].append(a)
        XY[1].append(b)
        if e <= 0:
            x = x + 1
            e += eS
        else:
            x = x + 1
            y = y + 1
            e += eD
    return XY