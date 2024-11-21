import pygame, board




if __name__ == "__main__":
    board_size = 9
    screen_size = (60 * board_size, (60 * board_size) + 100)
    pygame.init()
    screen = pygame.display.set_mode(screen_size)
    clock = pygame.time.Clock()
    running = True

    board = board.Board(board_size,board_size,screen, "easy")
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                temp = board.click(x, y)
                print(temp)
                if temp is not None:
                    board.select(temp[0],temp[1])

        board.draw()
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()