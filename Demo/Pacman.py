from config import *
import time

class Pacman:
    def __init__(self, app, pos, cell=None):
        self.app = app
        self.width = CELL_SIZE
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        self.open_mouth_turn = False
        self.target_pixel_pos = self.pixel_pos[:]           # Tọa độ đích để di chuyển
        self.speed = CELL_SIZE // 4                         # Tăng tốc di chuyển mượt hơn
        self.mouth_counter = 0                              # Đếm số frame để đổi miệng
        self.mouth_toggle_rate = 5                          # Đổi miệng mỗi 5 frame
        self.direction = 'default'                          # Hướng hiện tại
        self.next_direction = self.direction                # Hướng tiếp theo để pacman có thể đổi hướng mượt
        self.alive = True                                   # Kiểm tra xem pacman có chết hay sống    
        self.start_time = time.time()                      # Ghi nhận thời gian bắt đầu
        self.time_to_be_caught = None                      # Lưu thời gian khi Pacman bị bắt     
        self.started = False
        
        self.pacman_images = {
            "default": pygame.transform.scale(pygame.image.load(PACMAN_IMAGE), (self.width, self.width)),
            "up": pygame.transform.scale(pygame.image.load(PACMAN_UP), (self.width, self.width)),
            "down": pygame.transform.scale(pygame.image.load(PACMAN_DOWN), (self.width, self.width)),
            "left": pygame.transform.scale(pygame.image.load(PACMAN_LEFT), (self.width, self.width)),
            "right": pygame.transform.scale(pygame.image.load(PACMAN_RIGHT), (self.width, self.width))
        }
        
        
    def draw(self):
        if not self.alive:
            return   
        
        if self.pixel_pos != self.target_pixel_pos:
            self.mouth_counter += 1
            if self.mouth_counter >= self.mouth_toggle_rate:
                self.mouth_counter = 0
                self.open_mouth_turn = not self.open_mouth_turn
        
        pacman_image = self.pacman_images[self.direction] if self.open_mouth_turn else self.pacman_images["default"]
        
        # Xóa hình cũ
        if 0 <= self.pixel_pos[0] < APP_WIDTH and 0 <= self.pixel_pos[1] < APP_HEIGHT:
            self.app.screen.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        
        # vẽ hình mới
        self.app.screen.blit(pacman_image, (self.pixel_pos[0], self.pixel_pos[1]))
        # pygame.display.update()
        
    def get_current_pixel_pos(self):
        return [self.grid_pos[0] * CELL_SIZE + MAP_POS_X, 
                self.grid_pos[1] * CELL_SIZE + MAP_POS_Y]
        
        # half_cell = CELL_SIZE // 2  # Nửa kích thước ô
        # return [self.grid_pos[0] * CELL_SIZE + MAP_POS_X + half_cell, self.grid_pos[1] * CELL_SIZE + MAP_POS_Y + half_cell]
        
    
    def update(self, level, maze):
        if level < 6 or not self.started:
            return
        
        # target_x, target_y = self.target_pixel_pos
        # grid_x, grid_y = target_x // CELL_SIZE, target_y // CELL_SIZE
        # if maze[grid_y][grid_x] == "#":
        #     return
        
        dx = self.target_pixel_pos[0] - self.pixel_pos[0]
        dy = self.target_pixel_pos[1] - self.pixel_pos[1]

        if abs(dx) > self.speed:
            self.pixel_pos[0] += self.speed if dx > 0 else -self.speed
        else:
            self.pixel_pos[0] = self.target_pixel_pos[0]

        if abs(dy) > self.speed:
            self.pixel_pos[1] += self.speed if dy > 0 else -self.speed
        else:
            self.pixel_pos[1] = self.target_pixel_pos[1]

        if self.pixel_pos == self.target_pixel_pos:
            self.grid_pos = [
                (self.pixel_pos[0] - MAP_POS_X) // CELL_SIZE,
                (self.pixel_pos[1] - MAP_POS_Y) // CELL_SIZE
            ]
        
        self.draw()
        
        
    def appear(self):
        self.draw()
        
        
    def move(self, maze):
        if not self.started:
            return

        direction_map = {
            "default": (0, 0),
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }

        # Kiểm tra hướng hiện tại của Pac-Man có bị chặn không
        dx, dy = direction_map[self.direction]
        next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        can_continue = (0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != "#")

        if not can_continue:  # Nếu bị chặn, chỉ đổi hướng khi hướng mới hợp lệ
            dx, dy = direction_map[self.next_direction]
            next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
            if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != "#":
                self.direction = self.next_direction  # Đổi hướng ngay lập tức

        # Sau khi kiểm tra xong, Pac-Man tiếp tục đi nếu có thể
        dx, dy = direction_map[self.direction]
        next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy

        if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != "#":
            self.target_pixel_pos = [next_x * CELL_SIZE + MAP_POS_X, next_y * CELL_SIZE + MAP_POS_Y]
        else:
            self.target_pixel_pos = self.pixel_pos
        
    
    def check_collision_with_ghost(self, ghost_list, start_time):
        if start_time is None:
            return "safe"
        
        for ghost in ghost_list:
            if tuple(self.grid_pos) == tuple(ghost.grid_pos):
                self.alive = False
                self.time_to_be_caught = time.time() - start_time
                print(f"Pac-Man was arrested at {self.time_to_be_caught:.2f} s!")
                if self.time_to_be_caught is not None:
                    with open("game_log.txt", "a") as log_file:
                        log_file.write(f"Pac-Man arrested after {self.time_to_be_caught} s\n")
                return "dead"
        return "safe"
            
    
    def respawn(self, start_pos):
        self.grid_pos = start_pos
        self.pixel_pos = self.get_current_pixel_pos()
        self.target_pixel_pos = self.pixel_pos[:]
        self.direction = "right"
        self.alive = True
        
    def check_tunnel(self, tunnel_left, tunnel_right):
        if tuple(self.grid_pos) == tuple(tunnel_left):
            self.grid_pos = tunnel_right
            self.pixel_pos = self.get_current_pixel_pos()
        elif tuple(self.grid_pos) == tuple(tunnel_right):
            self.grid_pos = tunnel_left
            self.pixel_pos = self.get_current_pixel_pos()
        
        
    # def move(self, new_grid_pos, maze):
    #     """ Di chuyển pacman đến vị trí mới và vẽ lại """
    #     if maze[new_grid_pos[1]][new_grid_pos[0]] == "#":
    #         return
        
    #     if abs(self.pixel_pos[0] - self.target_pixel_pos[0]) < self.speed and abs(self.pixel_pos[1] - self.target_pixel_pos[1]) < self.speed:
    #         self.direction = self.next_direction
        
    #     self.target_pixel_pos = [new_grid_pos[0] * CELL_SIZE + MAP_POS_X, new_grid_pos[1] * CELL_SIZE + MAP_POS_Y]
    #     # self.next_direction = self.direction # Lưu hướng để pacman quay đầu hợp lí
    
    # def update_direction(self, new_grid_pos):
    #     """ Cập nhật hướng di chuyển của Pacman """
    #     direction_map = {
    #         (0, -1): "up",
    #         (0, 1): "down",
    #         (1, 0): "right",
    #         (-1, 0): "left"
    #     }
        
    #     delta = (new_grid_pos[0] - self.grid_pos[0], new_grid_pos[1] - self.grid_pos[1])
    #     self.direction = direction_map.get(delta, self.direction)
        
    # def update(self, maze):
    #     """ Cập nhật vị trí của pacman """
    #     new_x, new_y = self.target_pixel_pos
        
    #     # Kiểm tra tường
    #     if maze[new_y // CELL_SIZE][new_x // CELL_SIZE] == "#":
    #         self.target_pixel_pos = self.pixel_pos[:]
    #         return
        
    #     if self.pixel_pos[0] < new_x:
    #         self.pixel_pos[0] += self.speed
    #     elif self.pixel_pos[0] > new_x:
    #         self.pixel_pos[0] -= self.speed
            
    #     if self.pixel_pos[1] < new_y:
    #         self.pixel_pos[1] += self.speed
    #     elif self.pixel_pos[1] > new_y:
    #         self.pixel_pos[1] -= self.speed
            
    #     # Cập nhật grid_pos
    #     if abs(self.pixel_pos[0] - new_x) < self.speed and abs(self.pixel_pos[1] - new_y) < self.speed:
    #         self.pixel_pos = self.target_pixel_pos[:]
    #         self.grid_pos = [(self.pixel_pos[0] - MAP_POS_X) // CELL_SIZE, (self.pixel_pos[1] - MAP_POS_Y) // CELL_SIZE]
            
    #     self.draw()
    
    # def change_direction(self, new_direction, maze, level):
    #     if level < 6:
    #         return
        
    #     direction_map = {
    #         "default": (0, 0),
    #         "up": (0, -1),
    #         "down": (0, 1),
    #         "left": (-1, 0),
    #         "right": (1, 0)
    #     }
    #     dx, dy = direction_map[new_direction]
    #     next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        
    #     if not (0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze)):
    #         return
        
        
        
    #     if maze[next_y][next_x] != "#":
    #         self.direction = new_direction
    #         self.target_pixel_pos = [next_x * CELL_SIZE + MAP_POS_X, next_y * CELL_SIZE + MAP_POS_Y]
    
    # def move(self, maze):
    #     if not self.started:
    #         return
        
    #     direction_map = {
    #         "default": (0, 0),
    #         "up": (0, -1),
    #         "down": (0, 1),
    #         "left": (-1, 0),
    #         "right": (1, 0)
    #     }
        
    #     dx, dy = direction_map[self.next_direction]
    #     next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        
    #     if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != "#":
    #         self.direction = self.next_direction
            
    #     dx, dy = direction_map[self.direction]
    #     next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        
    #     # Kiểm tra nếu có tường thì không di chuyển
    #     if 0 <= next_x < len(maze[0]) and 0 <= next_y < len(maze) and maze[next_y][next_x] != "#":
    #         self.target_pixel_pos = [next_x * CELL_SIZE + MAP_POS_X, next_y * CELL_SIZE + MAP_POS_Y]
    #     else:
    #         self.direction = "default"
        


            





