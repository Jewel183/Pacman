import pygame

# Window App
APP_WIDTH, APP_HEIGHT = 610, 680
APP_CAPTION = r"Pacman Game"
FPS = 120

MAP_IMG = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Demo\\map0.jpg"
MAP_INPUT_TXT = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\map.txt"
MAP_NUM = len(MAP_IMG)


# Background
LEVEL_BACKGROUND = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Background\\level.jpg"
HOME_BACKGROUND = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Background\\background.jpg"
ABOUT_BACKGROUND = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Background\\about.jpg"

# Play screen
ROW_PADDING, COL_PADDING = 50, 60
MAP_WIDTH, MAP_HEIGHT = APP_WIDTH - ROW_PADDING, APP_HEIGHT - COL_PADDING

MAP_POS_X, MAP_POS_Y = ROW_PADDING // 2, COL_PADDING * 2 // 3
SCORE_POS = (30, 10)
READY_POS = (APP_WIDTH // 2, 10)
HOME_RECT = (APP_WIDTH - ROW_PADDING - 20, 10, 40, 20)
SPEED_RECT = (APP_WIDTH - ROW_PADDING - 150, 10, 110, 20)

CELL_SIZE = 20
ROW, COL = MAP_WIDTH // CELL_SIZE, MAP_HEIGHT // CELL_SIZE
SPEED = 250


FONT = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Font\\Pixelfy.ttf"

# Color
BACKGROUND_COLOR =(65, 98, 132)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
TOMATO = (255, 99, 71)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)


PACMAN_IMAGE = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Pacman\\0.png"
PACMAN_LEFT = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Pacman\\left.png"
PACMAN_RIGHT = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Pacman\\right.png"
PACMAN_UP = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Pacman\\up.png"
PACMAN_DOWN = r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Pacman\\down.png"

# BLACK_BG

MONSTER_IMAGES = {
    "red": r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Ghost\\red.png", 
    "blue": r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Ghost\\blue.png", 
    "pink": r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Ghost\\pink.png", 
    "orange": r"E:\\2024-2025\\HK2_2024-2025\\AI\\Project01\\Project-Search-Pacman\\Assets\\Ghost\\orange.png"
}

