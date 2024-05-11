#initialize constants
ROWS = 15
COLS = 15
TILE_SIZE = 64
GAME_NAME = "Sentinel Siege"
SIDE_PANEL = 200
SCREEN_WIDTH = TILE_SIZE*COLS
SCREEN_HEIGHT = TILE_SIZE*ROWS
FPS = 60

#Monosters constants
SPEED = 1.5
SPAWN_COOLDOWN = 400

#tower constants
ANIMATION_STEPS = 6
ANIMATION_DELAY = 50
TOWER_LEVELS = 3

# Tower's data
TOWER_DATA = [
    {
        #1
        "range": 90,
        "cooldown": 1500,
    },
    {
        #2
        "range": 110,
        "cooldown": 1500,
    },
    {
        #3
        "range": 200,
        "cooldown": 1500,
    }
]