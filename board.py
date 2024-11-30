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
        self.board_original = [row[:] for row in self.board]
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
            row = self.selected_cell.row
            col = self.selected_cell.col
            self.board[row][col] = 0


    def place_number(self, value):
        if self.selected_cell and self.selected_cell.value == 0:
            self.selected_cell.set_cell_value(value)
            self.selected_cell.sketched_value = 0
            row = self.selected_cell.row
            col = self.selected_cell.col
            self.board[row][col] = value

    def reset_to_original(self):
        self.cells = [[Cell(self.board_original[row][col], row, col, self.screen) for col in range(9)] for row in range(9)]
        self.selected_cell = None

    def is_full(self):
        for i,row in enumerate(self.board):
            for j, cell in enumerate(row):
                if cell== 0:
                    return False
        return True

    def update_board(self):
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.board[i][j] = col.value

    def find_empty(self):
        pass

    def check_board(self):
        for row in self.board:
            if len(row) != len(set(row)):
                return False
        for col in [[row[i] for row in self.board] for i in range(len(self.board[0]))]:
            if len(col) != len(set(row)):
                return False

        for i in range(3):
            for j in range(3):
                current_box = [row[3 * j:3 * j + 3] for row in self.board[3 * i:3 * i + 3]]
                temp = set()
                for row in current_box:
                    for num in row:
                        if num in temp:
                            return False
                        else:
                            temp.add(num)
        return True