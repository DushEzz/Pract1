import curses
from datetime import datetime
from pathlib import Path

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        screen.border("|", "|", "-", "-", "#", "#", "#", "#")

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        # for pos_x, row in enumerate(self.life.curr_generation):
        #     for pos_y, value in enumerate(row):
        for pos_y in range(self.life.cols):
            for pos_x in range(self.life.rows):
                symbol = arguments.symbol if self.life.curr_generation[pos_x][pos_y] else " "
                try:
                    screen.addstr(pos_x + 1, pos_y + 1, symbol, curses.A_STANDOUT)
                except curses.error:
                    continue

    def run(self) -> None:
        win = curses.initscr()
        curses.curs_set(0)
        limits = win.getmaxyx()
        if arguments.rows > limits[0] - 1 or arguments.cols > limits[1] - 1:
            raise ValueError(f'Невозможно отрисовать картинку такого размера. Максимальный размер {limits[0]}x{limits[1]}.')
        curses.noecho()
        win = curses.newwin(self.life.rows + 2, self.life.cols + 2, 0, 0)
        win.nodelay(True)
        running = True
        pause = False
        while running:
            if not self.life.is_changing or self.life.is_max_generations_exceeded:
                running = False
            char = win.getch()
            if char == ord(' '):
                pause = not pause
            if char == ord('s'):
                save_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                self.life.save(Path(f"saves/life_{save_time}.txt"))
            if char == ord('q'):
                running = False
            if not pause:
                win.clear()
                curses.delay_output(50)
                self.draw_borders(win)
                self.draw_grid(win)
                self.life.step()
                win.refresh()
        curses.endwin()
