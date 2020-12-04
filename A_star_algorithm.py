
import math
blocked = []
opened = []
closed = []
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
        if row-1 > 0 :
            if grid[row-1][column] == 0 and (row - 1, column) not in blocked:
                open_space.append((row - 1, column))
        if column-1 > 0 :
            if grid[row][column-1] == 0 and (row, column-1) not in blocked:
                open_space.append((row, column - 1))
        if row+1 < len(grid) :
            if grid[row+1][column] == 0 and (row + 1, column) not in blocked:
                open_space.append((row + 1, column))
        if column+1 < len(grid[0]) :
            if grid[row][column+1] == 0 and (row, column + 1) not in blocked:
                open_space.append((row, column + 1))
        if open_space == []:
            blocked.append((row,column))
        else:
            for s in open_space:
                for c in closed:
                    if c.location == s:
                        blocked.append((row,column))
        print(self.location)
        print(open_space)
        return open_space


#calculate the h value - gets the distance between the gaol and current location
def heuristic(neighbor, goal):
    distance = math.sqrt(((goal.location[0]-neighbor.location[0])**2)+((goal.location[1]-neighbor.location[1])**2))
    return distance;

def a_search(grid, start, goal):
     path = []
     start = location(None, start)
     goal = location(None, goal)
     
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
        if avail_moves == [] or (len(avail_moves) == 1 and x.prev!= None and avail_moves[0] == x.prev.location):
            print("backtrack")
            closed.remove(x)
            x = x.prev
            if closed == []:
                return []
            opened.append(x)
            closed.remove(x)
            print(x.location)
            continue
            
        at_open = -1
        h = []
        for shift in avail_moves:
            at_open = -1
            in_close = False
            for o in opened:
                if o.location == shift:
                    at_open = opened.index(shift)
            for c in closed:
                if c.location == shift:
                    in_close = True
                    continue
            if in_close == False:
                h.append([heuristic(location(x,shift), goal),shift])
        min = 100
        next = []
        for heur_val in h:
            if heur_val[0] < min:
                min = heur_val[0]
                next = heur_val[1]
            elif heur_val == min:
                if heur_val[0][1] == next[1]:
                    if (goal.location[0] - heur_val[0][0]) < (goal.location[0] - next[0]):
                        next = heur_val[1]
                elif heur_val[0][0] == next[0]:
                    if (goal.location[1] - heur_val[0][1]) < (goal.location[1] - next[1]):
                        next = heur_val[1]
        new_location = location(x,next)
        if at_open == -1:
            opened.append(new_location)
            c = opened[at_open]
            new_location.g_n = new_location.prev.g_n + 1
            new_location.h_n = heuristic(new_location, goal)
            new_location.f_n = new_location.g_n + new_location.h_n
            path.append((new_location.location[0]+1, new_location.location[1]+1))
     return [x.location]
