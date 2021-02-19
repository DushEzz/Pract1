import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        super().__init__(life)
        self.cell_size = cell_size
        self.speed = speed
        self.screen_size = self.cell_size * self.life.cols, self.cell_size * self.life.rows
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        for x in range(0, self.cell_size * self.life.cols, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (x, 0), (x, self.cell_size * self.life.rows))
        for y in range(0, self.cell_size * self.life.rows, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                             (0, y), (self.cell_size * self.life.cols, y))
        pass

    def draw_grid(self) -> None:
        s1 = 0
        s2 = 0
        for i in self.life.curr_generation:
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

    def run(self) -> None:
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))
        is_paused = True
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        is_paused = not is_paused
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if is_paused:
                            if self.life.curr_generation[event.pos[1] // self.cell_size][event.pos[0] // self.cell_size] == 0:
                                self.life.curr_generation[event.pos[1] // self.cell_size][event.pos[0] // self.cell_size] = 1
                            else:
                                self.life.curr_generation[event.pos[1] // self.cell_size][event.pos[0] // self.cell_size] = 0
                            if self.life.generations != self.life.max_generations:
                                self.draw_grid()
                                self.draw_lines()
                                pygame.display.flip()
            if not is_paused:
                if not self.life.is_max_generations_exceeded and self.life.is_changing:
                    self.life.step()
                    self.draw_grid()
                    self.draw_lines()
                    pygame.display.flip()
                    clock.tick(self.speed)
        pass
