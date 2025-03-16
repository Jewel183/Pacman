import pygame

# Window App
APP_WIDTH, APP_HEIGHT = 880, 680
APP_CAPTION = r"Pacman Game"
FPS = 120

MAP_IMG = r"./map0.jpg"
MAP_INPUT_TXT = r"./map0.txt"
MAP_NUM = len(MAP_IMG)

# Background
HOME_BACKGROUND = r"./Assets\\Background\\background.jpg"
LEADERBOARD = r"./Assets\\Background\\about.jpg"
ABOUT_BACKGROUND = r"./Assets\\Background\\about.jpg"
GAMEOVER_BACKGROUND = r"../Assets/bg/gameover_bg.png"
VICTORY_BACKGROUND = r"../Assets/bg/victory_bg.jpg"

# Screen state
STATE_HOME = "home"
STATE_PLAYING = "playing"
STATE_ABOUT = "about"
STATE_LEVEL = "level"
STATE_SETTING = "setting"
STATE_GAMEOVER = "gameover"
STATE_VICTORY = "victory"

# Home screen
HOME_BG_WIDTH, HOME_BG_HEIGHT = APP_WIDTH, APP_HEIGHT - 410
START_POS = pygame.Rect(150, 325, 300, 50)
SETTING_POS = pygame.Rect(150, 405, 300, 50)
ABOUT_POS = pygame.Rect(150, 485, 300, 50)
EXIT_POS = pygame.Rect(150, 565, 300, 50)

# Level screen
LEVEL_1_POS = pygame.Rect(150, 320, 300, 50)
LEVEL_2_POS = pygame.Rect(150, 390, 300, 50)
LEVEL_3_POS = pygame.Rect(150, 460, 300, 50)
LEVEL_4_POS = pygame.Rect(150, 530, 300, 50)
LEVEL_5_POS = pygame.Rect(150, 600, 300, 50)
BACK_LEVEL_POS = pygame.Rect(500, 600, 70, 50)

# About screen
BACK_POS = pygame.Rect(225, 530, 150, 50)

# Setting screen
OK_POS = pygame.Rect(225, 620, 100, 50)
TRIANGLE_1_POS = [[360, 620], [360, 670], [403.3, 645]]
TRIANGLE_2_POS = [[250, 620], [250, 670], [206.7, 645]]

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

# Gameover screen
COIN_IMAGE = r"../Assets/effects/coin.jpg"
COIN_POS = (200, 430)
COIN_WIDTH, COIN_HEIGHT = (200, 200)
GAMEOVER_BACKGROUND_WIDTH, GAMEOVER_BACKGROUND_HEIGHT = HOME_BG_WIDTH, HOME_BG_HEIGHT + 300

# Victory screen
PACMAN = r"../Assets/effects/pacman1.png"

VICTORY_WIDTH, VICTORY_HEIGHT = (500, 400)
PACMAN_WIDTH, PACMAN_HEIGHT = (500, 280)

# Score
SCORE_BONUS = 10
SPECIAL_SCORE = 40
SCORE_PENALTY = -1

#Font
# FONT 

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

# Pacman, Food, Monster
FOOD_IMAGE = r"./Assets\\Food\\dot.png"
POWER_PELLET_IMAGE = r"./Assets\\Food\\powerdot.png"
SPECIAL_FOOD_IMAGE = r"./Assets\\Food\\food.png"
POWER_PELLET_DURATION = 8

PACMAN_IMAGE = r"./Assets/Pacman/0.png"
PACMAN_LEFT = r"./Assets\\Pacman\\left.png"
PACMAN_RIGHT = r"./Assets\\Pacman\\right.png"
PACMAN_UP = r"./Assets\\Pacman\\up.png"
PACMAN_DOWN = r"./Assets\\Pacman\\down.png"

# BLACK_BG

MONSTER_IMAGES = {
    "red": r"./Assets\\Ghost\\red.png", 
    "blue": r"./Assets\\Ghost\\blue.png", 
    "pink": r"./Assets\\Ghost\\pink.png", 
    "orange": r"./Assets\\Ghost\\orange.png"
}

FRIGHTENED_IMAGE = r"./Assets\\Ghost\\powerup.png"

