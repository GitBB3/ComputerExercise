import random as rd
import math

class Ant:
    def __init__(self, nest_x, nest_y, env_memory, p_memory):
        self.x, self.y = nest_x, nest_y
        self.nest = [nest_x, nest_y]
        self.carrying = False # the ant is not carrying food
        self.avoiding_obstacle = False
        self.collision_dist = None
        self.env_memory = env_memory
        self.p_memory = p_memory

    def scan_environment(self, env, p_map):
        """
        The ant detects pheromones and obstacles around itself to update its local knowledge of the environment.
        """
        directions = [(0,0), (-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]
        for dx, dy in directions:
            if env.is_inside(self.x + dx, self.y + dy):
                if self.env_memory.grid[self.y + dy][self.x + dx] != env.get_type(self.x + dx, self.y + dy):
                    self.env_memory.grid[self.y + dy][self.x + dx] = env.get_type(self.x + dx, self.y + dy)
                if self.p_memory.pmap[self.y + dy][self.x + dx] != p_map.get(self.x + dx, self.y + dy):
                    self.p_memory.pmap[self.y + dy][self.x + dx] = p_map.get(self.x + dx, self.y + dy)

    def explore_rd(self, env, env_real):
        """
        Find food in the environment.
        """
        dx, dy = rd.choice([(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]) #change the random displacement
        if env.is_inside(self.x + dx, self.y + dy) and env.get_type(self.x + dx, self.y + dy)!='obstacle' :
            self.x = self.x + dx
            self.y = self.y + dy
            env.distance_walked +=1

        if env_real.grid[self.y][self.x] == 'food': # if the ant finds food
            self.carrying = True # carries the food
            env_real.grid[self.y][self.x] = 'empty' # the food is not on the cell anymore
    
    def back_nest_bug2(self, env, env_real):
        """
        Bring food back to the nest with Bug2 algorithm to avoid obstacles.
        """
        diff_x = self.nest[0] - self.x
        diff_y = self.nest[1] - self.y
        step_x = 1 if diff_x > 0 else -1 if diff_x < 0 else 0
        step_y = 1 if diff_y > 0 else -1 if diff_y < 0 else 0
        dist = math.hypot(diff_x,diff_y)

        if not self.avoiding_obstacle and env.is_inside(self.x + step_x, self.y + step_y) : # move straight to the nest
            if env.grid[self.y + step_y][self.x + step_x]=='obstacle':
                self.collision_dist = dist
                self.avoiding_obstacle = True
            else:
                self.x += step_x
                self.y += step_y
                env.distance_walked +=1
        elif self.avoiding_obstacle: # Bug2 algo to avoid obstacles
            directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]
            for step_x, step_y in directions:
                if env.is_inside(self.x + step_x, self.y + step_y):
                    if env.grid[self.y + step_y][self.x + step_x]!='obstacle':
                        self.x += step_x
                        self.y += step_y
                        env.distance_walked +=1
                        break
            new_dist = math.hypot(self.nest[0] - self.x, self.nest[1] - self.y)
            if new_dist < self.collision_dist:
                self.avoiding_obstacle = False

        if env.grid[self.y][self.x] == 'nest':
            self.carrying = False
            env_real.food_collected += 1 # counting the units of food collected for statistics

    def move(self, env, p_map):
        if not self.carrying:
            self.scan_environment(env, p_map)
            self.explore_rd(env,env)
        else:
            self.back_nest_bug2(env,env)
            p_map.add(self.x, self.y)
            self.scan_environment(env, p_map)
    
    def explore_ph(self, env):
        """
        Use a gradient descent on the local map of pheromones (p_memory) to find the location of food.
        """
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]
        moves = [(dx, dy, self.p_memory.pmap[self.y + dy][self.x + dx])
                 for dx, dy in directions
                 if self.env_memory.is_inside(self.x + dx, self.y + dy) and self.env_memory.grid[self.y + dy][self.x + dx] != 'obstacle'
                 ]
        dx, dy, max_pheromones = max(moves, key=lambda m: m[2])
        current_dist = math.hypot(self.x - self.nest[0], self.y - self.nest[1])
        new_dist = math.hypot(self.x + dx - self.nest[0], self.y + dy - self.nest[1])

        if max_pheromones > 0.0 and new_dist > current_dist: # if pheromones are detected around the ant and if the trail of pheromone enables to go further from the nest
            if self.env_memory.get_type(self.x + dx, self.y + dy) != 'obstacle':
                self.x += dx
                self.y += dy
                env.distance_walked +=1
        
        else: # if no pheromones are detected around the ant or if pheromones lead toward the nest
            self.explore_rd(self.env_memory,env)
        
        if env.grid[self.y][self.x] == 'food': # if the ant finds food
                self.carrying = True # carries the food
                env.grid[self.y][self.x] = 'empty' # the food is not on the cell anymore
        
    def move_on_memory(self, env, p_map):
        if not self.carrying:
            self.scan_environment(env, p_map) # scan the real environment (env, p_map)
            self.explore_ph(env) # look for food based on decentered knowledge (env_memory, p_memory)
        else:
            self.back_nest_bug2(self.env_memory,env) # bug2 algorithm to retrieve food based on decentered knowledge (env_memory, p_memory)
            p_map.add(self.x, self.y) # add pheromones on the real environment (env, p_map)
            self.scan_environment(env, p_map) # scan the real environment (env, p_map)