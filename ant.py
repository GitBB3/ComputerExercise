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
        directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]
        for dx, dy in directions:
            if env.is_inside(self.x + dx, self.y + dy):
                if self.env_memory.grid[self.y + dy][self.x + dx] != env.get_type(self.x + dx, self.y + dy):
                    self.env_memory.grid[self.y + dy][self.x + dx] = env.get_type(self.x + dx, self.y + dy)
                if self.p_memory.pmap[self.y + dy][self.x + dx] != p_map.get(self.x + dx, self.y + dy):
                    self.p_memory.pmap[self.y + dy][self.x + dx] = p_map.get(self.x + dx, self.y + dy)

    def explore_rd(self, env, p_map):
        """
        Find food in the environment.
        """
        dx, dy = rd.choice([(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]) #change the random displacement
        if env.is_inside(self.x + dx, self.y + dy) and env.get_type(self.x + dx, self.y + dy)!='obstacle' :
            self.x = self.x + dx
            self.y = self.y + dy

        if env.grid[self.y][self.x] == 'food': # if the ant finds food
            self.carrying = True # carries the food
            env.grid[self.y][self.x] = 'empty' # the food is not on the cell anymore
        
    def explore_ph(self, env, p_map):
        pass
    
    def back_nest_bug2(self, env):
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
        elif self.avoiding_obstacle: # Bug2 algo to avoid obstacles
            directions = [(-1,0), (1,0), (0,-1), (0,1), (-1,-1), (1,-1), (1,1), (-1,1)]
            for step_x, step_y in directions:
                if env.is_inside(self.x + step_x, self.y + step_y):
                    if env.grid[self.y + step_y][self.x + step_x]!='obstacle':
                        self.x += step_x
                        self.y += step_y
                        break
            new_dist = math.hypot(self.nest[0] - self.x, self.nest[1] - self.y)
            if new_dist < self.collision_dist:
                self.avoiding_obstacle = False

        if env.grid[self.y][self.x] == 'nest':
            self.carrying = False

    def move(self, env, p_map):
        if not self.carrying:
            self.scan_environment(env, p_map)
            self.explore_rd(env, p_map)
        else:
            self.back_nest_bug2(env)
            p_map.add(self.x, self.y)
            self.scan_environment(env, p_map)
