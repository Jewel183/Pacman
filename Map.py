import pygame
from config import *
from enum import Enum

class App:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))

class CState(Enum):
    MONSTER = 3  # Đại diện cho Ghost
    PACMAN = 4   # Đại diện cho Pac-Man

class Cell:
    def __init__(self, pos, state):
        self.pos = pos
        self.heuristic = 0
        self.visited = 0
        self.state = state

    def exist_monster(self):
        return CState.MONSTER in self.state

    def reset_heuristic(self):
        self.heuristic = 0

    def monster_leave(self):
        self.state.remove(CState.MONSTER)

    def monster_come(self):
        self.state.append(CState.MONSTER)

    def pacman_leave(self):
        self.state.remove(CState.PACMAN)

    def pacman_come(self):
        self.state.append(CState.PACMAN)

    def objective_function(self):
        return self.heuristic - self.visited

def input_raw(map_input_path):
    """ Đọc file bản đồ thô từ file txt """
    try:
        with open(map_input_path, "r") as f:
            pacman_pos = [int(x) for x in next(f).split()]
            raw_map = [[int(num) for num in line.strip()] for line in f]
    except FileNotFoundError:
        print(f"Không thể đọc file '{map_input_path}'. Kiểm tra lại đường dẫn!")
        return None, None

    return (pacman_pos[0], pacman_pos[1]), raw_map

def init_cells(raw_map, pacman_pos):
    """ Khởi tạo các ô trong bản đồ """
    cells = []

    for y in range(len(raw_map)):
        row = []
        for x in range(len(raw_map[y])):
            if raw_map[y][x] != 1:  # Không phải tường
                row.append(Cell((x, y), []))
                if pacman_pos == (x, y):
                    row[x].state.append(CState.PACMAN)
                    pacman_cell = row[x]
            else:
                row.append(None)  # Tường
        cells.append(row)

    return cells, pacman_cell

def read_map(map_input_path):
    """ Đọc file map và xây dựng đồ thị cho thuật toán tìm đường """
    pacman_pos, raw_map = input_raw(map_input_path)
    if pacman_pos is None or raw_map is None:
        return None, None, None

    ghost_positions = []
    graph_map = {}

    for y in range(len(raw_map)):
        for x in range(len(raw_map[y])):
            if raw_map[y][x] != 1:  # Không phải tường
                if raw_map[y][x] == 3:  # Ghost
                    ghost_positions.append((x, y))
                    raw_map[y][x] = 0  # Đặt lại thành đường đi
                
                cur = (x, y)
                graph_map[cur] = []

                # Kiểm tra đường đi bên trái
                if x - 1 >= 0 and raw_map[y][x - 1] != 1:
                    left = (x - 1, y)
                    graph_map[left].append(cur)
                    graph_map[cur].append(left)

                # Kiểm tra đường đi phía trên
                if y - 1 >= 0 and raw_map[y - 1][x] != 1:
                    up = (x, y - 1)
                    graph_map[up].append(cur)
                    graph_map[cur].append(up)

    return graph_map, pacman_pos, ghost_positions