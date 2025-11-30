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
        self.duration = 0
        ### Window for ACO
        self.root = tk.Tk()
        self.root.title("Ant Colony Simulation")
        self.canvas = tk.Canvas(
             self.root, width=env.width*cf.CELL, height=env.height*cf.CELL, bg="black"
        )
        self.canvas.pack()
        ### Interface window
        self.info_window = tk.Toplevel(self.root)
        self.info_window.title("ACO Feedback")
        self.info_window.geometry("400x100")
        self.info_window.configure(bg="#A9F7E3")
        self.info_label = tk.Label(self.info_window, text="Press <space> to START.", justify="left", anchor="nw", font=("Consolas",10), bg="#000000", fg="#A9F7E3")
        self.info_label.pack(fill="both", expand="True", padx=10, pady=10)

        self.running = False
        self.over = False
        self.root.bind("<space>", self.toggle)

        self.draw()

    def toggle(self, event=None):
        if self.over:
            return
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
            ant.move_on_memory(self.env, self.pmap)

        self.duration += cf.SPEED

        if self.env.food_collected == self.env.food_total: # end the simulation
            self.over = True 
            self.running = False

        self.draw()
        self.update_feedback()

        if self.running:
            self.root.after(cf.SPEED, self.step)

    def run(self):
        self.root.mainloop()

    def pheromone_color(self, p, max_p): #note: becomes very bright when every potential is very low
            intensity = int((p/max_p)*255)
            return f"#{intensity:02x}0000"

    def update_feedback(self):
        info_text = (f"Duration (s): {self.duration/1000}\n"
                     f"Units of food collected: {self.env.food_collected}/{self.env.food_total}\n"
                     f"Distance walked by ants (distance units): {self.env.distance_walked}\n"
                     f"Running: {self.running} (Press <space> to PAUSE)\n"
                     f"Completed: {self.over}")
        self.info_label.config(text=info_text)

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

        for ant in self.ants: # Differentiate ants carrying food or not
            if not ant.carrying:
                self.canvas.create_rectangle(ant.x*cf.CELL, ant.y*cf.CELL, (ant.x+1)*cf.CELL, (ant.y+1)*cf.CELL, fill="yellow", outline="")
                self.canvas.create_rectangle(ant.x*cf.CELL+cf.CELL//3, ant.y*cf.CELL+cf.CELL//3, (ant.x+1)*cf.CELL-cf.CELL//3, (ant.y+1)*cf.CELL-cf.CELL//3, fill="black", outline="")
            else:
                self.canvas.create_rectangle(ant.x*cf.CELL, ant.y*cf.CELL, (ant.x+1)*cf.CELL, (ant.y+1)*cf.CELL, fill="yellow", outline="")
                self.canvas.create_rectangle(ant.x*cf.CELL+cf.CELL//3, ant.y*cf.CELL+cf.CELL//3, (ant.x+1)*cf.CELL-cf.CELL//3, (ant.y+1)*cf.CELL-cf.CELL//3, fill="green", outline="")