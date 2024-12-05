import pygame
import board
import time
import pygame.mixer


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
        self.hovered_cell = None # Adding mouse hover effect
        self.pause_time = False # Adding pause to timer (for after winning)
        self.total_time = 0
        self.start_time= None # adding time

        #generate buttons
        self.start_buttons, self.game_buttons, self.end_button = self.init_buttons()

        # Sounds
        pygame.mixer.init()
        self.lose_sound = pygame.mixer.Sound("sounds/Lose_Sound1.wav")
        self.win_sound = pygame.mixer.Sound("sounds/Win_Sound1.wav")
        self.start_sound = pygame.mixer.Sound("sounds/Start_Sound1.wav")
        pygame.mixer.music.load("sounds/Background_Audio.mp3")
        pygame.mixer.music.play(-1)

    def init_buttons(self):
         # Button dimensions
        button_width = 300
        button_spacing = 30

        # Coordinates to center buttons
        x = (WINDOW_WIDTH - button_width) // 2
        y = (WINDOW_HEIGHT - (3 * BUTTON_HEIGHT + 2 * button_spacing)) // 2

        start_buttons = {
            "easy": pygame.Rect(x, y, button_width, BUTTON_HEIGHT),
            "medium": pygame.Rect(x, y + BUTTON_HEIGHT + button_spacing, button_width, BUTTON_HEIGHT),
            "hard": pygame.Rect(x, y + 2 * (BUTTON_HEIGHT + button_spacing), button_width, BUTTON_HEIGHT),
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

        if self.total_time == 0:
            self.total_time = time.time() - self.start_time
        sec = int(self.total_time // 60)
        min = int(self.total_time % 60)
        timfont = pygame.font.Font(None, 24)
        time_text = timfont.render(f'Total Time: {sec:02}:{min:02}', True, BLACK) # add total gamelength time
        screen.blit(time_text, (WINDOW_WIDTH // 2 - time_text.get_width() // 2, 120))

        pygame.draw.rect(screen, WHITE, self.end_button)
        text_surf = font.render("Exit", True, BLACK)
        screen.blit(text_surf, (self.end_button.x + (self.end_button.width - text_surf.get_width()) // 2,
                                self.end_button.y + (self.end_button.height - text_surf.get_height()) // 2))
        return self.end_button


    def draw_grid(self):
        for x in range(GRID_SIZE):
            for y in range(GRID_SIZE):
                rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(screen, WHITE, rect)
                pygame.draw.rect(screen, BLACK, rect, width=1)
        # Draw bold lines for 3x3 boxes
        for i in range(0, GRID_SIZE + 1, 3):
            pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, WINDOW_WIDTH), width=3)
            pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WINDOW_WIDTH, i * CELL_SIZE), width=3)
        if self.board:
            self.board.draw()

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

    def timer(self):
        if not self.pause_time:
            ttime=time.time() - self.start_time
            sec=int(ttime//60)
            min=int(ttime%60)
            timfont=pygame.font.Font(None,24)
            time_text=timfont.render(f' {sec:02}:{min:02}', True, BLACK)
            screen.blit(time_text, (WINDOW_WIDTH//2- time_text.get_width()//2, WINDOW_HEIGHT-97))

    def run(self):
        while self.running:
            if self.state == "start":
                easy_button, medium_button, hard_button = self.draw_start_screen()
            elif self.state == "game":
                self.draw_grid()
                reset_button, restart_button, exit_button = self.draw_buttons()
                if not self.pause_time:
                    self.timer()
            elif self.state == "won":
                if not self.pause_time:
                    self.pause_time = True
                    self.total_time = time.time() - self.start_time
                end_button = self.draw_win_screen()
            elif self.state == "lost":
                end_button = self.draw_lose_screen()

            if self.hovered_cell and self.state == "game":
                row, col = self.hovered_cell
                hover_rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                hover_surface = pygame.Surface((CELL_SIZE, CELL_SIZE))
                hover_surface.set_alpha(50)
                hover_surface.fill((0, 200, 200))
                screen.blit(hover_surface, (col * CELL_SIZE, row * CELL_SIZE))
                pygame.draw.rect(screen, BLACK, hover_rect, width=2)

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
                            self.start_sound.play()
                            self.start_time=time.time()
                        elif medium_button.collidepoint(event.pos):
                            self.difficulty = "medium"
                            self.board = board.Board(GRID_SIZE, GRID_SIZE, screen, self.difficulty)
                            self.state = "game"
                            self.start_sound.play()
                            self.start_time = time.time()
                        elif hard_button.collidepoint(event.pos):
                            self.difficulty = "hard"
                            self.board = board.Board(GRID_SIZE, GRID_SIZE, screen, self.difficulty)
                            self.state = "game"
                            self.start_sound.play()
                            self.start_time = time.time()
                elif self.state == "game":
                    if event.type == pygame.MOUSEMOTION:
                        x, y = event.pos
                        row = y // CELL_SIZE
                        col = x // CELL_SIZE
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE:
                            self.hovered_cell = (row,col)
                        else: self.hovered_cell = None
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
                                self.win_sound.play()
                                self.pause_time = True
                                self.state = "won"
                            else:
                                self.lose_sound.play()
                                self.pause_time = True
                                self.state = "lost"
                elif self.state == "won":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_button.collidepoint(event.pos):
                            self.pause_time = False
                            self.start_time = None
                            self.running = False
                elif self.state == "lost":
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if end_button.collidepoint(event.pos):
                            self.pause_time = False
                            self.start_time = None
                            self.state = "start"

        self.board.update_board()


if __name__ == "__main__":
    ui = SudokuUI()
    ui.run()
    pygame.quit()