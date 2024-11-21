import pygame


class Cell:
    def __init__(self, value, row, col, screen):
        self.original_value = value
        self.value = value
        self.row = row
        self.col = col
        self.screen = screen
        self.sketched_value = value
        self.selected = False
        self.font = pygame.font.Font(None, 40)

    def set_cell_value(self, value):
        self.value = value

    def set_sketched_value(self, value):
        self.sketched_value = value

    def draw(self):
        #making some assumptions about cell and screen resolution
        x = self.col * 60
        y = self.row * 60


        if self.original_value != 0:
            text = self.font.render(str(self.value), True, (0, 0, 0))
            self.screen.blit(text, (x + 20 + 3, y + 15 + 3))
        else:
            if self.sketched_value == 0 and self.value !=0:
                text = self.font.render(str(self.value), True, (255, 0, 0))
                self.screen.blit(text, (x + 20 + 3, y + 15 + 3))
            elif self.sketched_value != 0 and self.value ==0:
                text = self.font.render(str(self.sketched_value), True, (255, 128, 128))
                self.screen.blit(text, (x + 5, y + 5))
            else:
                text = self.font.render("", True, (0, 0, 0))
                self.screen.blit(text, (x + 20 + 3, y + 15 + 3))

        if self.selected:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, 60, 60), 3)
