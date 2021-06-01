from Cells import main_app
from rules import rule_one,rule_blank,conway_game_rule
import numpy as np

def main():
    my_app = main_app(def_state(),conway_game_rule)

def def_state():
    state = np.full((10,15,3),255)
    for i in range(5):
        for j in range(10):
            state[i+3,j+3] = (0,0,0)
    return state


if __name__ == '__main__':
    main()
