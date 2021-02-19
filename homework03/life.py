import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
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
            Матрица клеток размером `rows` х `cols`.
        """
        if randomize:
            return [[random.randint(0, 1) for _ in range(self.cols)] for _ in range(self.rows)]
        return [[0 for _ in range(self.cols)] for _ in range(self.rows)]

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
        neighbours = []
        rows = len(self.curr_generation)
        cols = len(self.curr_generation[1]) if rows else 0
        for row in range(max(0, cell[0] - 1), min(rows, cell[0] + 2)):
            for col in range(max(0, cell[1] - 1), min(cols, cell[1] + 2)):
                if (row, col) != cell:
                    neighbours.append(self.curr_generation[row][col])
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = deepcopy(self.curr_generation)
        for pos_x, row in enumerate(self.curr_generation):
            for pos_y, col in enumerate(row):
                pos = (pos_x, pos_y)
                neigh = sum(self.get_neighbours(pos))
                if col:
                    if neigh != 2 and neigh != 3:
                        new_grid[pos_x][pos_y] = 0
                    else:
                        new_grid[pos_x][pos_y] = 1
                else:
                    if neigh == 3:
                        new_grid[pos_x][pos_y] = 1
        return new_grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        if not self.is_max_generations_exceeded:
            self.prev_generation, self.curr_generation = (
                self.curr_generation,
                self.get_next_generation(),
            )
            self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:  # type: ignore
            return True
        return False

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.prev_generation != self.curr_generation:
            return True
        return False

    @staticmethod
    def from_file(filename: pathlib.Path) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла  .
        """
        new_grid = []
        with open(filename) as file:
            for row in file:
                new_grid.append([int(val) for val in row if (val == "0" or val == "1")])
        new_game = GameOfLife((len(new_grid), len(new_grid[0])))
        new_game.curr_generation = new_grid
        return new_game

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        if not pathlib.Path("saves").exists():
            pathlib.Path("saves").mkdir()
        if not pathlib.Path(filename).exists():
            pathlib.Path(filename).touch()
        with open(filename, "w") as file:
            for row in range(self.rows):
                for col in range(self.cols):
                    file.write(str(self.curr_generation[row][col]))
                file.write("\n")
