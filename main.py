from A_star_algorithm import a_search

def main():
    cols = 0
    rows = 0
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
                rows = int(values[1])
                cols = int(values[0])
            elif k == 1:
                num_of_robots = int(line) + k
            elif k <= num_of_robots:
                values = line.split(" ")
                x = int(values[0])-1
                y = int(values[1])-1
                robot_locations.append((x,y))
            elif k == num_of_robots + 1:
                values = line.split(" ")
                x = int(values[0])-1
                y = int(values[1])-1
                goal = (x,y)
            else:
                temp = []
                for j in line:
                    if j != '\n':
                        temp.append(int(j))
                room.append(temp)
            k += 1
    elif input_type == "data":
        try:
            x = int(input("Enter the number of rows: "))
            y = int(input("Enter the number of columns: "))
            num_of_robots = int(input("Enter the number of robots: "))
            for n in range(num_of_robots):
                i = int(input("Enter the row that robot "+str(n+1)+" is in: "))-1
                j = int(input("Enter the column that robot "+str(n+1)+" is in: "))-1
                robot_locations.append((i,j))
            goal_x = int(input("Enter the row of the rendezvous point: "))-1
            goal_y = int(input("Enter the column of the rendezvous point: "))-1
            goal = (goal_x,goal_y)
            for n in range(x):
                temp = []
                row = input("Enter row "+str(n+1)+":")
                for m in row:
                    temp.append(int(m))
                room.append(temp)
            print('\n')
            print('\n')
        except:
            print('incorrect input')
            return
    else:
        print('not an option')
        return
    robot_num = 0
    print("Rendezvous Point: " + "(" + str(goal[0]+1) + "," + str(goal[1]+1) + ")")
    for i in robot_locations:
        robot_num+=1
        path = a_search(room,i,goal)
        print("Robot " + str(robot_num) + " at " + "(" + str(i[0]+1) + "," + str(i[1]+1) + ")" + " takes the path:")
        print(path)
        new_grid = room
        for j in path:
            x = j[0]
            y = j[1]
            if j == path[-1]:
                room[-x][y] = "!"
            else:
                room[-x][y] = "-"
        for i in room:
            print('\n'
            for j in i:
                print (j,end = "")
        for j in path:
            x = j[0]
            y = j[1]
            room[-x][y] = 0
        print('\n')

main()
