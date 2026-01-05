from environment import Environment
from ant import Ant
from pheromone import PheromoneMap
from gui import SimulationGUI
from config_w import ConfigWindow
import config as cf

def main():
    cfw = ConfigWindow()
    cf.NB_ANTS = cfw.values["NB_ANTS"]
    cf.PHEROMONES_AMOUNT = cfw.values["PHEROMONES_AMOUNT"]
    cf.EVAPORATION_RATE = cfw.values["EVAPORATION_RATE"]
    cf.DIFFUSION_RATE = cfw.values["DIFFUSION_RATE"]
    cf.NB_FOOD_CLUSTERS = cfw.values["NB_FOOD_CLUSTERS"]
    cf.FOOD_CLUSTER_SIZE = cfw.values["FOOD_CLUSTER_SIZE"]
    cf.NB_OBSTACLES_CLUSTERS = cfw.values["NB_OBSTACLES_CLUSTERS"]
    cf.OBSTACLES_CLUSTER_SIZE = cfw.values["OBSTACLES_CLUSTER_SIZE"]


    env = Environment(cf.GRID_W, cf.GRID_H, 
                      cf.NEST_W, cf.NEST_H, 
                      cf.NB_FOOD_CLUSTERS, cf.FOOD_CLUSTER_SIZE, 
                      cf.NB_OBSTACLES_CLUSTERS, cf.OBSTACLES_CLUSTER_SIZE, 
                      cf.MIN_OBJ, cf.MAX_OBJ)  
    ants = [Ant(env.nest[1], env.nest[0], Environment(cf.GRID_W,cf.GRID_H,cf.NEST_W,cf.NEST_H,cf.NB_FOOD_CLUSTERS,cf.FOOD_CLUSTER_SIZE,cf.NB_OBSTACLES_CLUSTERS,cf.OBSTACLES_CLUSTER_SIZE,cf.MIN_OBJ,cf.MAX_OBJ), PheromoneMap(cf.GRID_W, cf.GRID_H)) for _ in range(cf.NB_ANTS)]
    pmap = PheromoneMap(cf.GRID_W, cf.GRID_H)
    gui = SimulationGUI(env, ants, pmap)
    gui.run()

if __name__ == "__main__":
    main()  