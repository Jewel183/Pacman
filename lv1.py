import pygame
import time
from config import *  # Import các giá trị như APP_WIDTH, APP_HEIGHT, CELL_SIZE
from Pacman import *  # Import Pac-Man
from Ghost import *  # Import thuật toán BFS
from Map import *  # Import hàm đọc bản đồ

class GridTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        pygame.display.set_caption("Level 1: Blue Ghost tìm Pac-Man (BFS)")
        self.font = pygame.font.SysFont("arial", 20)
        self.running = True

        # Load ảnh bản đồ
        self.map_img = pygame.image.load(MAP_IMG)
        self.map_img = pygame.transform.scale(self.map_img, (MAP_WIDTH, MAP_HEIGHT))

        # Đọc bản đồ từ file
        self.graph, self.pacman_pos, _ = read_map(MAP_INPUT_TXT)
        self.maze = self.create_maze()  # Chuyển map thành ma trận ký tự
        
        # Tạo Pac-Man (đứng yên)
        self.pacman = Pacman(self, self.pacman_pos)

        # Tạo ma xanh (Blue Ghost)
        self.ghost = Blue(self, (14, 13))

        # Thời gian bắt đầu tìm kiếm
        self.start_time = time.time()

    def create_maze(self):
        """ Chuyển bản đồ từ graph thành ma trận ký tự """
        max_x = max([x for x, y in self.graph.keys()])
        max_y = max([y for x, y in self.graph.keys()])
        
        # Điều chỉnh kích thước `maze` theo thực tế bản đồ
        maze = [['11' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
        for (x, y) in self.graph.keys():
            if 0 <= y < len(maze) and 0 <= x < len(maze[0]):  # Kiểm tra hợp lệ
                maze[y][x] = ' '  # Đường đi
        return maze


    def draw_grids(self):
        """ Vẽ lưới lên màn hình """
        for x in range(int(MAP_WIDTH / CELL_SIZE) + 1):
            num_surface = self.font.render(str(x % 10), True, WHITE)
            self.screen.blit(num_surface, (x * CELL_SIZE + MAP_POS_X + CELL_SIZE // 4, MAP_POS_Y - CELL_SIZE))
            pygame.draw.line(self.screen, (107, 107, 107),
                             (x * CELL_SIZE + MAP_POS_X, MAP_POS_Y),
                             (x * CELL_SIZE + MAP_POS_X, MAP_HEIGHT + MAP_POS_Y))

        for y in range(int(MAP_HEIGHT / CELL_SIZE) + 1):
            num_surface = self.font.render(str(y % 10), True, WHITE)
            self.screen.blit(num_surface, (MAP_POS_X - CELL_SIZE, y * CELL_SIZE + MAP_POS_Y))
            pygame.draw.line(self.screen, (107, 107, 107),
                             (MAP_POS_X, y * CELL_SIZE + MAP_POS_Y),
                             (MAP_WIDTH + MAP_POS_X, y * CELL_SIZE + MAP_POS_Y))

    def run(self):
        """ Vòng lặp chạy Level 1 """
        found_pacman = False  # Kiểm tra khi nào ma tìm thấy Pac-Man

        while self.running:
            self.screen.fill(BLACK)
            self.screen.blit(self.map_img, (MAP_POS_X, MAP_POS_Y))
            self.draw_grids()
            self.pacman.draw()
            self.ghost.draw()

            if not found_pacman:
                path = bfs(tuple(self.ghost.grid_pos), tuple(self.pacman.grid_pos), self.maze)
                # print(f"Full path: {path}")
                self.ghost.move_toward(path, self.maze)

                # Kiểm tra nếu ma xanh bắt được Pac-Man
                if tuple(self.ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Blue Ghost (BFS) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Số nút mở rộng: {self.ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.ghost.memory_usage} bytes")

                    # Chờ 30 giây trước khi đóng
                    pygame.time.delay(30000)
                    self.running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            pygame.display.update()

        pygame.quit()

if __name__ == "__main__":
    test = GridTest()
    test.run()
