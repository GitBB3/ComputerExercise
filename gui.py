import tkinter as tk

import config as cf
from environment import Environment
from ant import Ant
from pheromone import PheromoneMap

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

####################################################################
######################## GUI class #################################
####################################################################

class SimulationGUI:
    def __init__(self, pmap, ants, env):
        self.pmap = pmap
        self.ants = ants
        self.env = env
        self.duration = 0

        self.over = False
        self.running = False
        self.initialized = False

        self.root = tk.Tk()
        self.root.title("Ant Colony Simulation")

        # Full screen
        self.root.state("zoomed")

        # Top frame
        self.header = tk.Frame(self.root, height=60, bg="#3B1F1F", highlightthickness=2, highlightbackground="#92BC7E")
        self.header.pack(side="top", fill="x")

        header_label = tk.Label(self.header,
                                text = "ANT COLONY OPTIMIZATION",
                                fg = "#92BC7E",
                                bg="#3B1F1F",
                                font=20,
                                highlightthickness=2,
                                highlightbackground="#241010"
                                )
        header_label.pack(padx=20, pady=15, anchor="w")

        self.reset_bt = tk.Button(self.header,
                                  text="RESET",
                                  bg="#3B1F1F",
                                  fg="#92BC7E",
                                  activebackground="#92BC7E",
                                  activeforeground="#3B1F1F",
                                  relief="flat",
                                  width=6,
                                  height=2,
                                  command=self.reset)
        self.reset_bt.pack(side="right")
        self.icon_play="▶"
        self.play_bt = tk.Button(self.header,
                                 text=self.icon_play,
                                 font=10,
                                 bg="#3B1F1F",
                                 fg="#92BC7E",
                                 activebackground="#92BC7E",
                                 activeforeground="#3B1F1F",
                                 relief="flat",
                                 width=4,
                                 height=2,
                                 command=self.toggle)
        self.play_bt.pack(side="right")

        # Body frame
        self.body = tk.Frame(self.root)
        self.body.pack(fill="both", expand=True)
            
        self.sidepot = tk.Frame(self.body, width=50, bg="#241010")
        self.sidepot.pack(side="left", fill="y")
        sidepot_label = tk.Label(self.sidepot,
                 text="MODEL",
                 fg="white",
                 bg="#241010",
                 font=6)
        sidepot_label.pack(padx=10, pady=10)
        def pot_change(value):
            pass # changer la valeur globale
        self.pot = tk.Scale(self.sidepot,
                            from_=1,
                            to=0,
                            resolution=0.05,
                            orient="vertical",
                            command=pot_change,
                            bg="#92BC7E",
                            fg="#241010",
                            troughcolor="#241010",
                            activebackground="#3B1F1F",
                            highlightthickness=0
                            )
        self.pot.pack(fill="y", expand=True, padx=10, pady=10)
    

        self.sidefb = tk.Frame(self.body, width=600, bg="#3B1F1F")
        self.sidefb.pack(side="left", fill="y")

        self.param_frame = tk.Frame(self.sidefb, bg="#92BC7E") # TODO: change the initialization to tk.Entry()
        self.param_frame.pack(side="top", fill="x")
        param_label = tk.Label(self.param_frame,
                 text="PARAMETERS",
                 fg="#3B1F1F",
                 bg="#92BC7E",
                 anchor="w",
                 font=6)
        param_label.pack(fill="x", padx=5)
        # params_label = tk.Label(self.param_frame,
        #          text=f"NB_ANTS: {cf.NB_ANTS}\nPHEROMONES_AMOUNT: {cf.PHEROMONES_AMOUNT}\nEVAPORATION_RATE: {cf.EVAPORATION_RATE}\nDIFFUSION_RATE: {cf.DIFFUSION_RATE}\nNB_FOOD_CLUSTERS: {cf.NB_FOOD_CLUSTERS}\nFOOD_CLUSTER_SIZE: {cf.FOOD_CLUSTER_SIZE}\nNB_OBSTACLES_CLUSTERS: {cf.NB_OBSTACLES_CLUSTERS}\nOBSTACLES_CLUSTER_SIZE: {cf.OBSTACLES_CLUSTER_SIZE}\n",
        #          fg="#3B1F1F",
        #          bg="#92BC7E",
        #          anchor="w",
        #          justify="left")
        # params_label.pack(fill="x", padx=5)
        self.param_entries_frame = tk.Frame(self.param_frame, bg="#92BC7E")
        self.param_entries_frame.pack(fill="x", padx=5)
        self.values = {}
        self.entries = {}
        params = {
                "NB_ANTS" : cf.NB_ANTS,
                "PHEROMONES_AMOUNT" : cf.PHEROMONES_AMOUNT,
                "EVAPORATION_RATE" : cf.EVAPORATION_RATE,
                "DIFFUSION_RATE" : cf.DIFFUSION_RATE,
                "NB_FOOD_CLUSTERS" : cf.NB_FOOD_CLUSTERS,
                "FOOD_CLUSTER_SIZE" : cf.FOOD_CLUSTER_SIZE,
                "NB_OBSTACLES_CLUSTERS" : cf.NB_OBSTACLES_CLUSTERS,
                "OBSTACLES_CLUSTER_SIZE" : cf.OBSTACLES_CLUSTER_SIZE
                }
        for row, (param, value) in enumerate(params.items()):
            tk.Label(self.param_entries_frame, text=param, bg="#92BC7E").grid(row=row, column=0, padx=5, pady=5, sticky="w")
            entry = tk.Entry(self.param_entries_frame)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1)
            self.entries[param] = entry
        self.confirm_bt = tk.Button(self.param_frame, text="CONFIRM and START", command=self.confirm_params, bg="#3B1F1F", fg="#92BC7E")
        self.confirm_bt.pack(padx=2, pady=2)

        self.title_label = tk.Label(self.sidefb,
                                       text=f"FEEDBACK",
                                       fg="white",
                                       bg="#3B1F1F",
                                       font="6",
                                       anchor="w")
        self.title_label.pack(fill="x", padx=5)

        self.duration_label = tk.Label(self.sidefb,
                                       text=f"Duration: {self.duration/1000:.1f} s",
                                       fg="white",
                                       bg="#3B1F1F",
                                       anchor="w")
        self.duration_label.pack(fill="x", padx=5)

        self.distance_label = tk.Label(self.sidefb,
                                       text=f"Distance walked by the ants: {self.env.distance_walked} units",
                                       fg="white",
                                       bg="#3B1F1F",
                                       anchor="w")
        self.distance_label.pack(fill="x", padx=5)

        ## Graphs
        self.fig1 = Figure(figsize=(3,2), dpi=60)
        self.ax1 = self.fig1.add_subplot(111)
        self.ax1.set_title("% of food collected / Time")
        self.ax1.set_facecolor("#EFE6D8")
        self.canva_fig1 = FigureCanvasTkAgg(self.fig1, master=self.sidefb)
        self.widget1 = self.canva_fig1.get_tk_widget()
        self.widget1.pack(fill="x", padx=10, pady=10)
        self.time_history = []
        self.food_percent_history = []

        self.fig2 = Figure(figsize=(3,2), dpi=60)
        self.ax2 = self.fig2.add_subplot(111)
        self.ax2.set_title("Food collected / Time")
        self.ax2.set_facecolor("#EFE6D8")
        self.canva_fig2 = FigureCanvasTkAgg(self.fig2, master=self.sidefb)
        self.widget2 = self.canva_fig2.get_tk_widget()
        self.widget2.pack(fill="x", padx=10, pady=10)
        self.food_history = []

        self.fig3 = Figure(figsize=(3,2), dpi=60)
        self.ax3 = self.fig3.add_subplot(111)
        self.ax3.set_title("Food collected / Pheromones spread")
        self.ax3.set_facecolor("#EFE6D8")
        self.canva_fig3 = FigureCanvasTkAgg(self.fig3, master=self.sidefb)
        self.widget3 = self.canva_fig3.get_tk_widget()
        self.widget3.pack(fill="x", padx=10, pady=10)
        self.pheromone_history = []

        self.sim_frame = tk.Frame(self.body, bg="#241010")
        self.sim_frame.pack(fill="both", expand=True)
        self.cv_label = tk.Label(self.sim_frame,
                                       text=f"ANTS ENVIRONMENT",
                                       fg="white",
                                       bg="#241010",
                                       font="6",
                                       anchor="w")
        self.cv_label.pack(fill="x", padx=5)
        self.canvas = tk.Canvas(self.sim_frame,
                    width=self.env.width*cf.CELL,
                    height=self.env.height*cf.CELL,
                    bg="#3B1F1F")
        self.canvas.pack(expand=True)

    def confirm_params(self):
        self.values["NB_ANTS"] = int(self.entries["NB_ANTS"].get())
        self.values["PHEROMONES_AMOUNT"] = float(self.entries["PHEROMONES_AMOUNT"].get())
        self.values["EVAPORATION_RATE"] = float(self.entries["EVAPORATION_RATE"].get())
        self.values["DIFFUSION_RATE"] = float(self.entries["DIFFUSION_RATE"].get())
        self.values["NB_FOOD_CLUSTERS"] = int(self.entries["NB_FOOD_CLUSTERS"].get())
        self.values["FOOD_CLUSTER_SIZE"] = float(self.entries["FOOD_CLUSTER_SIZE"].get())
        self.values["NB_OBSTACLES_CLUSTERS"] = int(self.entries["NB_OBSTACLES_CLUSTERS"].get())
        self.values["OBSTACLES_CLUSTER_SIZE"] = float(self.entries["OBSTACLES_CLUSTER_SIZE"].get())

        self.param_entries_frame.pack_forget()
        self.confirm_bt.pack_forget()

        self.params_label = tk.Label(self.param_frame,
                 text=f"NB_ANTS: {self.values['NB_ANTS']}\nPHEROMONES_AMOUNT: {self.values['PHEROMONES_AMOUNT']}\nEVAPORATION_RATE: {self.values['EVAPORATION_RATE']}\nDIFFUSION_RATE: {self.values['DIFFUSION_RATE']}\nNB_FOOD_CLUSTERS: {self.values['NB_FOOD_CLUSTERS']}\nFOOD_CLUSTER_SIZE: {self.values['FOOD_CLUSTER_SIZE']}\nNB_OBSTACLES_CLUSTERS: {self.values['NB_OBSTACLES_CLUSTERS']}\nOBSTACLES_CLUSTER_SIZE: {self.values['OBSTACLES_CLUSTER_SIZE']}\n",
                 fg="#3B1F1F",
                 bg="#92BC7E",
                 anchor="w",
                 justify="left")
        self.params_label.pack(fill="x", padx=5)

        self.env = Environment(cf.GRID_W, cf.GRID_H, 
                      cf.NEST_W, cf.NEST_H, 
                      self.values["NB_FOOD_CLUSTERS"], self.values["FOOD_CLUSTER_SIZE"], 
                      self.values["NB_OBSTACLES_CLUSTERS"], self.values["OBSTACLES_CLUSTER_SIZE"], 
                      cf.MIN_OBJ, cf.MAX_OBJ)
        self.ants = [Ant(self.env.nest[1], self.env.nest[0], Environment(cf.GRID_W,cf.GRID_H,cf.NEST_W,cf.NEST_H,self.values["NB_FOOD_CLUSTERS"],self.values["FOOD_CLUSTER_SIZE"],self.values["NB_OBSTACLES_CLUSTERS"],self.values["OBSTACLES_CLUSTER_SIZE"],cf.MIN_OBJ,cf.MAX_OBJ), self.pmap) for _ in range(self.values["NB_ANTS"])]

        self.initialized = True

    def toggle(self, event=None):
        if self.over:
            return
        if self.initialized:
            self.running = not self.running
            if self.icon_play=="▶":
                self.icon_play="⏸"
                self.play_bt.config(text="⏸")
            elif self.icon_play=="⏸":
                self.icon_play="▶"
                self.play_bt.config(text="▶")
            if self.running:
                self.step()
    
    def step(self):
        """
        Update the simulation.
        """
        self.pmap.evaporate()
        self.pmap.diffuse()
        for ant in self.ants:
            ant.move_on_memory(self.env, self.pmap, self.pot.get())

        self.duration += cf.SPEED

        if self.env.food_collected == self.env.food_total: # end the simulation
            self.over = True 
            self.running = False

        self.draw()
        self.update_feedback()
        self.update_graphs()

        if self.running:
            self.root.after(cf.SPEED, self.step)
    
    def pheromone_color(self, p, max_p): #note: becomes very bright when every potential is very low
            return"#{:02x}{:02x}{:02x}".format(*[int(a+(b-a)*(p/max_p if max_p else 0))for a,b in zip((59,31,31),(224,48,48))]) # just a color interpolation

    def update_feedback(self):
        self.duration_label.config(text=f"Duration: {self.duration/1000:.1f} s")
        self.distance_label.config(text=f"Distance walked by the ants: {self.env.distance_walked} units")

    def update_graphs(self):
        percent = 100 * self.env.food_collected / self.env.food_total if self.env.food_total > 0 else 0
        total_pheromones = sum(sum(row) for row in self.pmap.pmap)
        time_s = self.duration / 1000
        self.food_history.append(self.env.food_collected)
        self.food_percent_history.append(percent)
        self.time_history.append(time_s)
        self.pheromone_history.append(total_pheromones)

        self.ax1.clear()
        self.ax1.set_title("% of food collected / Time")
        self.ax1.set_facecolor("#EFE6D8")
        self.ax1.set_ylim(0,100)
        self.ax1.plot(self.time_history, self.food_percent_history)
        self.canva_fig1.draw_idle()

        self.ax2.clear()
        self.ax2.set_title("Food collected / Time")
        self.ax2.set_facecolor("#EFE6D8")
        self.ax2.plot(self.time_history, self.food_history)
        self.canva_fig2.draw_idle()

        self.ax3.clear()
        self.ax3.set_title("Food collected / Pheromones spread")
        self.ax3.set_facecolor("#EFE6D8")
        self.ax3.plot(self.pheromone_history, self.food_history) # might have to print the ratio along time
        self.canva_fig3.draw_idle()



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
                self.canvas.create_rectangle(ant.x*cf.CELL+cf.CELL//3, ant.y*cf.CELL+cf.CELL//3, (ant.x+1)*cf.CELL-cf.CELL//3, (ant.y+1)*cf.CELL-cf.CELL//3, fill="#3B1F1F", outline="")
            else:
                self.canvas.create_rectangle(ant.x*cf.CELL, ant.y*cf.CELL, (ant.x+1)*cf.CELL, (ant.y+1)*cf.CELL, fill="yellow", outline="")
                self.canvas.create_rectangle(ant.x*cf.CELL+cf.CELL//3, ant.y*cf.CELL+cf.CELL//3, (ant.x+1)*cf.CELL-cf.CELL//3, (ant.y+1)*cf.CELL-cf.CELL//3, fill="green", outline="")

    def reset(self):
        self.running = False
        self.over = False
        self.initialized = False
        self.icon_play = "▶"
        self.play_bt.config(text="▶")
        self.duration = 0
        self.duration_label.config(text=f"Duration: {self.duration} s")
        self.distance_label.config(text=f"Distance walked by the ants: {self.env.distance_walked}")
        self.canvas.delete("all")
        
        self.time_history.clear()
        self.food_history.clear()
        self.food_percent_history.clear()
        self.pheromone_history.clear()
        self.ax1.clear()
        self.ax1.set_title(" of food collected / Time")
        self.ax1.set_facecolor("#EFE6D8")
        self.canva_fig1.draw_idle()
        self.ax2.clear()
        self.ax2.set_title("Food collected / Time")
        self.ax2.set_facecolor("#EFE6D8")
        self.canva_fig2.draw_idle()
        self.ax3.clear()
        self.ax3.set_title("Food collected / Pheromones spread")
        self.ax3.set_facecolor("#EFE6D8")
        self.canva_fig3.draw_idle()

        self.params_label.pack_forget()
        self.param_entries_frame.pack(fill="x", padx=5)
        self.confirm_bt.pack(padx=2, pady=2)

        self.pmap = PheromoneMap(cf.GRID_W, cf.GRID_H)

    def run(self):
        self.root.mainloop()