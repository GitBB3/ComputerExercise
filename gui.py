import tkinter as tk

import config as cf

####################################################################
######################## GUI class #################################
####################################################################

class SimulationGUI:
    def __init__(self, env):
        self.env = env
        self.root = tk.Tk()
        self.root.title("Ant Colony Simulation")
        self.canvas = tk.Canvas(
             self.root, width=env.width*cf.CELL, height=env.height*cf.CELL, bg="black"
        )
        self.canvas.pack()
        self.draw()
        
    def run(self):
        self.root.mainloop()

    def draw(self):
        pass