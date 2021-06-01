def isalive(cell):
    return cell[0]==0

def isdead(cell):
    return cell[0]==255

def rule_one(current_state):
    new_state = current_state.copy()
    rows,cols,useless = current_state.shape
    for i in range(rows):
        for j in range(cols):
            if j >0:                
                if isdead(current_state[i,j-1]):
                    new_state[i, j] = (255,255,255);
    return new_state

def rule_blank(current_state):
    return current_state


def conway_game_rule(current_state):
    new_state = current_state.copy()
    rows,cols,useless = current_state.shape
    for i in range(0,rows):
        for j in range(0,cols):
            #handle middle cells
            neighbors = get_neighbors_count(current_state,i,j,rows,cols)
            if isalive(current_state[i,j]):
                if not(neighbors==2 or neighbors ==3):
                    new_state[i,j] = (255,255,255)                    
            else:
                if neighbors==3:
                    new_state[i,j] = (0,0,0)
    return new_state


def get_neighbors_count(current_state,i,j,rows,cols):
    alive = 0
    for m in range(i-1,i+2):
        for n in range(j-1,j+2):
            if not(m==i and n==j):
                #edge cases are checked. All neighbors not in the grid around edge cases are supposed dead.
                if not(m==-1 or n==-1 or m == rows or n==cols):
                    if isalive(current_state[m,n]):
                        alive+=1

    return alive
    
    
