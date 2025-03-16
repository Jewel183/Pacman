import pygame
import time
from config import *  
from Pacman import *  
from Ghost import *  
from Map import *  

class Level3:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        pygame.display.set_caption("Level 3: Orange Ghost tìm Pac-Man (UCS)")
        self.font = pygame.font.SysFont(FONT, 20)
        self.running = True
        self.map_img = pygame.image.load(MAP_IMG)
        self.map_img = pygame.transform.scale(self.map_img, (MAP_WIDTH, MAP_HEIGHT))
        self.graph, self.pacman_pos, _ = read_map(MAP_INPUT_TXT)
        self.maze = self.create_maze() 
        self.pacman = Pacman(self, self.pacman_pos)
        self.ghost = Orange(self, (21, 14))
        self.start_time = time.time()
        self.back_button = pygame.Rect(265, 0, 80, 40)

    def create_maze(self):
        """ Chuyển bản đồ từ graph thành ma trận ký tự """
        max_x = max([x for x, y in self.graph.keys()])
        max_y = max([y for x, y in self.graph.keys()])
        
        maze = [[1 for _ in range(max_x + 1)] for _ in range(max_y + 1)]
        
        for (x, y) in self.graph.keys():
            if 0 <= y < len(maze) and 0 <= x < len(maze[0]):  
                maze[y][x] = ' '  
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
        self.screen.blit(self.map_img, (MAP_POS_X, MAP_POS_Y))  
        # self.draw_grids()  

        self.pacman.draw()
        self.ghost.draw()

        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            button_color = TOMATO  
        else:
            button_color = WHITE
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)
        text_surf = pygame.font.SysFont("arial", 30).render("Back", True, BLACK)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)

        pygame.display.update()
    

    def run(self):
        """ Vòng lặp chạy Level 3 """
        found_pacman = False  

        while self.running:
            self.draw()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.back_button.collidepoint(event.pos):
                        return "back"

            if not found_pacman:
                
                graph = {}
                for y in range(len(self.maze)):
                    for x in range(len(self.maze[0])):
                        if self.maze[y][x] != 1:  
                            pos = (x, y)
                            graph[pos] = []
                            # Thêm các hàng xóm hợp lệ
                            for nx, ny in [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]:
                                if 0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze) and self.maze[ny][nx] != 1:
                                    # Thêm trọng số (weight) - có thể đặt là 1 nếu chi phí đồng nhất
                                    graph[pos].append(((nx, ny), 1))

                # Gọi UCS
                path, expanded_nodes, memory_usage, search_time = ucs(
                    graph, 
                    tuple(self.ghost.grid_pos), 
                    tuple(self.pacman.grid_pos), 
                    track_stats=True
                )
                
                self.ghost.expanded_nodes = expanded_nodes
                self.ghost.memory_usage = memory_usage
                self.ghost.search_time = search_time
                
                if path:
                    self.ghost.move_toward(path, self.maze)
                
                
                if tuple(self.ghost.grid_pos) == tuple(self.pacman.grid_pos):
                    found_pacman = True
                    time_to_catch = time.time() - self.start_time
                    print(f"Orange Ghost (UCS) bắt được Pac-Man sau {time_to_catch:.4f} giây!")
                    print(f"Thời gian tìm kiếm UCS: {self.ghost.search_time:.4f} giây")
                    print(f"Số nút mở rộng: {self.ghost.expanded_nodes}")
                    print(f"Bộ nhớ sử dụng: {self.ghost.memory_usage} bytes")


            pygame.display.update()

        pygame.quit()
    

if __name__ == "__main__":
    test = Level3()
    test.run()
