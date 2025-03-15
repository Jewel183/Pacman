from config import *

class Leaderboard:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("timesnewroman", 30)
        self.title_font = pygame.font.SysFont("arial", 40, bold=True)
        self.scores = self.load_scores()
        self.back_button = pygame.Rect(250, 550, 150, 50)
        self.bg = pygame.image.load(HOME_BACKGROUND)
        self.bg = pygame.transform.scale(self.bg, (APP_WIDTH, APP_HEIGHT))
        self.is_hovering = False
        
    def load_scores(self):
        """ Load danh sách điểm từ file """
        try:
            with open("leaderboard.txt", "r") as file:
                scores = [int(line.strip()) for line in file.readlines()]
            return sorted(scores, reverse=True)[:5]
        except FileNotFoundError:
            return [0, 0, 0, 0, 0]
        
    def save_scores(self, new_score):
        self.scores.append(new_score)
        self.scores = sorted(self.scores, reverse=True)[:5]
        with open("leaderboard.txt", "w") as file:
            for score in self.scores:
                file.write(str(score) + "\n")
                
    def draw(self):
        """ Vẽ màn hình leaderboard """
        self.screen.blit(self.bg, (0, 0))

        # Tiêu đề
        title_text = self.title_font.render("🏆 Leaderboard 🏆", True, WHITE)
        self.screen.blit(title_text, (APP_WIDTH // 2 - title_text.get_width() // 2, 100))

        # Hiển thị danh sách điểm
        for i, score in enumerate(self.scores):
            score_text = self.font.render(f"{i+1}. {score} score", True, WHITE)
            self.screen.blit(score_text, (APP_WIDTH // 2 - 100, 200 + i * 50))

        # Vẽ nút quay lại
        pygame.draw.rect(self.screen, DARK_GREY, self.back_button, border_radius=10)
        back_text = self.font.render("Back", True, WHITE)
        back_text_rect = back_text.get_rect(center=self.back_button.center)
        self.screen.blit(back_text, back_text_rect)
        
        button_color = LIGHT_GREY if self.is_hovering else DARK_GREY
        pygame.draw.rect(self.screen, button_color, self.back_button)
        
        text_surf = self.font.render("BACK", True, WHITE)
        text_rect = text_surf.get_rect(center=self.back_button.center)
        self.screen.blit(text_surf, text_rect)

        pygame.display.update()
        
    def handle_event(self, event):
        """ Xử lý sự kiện nhấn nút quay lại """
        mouse_pos = pygame.mouse.get_pos()
        
        self.is_hovering = self.back_button.collidepoint(mouse_pos)
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_button.collidepoint(event.pos):
                return "back"  # Quay lại menu chính
        return None
    
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption("Test Leaderboard")

    leaderboard = Leaderboard(screen)
    running = True

    while running:
        screen.fill(BLACK)
        leaderboard.draw()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif leaderboard.handle_event(event) == "back":
                print("Quay lại menu")  # Khi bấm "Back"

        pygame.display.update()

    pygame.quit()