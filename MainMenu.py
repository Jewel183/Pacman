from config import *

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT, 30)
        
        self.buttons = {
            "Start": pygame.Rect(150, 405, 300, 50),
            "About": pygame.Rect(150, 485, 300, 50),
            "Exit": pygame.Rect(150, 565, 300, 50)
        } 
        
        self.bg = pygame.image.load(HOME_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        
    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        
        mouse_pos = pygame.mouse.get_pos()
        
        for text, rect in self.buttons.items():
            
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
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            for text, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, WHITE, rect, border_radius=10)
                    pygame.display.update()
                    pygame.time.delay(100) 
                    return text  
        return None



