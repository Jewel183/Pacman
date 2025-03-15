import pygame
from config import *
from Pacman import Pacman
from Food import Food

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    clock = pygame.time.Clock()

    # Map đơn giản (Pac-Man chỉ đi trên '.')
    maze = [
        "####################",
        "#.................F#",
        "#..................#",
        "#F................F#",
        "####################",
    ]

    app = App()
    pacman = Pacman(app, [1, 1])  # Truyền app thay vì screen

    # Tạo danh sách thức ăn từ map
    food_list = []
    for row in range(len(maze)):
        for col in range(len(maze[row])):
            if maze[row][col] == "F":
                food_list.append(Food(app, [col, row]))  # Truyền app thay vì screen

    running = True
    next_direction = pacman.direction  # Hướng tiếp theo do người chơi chọn

    while running:
        screen.fill(BLACK)  # Xóa màn hình mỗi frame

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Khi bấm phím, lưu hướng mong muốn vào next_direction
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    next_direction = "up"
                if event.key == pygame.K_DOWN:
                    next_direction = "down"
                if event.key == pygame.K_LEFT:
                    next_direction = "left"
                if event.key == pygame.K_RIGHT:
                    next_direction = "right"

        # Kiểm tra nếu có thể đổi hướng thì đổi
        pacman.change_direction(next_direction, maze)

        # Pac-Man di chuyển theo hướng hiện tại
        pacman.move_forward(maze)

        # Cập nhật Pac-Man
        pacman.update()

        # Vẽ thức ăn trước, để Pac-Man hiển thị trên cùng
        for food in food_list:
            if not food.eaten:
                food.draw()

        # Kiểm tra va chạm với thức ăn
        pacman.eat_food(food_list)

        # **Vẽ Pac-Man Cuối Cùng**
        pacman.draw()

        # Cập nhật màn hình
        pygame.display.update()
        clock.tick(10)  # Giữ FPS ổn định

    pygame.quit()
