from config import *
from Food import *

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
        self.direction = 'right'                            # Hướng hiện tại
        self.next_direction = self.direction                # Hướng tiếp theo để pacman có thể đổi hướng mượt
        
        self.alive = True                                   # Kiểm tra xem pacman có chết hay sống         
        self.score = 0                                      # Điểm pacman kiếm được
        self.power_time = 0                                 # Thời gian trong trạng thái power
        
        self.pacman_images = {
            "default": pygame.transform.scale(pygame.image.load(PACMAN_IMAGE), (self.width, self.width)),
            "up": pygame.transform.scale(pygame.image.load(PACMAN_UP), (self.width, self.width)),
            "down": pygame.transform.scale(pygame.image.load(PACMAN_DOWN), (self.width, self.width)),
            "left": pygame.transform.scale(pygame.image.load(PACMAN_LEFT), (self.width, self.width)),
            "right": pygame.transform.scale(pygame.image.load(PACMAN_RIGHT), (self.width, self.width))
        }
        
        self.cell = cell
        
    def draw(self):
        # Draw the Pacman 
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
        pygame.display.update()
        
    def get_current_pixel_pos(self):
        """ Tính toán vị trí pixel của Pacman dựa vào vị trí lưới """
        half_cell = CELL_SIZE // 2
        offset = half_cell - self.width // 2
        
        return [self.grid_pos[0] * CELL_SIZE + offset + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + offset + MAP_POS_Y]
        
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
    
    def update(self):
        """ Cập nhật vị trí của Pac-Man mỗi frame """
        dx = self.target_pixel_pos[0] - self.pixel_pos[0]
        dy = self.target_pixel_pos[1] - self.pixel_pos[1]

        # Di chuyển từng chút một đến vị trí mục tiêu
        if abs(dx) > self.speed:
            self.pixel_pos[0] += self.speed if dx > 0 else -self.speed
        else:
            self.pixel_pos[0] = self.target_pixel_pos[0]

        if abs(dy) > self.speed:
            self.pixel_pos[1] += self.speed if dy > 0 else -self.speed
        else:
            self.pixel_pos[1] = self.target_pixel_pos[1]

        # Khi đến đúng ô mới, cập nhật lại vị trí trên lưới
        if self.pixel_pos == self.target_pixel_pos:
            self.grid_pos = [
                (self.pixel_pos[0] - MAP_POS_X) // CELL_SIZE,
                (self.pixel_pos[1] - MAP_POS_Y) // CELL_SIZE
            ]
        
        self.draw()
        
    def change_direction(self, new_direction, maze):
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        dx, dy = direction_map[new_direction]
        next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        
        if maze[next_y][next_x] != "#":
            self.direction = new_direction
            
            self.target_pixel_pos = [
                next_x * CELL_SIZE + MAP_POS_X,
                next_y * CELL_SIZE + MAP_POS_Y
            ]
            
    def move_forward(self, maze):
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        dx, dy = direction_map[self.direction]
        next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy

        if maze[next_y][next_x] != "#":
            self.grid_pos = [next_x, next_y]
            self.pixel_pos = self.get_current_pixel_pos()
        
    def appear(self):
        self.draw()
        
    def move(self, maze):
        direction_map = {
            "up": (0, -1),
            "down": (0, 1),
            "left": (-1, 0),
            "right": (1, 0)
        }
        dx, dy = direction_map[self.direction]
        next_x, next_y = self.grid_pos[0] + dx, self.grid_pos[1] + dy
        
        # Kiểm tra nếu có tường thì không di chuyển
        if maze[next_y][next_x] == "#":
            return
        
        self.target_pixel_pos = [
            next_x * CELL_SIZE + MAP_POS_X,
            next_y * CELL_SIZE + MAP_POS_Y
        ]
        
    # def move(self, new_grid_pos, maze):
    #     """ Di chuyển pacman đến vị trí mới và vẽ lại """
    #     if maze[new_grid_pos[1]][new_grid_pos[0]] == "#":
    #         return
        
    #     if abs(self.pixel_pos[0] - self.target_pixel_pos[0]) < self.speed and abs(self.pixel_pos[1] - self.target_pixel_pos[1]) < self.speed:
    #         self.direction = self.next_direction
        
    #     self.target_pixel_pos = [new_grid_pos[0] * CELL_SIZE + MAP_POS_X, new_grid_pos[1] * CELL_SIZE + MAP_POS_Y]
    #     # self.next_direction = self.direction # Lưu hướng để pacman quay đầu hợp lí
    
    def eat_food(self, food_list):
        for food in food_list:
            if food.get_pos() == tuple(self.grid_pos):
                self.score += food.get_effect()
                food_list.remove(food)
                return food.get_effect()
        return None
    
    def check_collision_with_ghost(self, ghost_list):
        for ghost in ghost_list:
            if tuple(self.grid_pos) == tuple(ghost.grid_pos):
                if ghost.is_frightened:
                    ghost.respawn()
                    self.score += 200
                else:
                    self.alive = False
                    return "dead"
        return "safe"
            
    def check_win(self, food_list):
        return len(food_list) == 0
    
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
            
    def power_mode(self):
        self.power_time = pygame.time.get_ticks()
        


            





