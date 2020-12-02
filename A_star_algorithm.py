
import math

class location():

    def __init__(self, prev=None, location=None):
        self.location = location
        self.prev = prev
        self.f_n = 0
        self.g_n = 0
        self.h_n = 0

    def gen_avail_moves(self, grid, goal):
        open_space = []
        row = self.location[0]
        column = self.location[1]
        if row-1 > 0 and row >= goal.location[0]:
            if grid[row-1][column] == 0:
                open_space.append((row - 1, column))
        if column-1 > 0 and column > goal.location[1]:
            if grid[row][column-1] == 0:
                open_space.append((row, column - 1))
        if row+1 < len(grid)-1 and row <= goal.location[0]:
            if grid[row+1][column] == 0:
                open_space.append((row + 1, column))
        if column+1 < len(grid[0])-1 and column <= goal.location[1]:
            if grid[row][column+1] == 0:
                open_space.append((row, column + 1))
        return open_space


#calculate the h value - gets the distance between the gaol and current location
def heuristic(neighbor, goal):
    distance = math.sqrt(((goal.location[0]-neighbor.location[0])**2)+((goal.location[1]-neighbor.location[1])**2) )
    return distance;

def a_search(grid, start, goal):
     path = []
     start = location(None, start)
     goal = location(None, goal)
     
     opened = []
     closed = []

     path.append((start.location[0]+1,start.location[1]+1))
     opened.append(start)

     while len(opened) > 0:
        x = opened.pop(0)
        if(x.location == goal.location):
            if len(closed) > 0:
                return path
            else:
                return [x]
        closed.append(x)
        avail_moves = x.gen_avail_moves(grid, goal)
        at_open = -1
        h = []
        for shift in avail_moves:
            at_open = -1
            if shift in opened:
                at_open = opened.index(shift)
            if shift in closed:
                continue
            h.append([heuristic(location(x,shift), goal),shift])
        min = 100
        next = []
        for heur_val in h:
            if heur_val[0] < min:
                min = heur_val[0]
                next = heur_val[1]
        new_location = location(x,next)
        if at_open == -1:
            opened.append(new_location)
            c = opened[at_open]
            new_location.g_n = new_location.prev.g_n + 1
            new_location.h_n = heuristic(new_location, goal)
            new_location.f_n = new_location.g_n + new_location.h_n
            path.append((new_location.location[0]+1, new_location.location[1]+1))
     return [x]
