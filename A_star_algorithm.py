
import math

# initialize arrays to hold blocked, open and closed coordinates(positions)
opened = []
closed = []
r_path = []

class location():

    def __init__(self, prev=None, location=None):
        """
        -------------------------------------------------------
        Initializes a node (coordinate) having a location within
        room
        -------------------------------------------------------
        Parameters:
        prev - coordinates of the last position in the room
        location - coordinates represeting current position 
                   in the room
        -------------------------------------------------------
        """

        # coordinates of the current position in room
        self.location = location

        # coordinates of the last position (from where current position was reached) in room
        self.prev = prev

        # f,g,h value (a star algorithm) of the current position in the room
        self.f_n = 0
        self.g_n = 0
        self.h_n = 0

    def gen_avail_moves(self, grid, goal, blocked):
        """
        --------------------------------------------------------------
        Determines open spaces available around current position
        (where move can be made and has no obstacles)
        --------------------------------------------------------------
        Parameters:
        grid - array holding room details
        goal - coordinates of rendezvous point

        Returns:
        open_space - an array holding all open spaces (available moves)
                     around current position
        ---------------------------------------------------------------
        """ 
        # initialize array to hold available moves (open spaces)
        open_space = []
        # get coordinates of current positon
        row = self.location[0]
        column = self.location[1]

        # check if move down is possible
        if row-1 >= 0 :
            # if neighbour position is not an obstacle, add to available spaces array
            if grid[row-1][column] == 0 and (row - 1, column) not in blocked:
                open_space.append((row - 1, column))

        # check if move left is possible
        if column-1 >= 0 :
            # if neighbour position is not an obstacle, add to available spaces array
            if grid[row][column-1] == 0 and (row, column-1) not in blocked:
                open_space.append((row, column - 1))

        # check if move up is possible
        if row+1 < len(grid) :
            # if neighbour position is not an obstacle, add to available spaces array
            if grid[row+1][column] == 0 and (row + 1, column) not in blocked:
                open_space.append((row + 1, column))

        # check if move right is possible
        if column+1 < len(grid[0]) :
            # if neighbour position is not an obstacle, add to available spaces array
            if grid[row][column+1] == 0 and (row, column + 1) not in blocked:
                open_space.append((row, column + 1))

        # if no open space available, add coordinates to the blocked array    
        if open_space == []:
            blocked.append((row,column))

        else:
            for s in open_space:
                for c in closed:
                    if c.location == s:
                        blocked.append((row,column))
        # return available open spaces for current position
        return open_space,blocked


#calculate the h value - gets the distance between the goal and current location
def heuristic(neighbor, goal):
    distance = math.sqrt(((goal.location[0]-neighbor.location[0])**2)+((goal.location[1]-neighbor.location[1])**2))
    return distance

def a_search(grid, start, point, one_opening):
    
    # initialize array to hold the robot's path
     path = []
     blocks = []
     i=0

     # initialize location of start position and rendezvous point
     start = location(None, start)
     goal = location(None, point)
         
     # add start position to path and opened array
     path.append((start.location[1],start.location[0]))
     opened.append(start)
    
    
    # loop through until opened is not empty
     while len(opened) > 0:
        
        # get current position
        x = opened.pop(0)

        # if current position is rendezvous point, return path of the robot
        if(x.location == point):
            if len(closed) > 0:
                r_path.append(path)
                return path, r_path
            else:
                r_path.append(path)
                return [x], r_path
        
        # determine available moves for current position
        avail_moves, new_block = x.gen_avail_moves(grid, goal, blocks)
        blocks.append(new_block)
        if avail_moves == [] or (len(avail_moves) == 1 and x.prev!= None and avail_moves[0] == x.prev.location):
            x = x.prev
            path.pop(-1)
            if closed == []:
                return [], r_path
            opened.append(x)
            closed.remove(x)
            continue
        else:
            for p in r_path:
                if p!=[] and i < len(p):
                    if p[i] in avail_moves and p[i]!=(point[0],point[1]):
                         avail_moves.pop(avail_moves.index(p[i]))
            if avail_moves == []:
                new_location = location(x,x)
                opened.append(new_location)
                c = opened[at_open]
                new_location.g_n = new_location.prev.g_n + 1
                new_location.h_n = heuristic(new_location, goal)
                new_location.f_n = new_location.g_n + new_location.h_n
                path.append((new_location.location[1], new_location.location[0]))
                i+=1
                continue
            
        at_open = -1
        h = []

        # loop through all available moves
        for shift in avail_moves:
            at_open = -1
            in_close = False

            # determine if an available move is in the opened array
            for o in opened:
                if o.location == shift:
                    at_open = opened.index(shift)
            # determine if an available move is in the closed array
            for c in closed:
                if c.location == shift:
                    in_close = True
                    continue
            # calculate the h value for the available move
            for o in range(len(one_opening)-1,-1,-1):
                if shift[0] <= (len(grid)-one_opening[o]):
                    goal.location = ((len(grid)-one_opening[o]),grid[(len(grid)-one_opening[o])-1].index(0))
                    break
                else:
                    goal.location = (point[0],point[1])
            h.append([heuristic(location(x,shift), goal),shift])
        closed.append(x)
        # determine which available move is the best option
        min = 100000000000000000000000000000000000000000000
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

        # calculate the g, h and f values for this position
        if at_open == -1:
            opened.append(new_location)
            c = opened[at_open]
            new_location.g_n = new_location.prev.g_n + 1
            new_location.h_n = heuristic(new_location, goal)
            new_location.f_n = new_location.g_n + new_location.h_n
            path.append((new_location.location[1], new_location.location[0]))
            i+=1
     r_path.append(path)
     return [x.location], r_path
