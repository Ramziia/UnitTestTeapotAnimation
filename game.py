import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time
import reading_file.reading
import scale_file.scale
import draw_file.create_lines_for_triangles
import draw_file.Color


#класс игры
class Game:

    def __init__(self, pic_size=512):
        # сохранили параметр как поле класса
        self.pic_size = pic_size
        # Угол поворота картинки
        self.angle = np.pi / 10
        self.last_x = 0
        self.last_y = 0
        # Кол-во кликов на определенный чайник
        self.click_count = 0
        # TODO считать вершины и грани. Адаптировать размер вершин
        # Открываем файл с вершинами
        path = "small_teapot.obj"
        f = open(path)
        # Размер бокса, в котором находится изображение чайника
        self.m = 50
        # Размер чайника
        self.teapot_size = 1
        # Считывание вершин v из файла
        self.xy = reading_file.reading.coord_v(f)
        # Считывание вершин f треугольников
        triangles = reading_file.reading.coord_f(f)
        # Масштабирование
        self.xy = scale_file.scale.alt(self.m, self.xy)
        # Отрисовка трегольников по Брезен (смысла здесь нет, так как закрашиваем весь чайник)
        self.xy = draw_file.create_lines_for_triangles.create_lines(triangles, self.xy)
        # Раскрашиваем чайник
        self.xy = draw_file.Color.Color(self.xy, triangles)

        self.xy.append(np.ones(len(self.xy[0])))
        self.xy = np.array(self.xy)
        self.xy = np.array(self.xy).astype(int)
        # Массивы сдвинутых вершин, которые будем отрисовывать
        self.moved_xy = self.xy
        # Середины чайника
        self.med = np.array((self.xy.max(1) - self.xy.min(1))/2).astype(int)
        # проверяет нужно ли завершить игру
        self.finish = False
        # готовит окна
        self.fig, self.ax = plt.subplots()
        self.fig.suptitle("Game")
        pass
        # Обработчик на клик мышкой-выстрел
        cid = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        # подготовка изображения-массива
        self.img = np.zeros((pic_size, pic_size, 3), dtype=np.uint8)
        # визуализация с анимацией
        self.im = plt.imshow(self.img, animated=True)
        # запуск анимации
        # self.fig - окно для анимации
        # self.update - функция отрисовки каждого кадра
        # self.init_target - функция, которая отработает перед запуском анимациии
        # self.end_game - функция-обман для matplotlib. Matplotlib требует точного количества кадров для завершения анимации. Мы же сделаем бесконечный генератор.
        # interval - количество миллисекунд, после которых снова вызывается функция self.update
        # exit()
        self.ani = FuncAnimation(self.fig, self.update, init_func=self.init_target, frames=self.end_game, blit=True, interval = 5)
        plt.show()

    #остановит игру
    def end_game(self):
        i = 0
        while not self.finish:
            i += 1
            yield i
    #функция инициализациии полета
    def init_target(self, x0=0, y0=None, alpha=None, v0=None, ang = np.pi/20,  click_count = None):
        """
        Эмулирует полёт под углом к горизонту с ускорением свободного падения
        :param x0: стартовая координата x тела
        :param y0: стартовая координата y тела
        :param alpha: угол в градусах по отношению к горизонту
        :param v0: начальная скорость
        :return:
        """
        if click_count == 1:
            self.click_count += 1
        if click_count == None:
            self.click_count = 0
        if click_count == 0:
            self.click_count = click_count
        if self.click_count >= 2:
            self.teapot_size = 2
        else:
            self.teapot_size = 1
        self.angle = ang
        if x0 == 0:
            x0 = int(self.m/2)
        # Обнулили поле
        self.img = np.zeros((self.pic_size, self.pic_size, 3), dtype=np.uint8)
        # Если в функцию не передали такой параметр, генерируем случаную координату y
        if y0 is None:
            y0 = np.random.randint(int(self.m/2), int(self.pic_size - self.m/2))
        # то же самое с углом
        if alpha is None:
            alpha = np.deg2rad(np.random.randint(20, 50))
        # и со скоростью
        if v0 is None:
            v0 = np.random.randint(20, 50)
        # фиксируем начальное время - оно понадобится для вычисленния новых координат
        self.t = time.time()
        self.v0 = v0
        self.x0 = x0
        self.y0 = y0
        self.alpha = alpha
        # неземное ускорение свободного падения
        self.g = 3 * 9.8
        # начальные проекции скоростей
        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha)
        return self.im,

    # функция отрисовки
    def update(self, par):
        # посмотрели сколько прошло времени с момента запуска снаряда
        cur_t = time.time() - self.t
        # пересчитали положение снаряда
        cur_x = self.x0 + self.v0 * cur_t * np.cos(self.alpha)
        cur_y = self.y0 + self.v0 * cur_t * np.sin(self.alpha) - self.g * cur_t * cur_t / 2
        # если вышли за вертикальные пределы изображения или каким-то образом влево - проиграли
        # TODO закончить условие проигрыша
        # Удар о верхнюю грань: замедляется, размер становится изначальным
        if cur_y + self.m * self.teapot_size/2 >= self.pic_size:
            self.init_target(self.last_x, self.last_y, np.deg2rad(-45))
            return self.im,
        else:
            # Чайник ушел вправо, запустится новый
            if cur_x + self.m * self.teapot_size >= self.pic_size:
                self.init_target()
                return self.im,
            else:
                # Условие проигрыша, окно просто закроется
                if cur_x - self.m * self.teapot_size / 2 < 0 or cur_y - self.m * self.teapot_size < 0:
                    self.xy =[]
                    self.end_game()

        # TODO отрисовка чайника, летящего по параболической траектории и прочие плюшки (о них ниже)
        # Закрасим старое изображение цветом фона
        self.img[self.moved_xy[0], self.moved_xy[1]] = (0, 0, 0)
        # self.last_x положение снаряда(середины чайника)
        self.last_x = int(cur_x)
        self.last_y = int(cur_y)
        # При нажатии на чайник, он крутится быстрее, со временем замедляется
        self.angle = self.angle + np.pi/15 + np.pi/self.angle
        # Перемещаем чайник, чтобы его середина была в центре вычисленного положения снаряда
        T = np.array([
            [1, 0, self.last_x - self.med[0]],
            [0, 1, self.last_y - self.med[1]],
            [0, 0, 1]])
        # Чтобы чайник кружился относительно центра масс, относительно точки- середины, сместим его в начало координат
        M1 = np.array([
            [1, 0, -self.last_x],
            [0, 1, -self.last_y],
            [0, 0, 1]])
        # Матрица размера
        S = np.array([
            [self.teapot_size, 0, 0],
            [0, self.teapot_size, 0],
            [0, 0, 1]])
        # Матрица поворота
        M2 = np.array([
            [np.cos(self.angle), np.sin(self.angle), 0],
            [-np.sin(self.angle), np.cos(self.angle), 0],
            [0, 0, 1]])
        # Возвращаем из центра в нужное место
        M3 = np.array([
            [1, 0, self.last_x],
            [0, 1, self.last_y],
            [0, 0, 1]])
        M = np.dot(M3, np.dot(M2, np.dot(S, M1)))
        K = np.dot(M, T)
        self.moved_xy = np.dot(K, self.xy)
        # После работы с матрицами, нужно снова сделать значения массива int
        self.moved_xy = np.array(self.moved_xy).astype(int)
        #рисуем снаряд
        self.img[self.moved_xy[0], self.moved_xy[1]] = (255, 0,0 )
        # запомнили скорости текущие
        self.vx = self.v0 * np.cos(self.alpha)
        self.vy = self.v0 * np.sin(self.alpha) - self.g * cur_t
        #обновили буфер отрисовки
        self.im.set_array(np.rot90(self.img))
        return self.im,

    # функция выстрела
    def onclick(self, event):
        # задали размер хитбокса, self.m - изначальный размер картинки,
        heat_box = self.m * self.teapot_size
        # вывели дебаг информацию
        # print(self.last_x, self.last_y, event.xdata, event.ydata, self.vx, self.vy)
        # Если кликнули в место, где сейчас летит снаряд
        if self.last_x - heat_box < event.xdata and event.xdata < self.last_x + heat_box and \
                self.pic_size-self.last_y - heat_box < event.ydata and event.ydata < self.pic_size-self.last_y + heat_box:
            # придать ему доп скорость и подкинуть от текущего положения
            #TODO  Заставить чайник вращаться, чайник должен вращаться быстро, а спустя некторое время замедлять вращение и вовсе его прекращать
            # После второго попадания по тому же чайнику, увеличить его размер в два раза, сохранив текущую ориентацию вращения
            self.init_target(self.last_x, self.last_y, np.deg2rad(45), self.v0 + np.abs(self.vx), np.pi/10, 1)
gg=Game()
