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
                if temp is not None:
                    board.select(temp[0],temp[1])

            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT):
                    if board.selected_cell is None:
                        board.select(0,0)
                    else:
                        temp_row = board.selected_cell.row
                        temp_col = board.selected_cell.col
                        if event.key == pygame.K_UP:
                            temp_row-=1
                        if event.key == pygame.K_DOWN:
                            temp_row+=1
                        if event.key == pygame.K_LEFT:
                            temp_col-=1
                        if event.key == pygame.K_RIGHT:
                            temp_col+=1
                        temp_row = max(0, min(temp_row, board_size-1))
                        temp_col = max(0, min(temp_col, board_size-1))
                        board.select(temp_row, temp_col)
                if event.key == pygame.K_RETURN and (board.selected_cell is not None) and board.selected_cell.sketched_value != 0:
                    board.place_number(board.selected_cell.sketched_value)

                if (pygame.K_1 <= event.key <= pygame.K_9) and board.selected_cell is not None:
                    num = event.key - pygame.K_0
                    board.sketch(num)



        board.draw()
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()