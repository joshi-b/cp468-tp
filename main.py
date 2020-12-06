from A_star_algorithm import a_search

def main():

    # initialize variables to hold room dimensions and an array to hold room details
    rows = 0
    columns = 0
    room = []

    # initialize variables to hold number of robots, robot start locations and rendezvous point
    robot_numbers = 0
    robots_start = []
    one_opening = []
    goal = (0,0)

    file = ''

    # ask user for type of input
    input_type = input("Enter data or file: ")

    # if input type is file, extract details from the file
    if input_type == "file":
        file_name = input("Enter filename: ")
        file = open(file_name,"r")

        # initialize variable to keep track of what line we are at in the file
        line_number = 0

        # loop through each line in the file
        for i in file:
            # chcek if  the line has a new line character at the end, remove character if it does
            if i[:-1] == '\n':
                line = i[:-1]
            else:
                line = i
            # if at first line of the file, extract room dimensions and save in variables
            if line_number == 0:
                info = line.split(" ")
                columns = int(info[1])
                rows = int(info[0])
            # if at second line of the file, extract number of robots and save in variable
            elif line_number == 1:
                robot_numbers = int(line) + 1  #add 1 to account for line number
            # while at a line containing robot start coordinates, extract coordinates and add to robot start locations array
            elif line_number <= robot_numbers:
                info = line.split(" ")
                x = int(info[1])
                y = int(info[0])
                robots_start.append((x,y))
            # if at the line after robot coordinates are done, extract rendezvous coordinates and save in varaiable
            elif line_number == robot_numbers + 1:
                info = line.split(" ")
                x = int(info[1])
                y = int(info[0])
                goal = (x,y)
            # if at a room details line, extract each character in line and save in a temp array, then add temp array to room details array
            else:
                temp_row = []
                count = 0
                for character in line:
                    if character != '\n':
                        temp_row.append(int(character))
                    if character!='\n' and int(character) == 0:
                        count+=1
                room.insert(0,temp_row)
                if count == 1:
                    one_opening.append(line_number-robot_numbers-2)
            # increment line number of file
            line_number += 1

    # if input type is data, prompt user for details
    elif input_type == "data":
        try:
            # prompt user for room dimensions and number of robots
            x = int(input("Enter the number of rows: "))
            y = int(input("Enter the number of columns: "))
            robot_numbers = int(input("Enter the number of robots: "))
            # for each robot, prompt user for robot's start coordinates and add to robot start locations array
            for n in range(robot_numbers):
                j = int(input("Enter the column that robot "+str(n+1)+" is in: "))
                i = int(input("Enter the row that robot "+str(n+1)+" is in: "))
                robots_start.append((i,j))
            # prompt user for rendezvous coordinates
            goal_y = int(input("Enter the column of the rendezvous point: "))
            goal_x = int(input("Enter the row of the rendezvous point: "))
            goal = (goal_x,goal_y)
            # prompt user for room details per row
            for n in range(x):
                temp = []
                row = input("Enter row "+str(n+1)+":")
                count=0
                for m in row:
                    temp.append(int(m))
                    if m == 0:
                        count+=1
                room.insert(0,temp)
                if count == 1:
                    one_opening.append(n)
            print('\n')
            print('\n')
        except:
            print('incorrect input')
            return
    # if input type not valid, tell user
    else:
        print('not an option')
        return

    # initialize a variable to hold which robot's path we are determining
    robot_num = 0

    # print out rendezvous point of this room
    print("\nRendezvous Point: " + "(" + str(goal[1]) + "," + str(goal[0]) + ")")

    # for each robot, determine it's path and output it
    for i in robots_start:

        # initialize an array to hold robot's path and increment robot number
        path = []
        robot_num+=1

        # check if robot start position is an obstacle, if it is, let user know
        if room[i[0]][i[1]] == 1:
            print("Robot can not be at an obstacle")
            path = [(i[1],i[0])]
        # check if rendezvous point is an obstacle, if it is, ler user know
        elif room[goal[0]][goal[1]] == 1:
            print("Rendezvous point is at an obstacle")
            return
        # if robot and rendezvous point not an obstacle, determine robot's path
        else:
            print("Robot " + str(robot_num) + " at " + "(" + str(i[1]) + "," + str(i[0]) + ")" + " takes the path:")
            # perform a star search algorithm to determine robot's path
            path = a_search(room,i,goal,one_opening)

        # if path output empty, let user know
        if path == []:
            print("No path for the robot to take")
            continue

        # print out the path output for the robot
        print(path)
        print('\n')

        # loop through each coordinate of the path and change it's output for clear visual
        for j in path:

            # determine coordinates
            x = j[1]
            y = j[0]

            # if coordinates are the last step of the path (meaning the rendezvous point), change its output to X
            if j == path[-1]:
                room[x][y] = "X"
            # if coordinates are the first step of the path (meaning the start position), change its output to ^
            elif j == path[0]:
                room[x][y] = "^"
            # for any other steps in the path, change its output to -
            else:
                room[x][y] = "-"

        # loop through each row of the room and output it with the changes made above for clear visual of robot's path
        for k in range(len(room)-1,-1,-1):
            for j in room[k]:
                print (j,end = "")
            print('\n')

        # loop through each coordinate in path and change output back to 0 (prep room for next robot)
        for j in path:
            x = j[1]
            y = j[0]
            room[x][y] = 0

        print('\n')

# run the main function of the program
main()
