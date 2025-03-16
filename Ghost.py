from config import *
from collections import deque     
import heapq
import sys
import time

def get_neighbors_bfs(pos, maze):
    x, y = pos
    neighbors = [
        (x, y - 1), (x, y + 1),  # Lên, Xuống
        (x - 1, y), (x + 1, y)   # Trái, Phải
    ]
    return [(nx, ny) for nx, ny in neighbors if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze) and maze[ny][nx] != 1]


def bfs(start, goal, maze, track_stats=False):
    search_start_time = time.time()
    queue = deque([(start, [start])])  
    visited = {start}
    expanded_nodes = 0
    # max_memory = sys.getsizeof(queue) + sys.getsizeof(visited)

    while queue:
        current, path = queue.popleft()
        expanded_nodes += 1

        if current == goal:
            search_time = time.time() - search_start_time
            
            
            # print(f"[DEBUG] BFS - Expanded Nodes: {expanded_nodes}, Memory: {memory_usage} bytes")
            
            if track_stats:
                memory_usage = sys.getsizeof(queue) + sys.getsizeof(visited)
                return path, expanded_nodes, memory_usage, search_time
            return path  # Trả về đường đi (bỏ ô đầu tiên vì đó là vị trí hiện tại)

        for neighbor in get_neighbors_bfs(current, maze):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))

    # max_memory = max(max_memory, sys.getsizeof(queue) + sys.getsizeof(visited))
    search_time = time.time() - search_start_time 
    return ([], expanded_nodes, sys.getsizeof(queue) + sys.getsizeof(visited), search_time) if track_stats else []


def get_neighbors_dfs(pos, maze):
    """ Trả về danh sách ô hợp lệ (trái, phải, trên, dưới, không đi chéo) """
    x, y = pos
    neighbors = [
        (x - 1, y),  # Trái
        (x + 1, y),  # Phải
        (x, y - 1),  # Lên
        (x, y + 1)   # Xuống
    ]
    return [
        (nx, ny) for nx, ny in neighbors 
        if 0 <= nx < len(maze[0]) and 0 <= ny < len(maze)  # Đảm bảo không ra ngoài bản đồ
        and maze[ny][nx] != 1  # Kiểm tra không phải tường
    ]
    

def dfs(start, goal, maze, track_stats=False):
    """Tìm đường từ start đến goal bằng DFS."""
    search_start_time = time.time()
    stack = [(start, [start])]
    visited = {start}
    expanded_nodes = 0 

    while stack:
        current, path = stack.pop()
        expanded_nodes += 1  

        if current == goal:
            search_time = time.time() - search_start_time  
            if track_stats:
                memory_usage = sys.getsizeof(stack) + sys.getsizeof(visited)  
                return path, expanded_nodes, memory_usage, search_time
            return path  # Trả về đường đi nếu đến Pac-Man

        neighbors = get_neighbors_dfs(current, maze)

        for neighbor in neighbors:
            if neighbor not in visited:
                visited.add(neighbor)
                stack.append((neighbor, path + [neighbor]))

    search_time = time.time() - search_start_time
    if track_stats:
        memory_usage = sys.getsizeof(stack) + sys.getsizeof(visited)
        return [], expanded_nodes, memory_usage, search_time
    # return ([], expanded_nodes, sys.getsizeof(stack) + sys.getsizeof(visited), search_time) if track_stats else []
    return []

def ucs(graph, start, goal, track_stats=False):
    """Tìm đường bằng Uniform Cost Search"""
    search_start_time = time.time()
    priority_queue = [(0, start, [start])]
    visited = {}
    expanded_nodes = 0  

    while priority_queue:
        cost, node, path = heapq.heappop(priority_queue)
        expanded_nodes += 1 

        if node in visited:
            continue

        visited[node] = cost

        if node == goal:
            search_time = time.time() - search_start_time  
            if track_stats:
                memory_usage = sys.getsizeof(priority_queue) + sys.getsizeof(visited)  
                return path, expanded_nodes, memory_usage, search_time
            return path  # Trả về đường đi thay vì chỉ trả về cost

        for neighbor, weight in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(priority_queue, (cost + weight, neighbor, path + [neighbor]))

    search_time = time.time() - search_start_time
    return ([], expanded_nodes, sys.getsizeof(priority_queue) + sys.getsizeof(visited), search_time) if track_stats else []


def a_star(graph, start, goal, heuristic, track_stats=False):
    search_start_time = time.time()
    priority_queue = [(heuristic[start], 0, start, [start])]
    visited = {}
    expanded_nodes = 0 
    
    while priority_queue:
        _, cost, node, path = heapq.heappop(priority_queue)
        expanded_nodes += 1 
         
        if node in visited:
            continue
        
        visited[node] = cost
        if node == goal:
            search_time = time.time() - search_start_time  
            if track_stats:
                memory_usage = sys.getsizeof(priority_queue) + sys.getsizeof(visited)  
                return path, expanded_nodes, memory_usage, search_time
            #  print(f"A*: Time {search_time:.4f}s, Expand Node {expanded_nodes}, Memory {memory_usage} bytes")
            return path
        
        for neighbor, weight in graph.get(node, []):
            new_cost = cost + weight
            if neighbor not in visited:
                estimated_cost = new_cost + heuristic[neighbor]
                heapq.heappush(priority_queue, (estimated_cost, new_cost, neighbor, path + [neighbor]))
                
    search_time = time.time() - search_start_time
    return ([], expanded_nodes, sys.getsizeof(priority_queue) + sys.getsizeof(visited), search_time) if track_stats else []


def manhattan_distance(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


class Ghost:
    def __init__(self, app, pos, ghost_type="red", cell=None):
        self.app = app
        self.width = CELL_SIZE - 2
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        # self.pixel_pos = [self.grid_pos[0] * CELL_SIZE, self.grid_pos[1] * CELL_SIZE]
        self.direction = 'up'
        self.ghost_type = ghost_type                    # Loai ma (red, blue, pink, orange)
        self.speed = CELL_SIZE // 6
        self.last_move_time = 0
        self.start_time = time.time()                   # Ghi nhận thời gian bắt đầu
        self.time_to_catch_pacman = None                # Lưu thời gian bắt được pacman
        
        self.ghost_image = pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[ghost_type]), (self.width, self.width))
    
        
    def draw(self):
        if not self.app or not hasattr(self.app, "screen"):
            return
        # self.app.screen.fill(BLACK, (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        
        pygame.draw.rect(self.app.screen, BLACK, (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        # if 0 <= self.pixel_pos[0] < APP_WIDTH and 0 <= self.pixel_pos[1] < APP_HEIGHT:
        self.app.screen.blit(self.ghost_image, (self.pixel_pos[0], self.pixel_pos[1]))
        pygame.display.update((self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
            
            
    def get_current_pixel_pos(self):
        # return [self.grid_pos[0] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_X,
        #         self.grid_pos[1] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_Y]
        #  return [self.grid_pos[0] * CELL_SIZE, self.grid_pos[1] * CELL_SIZE]
        
        half_cell = CELL_SIZE // 2
        offset = half_cell - self.width // 2  # Để ghost nằm giữa ô
        
        return [
            self.grid_pos[0] * CELL_SIZE + offset + MAP_POS_X,
            self.grid_pos[1] * CELL_SIZE + offset + MAP_POS_Y
        ]
        
        
    def update_direction(self, new_grid_pos):
        if new_grid_pos == self.grid_pos:
            return
        direction_map = {
            (0, -1): "up",
            (0, 1): "down",
            (-1, 0): "left",
            (1, 0): "right"
        }
        delta = (new_grid_pos[0] - self.grid_pos[0], new_grid_pos[1] - self.grid_pos[1])
        self.direction = direction_map.get(delta, self.direction)
                       
                            
    def update(self, new_grid_pos, maze):
        if (
            new_grid_pos is None 
            or new_grid_pos == self.grid_pos 
            or new_grid_pos[1] < 0 
            or new_grid_pos[1] >= len(maze) 
            or new_grid_pos[0] < 0 
            or new_grid_pos[0] >= len(maze[0])
        ):
            return  
        self.update_direction(new_grid_pos)
        self.app.screen.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width)) # Xóa ma cũ
        self.grid_pos = new_grid_pos
        self.pixel_pos = self.get_current_pixel_pos()    
        self.draw()
    
    
    def move(self, new_grid_pos, maze):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_move_time < 150:
            return
        self.last_move_time = current_time
        
        if (
            new_grid_pos[1] < 0 or new_grid_pos[1] >= len(maze) 
            or new_grid_pos[0] < 0 or new_grid_pos[0] >= len(maze[0]) 
            or maze[new_grid_pos[1]][new_grid_pos[0]] == 1
        ):
            return
            
        self.update(new_grid_pos, maze)
        self.draw()
    
    # def appear(self):
    #     self.draw()
    
    
    def move_toward(self, path, maze):
        if not path or len(path) < 2:
            print("Ghost has no valid path!")
            return
        
        next_x, next_y = path[1]
        print(f"Ghost moving to: {next_x}, {next_y}")  # Debug
        
        if maze[next_y][next_x] == 1:
            # print(f"Ghost blocked by wall at {next_x}, {next_y}")
            return  

        self.update_direction((next_x, next_y))
        self.move([next_x, next_y], maze)

        pygame.display.update()
            
    
    def check_catch_pacman(self, pacman):
        if not hasattr(pacman, "grid_pos"):
            return  
        if self.grid_pos == pacman.grid_pos and self.time_to_catch_pacman is None:
            self.time_to_catch_pacman = time.time() - self.start_time
            print(f"{self.ghost_type} catch Pacman after {self.time_to_catch_pacman:.2f} second!")

                                  
class Blue(Ghost): # BFS
    def __init__(self, app, pos):
        super().__init__(app, pos, "blue")
        self.expanded_nodes = 0
        self.memory_usage = 0
        self.search_time = 0
        
    def move_blue(self, pacman_pos, maze):
        path, expanded_nodes, memory_usage, search_time = bfs(tuple(self.grid_pos), tuple(pacman_pos), maze, track_stats=True)
        self.expanded_nodes = expanded_nodes
        self.memory_usage = memory_usage
        self.search_time = search_time
        
        self.move_toward(path, maze)
        
        
class Pink(Ghost): # DFS
    def __init__(self, app, pos):
        super().__init__(app, pos, "pink")
        self.expanded_nodes = 0
        self.memory_usage = 0
        self.search_time = 0
    
    def move_pink(self, pacman_pos, maze):
        path, expanded_nodes, memory_usage, search_time = dfs(tuple(self.grid_pos), tuple(pacman_pos), maze, True)

        self.expanded_nodes = expanded_nodes
        self.memory_usage = memory_usage
        self.search_time = search_time

        print(f"Pink Ghost (DFS) - Time: {search_time:.4f}s, Expand Node: {expanded_nodes}, Memory: {memory_usage} bytes")
        
        self.move_toward(path, maze)
        
        
class Orange(Ghost): # UCS
    def __init__(self, app, pos):
        super().__init__(app, pos, "orange")
        self.expanded_nodes = 0
        self.memory_usage = 0
        self.search_time = 0
        
    def move_orange(self, pacman_pos, graph, maze):
        path, expanded_nodes, memory_usage, search_time = ucs(graph, tuple(self.grid_pos), tuple(pacman_pos), True)

        self.expanded_nodes = expanded_nodes
        self.memory_usage = memory_usage
        self.search_time = search_time

        print(f"Orange Ghost (UCS) - Time: {search_time:.4f}s, Expand Node: {expanded_nodes}, Memory: {memory_usage} bytes")
        
        self.move_toward(path, maze)
        
        
class Red(Ghost): # A*
    def __init__(self, app, pos):
        super().__init__(app, pos, "red")
        self.expanded_nodes = 0
        self.memory_usage = 0
        self.search_time = 0
    
    def move_red(self, pacman_pos, graph, heuristic, maze):
        path, expanded_nodes, memory_usage, search_time = a_star(graph, tuple(self.grid_pos), tuple(pacman_pos), heuristic, True)

        self.expanded_nodes = expanded_nodes
        self.memory_usage = memory_usage
        self.search_time = search_time

        print(f"Red Ghost (A*) - Time: {search_time:.4f}s, Expand Node: {expanded_nodes}, Memory: {memory_usage} bytes")
        
        self.move_toward(path, maze)
        
        
# class App:
#     def __init__(self):
#         self.screen = pygame.display.set_mode((800, 680))

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
    
#     maze = [
#         "####################",
#         "#..................#",
#         "#..................#",
#         "#..................#",
#         "####################",
#     ]

#     while running:
#         app.screen.fill((0, 0, 0))  # Xóa màn hình mỗi frame
        
#         red_ghost.draw()  # Vẽ ma lên màn hình
#         blue_ghost.draw()
#         pink_ghost.draw()
#         orange_ghost.draw()
        
#         red_ghost.move([red_ghost.grid_pos[0] + 1, red_ghost.grid_pos[1]], maze)
#         blue_ghost.move([blue_ghost.grid_pos[0] - 1, blue_ghost.grid_pos[1]], maze)
#         pink_ghost.move([pink_ghost.grid_pos[0], pink_ghost.grid_pos[1] + 1], maze)
#         orange_ghost.move([orange_ghost.grid_pos[0], orange_ghost.grid_pos[1] - 1], maze)
        
#         # pygame.display.update()
#         pygame.display.flip()
#         clock.tick(10)  # Giới hạn FPS về 30

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False

#     pygame.quit()