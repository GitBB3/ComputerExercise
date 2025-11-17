from environment import Environment
from gui import SimulationGUI
import config as cf

def main():
    env = Environment(cf.GRID_W, cf.GRID_H, cf.NB_FOOD_CLUSTERS, cf.FOOD_CLUSTER_SIZE, cf.NB_OBSTACLES_CLUSTERS, cf.OBSTACLES_CLUSTER_SIZE, cf.MIN_OBJ, cf.MAX_OBJ)
    gui = SimulationGUI(env)
    gui.run()

if __name__ == "__main__":
    main()