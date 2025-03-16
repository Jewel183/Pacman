from config import *

class About:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("timesnewroman", 25)
        self.title_font = pygame.font.SysFont(FONT, 60)
        
        self.back_button = pygame.Rect(100, 580, 150, 50)
        self.bg = pygame.image.load(ABOUT_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        self.is_hovering = False  # Kiểm tra hover cho nút Back

        # Nội dung About
        self.about_text = [
            "Project 1. Search",
            "Developed by: ",
            "23127094 - Hoàng Nhân",
            "23127134 - Phan Phú Trọng",
            "23127200 - Nguyễn Minh Kha",
            "23127246 - Nguyễn Trần Thiên Phú"
        ]
        
        self.box_width, self.box_height = 500, 300  # Kích thước bảng
        self.box_pos = (APP_WIDTH // 2 - self.box_width // 2, 180)  # Vị trí bảng

    def draw(self):
        """ Vẽ màn hình About """
        self.screen.blit(self.bg, (0, 0))
        
        # Vẽ bảng nền mờ
        box_surface = pygame.Surface((self.box_width, self.box_height), pygame.SRCALPHA)
        box_surface.fill((0, 0, 0, 180))  # Màu đen với độ trong suốt 180/255
        self.screen.blit(box_surface, self.box_pos)

        # Hiển thị tiêu đề
        title_text = self.title_font.render("Information", True, WHITE)
        self.screen.blit(title_text, (APP_WIDTH // 2 - title_text.get_width() // 2, 120))

        # Hiển thị nội dung
        for i, line in enumerate(self.about_text):
            text_surface = self.font.render(line, True, WHITE)
            if i == 0:
                text_x = self.box_pos[0] + self.box_width // 2 - text_surface.get_width() // 2
            else:
                text_x = self.box_pos[0] + 50
            text_y = self.box_pos[1] + 30 + i * 40  # Cách lề trên của bảng 30px
            self.screen.blit(text_surface, (text_x, text_y))
            
        # Hiệu ứng hover cho nút Back
        # button_color = LIGHT_GREY if self.is_hovering else DARK_GREY
        mouse_pos = pygame.mouse.get_pos()
        if self.back_button.collidepoint(mouse_pos):
            button_color = LIGHT_GREY  
        else:
            button_color = DARK_GREY
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)

        text_surf = self.font.render("BACK", True, WHITE)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)

        pygame.display.update()

    def handle_event(self, event):
        """ Xử lý sự kiện cho màn hình About """
        mouse_pos = pygame.mouse.get_pos()
        self.is_hovering = self.back_button.collidepoint(mouse_pos)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "back"
        return None


def main():
    pygame.init()

    # Tạo cửa sổ game
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption("Test ABOUT SCREEN")

    # Tạo đối tượng màn hình About
    about_screen = About(screen)

    running = True
    while running:
        screen.fill(BLACK)  # Xóa màn hình
        about_screen.draw()  # Vẽ màn hình About
        
        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if about_screen.handle_event(event) == "back":
                    print("Back button clicked! Quitting test...")
                    running = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
