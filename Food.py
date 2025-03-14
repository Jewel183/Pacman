import pygame.image
from config import *

class Food:
    def __init__(self, app, pos, food_type="normal", cell=None):
        self.app = app
        self.width = 10
        self.grid_pos = [pos[0], pos[1]]
        self.pixel_pos = self.get_current_pixel_pos()
        self.food_type = food_type
        
        food_images = {
            "normal": FOOD_IMAGE,
            "power_pellet": POWER_PELLET_IMAGE,
            "special": SPECIAL_FOOD_IMAGE
        }
        if food_type == "power_pellet" or food_type == "special":
            self.image = pygame.transform.scale(pygame.image.load(food_images[food_type]), (self.width * 2, self.width * 2))
        else:
            self.image = pygame.transform.scale(pygame.image.load(food_images[food_type]), (self.width, self.width))
        self.cell = cell
        
    def appear(self):
        """Hien thi thuc an len man hinh"""
        self.draw()
        
    def get_pos(self):
        return self.grid_pos[0], self.grid_pos[1]
    
    def get_current_pixel_pos(self):
        """Lay vi tri pixel hien tai cua thuc an"""
        return [self.grid_pos[0] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_X,
                self.grid_pos[1] * CELL_SIZE + CELL_SIZE // 2 - self.width // 2 + MAP_POS_Y]
        
    def draw(self):
        """Ve thuc an len man hinh"""
        food_rect = self.app.screen.blit(self.image, (self.pixel_pos[0], self.pixel_pos[1]))
        pygame.display.update(food_rect)
        
    def get_effect(self):
        """Trả về hiệu ứng cho từng loại thức ăn"""
        if self.food_type == "normal":
            return SCORE_BONUS # Cộng điểm bình thường
        elif self.food_type == "power_pellet":
            return "frightened"
        elif self.food_type == "special":
            return SPECIAL_SCORE
        return None
    
if __name__ == "__main__":
    pygame.init()
    
    # Tạo cửa sổ để test
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption("Test Food")
    screen.fill((0, 0, 0))  # Màu nền đen

    # Fake app có màn hình
    class FakeApp:
        def __init__(self, screen):
            self.screen = screen

    app = FakeApp(screen)

    # Tạo các thức ăn test
    food1 = Food(app, (5, 5), "normal")
    food2 = Food(app, (10, 10), "power_pellet")
    food3 = Food(app, (7, 7), "special")

    # Hiển thị thức ăn
    food1.appear()
    food2.appear()
    food3.appear()

    pygame.display.update()

    # Chạy vòng lặp hiển thị
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()
