import pygame
import random

from pygame.locals import *
from typing import List, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

        # Список клеток (при объявлении объекта он сразу же генерируется)
        self.sp = self.create_grid()

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.width, y))

    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()
            self.draw_lines()
            self.sp = self.get_next_generation()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = True) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        life_list = [[0] * self.cell_width for i in range(self.cell_height)]
        if randomize:
            life_list = []
            for i in range(self.cell_height):
                part = []
                for j in range(self.cell_width):
                    part.append(random.randint(0, 1))
                life_list.append(part)
        return life_list
        pass

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        s1 = 0
        s2 = 0
        for i in self.sp:
            for j in i:
                if j == 0:
                    pygame.draw.rect(self.screen, pygame.Color('white'),
                                     (self.cell_size * s1, self.cell_size * s2, self.cell_size, self.cell_size))
                else:
                    pygame.draw.rect(self.screen, pygame.Color('green'),
                                     (self.cell_size * s1, self.cell_size * s2, self.cell_size, self.cell_size))
                s1 += 1
            s1 = 0
            s2 += 1
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        if cell == (0, 0):
            return [self.sp[0][1], self.sp[1][1], self.sp[1][0]]
        elif cell == (0, self.cell_width - 1):
            return [self.sp[0][cell[1] - 1], self.sp[1][cell[1] - 1], self.sp[1][cell[1]]]
        elif cell == (self.cell_height - 1, self.cell_width - 1):
            return [self.sp[cell[0] - 1][cell[1] - 1], self.sp[cell[0] - 1][cell[1]], self.sp[cell[0]][cell[1] - 1]]
        elif cell == (self.cell_height - 1, 0):
            return [self.sp[cell[0] - 1][0], self.sp[cell[0] - 1][1], self.sp[self.sp[cell[0]][1]]]
        elif cell[0] == 0:
            return [self.sp[0][cell[1] + 1], self.sp[0][cell[1] - 1], self.sp[1][cell[1] - 1], self.sp[1][cell[1]], self.sp[1][cell[1] + 1]]
        elif cell[1] == 0:
            return [self.sp[cell[0] + 1][0], self.sp[cell[0] - 1][0], self.sp[cell[0] + 1][1], self.sp[cell[0] - 1][1], self.sp[cell[0]][1]]
        elif cell[0] == self.cell_height - 1:
            return [self.sp[cell[0]][cell[1] - 1], self.sp[cell[0]][cell[1] + 1], self.sp[cell[0] - 1][cell[1] - 1], self.sp[cell[0] - 1][cell[1]], self.sp[cell[0] - 1][cell[1] + 1]]
        elif cell[1] == self.cell_width - 1:
            return [self.sp[cell[0] + 1][cell[1]], self.sp[cell[0] - 1][cell[1]], self.sp[cell[0] + 1][cell[1] - 1], self.sp[cell[0] - 1][cell[1] - 1], self.sp[cell[0]][cell[1] - 1]]
        else:
            return [self.sp[cell[0] + 1][cell[1] - 1], self.sp[cell[0] + 1][cell[1]], self.sp[cell[0] + 1][cell[1] + 1], self.sp[cell[0]][cell[1] - 1], self.sp[cell[0]][cell[1] + 1], self.sp[cell[0] - 1][cell[1] - 1], self.sp[cell[0] - 1][cell[1]], self.sp[cell[0] - 1][cell[1] + 1]]
        pass

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        dict_neib = dict()
        next_gen = self.sp.copy()
        for i in range(self.cell_height):
            for j in range(self.cell_width):
                dict_neib[(i, j)] = self.get_neighbours((i, j))
        for i in dict_neib.keys():
            if next_gen[i[0]][i[1]] == 0:
                if dict_neib[i].count(1) == 3:
                    next_gen[i[0]][i[1]] = 1
            else:
                if dict_neib[i].count(1) != 3 and dict_neib[i].count(1) != 2:
                    next_gen[i[0]][i[1]] = 0
        return next_gen
        pass
