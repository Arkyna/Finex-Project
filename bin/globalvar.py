#######################
#initialize constants
#######################
ROWS = 15
COLS = 15
TILE_SIZE = 64
GAME_NAME = "Sentinel Siege"
SIDE_PANEL = 200
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 960
FPS = 60
HEALTH = 1
MONEY = 1000
LEVEL_COMPLETE_REWARD = 100
TOTAL_LEVELS = 1

#######################
# Tower's Constants
#######################
ANIMATION_STEPS = 6
ANIMATION_DELAY = 30
TOWER_LEVELS = 3
BUY_COST = 50
UPGRADE_COST = 100
DAMAGE = 5

# Tower's Data
TOWER_DATA = [
    {
        #1
        "range": 110,
        "cooldown": 1500,
    },
    {
        #2
        "range": 150,
        "cooldown": 1500,
    },
    {
        #3
        "range": 200,
        "cooldown": 1500,
    }
]

#######################
# Monster's Constants
#######################
SPEED = 1.5
SPAWN_COOLDOWN = 400
KILL_REWARD = 100

# Monster's Data
ENEMY_SPAWN_DATA = [
  {
    #1
    "weak": 1,
    "medium": 1,
    "strong": 0,
    "elite": 0
  },
  {
    #2
    "weak": 30,
    "medium": 0,
    "strong": 0,
    "elite": 0
  },
  {
    #3
    "weak": 20,
    "medium": 5,
    "strong": 0,
    "elite": 0
  },
  {
    #4
    "weak": 30,
    "medium": 15,
    "strong": 0,
    "elite": 0
  },
  {
    #5
    "weak": 5,
    "medium": 20,
    "strong": 0,
    "elite": 0
  },
  {
    #6
    "weak": 15,
    "medium": 15,
    "strong": 4,
    "elite": 0
  },
  {
    #7
    "weak": 20,
    "medium": 25,
    "strong": 5,
    "elite": 0
  },
  {
    #8
    "weak": 10,
    "medium": 20,
    "strong": 15,
    "elite": 0
  },
  {
    #9
    "weak": 15,
    "medium": 10,
    "strong": 5,
    "elite": 0
  },
  {
    #10
    "weak": 0,
    "medium": 100,
    "strong": 0,
    "elite": 0
  },
  {
    #11
    "weak": 5,
    "medium": 10,
    "strong": 12,
    "elite": 2
  },
  {
    #12
    "weak": 0,
    "medium": 15,
    "strong": 10,
    "elite": 5
  },
  {
    #13
    "weak": 20,
    "medium": 0,
    "strong": 25,
    "elite": 10
  },
  {
    #14
    "weak": 15,
    "medium": 15,
    "strong": 15,
    "elite": 15
  },
  {
    #15
    "weak": 25,
    "medium": 25,
    "strong": 25,
    "elite": 25
  }
]

ENEMY_DATA = {
    "weak": {
    "health": 10,
    "speed": 1
  },
    "medium": {
    "health": 15,
    "speed": 2
  },
    "strong": {
    "health": 20,
    "speed": 3
  },
    "elite": {
    "health": 30,
    "speed": 4
  }
}