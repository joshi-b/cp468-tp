from A_star_algorithm import a_search

def main():
    #opening input file
    fv = open("input.txt","r")
    
    #defining variables to make the grid
    cols = 0
    rows = 0
    num_of_robots = 0
    robot_locations = []
    grid = []
    end = (0,0)
    
    
    #going through file and extracting data
    x = 0
    for i in fv:
        if i[:-1] == '\n':
            z = i[:-1]
        else:
            z = i
        #cols and rows
        if x == 0:
            values = z.split(" ")
            rows = int(values[1])
            cols = int(values[0])
        #number of robots
        elif x == 1:
            num_of_robots = int(z) + x
        #locations of robot
        elif x <= num_of_robots:
            values = z.split(" ")
            a = int(values[0])-1
            b = int(values[1])-1
            robot_locations.append((a,b))
        elif x == num_of_robots + 1:
            values = z.split(" ")
            a = int(values[0])-1
            b = int(values[1])-1
            end = (a,b)
        else:
            temp_grid = []
            for j in z:
                if j != '\n':
                    temp_grid.append(int(j))
            grid.append(temp_grid)
        x += 1
         
    robot_num = 0
    for i in robot_locations:
        robot_num+=1
        path = a_search(grid,i,end)
        print("Robot " + str(robot_num) + " at " + str(i[0]+1) + "," + str(i[1]+1) + " takes the path:")
        print(path)
        new_grid = grid
        for j in path:
            x = j[0]
            y = j[1]
            if j == path[-1]:
                grid[-x][y] = "!"
            else:
                grid[-x][y] = "-"
        for i in grid:
            print()
            for j in i:
                print (j,end = "")
        for j in path:
            x = j[0]
            y = j[1]
            grid[-x][y] = 0
        print('\n')

main()