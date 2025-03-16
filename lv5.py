import pygame
import time
from config import *  # Import các giá trị như APP_WIDTH, APP_HEIGHT, CELL_SIZE
from Pacman import *  # Import Pac-Man
from Ghost import *  # Import thuật toán BFS
from Map import *  # Import hàm đọc bản đồ

class Level5:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        pygame.display.set_caption("Level 1: Blue Ghost tìm Pac-Man (BFS)")
        self.font = pygame.font.SysFont("arial", 20)
        self.running = True
        self.map_img = pygame.image.load(MAP_IMG)
        self.map_img = pygame.transform.scale(self.map_img, (MAP_WIDTH, MAP_HEIGHT))
        self.graph, self.pacman_pos, _ = read_map(MAP_INPUT_TXT)
        self.maze = self.create_maze() 
        self.pacman = Pacman(self, self.pacman_pos)
        
        # // 26 29 // 1 29 // 13 14 // 26 1 // 1 20
        self.blue_ghost = Blue(self, (26, 29))
        self.pink_ghost = Pink(self, (1, 29))
        self.orange_ghost = Orange(self, (13, 14))
        self.red_ghost = Red(self, (1, 20))
        
        
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
        # self.draw_grids()  # Vẽ lưới (nếu muốn)

        # Vẽ Pac-Man & Ghost
        self.pacman.draw()
        self.blue_ghost.draw()
        self.pink_ghost.draw()
        self.orange_ghost.draw()
        self.red_ghost.draw()

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
        """ Vòng lặp chạy Level 5 """
        found_pacman = [False, False, False, False]  # Kiểm tra khi nào ma tìm thấy Pac-Man

        while self.running:
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return "back"

            if not found_pacman[0]:
                # BFS
                path1, expanded_nodes1, memory_usage1, search_time1 = bfs(tuple(self.blue_ghost.grid_pos), tuple(self.pacman.grid_pos), self.maze, track_stats=True)
                
                self.blue_ghost.expanded_nodes = expanded_nodes1
                self.blue_ghost.memory_usage = memory_usage1
                self.blue_ghost.search_time = search_time1
                if path1:
                    self.blue_ghost.move_toward(path1, self.maze)
                # Kiểm tra nếu ma xanh bắt được Pac-Man
                if tuple(self.blue_ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman[0] = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Blue Ghost (BFS) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Thời gian tìm kiếm BFS: {self.blue_ghost.search_time:.4f} giây")
                    print(f"Số nút mở rộng: {self.blue_ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.blue_ghost.memory_usage} bytes")
                    
            
            if not found_pacman[2]: 
                # UCS
                graph3 = {}
                for y in range(len(self.maze)):
                    for x in range(len(self.maze[0])):
                        if self.maze[y][x] != 1:  # Nếu không phải tường
                            pos = (x, y)
                            graph3[pos] = []
                            # Thêm các hàng xóm hợp lệ
                            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] != 1:
                                    # Thêm trọng số (weight) - có thể đặt là 1 nếu chi phí đồng nhất
                                    graph3[pos].append(((nx, ny), 1))

                # Gọi UCS
                path3, expanded_nodes3, memory_usage3, search_time3 = ucs(
                    graph3, 
                    tuple(self.orange_ghost.grid_pos), 
                    tuple(self.pacman.grid_pos), 
                    track_stats=True
                )
                
                self.orange_ghost.expanded_nodes = expanded_nodes3
                self.orange_ghost.memory_usage = memory_usage3
                self.orange_ghost.search_time = search_time3
                
                if path3:
                    self.orange_ghost.move_toward(path3, self.maze)
                
                # Kiểm tra nếu ma xanh bắt được Pac-Man
                if tuple(self.orange_ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman[2] = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Orange Ghost (UCS) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Thời gian tìm kiếm UCS: {self.orange_ghost.search_time:.4f} giây")
                    print(f"Số nút mở rộng: {self.orange_ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.orange_ghost.memory_usage} bytes")
                    
                    
            if not found_pacman[3]:
                #  A*
                graph4 = {}
                for y in range(len(self.maze)):
                    for x in range(len(self.maze[0])):
                        if self.maze[y][x] != 1:  # Nếu không phải tường
                            pos = (x, y)
                            graph4[pos] = []
                            # Thêm các hàng xóm hợp lệ
                            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] != 1:
                                    graph4[pos].append(((nx, ny), 1))  # Trọng số 1 cho mỗi bước đi

                pacman_pos = tuple(self.pacman.grid_pos)
                heuristic = {}
                for y in range(len(self.maze)):
                    for x in range(len(self.maze[0])):
                        if self.maze[y][x] != 1:  # Nếu không phải tường
                            pos = (x, y)
                            # Tính khoảng cách Manhattan
                            heuristic[pos] = manhattan_distance(pos, pacman_pos)

                path4, expanded_nodes4, memory_usage4, search_time4 = a_star(
                    graph4, 
                    tuple(self.red_ghost.grid_pos), 
                    tuple(self.pacman.grid_pos), 
                    heuristic, 
                    track_stats=True
                )
                
                # path, expanded_nodes, memory_usage, search_time = bfs(tuple(self.ghost.grid_pos), tuple(self.pacman.grid_pos), self.maze, track_stats=True)
                
                self.red_ghost.expanded_nodes = expanded_nodes4
                self.red_ghost.memory_usage = memory_usage4
                self.red_ghost.search_time = search_time4
                
                if path4:
                    self.red_ghost.move_toward(path4, self.maze)
                
                # Kiểm tra nếu ma xanh bắt được Pac-Man
                if tuple(self.red_ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman[3] = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Red Ghost (A*) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Thời gian tìm kiếm A*: {self.red_ghost.search_time:.4f} giây")
                    print(f"Số nút mở rộng: {self.red_ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.red_ghost.memory_usage} bytes")
                    

            pygame.display.update()

        pygame.quit()
        
        
if __name__ == "__main__":
    test = Level5()
    test.run()
