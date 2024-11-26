import pygame
import sys

# Constants
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 700
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

        # Draw bold lines for 3x3 boxes
        for i in range(0, GRID_SIZE + 1, 3):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_WIDTH), width=3)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), width=3)

    def draw_buttons(self):
        reset_button = pygame.Rect(50, WINDOW_HEIGHT - 130, 150, BUTTON_HEIGHT)
        restart_button = pygame.Rect(225, WINDOW_HEIGHT - 130, 150, BUTTON_HEIGHT)
        exit_button = pygame.Rect(400, WINDOW_HEIGHT - 130, 150, BUTTON_HEIGHT)

        pygame.draw.rect(screen, GREEN, reset_button)
        pygame.draw.rect(screen, LIGHT_BLUE, restart_button)
        pygame.draw.rect(screen, RED, exit_button)

        screen.blit(font.render("Reset", True, BLACK), (85, WINDOW_HEIGHT - 120))
        screen.blit(font.render("Restart", True, BLACK), (245, WINDOW_HEIGHT - 120))
        screen.blit(font.render("Exit", True, WHITE), (440, WINDOW_HEIGHT - 120))

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
                            self.state = "game"
                        elif medium_button.collidepoint(event.pos):
                            self.difficulty = "medium"
                            self.state = "game"
                        elif hard_button.collidepoint(event.pos):
                            self.difficulty = "hard"
                            self.state = "game"
                    elif self.state == "game":
                        if reset_button.collidepoint(event.pos):
                            print("Reset button clicked")
                        elif restart_button.collidepoint(event.pos):
                            self.state = "start"
                        elif exit_button.collidepoint(event.pos):
                            self.running = False


if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()
    sys.exit()