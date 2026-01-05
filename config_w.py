import tkinter as tk
import config as cf

class ConfigWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Simulation Parameters")
        self.root.geometry("300x300")
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
            tk.Label(self.root, text=param).grid(row=row, column=0, padx=10, pady=5, sticky="w")
            entry = tk.Entry(self.root)
            entry.insert(0, str(value))
            entry.grid(row=row, column=1, padx=10, pady=5)
            self.entries[param] = entry
        
        tk.Button(self.root, text="CONFIRM and START", command=self.validate).grid(row=row+2, column=0, columnspan=2, pady=20)
        self.root.mainloop()
    
    def validate(self):
        self.values["NB_ANTS"] = int(self.entries["NB_ANTS"].get())
        self.values["PHEROMONES_AMOUNT"] = float(self.entries["PHEROMONES_AMOUNT"].get())
        self.values["EVAPORATION_RATE"] = float(self.entries["EVAPORATION_RATE"].get())
        self.values["DIFFUSION_RATE"] = float(self.entries["DIFFUSION_RATE"].get())
        self.values["NB_FOOD_CLUSTERS"] = int(self.entries["NB_FOOD_CLUSTERS"].get())
        self.values["FOOD_CLUSTER_SIZE"] = float(self.entries["FOOD_CLUSTER_SIZE"].get())
        self.values["NB_OBSTACLES_CLUSTERS"] = int(self.entries["NB_OBSTACLES_CLUSTERS"].get())
        self.values["OBSTACLES_CLUSTER_SIZE"] = float(self.entries["OBSTACLES_CLUSTER_SIZE"].get())

        self.root.destroy()