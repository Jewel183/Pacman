from config import *

class Level:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont(FONT, 30)
        self.title_font = pygame.font.SysFont(FONT, 40, bold=True)
        
        self.buttons = {
            "Level 1": pygame.Rect(150, 105, 300, 50),
            "Level 2": pygame.Rect(150, 190, 300, 50),
            "Level 3": pygame.Rect(150, 275, 300, 50),
            "Level 4": pygame.Rect(150, 360, 300, 50),
            "Level 5": pygame.Rect(150, 445, 300, 50),
            "Level 6": pygame.Rect(150, 530, 300, 50)
        } 
        
        self.back_button = pygame.Rect(50, 600, 100, 50)
        
        self.bg = pygame.image.load(LEVEL_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        
    
    def draw(self):
        title_text = self.title_font.render("Choose the level you want", True, WHITE)
        self.screen.blit(title_text, (APP_WIDTH // 2 - title_text.get_width() // 2, 120))
        
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
            
        button_color = LIGHT_GREY if self.back_button.collidepoint(mouse_pos) else DARK_GREY
        pygame.draw.rect(self.screen, button_color, self.back_button, border_radius=10)

        text_surf = self.font.render("Back", True, WHITE)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)
        pygame.display.update()
        
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if self.back_button.collidepoint(mouse_pos):
                return "back"
            
            for text, rect in self.buttons.items():
                if rect.collidepoint(mouse_pos):
                    pygame.draw.rect(self.screen, WHITE, rect, border_radius=10)
                    pygame.display.update()
                    pygame.time.delay(100) 
                    return text  
        return None
    