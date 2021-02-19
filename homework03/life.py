import pathlib
import random

from typing import List, Optional, Tuple

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:

    def __init__(
            self,
            size: Tuple[int, int],
            randomize: bool = True,
            max_generations: Optional[float] = float('inf')
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Резервный список клеток
        self.pp = self.prev_generation.copy()
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        life_list = [[0] * self.cols for i in range(self.rows)]
        if randomize:
            life_list = []
            for i in range(self.rows):
                part = []
                for j in range(self.cols):
                    part.append(random.randint(0, 1))
                life_list.append(part)
        return life_list
        pass

    def get_neighbours(self, cell: Cell) -> Cells:
        if cell == (0, 0):
            return [self.curr_generation[0][1], self.curr_generation[1][1], self.curr_generation[1][0]]
        elif cell == (0, self.cols - 1):
            return [self.curr_generation[0][cell[1] - 1], self.curr_generation[1][cell[1] - 1], self.curr_generation[1][cell[1]]]
        elif cell == (self.rows - 1, self.cols - 1):
            return [self.curr_generation[cell[0] - 1][cell[1] - 1], self.curr_generation[cell[0] - 1][cell[1]], self.curr_generation[cell[0]][cell[1] - 1]]
        elif cell == (self.rows - 1, 0):
            return [self.curr_generation[cell[0] - 1][0], self.curr_generation[cell[0] - 1][1], self.curr_generation[self.curr_generation[cell[0]][1]]]
        elif cell[0] == 0:
            return [self.curr_generation[0][cell[1] + 1], self.curr_generation[0][cell[1] - 1], self.curr_generation[1][cell[1] - 1], self.curr_generation[1][cell[1]],
                    self.curr_generation[1][cell[1] + 1]]
        elif cell[1] == 0:
            return [self.curr_generation[cell[0] + 1][0], self.curr_generation[cell[0] - 1][0], self.curr_generation[cell[0] + 1][1], self.curr_generation[cell[0] - 1][1],
                    self.curr_generation[cell[0]][1]]
        elif cell[0] == self.rows - 1:
            return [self.curr_generation[cell[0]][cell[1] - 1], self.curr_generation[cell[0]][cell[1] + 1], self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1]], self.curr_generation[cell[0] - 1][cell[1] + 1]]
        elif cell[1] == self.cols - 1:
            return [self.curr_generation[cell[0] + 1][cell[1]], self.curr_generation[cell[0] - 1][cell[1]], self.curr_generation[cell[0] + 1][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1] - 1], self.curr_generation[cell[0]][cell[1] - 1]]
        else:
            return [self.curr_generation[cell[0] + 1][cell[1] - 1], self.curr_generation[cell[0] + 1][cell[1]], self.curr_generation[cell[0] + 1][cell[1] + 1],
                    self.curr_generation[cell[0]][cell[1] - 1], self.curr_generation[cell[0]][cell[1] + 1], self.curr_generation[cell[0] - 1][cell[1] - 1],
                    self.curr_generation[cell[0] - 1][cell[1]], self.curr_generation[cell[0] - 1][cell[1] + 1]]
        pass

    def get_next_generation(self) -> Grid:
        dict_neib = dict()
        next_gen = self.curr_generation
        for i in range(self.rows):
            for j in range(self.cols):
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

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.pp = self.prev_generation.copy()
        self.prev_generation.clear()
        part = []
        for i in range(self.rows):
            for j in range(self.cols):
                part.append(self.curr_generation[i][j])
            self.prev_generation.append(part)
            part = []
        self.curr_generation = self.get_next_generation()
        self.generations += 1
        pass

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.generations >= self.max_generations:
            return True
        else:
            return False
        pass

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        else:
            return True
        pass

    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        """
        Прочитать состояние клеток из указанного файла.
        """
        file_life = open(filename, 'r')
        e = []
        s = []
        for i in file_life.read():
            if i != '\n':
                e.append(int(i))
            else:
                s.append(e)
                e = []
        s.append(e)
        new_class = GameOfLife((len(s), len(s[0])))
        new_class.curr_generation = s
        file_life.close()
        return new_class
        pass

    def save(self, filename: pathlib.Path) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        file_life = open(filename, 'a')
        s = self.curr_generation
        for i in range(len(s)):
            for j in range(len(s[0])):
                file_life.write(str(s[i][j]))
            if i != len(s) - 1:
                file_life.write('\n')
        file_life.close()
        pass
