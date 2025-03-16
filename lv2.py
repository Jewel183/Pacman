import pygame
import time
from config import *  # Import các giá trị như APP_WIDTH, APP_HEIGHT, CELL_SIZE
from Pacman import *  # Import Pac-Man
from Ghost import *  # Import thuật toán BFS
from Map import *  # Import hàm đọc bản đồ

class Level2:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        pygame.display.set_caption("Level 2: Pink Ghost tìm Pac-Man (DDFS)")
        self.font = pygame.font.SysFont("arial", 20)
        self.running = True
        self.map_img = pygame.image.load(MAP_IMG)
        self.map_img = pygame.transform.scale(self.map_img, (MAP_WIDTH, MAP_HEIGHT))
        self.graph, self.pacman_pos, _ = read_map(MAP_INPUT_TXT)
        self.maze = self.create_maze() 
        self.pacman = Pacman(self, self.pacman_pos)
        self.ghost = Pink(self, (12, 5))
        self.start_time = time.time()
        self.back_button = pygame.Rect(0, 0, 80, 40)

    def create_maze(self):
        """ Chuyển bản đồ từ graph thành ma trận ký tự """
        max_x = max([x for x, y in self.graph.keys()])
        max_y = max([y for x, y in self.graph.keys()])
        
        # Điều chỉnh kích thước `maze` theo thực tế bản đồ
        maze = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
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
            
    
    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.map_img, (MAP_POS_X, MAP_POS_Y))  # Vẽ bản đồ
        self.draw_grids()  # Vẽ lưới (nếu muốn)

        # Vẽ Pac-Man & Ghost
        self.pacman.draw()
        self.ghost.draw()

        # Vẽ nút BACK
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            button_color = LIGHT_GREY  
        else:
            button_color = DARK_GREY
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)
        text_surf = pygame.font.SysFont("arial", 30).render("Back", True, WHITE)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)

        pygame.display.update()
    

    def run(self):
        """ Vòng lặp chạy Level 2 """
        found_pacman = False  # Kiểm tra khi nào ma tìm thấy Pac-Man

        while self.running:
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return "back"

            if not found_pacman:
                path, expanded_nodes, memory_usage, search_time = dfs(tuple(self.ghost.grid_pos), tuple(self.pacman.grid_pos), self.maze, track_stats=True)
                
                self.ghost.expanded_nodes = expanded_nodes
                self.ghost.memory_usage = memory_usage
                self.ghost.search_time = search_time
                
                if path:
                    self.ghost.move_toward(path, self.maze)
                
                
                if tuple(self.ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Blue Ghost (BFS) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Thời gian tìm kiếm BFS: {self.ghost.search_time:.4f} giây")
                    print(f"Số nút mở rộng: {self.ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.ghost.memory_usage} bytes")

            pygame.display.update()

        pygame.quit()
        
        
    

if __name__ == "__main__":
    test = Level2()
    test.run()