from Cells import main_app
from rules import functions
import numpy as np
import json

def main():
    state,function = def_state()
    my_app = main_app(state,function)

def def_state():
    with open("config.json") as f:
        config = json.load(f)

    rows = config['size'][0]
    cols = config['size'][1]
    
    state = np.full((rows,cols,3),255)

    #color individual ones
    individuals = config['initial-state']['individual']
    for _ in individuals:
        #I want to count from 1 not 0 in the grid
        state[_[0]-1,_[1]-1] = (0,0,0)

    #color range ones
    
    row_data_collective = config['initial-state']['range']['rows']
    col_data_collective = config['initial-state']['range']['cols']
    total_items = len(row_data_collective)
    
    if total_items > 0:
        for i in range(total_items):
            row_data,col_data = row_data_collective[i],col_data_collective[i]
            if len(row_data) >0 and len(col_data)>0:
                state[row_data[0]-1:row_data[1],col_data[0]-1:col_data[1]] = (0,0,0)
            elif len(row_data) >0:
                state[row_data[0]-1:row_data[1]] = (0,0,0)             
            elif len(col_data)>0:                
                state[:,col_data[0]-1:col_data[1]]= (0,0,0)


    function = functions[config['function']]
    return state,function
                
if __name__ == '__main__':
    main()
