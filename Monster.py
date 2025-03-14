from config import *
import Food       

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
        
        # Load anh cac con ma theo 
        
        # self.monster_images = {
        #     "up": pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]["up"]), (self.width, self.width)),
        #     "down": pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]["down"]), (self.width, self.width)),
        #     "left": pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]["left"]), (self.width, self.width)),
        #     "right": pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]["right"]), (self.width, self.width))
        # }
        
        self.ghost_image = pygame.transform.scale(pygame.image.load(MONSTER_IMAGES[monster_type]), (self.width, self.width))
        self.frightened_image = pygame.transform.scale(pygame.image.load(FRIGHTENED_IMAGE), (self.width, self.width))
        
        # self.black_background = pygame.Surface((self.width, self.width))
        self.initial_cell = cell
        self.cell = cell 
        
        
    def frightened_mode(self):
        """Kich hoat che do so hay khi Pacman an power pellet"""
        self.is_frightened = True
        self.frightened_time = pygame.time.get_ticks() # Ghi lai thoi gian bat dau
        
    def draw(self):
        current_time = pygame.time.get_ticks()
        if self.is_frightened:
            if current_time - self.frightened_time > POWER_PELLET_DURATION * 1000:
                self.is_frightened = False
            image = self.frightened_image
        else:
            image = self.ghost_image
                    
        # image = self.monster_images.get(self.direction, self.monster_images["up"])
        self.app.screen.blit(image, (self.pixel_pos[0], self.pixel_pos[1]))
            
    def get_current_pixel_pos(self):
        return [self.grid_pos[0] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_Y]
        
    # def update_direction(self, new_grid_pos):
    #     direction_map = {
    #         (1, 0): 'right',
    #         (-1, 0): 'left',
    #         (0, 1): 'down',
    #         (0, -1): 'up' 
    #     }
        
    #     delta = (new_grid_pos[0] - self.grid_pos[0], new_grid_pos[1] - self.grid_pos[1])
    #     self.direction = direction_map.get(delta, self.direction)
                            
    def update(self, new_grid_pos):
        """Cập nhật vị trí của con ma"""
        self.app.screen.fill((0, 0, 0), (self.pixel_pos[0], self.pixel_pos[1], self.width, self.width)) # Xóa ma cũ
        self.grid_pos = new_grid_pos
        self.pixel_pos = self.get_current_pixel_pos()    
    
    
    def move(self, new_grid_pos):
        self.update(new_grid_pos)
        self.draw()
    
    def appear(self):
        self.draw()
        
    def get_around_cells_of_initial_cell(self, graph_map):
        return graph_map[self.initial_cell]

    def get_around_cells(self, graph_map):
        return graph_map[self.cell] 
    
    
                                 
class Red(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "red", cell)
        # self.speed = 2
        
class Blue(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "blue", cell)
        # self.speed = 2
        
class Pink(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "pink", cell)
        # self.speed = 2
        
class Orange(Ghost):
    def __init__(self, app, pos, cell=None):
        super().__init__(app, pos, "orange", cell)
        # self.speed = 2
        
class App:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 680))

if __name__ == "__main__":
    pygame.init()
    # screen = pygame.display.set_mode((610, 680))  # Khởi tạo cửa sổ game
    pygame.display.set_caption("Test Ghost")

    app = App()
    clock = pygame.time.Clock()
    running = True

    # Tạo một con ma màu đỏ để test
    red_ghost = Red(app=app, pos=(10, 10))  # Đặt tạm app=None, chỉ test hiển thị
    blue_ghost = Blue(app=app, pos=(12, 10))
    pink_ghost = Pink(app=app, pos=(14, 10))
    orange_ghost = Orange(app=app, pos=(16, 10))

    while running:
        app.screen.fill((0, 0, 0))  # Xóa màn hình mỗi frame
        
        red_ghost.draw()  # Vẽ ma lên màn hình
        blue_ghost.draw()
        pink_ghost.draw()
        orange_ghost.draw()
        
        red_ghost.move([red_ghost.grid_pos[0] + 1, red_ghost.grid_pos[1]])
        blue_ghost.move([blue_ghost.grid_pos[0] - 1, blue_ghost.grid_pos[1]])
        pink_ghost.move([pink_ghost.grid_pos[0], pink_ghost.grid_pos[1] + 1])
        orange_ghost.move([orange_ghost.grid_pos[0], orange_ghost.grid_pos[1] - 1])
        
        # pygame.display.update()
        pygame.display.flip()
        clock.tick(10)  # Giới hạn FPS về 30

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
