import tkinter as tk

import config as cf

####################################################################
######################## GUI class #################################
####################################################################

class SimulationGUI:
    def __init__(self, env, ants, pmap):
        self.env = env
        self.ants = ants
        self.pmap = pmap
        self.root = tk.Tk()
        self.root.title("Ant Colony Simulation")
        self.canvas = tk.Canvas(
             self.root, width=env.width*cf.CELL, height=env.height*cf.CELL, bg="black"
        )
        self.canvas.pack()
        self.running = False
        self.root.bind("<space>", self.toggle)

        self.draw()

    def toggle(self, event=None):
        self.running = not self.running
        if self.running:
            self.step()

    def step(self):
        """
        Update the simulation.
        """
        self.pmap.evaporate()
        self.pmap.diffuse()
        for ant in self.ants:
            ant.move(self.env, self.pmap)

        self.draw()

        if self.running:
            self.root.after(cf.SPEED, self.step)

    def run(self):
        self.root.mainloop()

    def pheromone_color(self, p, max_p): #note: becomes very bright when every potential is very low
            intensity = int((p/max_p)*255)
            return f"#{intensity:02x}0000"

    def draw(self):
        """
        Display the simulation.
        """
        self.canvas.delete("all") #clear the window
        
        max_pheromone = max(max(row) for row in self.pmap.pmap)
        if max_pheromone > 0.0:
            for y in range(self.pmap.height): # plot the pheromones
                for x in range(self.pmap.width):
                    p = self.pmap.pmap[y][x]
                    if p > 0.0:
                        color = self.pheromone_color(p, max_pheromone)
                        self.canvas.create_rectangle(x*cf.CELL, y*cf.CELL, (x+1)*cf.CELL, (y+1)*cf.CELL, fill=color, outline="")
        
        for y in range(self.env.height): #plot the food and obstacles
            for x in range(self.env.width):
                type_obj = self.env.grid[y][x]
                if type_obj=='food':
                    color='green'
                    self.canvas.create_rectangle(x*cf.CELL, y*cf.CELL, (x+1)*cf.CELL, (y+1)*cf.CELL, fill=color, outline="")
                elif type_obj=='obstacle':
                    color='orange'
                    self.canvas.create_rectangle(x*cf.CELL, y*cf.CELL, (x+1)*cf.CELL, (y+1)*cf.CELL, fill=color, outline="")
                elif type_obj=='nest':
                    color='blue'
                    self.canvas.create_rectangle(x*cf.CELL, y*cf.CELL, (x+1)*cf.CELL, (y+1)*cf.CELL, fill=color, outline="")

        for ant in self.ants:
            self.canvas.create_rectangle(ant.x*cf.CELL, ant.y*cf.CELL, (ant.x+1)*cf.CELL, (ant.y+1)*cf.CELL, fill="yellow", outline="")
