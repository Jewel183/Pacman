from config import *
from collections import deque     
import heapq

def get_neighbors(pos, maze):
    """Trả về danh sách ô có thể đi đến (không phải tường)"""
    x, y = pos
    neighbors = [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    valid_neighbors = []

    for nx, ny in neighbors:
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] != '#':
            valid_neighbors.append((nx, ny))

    return valid_neighbors

def bfs(start, goal, maze):
    """Tìm đường từ start đến goal bằng BFS"""
    queue = deque([(start, [start])])  
    visited = {start}
    # visited = set()
    # visited.add(start)

    while queue:
        current, path = queue.popleft()

        if current == goal:
            return path[1:]  # Trả về đường đi (bỏ ô đầu tiên vì đó là vị trí hiện tại)

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    return []  # Không tìm thấy đường đi

def dfs(start, goal, maze):
    """Tìm đường từ start đến goal bằng DFS."""
    stack = [(start, [start])]  # (ô hiện tại, đường đi)
    visited = {start}
    # visited = set()
    # visited.add(start)

    while stack:
        current, path = stack.pop()

        if current == goal:
            return path  # Trả về đường đi nếu đến Pac-Man

        for neighbor in get_neighbors(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    return []  # Không tìm thấy đường đi

def ucs(graph, start, goal):
    """Tìm đường bằng Uniform Cost Search"""
    priority_queue = [(0, start, [start])]
    visited = {}

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)

        if node in visited:
            continue

        visited[node] = cost

        if node == goal:
            return path  # Trả về đường đi thay vì chỉ trả về cost

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor, path + [neighbor]))

    return []  # Không tìm thấy đường


def a_star(graph, start, goal, heuristic):
    priority_queue = [(heuristic[start], 0, start, [start])]
    visited = {}
    
    while priority_queue:
        estimate, cost, node, path = heapq.heappop(priority_queue)
        if node in visited:
            continue
        
        visited[node] = cost
        if node == goal:
            return path
        
        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                estimated_cost = cost + weight + heuristic[neighbor]
                heapq.heappush(priority_queue, (estimated_cost, cost + weight, neighbor, path + [neighbor]))
                
    return []

def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])




class Ghost:
    def __init__(self, app, pos, monster_type="red", cell=None):
        self.app = app
        self.width = CELL_SIZE - 2
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        self.direction = 'up'
        self.monster_type = monster_type        # Loai quai vat (red, blue, pink, orange)
        self.is_frightened = False              # Trang thai so hai
        self.frightened_time = 0                # Bo dem thoi gian o trang thai so hai
        
        self.ghost_image = pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]), (self.width, self.width))
        self.frightened_image = pygame.transform.scale(pygame.image.load(FRIGHTENED_IMAGE), (self.width, self.width))
        
        # self.black_background = pygame.Surface((self.width, self.width))
        self.initial_cell = cell
        self.cell = cell 
        
        
    def frightened_mode(self):
        """Kich hoat che do so hay khi Pacman an power pellet"""
        self.is_frightened = True
        self.frightened_time = pygame.time.get_ticks() # Ghi lai thoi gian bat dau
        
    def check_frightened_timeout(self):
        if self.is_frightened and pygame.time.get_ticks() - self.frightened_time > POWER_PELLET_DURATION * 1000:
            self.is_frightened = False
        
    def draw(self):
        # current_time = pygame.time.get_ticks()
        # if self.is_frightened:
        #     if current_time - self.frightened_time > POWER_PELLET_DURATION * 1000:
        #         self.is_frightened = False
        #     image = self.frightened_image
        # else:
        #     image = self.ghost_image
        if not self.app or not hasattr(self.app, "screen"):
            return
        image = self.frightened_image if self.is_frightened else self.ghost_image  
        # image = self.monster_images.get(self.direction, self.monster_images["up"])
        self.app.screen.blit(image, (self.pixel_pos[0], self.pixel_pos[1]))
            
    def get_current_pixel_pos(self):
        return [self.grid_pos[0] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_Y]
                            
    def update(self, new_grid_pos):
        """Cập nhật vị trí của con ma"""
        if new_grid_pos is None or new_grid_pos == self.grid_pos:
            return # Giữ nguyên nếu không có vị trí mớimới
        
        self.app.screen.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width)) # Xóa ma cũ
        # self.app.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        self.grid_pos = new_grid_pos
        self.pixel_pos = self.get_current_pixel_pos()    
    
    
    def move(self, new_grid_pos):
        if new_grid_pos is None or new_grid_pos == self.grid_pos:
            return  # Không cập nhật nếu không có vị trí mới
        
        self.update(new_grid_pos)
        self.draw()
    
    # def appear(self):
    #     self.draw()
    
    def move_toward(self, path):
        if path and len(path) > 1:
            next_pos = path[1]
            print(f"{self.monster_type} Ghost moves to {next_pos}")
            self.move(next_pos)
    
    
                                 
class Red(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "red", cell)
    
    def move_red(self, pacman_pos, graph, heuristic):
        """ Di chuyển theo đường tìm được từ A* """
        path = a_star(graph, tuple(self.grid_pos), tuple(pacman_pos), heuristic)
        self.move_toward(path)
        
class Blue(Ghost): # Dùng bfsbfs
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "blue", cell)
        
    def move_blue(self, pacman_pos, maze):
        """ Di chuyển theo đường tìm được từ bfs """
        path = bfs(tuple(self.grid_pos), tuple(pacman_pos), maze)
        self.move_toward(path)
        
class Pink(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "pink", cell)
    
    def move_pink(self, pacman_pos, maze):
        """ Di chuyển theo đường tìm được từ dfs """
        path = dfs(tuple(self.grid_pos), tuple(pacman_pos), maze)
        self.move_toward(path)
        
class Orange(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "orange", cell)
        
    def move_orange(self, pacman_pos, graph):
        """ Di chuyển theo đường tìm được từ ucs """
        path = ucs(graph, tuple(self.grid_pos), tuple(pacman_pos))
        self.move_toward(path)
        
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 680))

# if __name__ == "__main__":
#     pygame.init()
#     screen = pygame.display.set_mode((610, 680))  # Khởi tạo cửa sổ game
#     pygame.display.set_caption("Test Ghost")

#     app = App()
#     clock = pygame.time.Clock()
#     running = True

#     # Tạo một con ma màu đỏ để test
#     red_ghost = Red(app=app, pos=(10, 10))  # Đặt tạm app=None, chỉ test hiển thị
#     blue_ghost = Blue(app=app, pos=(12, 10))
#     pink_ghost = Pink(app=app, pos=(14, 10))
#     orange_ghost = Orange(app=app, pos=(16, 10))

#     while running:
#         app.screen.fill((0, 0, 0))  # Xóa màn hình mỗi frame
        
#         red_ghost.draw()  # Vẽ ma lên màn hình
#         blue_ghost.draw()
#         pink_ghost.draw()
#         orange_ghost.draw()
        
#         # red_ghost.move([red_ghost.grid_pos[0] + 1, red_ghost.grid_pos[1]])
#         # blue_ghost.move([blue_ghost.grid_pos[0] - 1, blue_ghost.grid_pos[1]])
#         # pink_ghost.move([pink_ghost.grid_pos[0], pink_ghost.grid_pos[1] + 1])
#         # orange_ghost.move([orange_ghost.grid_pos[0], orange_ghost.grid_pos[1] - 1])
        
#         # pygame.display.update()
#         pygame.display.flip()
#         clock.tick(10)  # Giới hạn FPS về 30

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#     pygame.quit()