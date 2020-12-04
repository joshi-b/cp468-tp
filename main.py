from A_star_algorithm import a_search

def main():
    
    rows = 0
    columns = 0
    num_of_robots = 0
    robot_locations = []
    room = []
    goal = (0,0)
    file = ''
    input_type = input("Enter data or file: ")
    if input_type == "file":
        file = input("Enter filename: ")
        f = open(file,"r")
        k = 0
        for i in f:
            if i[:-1] == '\n':
                line = i[:-1]
            else:
                line = i
            if k == 0:
                values = line.split(" ")
                columns = int(values[1])
                rows = int(values[0])
            elif k == 1:
                num_of_robots = int(line) + k
            elif k <= num_of_robots:
                values = line.split(" ")
                x = int(values[1])
                y = int(values[0])
                robot_locations.append((x,y))
            elif k == num_of_robots + 1:
                values = line.split(" ")
                x = int(values[1])
                y = int(values[0])
                goal = (x,y)
            else:
                temp = []
                for j in line:
                    if j != '\n':
                        temp.append(int(j))
                room.insert(0,temp)
            k += 1
    elif input_type == "data":
        try:
            x = int(input("Enter the number of rows: "))
            y = int(input("Enter the number of columns: "))
            num_of_robots = int(input("Enter the number of robots: "))
            for n in range(num_of_robots):
                i = int(input("Enter the row that robot "+str(n+1)+" is in: "))
                j = int(input("Enter the column that robot "+str(n+1)+" is in: "))
                robot_locations.append((j,i))
            goal_x = int(input("Enter the row of the rendezvous point: "))
            goal_y = int(input("Enter the column of the rendezvous point: "))
            goal = (goal_y,goal_x)
            for n in range(x):
                temp = []
                row = input("Enter row "+str(n+1)+":")
                for m in row:
                    temp.append(int(m))
                room.insert(0,temp)
            print('\n')
            print('\n')
        except:
            print('incorrect input')
            return
    else:
        print('not an option')
        return

    robot_num = 0

    print("\nRendezvous Point: " + "(" + str(goal[1]) + "," + str(goal[0]) + ")")
    
    for i in robot_locations:
        path = []
        robot_num+=1



        if room[i[0]][i[1]] == 1:
            print("Robot can not be at an obstacle")
            path = [(i[1],i[0])]
        elif room[goal[0]][goal[1]] == 1:
            print("Rendezvous point is at an obstacle")
            return
        else:
            print("Robot " + str(robot_num) + " at " + "(" + str(i[1]) + "," + str(i[0]) + ")" + " takes the path:")
            path = a_search(room,i,goal)
            
        if path == []:
            print("No path for the robot to take")
            return

        print(path)
        print('\n')

        for j in path:

            x = j[1]
            y = j[0]

            if j == path[-1]:
                room[x][y] = "X"
            elif j == path[0]:
                room[x][y] = "^"
            else:
                room[x][y] = "-"
       
        for k in range(len(room)-1,-1,-1):
            for j in room[k]:
                print (j,end = "")
            print('\n')
        for j in path:

            x = j[1]
            y = j[0]

            room[x][y] = 0
        print('\n')

main()
