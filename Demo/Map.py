import pygame
from config import *
from Pacman import Pacman
from enum import Enum

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))


class CState(Enum):
    FOOD = 2
    MONSTER = 3
    PACMAN = 4

class Cell:
    def __init__(self, pos, state):
        self.pos = pos
        self.heuristic = 0
        self.visited = 0
        self.state = state


    def exist_food(self):
        return CState.FOOD in self.state


    def exist_monster(self):
        return CState.MONSTER in self.state


    def reset_heuristic(self):
        self.heuristic = 0


    def food_ate(self):
        self.state.remove(CState.FOOD)


    def monster_leave(self):
        self.state.remove(CState.MONSTER)


    def monster_come(self):
        self.state.append(CState.MONSTER)


    def pacman_leave(self):
        self.state.remove(CState.PACMAN)


    def pacman_come(self):
        self.state.append(CState.PACMAN)

        if CState.FOOD in self.state:
            self.state.remove(CState.FOOD)

        self.visited += 1


    def objective_function(self):
        return self.heuristic - self.visited


def input_raw(map_input_path):
    try:
        f = open(map_input_path, "r")
    except:
        print("Can not read file \'" + map_input_path + "\'. Please check again!")
        return None

    pacman_pos = [int(x) for x in next(f).split()]
    raw_map = [[int(num) for num in line if num != '\n'] for line in f]

    return (pacman_pos[0], pacman_pos[1]), raw_map


def init_cells(raw_map, pacman_pos):
    cells = []

    for y in range(len(raw_map)):
        row = []
        for x in range(len(raw_map[y])):
            if raw_map[y][x] != 1:
                if raw_map[y][x] == 0:
                    row.append(Cell((x, y), []))
                else:
                    row.append(Cell((x, y), [CState(raw_map[y][x])]))

                if pacman_pos == (x, y):
                    row[x].state.append(CState(4))
                    pacman_cell = row[x]
            else:
                row.append(None)
        cells.append(row)

    return cells, pacman_cell


def read_map(map_input_path):
    pacman_pos, raw_map = input_raw(map_input_path)
    food_pos = None
    monster_pos_list = []

    graph_map = {}
    for y in range(len(raw_map)):
        for x in range(len(raw_map[y])):
            if raw_map[y][x] != 1:
                if raw_map[y][x] == 2:
                    food_pos = (x, y)
                elif raw_map[y][x] == 3:
                    monster_pos_list.append((x, y))
                    raw_map[y][x] = 1

                cur = (x, y)
                graph_map[cur] = []

                if x - 1 >= 0 and raw_map[y][x - 1] != 1:
                    left = (x - 1, y)
                    graph_map[left] = graph_map[left] + [cur]
                    graph_map[cur] = graph_map[cur] + [left]

                if y - 1 >= 0 and raw_map[y - 1][x] != 1:
                    up = (x, y - 1)
                    graph_map[up] = graph_map[up] + [cur]
                    graph_map[cur] = graph_map[cur] + [up]

    return graph_map, pacman_pos, food_pos, monster_pos_list



if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    clock = pygame.time.Clock()

    #cells, graph_cell, pacman_cell, graph_map, food_cell_list, monster_cell_list = read_map(r"./map.txt")

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
    # food_list = []
    # for row in range(len(maze)):
    #     for col in range(len(maze[row])):
    #         if maze[row][col] == "F":
    #             food_list.append(Food(app, [col, row]))  # Truyền app thay vì screen

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
        # pacman.change_direction(next_direction, maze)

        # Pac-Man di chuyển theo hướng hiện tại
        # pacman.move_forward(maze)
        pacman.move(maze)
        # Cập nhật Pac-Man
        pacman.update(6, maze)

        # Vẽ thức ăn trước, để Pac-Man hiển thị trên cùng
        # for food in food_list:
        #     if not food.eaten:
        #         food.draw()

        # # Kiểm tra va chạm với thức ăn
        # pacman.eat_food(food_list)

        # **Vẽ Pac-Man Cuối Cùng**
        pacman.draw()

        # Cập nhật màn hình
        pygame.display.update()
        clock.tick(10)  # Giữ FPS ổn định

    pygame.quit()
