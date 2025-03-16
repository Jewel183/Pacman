import pygame
from config import *  # Import các giá trị như APP_WIDTH, APP_HEIGHT, CELL_SIZE
from Pacman import Pacman  # Import Pac-Man
from Ghost import Blue  # Import ma xanh (Blue Ghost dùng BFS)

class GridTest:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
        pygame.display.set_caption("Test Pac-Man & Ghost trên Map")
        self.font = pygame.font.SysFont("arial", 20)
        self.running = True

        # Load ảnh bản đồ
        self.map_img = pygame.image.load(MAP_IMG)  # Đường dẫn tới file ảnh
        self.map_img = pygame.transform.scale(self.map_img, (MAP_WIDTH, MAP_HEIGHT))  # Resize cho đúng kích thước

        # Tạo Pac-Man ở vị trí (5, 5)
        self.pacman = Pacman(self, (5, 5))

        # Tạo ma xanh (Blue Ghost) ở vị trí (10, 10)
        self.ghost = Blue(self, (10, 11))

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

    def run(self):
        """ Vòng lặp chạy chương trình """
        while self.running:
            self.screen.fill(BLACK)  # Xóa màn hình
            self.screen.blit(self.map_img, (MAP_POS_X, MAP_POS_Y))  # Hiển thị bản đồ
            self.draw_grids()  # Vẽ lưới lên bản đồ
            self.pacman.draw()  # Vẽ Pac-Man
            self.ghost.draw()  # Vẽ con ma

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False  # Thoát vòng lặp nếu bấm đóng cửa sổ

            pygame.display.update()  # Cập nhật màn hình

        pygame.quit()  # Kết thúc pygame

if __name__ == "__main__":
    test = GridTest()
    test.run()
