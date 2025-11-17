from environment import Environment
from gui import SimulationGUI
import config as cf

def main():
    env = Environment(cf.GRID_W, cf.GRID_H)
    gui = SimulationGUI(env)
    gui.run()

if __name__ == "__main__":
    main()