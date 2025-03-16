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
        self.speed = 0.2                         # Tăng tốc di chuyển mượt hơn
        self.mouth_counter = 0                              # Đếm số frame để đổi miệng
        self.mouth_toggle_rate = 5                          # Đổi miệng mỗi 5 frame
        self.direction = 'default'                          # Hướng hiện tại
        self.next_direction = self.direction                # Hướng tiếp theo để pacman có thể đổi hướng mượt
        self.alive = True                                   # Kiểm tra xem pacman có chết hay sống    
        self.start_time = time.time()                       # Ghi nhận thời gian bắt đầu
        self.time_to_be_caught = None                       # Lưu thời gian khi Pacman bị bắt     
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
        
        if 0 <= self.pixel_pos[0] < APP_WIDTH and 0 <= self.pixel_pos[1] < APP_HEIGHT:
            self.app.screen.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        
        self.app.screen.blit(pacman_image, (self.pixel_pos[0], self.pixel_pos[1]))
        
        
    def get_current_pixel_pos(self):
        return [self.grid_pos[0] * CELL_SIZE + MAP_POS_X, 
                self.grid_pos[1] * CELL_SIZE + MAP_POS_Y]
        
    
    def move(self, maze):
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

        if self.direction == "up":
            new_pos = (self.grid_pos[0], self.grid_pos[1] - 1)
        elif self.direction == "down":
            new_pos = (self.grid_pos[0], self.grid_pos[1] + 1)
        elif self.direction == "left":
            new_pos = (self.grid_pos[0] - 1, self.grid_pos[1])
        elif self.direction == "right":
            new_pos = (self.grid_pos[0] + 1, self.grid_pos[1])
        else:
            new_pos = self.grid_pos

        if maze[new_pos[1]][new_pos[0]] != 1:
            self.grid_pos = new_pos

        self.pixel_pos = [MAP_POS_X + self.grid_pos[0] * CELL_SIZE, MAP_POS_Y + self.grid_pos[1] * CELL_SIZE]
        
        
    def update(self, level, maze):
        if not self.started:
            return
        self.move(maze)
        

        
    
    def check_collision_with_ghost(self, ghost_list, start_time):
        if start_time is None:
            return "safe"
        
        for ghost in ghost_list:
            if tuple(self.grid_pos) == tuple(ghost.grid_pos):
                self.alive = False
                self.time_to_be_caught = time.time() - start_time
                print(f"Pac-Man was arrested at {self.time_to_be_caught:.2f} s!")
                return "dead"
        return "safe"
            
        
        


            





