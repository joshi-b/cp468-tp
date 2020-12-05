
import math

# initialize arrays to hold blocked, open and closed coordinates(positions)
blocked = []
opened = []
closed = []


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

    def gen_avail_moves(self, grid, goal):
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
        if row-1 > 0 :
            # if neighbour position is not an obstacle, add to available spaces array
            if grid[row-1][column] == 0 and (row - 1, column) not in blocked:
                open_space.append((row - 1, column))

        # check if move left is possible
        if column-1 > 0 :
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
        return open_space


#calculate the h value - gets the distance between the goal and current location
def heuristic(neighbor, goal):
    distance = math.sqrt(((goal.location[0]-neighbor.location[0])**2)+((goal.location[1]-neighbor.location[1])**2))
    return distance

def a_search(grid, start, goal):

    # initialize array to hold the robot's path
     path = []

     # initialize location of start position and rendezvous point
     start = location(None, start)
     goal = location(None, goal)
     
     # add start position to path and opened array
     path.append((start.location[1],start.location[0]))
     opened.append(start)
    
    
    # loop through until opened is not empty
     while len(opened) > 0:
        
        # get current position
        x = opened.pop(0)

        # if current position is rendezvous point, return path of the robot
        if(x.location == goal.location):
            if len(closed) > 0:
                return path
            else:
                return [x]
        
        # determine available moves for current position
        avail_moves = x.gen_avail_moves(grid, goal)
        
        if avail_moves == [] or (len(avail_moves) == 1 and x.prev!= None and avail_moves[0] == x.prev.location):
            x = x.prev
            path.pop(-1)
            if closed == []:
                return []
            opened.append(x)
            closed.remove(x)
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
            h.append([heuristic(location(x,shift), goal),shift])
        closed.append(x)
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
            path.append((new_location.location[1], new_location.location[0]))
     return [x.location]
