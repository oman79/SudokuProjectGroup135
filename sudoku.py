import pygame
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
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Initialize PyGame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Sudoku Group 135")

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 50)



class SudokuUI:
    def __init__(self):
        self.running = True
        self.state = "start"  # Possible states: start, game, win, lose
        self.board = None
        self.selected_cell = None
        self.difficulty = None

        #generate buttons
        self.start_buttons, self.game_buttons, self.end_button = self.init_buttons()

    def init_buttons(self):
         # Button dimensions
        button_width = 400
        button_height = BUTTON_HEIGHT
        button_spacing = 20  # Space between buttons

        # Center buttons vertically and horizontally
        center_x = (WINDOW_WIDTH - button_width) // 2
        start_y = (WINDOW_HEIGHT - (3 * button_height + 2 * button_spacing)) // 2

        start_buttons = {
            "easy": pygame.Rect(center_x, start_y, button_width, button_height),
            "medium": pygame.Rect(center_x, start_y + button_height + button_spacing, button_width, button_height),
            "hard": pygame.Rect(center_x, start_y + 2 * (button_height + button_spacing), button_width, button_height),
        }

        game_buttons = {
            "reset": pygame.Rect(25, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT),
            "restart": pygame.Rect(200, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT),
            "exit": pygame.Rect(375, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT),
        }

        end_button = pygame.Rect(200, WINDOW_HEIGHT - 80, 150, BUTTON_HEIGHT)
        return start_buttons, game_buttons, end_button

    def draw_start_screen(self):
        screen.fill(LIGHT_BLUE)
        title_text = title_font.render("Welcome to Sudoku!", True, BLACK)
        screen.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 75))

        for title, rect in self.start_buttons.items():
            pygame.draw.rect(screen, WHITE, rect)
            text_surf = font.render(title.capitalize(), True, BLACK)
            screen.blit(text_surf, (rect.x + (rect.width - text_surf.get_width()) // 2, rect.y + (rect.height - text_surf.get_height()) // 2))

        return self.start_buttons["easy"], self.start_buttons["medium"], self.start_buttons["hard"]

    def draw_lose_screen(self):
        screen.fill(LIGHT_BLUE)
        text = title_font.render("You Lost!", True, BLACK)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 75))
        pygame.draw.rect(screen, WHITE, self.end_button)
        text_surf = font.render("Restart", True, BLACK)
        screen.blit(text_surf, (self.end_button.x + (self.end_button.width - text_surf.get_width()) // 2, self.end_button.y + (self.end_button.height - text_surf.get_height()) // 2))
        return self.end_button

    def draw_win_screen(self):
        screen.fill(LIGHT_BLUE)
        text = title_font.render("You Won!", True, BLACK)
        screen.blit(text, (WINDOW_WIDTH // 2 - text.get_width() // 2, 75))
        pygame.draw.rect(screen, WHITE, self.end_button)
        text_surf = font.render("Exit", True, BLACK)
        screen.blit(text_surf, (self.end_button.x + (self.end_button.width - text_surf.get_width()) // 2,
                                self.end_button.y + (self.end_button.height - text_surf.get_height()) // 2))
        return self.end_button


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
        for title, rect in self.game_buttons.items():
            color = WHITE
            color_text = BLACK
            if title == "reset":
                color = GREEN
            elif title == "restart":
                color = YELLOW
            elif title == "exit":
                color = RED
                color_text = WHITE

            # Draw the button
            pygame.draw.rect(screen, color, rect)
            text_surface = font.render(title.capitalize(), True, color_text)
            # Draw the text on the button
            screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2, rect.y + (rect.height - text_surface.get_height()) // 2))

        return self.game_buttons["reset"], self.game_buttons["restart"], self.game_buttons["exit"]

    def run(self):
        while self.running:
            screen.fill(WHITE)
            if self.state == "start":
                easy_button, medium_button, hard_button = self.draw_start_screen()
            elif self.state == "game":
                self.draw_grid()
                reset_button, restart_button, exit_button = self.draw_buttons()
            elif self.state == "won":
                end_button = self.draw_win_screen()
            elif self.state == "lost":
                end_button = self.draw_lose_screen()

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

                if self.state == "start":
                    if event.type == pygame.MOUSEBUTTONDOWN:
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
                    if event.type == pygame.MOUSEBUTTONDOWN:
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

                    if self.board is not None:
                        if self.board.is_full():
                            if self.board.check_board():
                                self.state = "won"
                            else:
                                self.state = "lost"
                elif self.state == "won":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_button.collidepoint(event.pos):
                            self.running = False
                elif self.state == "lost":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_button.collidepoint(event.pos):
                            self.state = "start"

        self.board.update_board()


if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()