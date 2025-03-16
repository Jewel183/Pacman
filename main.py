import pygame
from config import *
from MainMenu import MainMenu
from Level import Level
from About import About
from lv1 import *
from lv2 import *
from lv3 import *
from lv4 import *
from lv5 import *

def main():
    pygame.init()
    screen = pygame.display.set_mode((APP_WIDTH, APP_HEIGHT))
    pygame.display.set_caption("Pac-Man AI Project")

    main_menu = MainMenu(screen)
    level_screen = Level(screen)
    about_screen = About(screen)

    game_state = "menu"

    running = True
    while running:
        screen.fill(BLACK)  
        
        if game_state == "menu":
            main_menu.draw()
        elif game_state == "level":
            level_screen.draw()
        elif game_state == "about":
            about_screen.draw()

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
                if result == "Level 1":
                    level1 = Level1()
                    level1.run()
                    if result == "back":
                        game_state = "level"
                elif result == "Level 2":
                    level2 = Level2()
                    level2.run()
                    if result == "back":
                        game_state = "level"
                elif result == "Level 3":
                    level3 = Level3()
                    level3.run()
                    if result == "back":
                        game_state = "level"
                elif result == "Level 4":
                    level4 = Level4()
                    level4.run()
                    if result == "back":
                        game_state = "level"
                elif result == "Level 5":
                    level5 = Level5()
                    level5.run()
                    if result == "back":
                        game_state = "level"
                elif result == "back":
                    game_state = "menu"
                # elif event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                #     game_state = "menu"  # Trở về menu chính
                
            elif game_state == "about":
                result = about_screen.handle_event(event)
                if result == "back":
                    game_state = "menu"  

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()
