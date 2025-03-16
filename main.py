import pygame
from config import *
from MainMenu import MainMenu
from Level import Level
from About import About

def main():
    pygame.init()

    # Tạo cửa sổ game
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption("Pac-Man AI Project")

    # Khởi tạo các màn hình
    main_menu = MainMenu(screen)
    level_screen = Level(screen)
    about_screen = About(screen)

    # Trạng thái game (bắt đầu từ menu chính)
    game_state = "menu"

    running = True
    while running:
        screen.fill(BLACK)  # Xóa màn hình
        
        if game_state == "menu":
            main_menu.draw()
        elif game_state == "level":
            level_screen.draw()
        elif game_state == "about":
            about_screen.draw()

        # Xử lý sự kiện
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "menu":
                result = main_menu.handle_event(event)
                if result == "Start":
                    game_state = "level"  # Chuyển đến màn hình chọn level
                elif result == "About":
                    game_state = "about"  # Chuyển đến màn hình About
                elif result == "Exit":
                    running = False  # Thoát game
            
            elif game_state == "level":
                result = level_screen.handle_event(event)
                if result:  
                    print(f"Chọn {result} để bắt đầu game!")  # Sau này sẽ xử lý vào game
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    game_state = "menu"  # Trở về menu chính
                
            if game_state == "level":
                result = level_screen.handle_event(event)
                if result == "back":
                    game_state = "menu"    
            
            elif game_state == "about":
                result = about_screen.handle_event(event)
                if result == "back":
                    game_state = "menu"  # Trở về menu chính

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
