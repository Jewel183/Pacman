from config import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("arial", 30)
        
        self.buttons = {
            "Start": pygame.Rect(150, 405, 300, 50),
            "About": pygame.Rect(150, 485, 300, 50),
            "Exit": pygame.Rect(150, 565, 300, 50)
        } 
        
        self.bg = pygame.image.load(HOME_BACKGROUND)
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
        pygame.display.update()
        
    def handle_event(self, event):
        # Xử lí click chuột
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
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
#     pygame.display.set_caption("Test Main Menu")

#     # Tạo đối tượng menu
#     menu = MainMenu(screen)

#     running = True
#     while running:
#         screen.fill(BLACK)  # Xóa màn hình
#         menu.draw()  # Vẽ menu
        
#         # Xử lý sự kiện
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#             elif event.type == pygame.MOUSEBUTTONDOWN:
#                 clicked_button = menu.handle_event(event)
#                 if clicked_button:
#                     print(f"Nút '{clicked_button}' được nhấn!")  # In ra tên nút khi bấm

#         pygame.display.update()

#     pygame.quit()