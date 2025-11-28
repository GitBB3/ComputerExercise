import random as rd

class Ant:
    def __init__(self, nest_x, nest_y):
        self.x, self.y = nest_x, nest_y
        self.nest = [nest_x, nest_y]
    
    def explore_rd(self, env):
        dx, dy = rd.choice([(-1,0), (1,0), (0,-1), (0,1)]) #change the random displacement
        if 0 <= self.x + dx < env.width and 0 <= self.y + dy < env.height and env.grid[self.y + dy][self.x + dx]!='obstacle' :
            self.x = self.x + dx
            self.y = self.y + dy