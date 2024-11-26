import pygame
import sys
import board

# Constants
WINDOW_WIDTH = 540
WINDOW_HEIGHT = 640
GRID_SIZE = 9
CELL_SIZE = WINDOW_WIDTH // GRID_SIZE
BUTTON_HEIGHT = 50

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GRAY = (200, 200, 200)
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize PyGame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku Game")

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)


class SudokuUI:
    def __init__(self):
        self.running = True
        self.state = "start"  # Possible states: start, game, win, lose
        self.board = None
        self.selected_cell = None
        self.difficulty = None

    def draw_start_screen(self):
        screen.fill(LIGHT_BLUE)
        title_text = font.render("Welcome to Sudoku!", True, BLACK)
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 50))

        easy_button = pygame.Rect(100, 200, 400, BUTTON_HEIGHT)
        medium_button = pygame.Rect(100, 300, 400, BUTTON_HEIGHT)
        hard_button = pygame.Rect(100, 400, 400, BUTTON_HEIGHT)

        pygame.draw.rect(screen, WHITE, easy_button)
        pygame.draw.rect(screen, WHITE, medium_button)
        pygame.draw.rect(screen, WHITE, hard_button)

        screen.blit(font.render("Easy", True, BLACK), (250, 210))
        screen.blit(font.render("Medium", True, BLACK), (240, 310))
        screen.blit(font.render("Hard", True, BLACK), (250, 410))

        return easy_button, medium_button, hard_button

    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect, width=1)
        self.board.draw()

        # Draw bold lines for 3x3 boxes
        for i in range(0, GRID_SIZE + 1, 3):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_WIDTH), width=3)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), width=3)

    def draw_buttons(self):
        reset_button = pygame.Rect(25, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT)
        restart_button = pygame.Rect(200, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT)
        exit_button = pygame.Rect(375, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT)

        pygame.draw.rect(screen, GREEN, reset_button)
        pygame.draw.rect(screen, YELLOW, restart_button)
        pygame.draw.rect(screen, RED, exit_button)

        screen.blit(font.render("Reset", True, BLACK), (70, WINDOW_HEIGHT - 70))
        screen.blit(font.render("Restart", True, BLACK), (230, WINDOW_HEIGHT - 70))
        screen.blit(font.render("Exit", True, WHITE), (425, WINDOW_HEIGHT - 70))

        return reset_button, restart_button, exit_button

    def run(self):
        while self.running:
            screen.fill(WHITE)
            if self.state == "start":
                easy_button, medium_button, hard_button = self.draw_start_screen()
            elif self.state == "game":
                self.draw_grid()
                reset_button, restart_button, exit_button = self.draw_buttons()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.state == "start":
                        if easy_button.collidepoint(event.pos):
                            self.difficulty = "easy"
                            self.board = board.Board(GRID_SIZE,GRID_SIZE,screen, self.difficulty)
                            self.state = "game"
                        elif medium_button.collidepoint(event.pos):
                            self.difficulty = "medium"
                            self.board = board.Board(GRID_SIZE, GRID_SIZE, screen, self.difficulty)
                            self.state = "game"
                        elif hard_button.collidepoint(event.pos):
                            self.difficulty = "hard"
                            self.board = board.Board(GRID_SIZE, GRID_SIZE, screen, self.difficulty)
                            self.state = "game"
                    elif self.state == "game":
                        if reset_button.collidepoint(event.pos):
                            self.board.reset_to_original()
                        elif restart_button.collidepoint(event.pos):
                            self.state = "start"
                        elif exit_button.collidepoint(event.pos):
                            self.running = False

                        x, y = event.pos
                        temp = self.board.click(x, y)
                        if temp is not None:
                            self.board.select(temp[0], temp[1])
                elif event.type == pygame.KEYDOWN:
                    if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                        if self.board.selected_cell is None:
                            self.board.select(0, 0)
                        else:
                            temp_row = self.board.selected_cell.row
                            temp_col = self.board.selected_cell.col
                            if event.key == pygame.K_UP:
                                temp_row -= 1
                            if event.key == pygame.K_DOWN:
                                temp_row += 1
                            if event.key == pygame.K_LEFT:
                                temp_col -= 1
                            if event.key == pygame.K_RIGHT:
                                temp_col += 1
                            temp_row = max(0, min(temp_row, GRID_SIZE - 1))
                            temp_col = max(0, min(temp_col, GRID_SIZE - 1))
                            self.board.select(temp_row, temp_col)
                    if event.key == pygame.K_RETURN and (
                            self.board.selected_cell is not None) and self.board.selected_cell.sketched_value != 0:
                        self.board.place_number(self.board.selected_cell.sketched_value)

                    if (pygame.K_1 <= event.key <= pygame.K_9) and self.board.selected_cell is not None:
                        num = event.key - pygame.K_0
                        self.board.sketch(num)


if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()
    sys.exit()