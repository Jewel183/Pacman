import pygame
from Pacman import Pacman
from Ghost import *
from config import *

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    clock = pygame.time.Clock()

    # Map đơn giản để test
    maze = [
        "####################",
        "#...............#..#",
        "#..####...#####.#..#",
        "#...............#..#",
        "#####.#####.#####..#",
        "#..................#",
        "####################",
    ]

    # Khởi tạo Pacman
    # app = pygame.Surface((APP_WIDTH, APP_HEIGHT))  # Ứng dụng giả để truyền vào Pacman
    app = App()
    pacman = Pacman(app, [1, 1])

    # Khởi tạo Ghosts
    red_ghost = Red(app, [10, 5])
    blue_ghost = Blue(app, [15, 3])

    ghosts = [red_ghost, blue_ghost]

    def draw_maze():
        for row_idx, row in enumerate(maze):
            for col_idx, cell in enumerate(row):
                if cell == "#":
                    pygame.draw.rect(screen, (50, 50, 255), (col_idx * CELL_SIZE, row_idx * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    # Vòng lặp game
    running = True
    while running:
        screen.fill((0, 0, 0))  # Xóa màn hình
        draw_maze()  # Vẽ lại mê cung
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        # Điều khiển Pacman
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            pacman.change_direction("up", maze)
        elif keys[pygame.K_DOWN]:
            pacman.change_direction("down", maze)
        elif keys[pygame.K_LEFT]:
            pacman.change_direction("left", maze)
        elif keys[pygame.K_RIGHT]:
            pacman.change_direction("right", maze)
        
        # Cập nhật Pacman
        pacman.update()
        pacman.draw()
        
        # Cập nhật và vẽ Ghosts
        for ghost in ghosts:
            ghost.move_toward(bfs(tuple(ghost.grid_pos), tuple(pacman.grid_pos), maze), maze)  # Ma xanh dùng BFS
            ghost.draw()
        
        # Kiểm tra va chạm giữa Pacman và Ghost
        for ghost in ghosts:
            if pacman.grid_pos == ghost.grid_pos:
                print("Game Over!")
                running = False
        
        pygame.display.update()
        clock.tick(30)

    pygame.quit()
