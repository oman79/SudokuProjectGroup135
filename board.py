import pygame
from cell import Cell
from sudoku_generator import SudokuGenerator, generate_sudoku


class Board:
    def __init__(self, width, height, screen, difficulty):
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        removed_cells = {"easy": 30, "medium": 40, "hard": 50}
        self.board = generate_sudoku(9, removed_cells[difficulty])
        self.cells = [[Cell(self.board[row][col], row, col, screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def draw(self):
        self.screen.fill("lightblue")
        for i in range(10):
            line_width = 4 if i % 3 == 0 else 2
            pygame.draw.line(self.screen, (0, 0, 0), (0, i * 60), (540, i * 60), line_width)
            pygame.draw.line(self.screen, (0, 0, 0), (i * 60, 0), (i * 60, 540), line_width)
        for row in self.cells:
            for cell in row:
                cell.draw()

    def select(self, row, col):
        if self.selected_cell:
            self.selected_cell.selected = False
        self.selected_cell = self.cells[row][col]
        self.selected_cell.selected = True

    def click(self, x, y):
        if 0 <= x <= self.width*60 and 0 <= y <= self.height*60:
            return y // 60, x // 60
        return None

    def clear(self):
        if self.board[self.selected_cell.row][self.selected_cell.col]==0:
            self.selected_cell.set_sketched_value(0)
            self.selected_cell.set_cell_value(0)

    def sketch(self, value):
        if self.selected_cell and self.selected_cell.original_value == 0:
            self.selected_cell.set_cell_value(0)
            self.selected_cell.set_sketched_value(value)

    def place_number(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.sketched_value = 0

    def reset_to_original(self):
        pass

    def is_full(self):
        pass

    def update_board(self):
        pass

    def find_empty(self):
        pass

    def check_board(self):
        pass
