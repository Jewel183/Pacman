import pygame
from config import *
from MainMenu import MainMenu
from Leaderboard import Leaderboard
from About import About

def main():
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption("Pac-Man Game")

    # Khởi tạo màn hình chính và leaderboard
    main_menu = MainMenu(screen)
    leaderboard = Leaderboard(screen)
    about = About(screen)

    current_screen = "menu"  # Trạng thái hiện tại của màn hình
    running = True

    while running:
        screen.fill(BLACK)  # Xóa màn hình

        # Hiển thị màn hình hiện tại
        if current_screen == "menu":
            main_menu.draw()
        elif current_screen == "leaderboard":
            leaderboard.draw()
        elif current_screen == "about":
            about.draw()

        # Lắng nghe sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if current_screen == "menu":
                action = main_menu.handle_event(event)
                if action == "Start":
                    print("Start are clicking")
                if action == "Leaderboard":
                    current_screen = "leaderboard"  # Chuyển sang leaderboard
                elif action == "About":
                    current_screen = "about"
                elif action == "Exit":
                    running = False
            elif current_screen == "leaderboard":
                action = leaderboard.handle_event(event)
                if action == "back":
                    current_screen = "menu"  # Quay lại menu chính
            elif current_screen == 'about':
                action = about.handle_event(event)
                if action == "back":
                    current_screen = "menu"

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
