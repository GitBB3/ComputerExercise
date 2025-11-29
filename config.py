####################################################################
################## Simulation parameters ###########################
####################################################################

### Simulation parameters
SPEED = 100 # ms between steps

### Environment size
GRID_H = 30 # height of the environment
GRID_W = 60 # width of the environment
CELL = 15 # size of a cell in the environment grid in pixels
NEST_H = GRID_H // 2 # position of the nest (set to the middle of the environment)
NEST_W = GRID_W // 2

### Objects quantity
NB_FOOD_CLUSTERS = 4
FOOD_CLUSTER_SIZE = 4
NB_OBSTACLES_CLUSTERS = 3
OBSTACLES_CLUSTER_SIZE = 3
MIN_OBJ = 10
MAX_OBJ = 25

### Ants quantity
NB_ANTS = 10

### Pheromones caracteristics
PHEROMONES_AMOUNT = 2.0
EVAPORATION_RATE = 0.02
DIFFUSION_RATE = 0.01