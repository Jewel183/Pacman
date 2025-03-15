from config import *

class About:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 25)
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        
        self.back_button = pygame.Rect(250, 550, 150, 50)
        self.bg = pygame.image.load(ABOUT_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        self.is_hovering = False  # Kiểm tra hover cho nút Back

        # Nội dung About
        self.about_text = [
            "Pac-Man AI Project",
            "Developed by: Your Team Name",
            "Using Python & Pygame",
            "AI Algorithms: BFS, DFS, A*, UCS",
            "Enjoy the game!"
        ]

    def draw(self):
        """ Vẽ màn hình About """
        self.screen.blit(self.bg, (0, 0))

        # Hiển thị tiêu đề
        title_text = self.title_font.render("About the Game", True, WHITE)
        self.screen.blit(title_text, (APP_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Hiển thị nội dung
        for i, line in enumerate(self.about_text):
            text_surface = self.font.render(line, True, WHITE)
            self.screen.blit(text_surface, (APP_WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 40))

        # Hiệu ứng hover cho nút Back
        button_color = LIGHT_GREY if self.is_hovering else DARK_GREY
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
