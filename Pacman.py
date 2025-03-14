from config import *

class Pacman:
    def __init__(self, app, pos, cell=None):
        self.app = app
        self.width = CELL_SIZE
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        self.direction = 'right' # Hướng hiện tại
        self.open_mouth_turn = False
        # self.target_pixel_pos = self.pixel_pos[:]  # Tọa độ đích để di chuyển
        # self.speed = 2  # Tăng tốc di chuyển mượt hơn
        # self.mouth_counter = 0  # Đếm số frame để đổi miệng
        # self.mouth_toggle_rate = 5  # Đổi miệng mỗi 5 frame
        # self.next_direction = self.direction
        
        
        self.pacman_images = {
            "default": pygame.transform.scale(pygame.image.load(PACMAN_IMAGE), (self.width, self.width)),
            "up": pygame.transform.scale(pygame.image.load(PACMAN_UP), (self.width, self.width)),
            "down": pygame.transform.scale(pygame.image.load(PACMAN_DOWN), (self.width, self.width)),
            "left": pygame.transform.scale(pygame.image.load(PACMAN_LEFT), (self.width, self.width)),
            "right": pygame.transform.scale(pygame.image.load(PACMAN_RIGHT), (self.width, self.width))
        }
        
        self.cell = cell
        
        # brain
        self.food_cell_in_brain_list = []
        self.path_to_food_cell_in_brain_list = []
        
        # sight
        self.food_cell_in_sight_list = []
        self.monster_cell_in_sight_list = []
        
    def draw(self):
        # Draw the Pacman 
        # self.mouth_counter += 1
        # is_open = (self.mouth_counter // self.mouth_toggle_rate) % 2 == 0
        
        pacman_image = self.pacman_images[self.direction] if self.open_mouth_turn else self.pacman_images["default"]
        
        # Luân phiên đổi ảnh mở đóng miệng
        self.open_mouth_turn = not self.open_mouth_turn
        
        self.app.screen.blit(pacman_image, (self.pixel_pos[0], self.pixel_pos[1]))
        
        # Cap nhat man hinh
        pygame.display.update()
        
    def get_current_pixel_pos(self):
        """ Tính toán vị trí pixel của Pacman dựa vào vị trí lưới """
        half_cell = CELL_SIZE // 2
        offset = half_cell - self.width // 2
        
        return [self.grid_pos[0] * CELL_SIZE + offset + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + offset + MAP_POS_Y]
        
    def update_direction(self, new_grid_pos):
        """ Cập nhật hướng di chuyển của Pacman """
        direction_map = {
            (0, -1): "up",
            (0, 1): "down",
            (1, 0): "right",
            (-1, 0): "left"
        }
        
        delta = (new_grid_pos[0] - self.grid_pos[0], new_grid_pos[1] - self.grid_pos[1])
        self.direction = direction_map.get(delta, self.direction)
        
    def update(self, new_grid_pos):
        """ Cập nhật vị trí của pacman """
        
        # Xóa hình pacman cũ
        self.app.screen.blit(self.app.background, (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width))
        
        # Cập nhật lại hướng di chuyển và vị trí mới
        self.update_direction(new_grid_pos)
        self.grid_pos = new_grid_pos
        self.pixel_pos = self.get_current_pixel_pos()
            
    def empty_brain(self):
        return len(self.food_cell_in_sight_list) != 0
    
    def have_monster_in_cur_right(self):
        return len(self.monster_cell_in_sight_list) != 0
    
    def have_food_cur_in_sight(self):
        return len(self.food_cell_in_sight_list) != 0
    
    def spread_peas(self, pacman_old_cell):
        for path_to_food_cell in self.path_to_food_cell_in_brain_list:
            if path_to_food_cell is not None:
                path_to_food_cell.append(pacman_old_cell)
            
    def back_track(self, graph_map):
        if not self.path_to_food_cell_in_brain_list or not self.path_to_food_cell_in_brain_list[-1]:
            return self.grid_pos
        
        return self.path_to_food_cell_in_brain_list[-1].pop(-1) if self.path_to_food_cell_in_brain_list[-1] else None
        
        # for path_to_food_cell in reversed(self.path_to_food_cell_in_brain_list):
        #     if path_to_food_cell:
        #         next_cell = path_to_food_cell.pop(-1)
        #         return next_cell
        
        # return None
        # next_cell = self.path_to_food_cell_in_brain_list[-1][-1]
        # for path_to_food_cell in self.path_to_food_cell_in_brain_list:
        #     if path_to_food_cell:
        #         path_to_food_cell.pop(-1)
            
        # return next_cell
    
    def nearby_monster_cell(self, food_cell):
        return any(
            abs(monster_cell.pos[0] - food_cell.pos[0]) + abs(monster_cell.pos[1] - food_cell.pos[1]) <= 2
            for monster_cell in self.monster_cell_in_sight_list
        )
        
    def appear(self):
        self.draw()
        
    def move(self, new_grid_pos):
        """ Di chuyển pacman đến vị trí mới và vẽ lại """
        if new_grid_pos is not None:
            self.update(new_grid_pos)
            self.draw()
    
    
    def observe_recursive(self, graph_map, parent_cell, cur_cell, sight):
        if sight < 0 or cur_cell is None:
            return

        if cur_cell.exist_food() and cur_cell not in self.food_cell_in_sight_list:
            self.food_cell_in_sight_list.append(cur_cell)
            
        if cur_cell.exist_monster() and cur_cell not in self.monster_cell_in_sight_list:
            self.monster_cell_in_sight_list.append(cur_cell)
            
        for neighbor_cell in graph_map.get(cur_cell, []):
            if neighbor_cell != parent_cell:
                self.observe_recursive(graph_map, cur_cell, neighbor_cell, sight - 1)
    
    def observe(self, graph_map, sight):
        # Reset sight list
        self.food_cell_in_sight_list.clear()
        self.monster_cell_in_sight_list.clear()
        
        # Update current sight
        if self.cell and self.cell in graph_map:
            for neighbor_cell in graph_map[self.cell]:
                self.observe_recursive(graph_map, self.cell, neighbor_cell, sight - 1)
            
        # Loạioại bỏ thức ăn gần quái vật
        nearby_monster_food_cells = {cell for cell in self.food_cell_in_sight_list if self.nearby_monster_cell(cell)}
        self.food_cell_in_sight_list = [cell for cell in self.food_cell_in_sight_list if cell not in nearby_monster_food_cells]
        
        # Loại bỏ thức ăn khỏi bộ nhớ nếu gần quái vật
        if self.food_cell_in_brain_list:
            updated_brain_list = []
            updated_path = []
            for food, path in zip(self.food_cell_in_brain_list, self.path_to_food_cell_in_brain_list):
                if food not in nearby_monster_food_cells:
                    updated_brain_list.append(food)
                    updated_path.append(path)
                    
            self.food_cell_in_brain_list = updated_brain_list
            self.path_to_food_cell_in_brain_list = updated_path
        
        # Thêm thức ăn mới vào bộ nhớ
        for food_cell in self.food_cell_in_sight_list:
            if food_cell in self.food_cell_in_brain_list:
                idx = self.food_cell_in_brain_list.index(food_cell)
                self.food_cell_in_brain_list.pop(idx)
                self.path_to_food_cell_in_brain_list.pop(idx)
                
            self.food_cell_in_brain_list.append(food_cell)
            self.path_to_food_cell_in_brain_list.append([])
            


            





