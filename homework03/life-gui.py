from datetime import datetime
from pathlib import Path

import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        # Размер клетки
        self.cell_size = cell_size

        # Ширина и высота окна
        self.width = self.life.cols * self.cell_size
        self.height = self.life.rows * self.cell_size
        self.screen_size = self.width, self.height

        # Инициализация окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Скорость игры
        self.speed = speed

        # Цвета клеток
        self.primary_color = arguments.primary_color
        self.secondary_color = arguments.secondary_color

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        for pos_x, row in enumerate(self.life.curr_generation):
            for pos_y, col in enumerate(row):
                color = self.secondary_color
                if col:
                    color = self.primary_color
                pygame.draw.rect(
                    self.screen,
                    color,
                    (
                        self.cell_size * pos_y + 1,
                        self.cell_size * pos_x + 1,
                        self.cell_size - 1,
                        self.cell_size - 1,
                    ),
                )

    def run(self) -> None:
        """
        Запустить игру.

        Управление:
        Пробел - Пауза.
        Esc - Выход из игры.
        Нажатие ЛКМ - "закрасить" клетку.
        Вверх - сохранение "жизни" в файл вида life_*time*.txt
        """
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))
        running = True
        paused = False
        while running:
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            for event in pygame.event.get():
                if event.type == QUIT:  # type: ignore
                    running = False
                if event.type == KEYDOWN:  # type: ignore
                    if event.key == K_ESCAPE:  # type: ignore
                        running = False
                    elif event.key == K_SPACE:  # type: ignore
                        paused = True if not paused else False
                    elif event.key == K_DOWN:  # type: ignore
                        save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        self.life.save(Path(f"saves/life_{save_time}.txt"))
                if event.type == MOUSEBUTTONDOWN:  # type: ignore
                    click_position = pygame.mouse.get_pos()
                    pos_x, pos_y = (
                        click_position[1] // self.cell_size,
                        click_position[0] // self.cell_size,
                    )
                    if self.life.curr_generation[pos_x][pos_y]:
                        self.life.curr_generation[pos_x][pos_y] = 0
                    else:
                        self.life.curr_generation[pos_x][pos_y] = 1
            self.draw_lines()
            self.draw_grid()
            if not paused:
                self.life.step()
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()
