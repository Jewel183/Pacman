from config import *

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 30)
        
        self.buttons = {
            "Level 1": pygame.Rect(280, 110, 300, 50),
            "Level 2": pygame.Rect(280, 195, 300, 50),
            "Level 3": pygame.Rect(280, 280, 300, 50),
            "Level 4": pygame.Rect(280, 365, 300, 50),
            "Level 5": pygame.Rect(280, 450, 300, 50),
            "Level 6": pygame.Rect(280, 535, 300, 50)
        } 
        
        self.back_button = pygame.Rect(100, 580, 150, 50)
        
        self.bg = pygame.image.load(LEVEL_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        
    
    def draw(self):
        """ Vẽ button với hiệu ứng hover và click """
        self.screen.blit(self.bg, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        
        for text, rect in self.buttons.items():
            # Hiệu ứng hover khi di chuột vào
            if rect.collidepoint(mouse_pos):
                button_color = LIGHT_GREY
            else:
                button_color = DARK_GREY
            
            pygame.draw.rect(self.screen, button_color, rect, border_radius=10)
            
            text_surf = self.font.render(text, True, WHITE)
            text_rect = text_surf.get_rect(center=rect.center)
            self.screen.blit(text_surf, text_rect)
            
        button_color = LIGHT_GREY if self.back_button.collidepoint(mouse_pos) else DARK_GREY
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)

        text_surf = self.font.render("Back", True, WHITE)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        
        
    def handle_event(self, event):
        # Xử lí click chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.back_button.collidepoint(mouse_pos):
                return "back"
            
            for text, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, WHITE, rect, border_radius=10)
                    pygame.display.update()
                    pygame.time.delay(100) # Giữ hiệu ứng trong ms
                    return text  # Trả về tên của nút được nhấn
        return None
    

# if __name__ == "__main__":
#     pygame.init()

#     # Tạo cửa sổ game
#     screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
#     pygame.display.set_caption("Test LEVEL")

#     # Tạo đối tượng menu
#     level = Level(screen)

#     running = True
#     while running:
#         screen.fill(BLACK)  # Xóa màn hình
#         level.draw()  # Vẽ menu
        
#         # Xử lý sự kiện
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 clicked_button = level.handle_event(event)
#                 if clicked_button:
#                     print(f"Nút '{clicked_button}' được nhấn!")  # In ra tên nút khi bấm

#         pygame.display.update()

#     pygame.quit()