import config as cf

class PheromoneMap:
    def __init__(self, width, height):
        """
        A potential map of the quantity of pheromones to determine in which direction to go.
        """
        self.width = width
        self.height = height
        self.pmap = [[0.0 for _ in range(width)] for _ in range(height)]  # initialize with null potential everywhere because the environment is unknown
    
    def is_inside(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get(self, x, y):
        """
        Get the potential of a cell if it lies within the limits of the environment.
        """
        if self.is_inside(x, y):
            return self.pmap[y][x]
        return 0.0 # no attraction if the zone is out of the environment
    
    def add(self, x, y, p_amount=cf.PHEROMONES_AMOUNT):
        """
        Add pheromones in a cell.
        """
        if self.is_inside(x, y):
            self.pmap[y][x] += p_amount
    
    def evaporate(self, evaporation_rate=cf.EVAPORATION_RATE):
        """
        Evaporation of pheromones with time.
        """
        for y in range(self.height):
            for x in range(self.width):
                self.pmap[y][x] *= (1 - evaporation_rate)
    
    def diffuse(self, diffusion_rate=cf.DIFFUSION_RATE):
        """
        Diffusion of pheromones in space.
        """
        new_pmap = [[0.0 for _ in range(self.width)] for _ in range(self.height)]

        for y in range(self.height):
            for x in range(self.width):
                new_potential = self.pmap[y][x] * (1 - 8*diffusion_rate) # pheromones diffusing from a cell to its neighbours
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]: # all cells around
                    if self.is_inside(x + dx, y + dy):
                        new_potential += self.pmap[y+dy][x+dx] * diffusion_rate # augmentation of pheromones due to the diffusion in neighbouring cells
                    else:
                        new_potential += self.pmap[y][x] * diffusion_rate # convention to maintain continuity of pheromone intensity at the border of the environment
                new_pmap[y][x] = new_potential
        self.pmap = new_pmap