from A_star_algorithm import a_search
import pygame, sys
import os
import time

def main():
    print('\n')
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
        if not os.path.exists(file_name):
            print("File not Found")
            return
        file = open(file_name,"r")
        
        # initialize variable to keep track of what line we are at in the file
        line_number = 0

        # loop through each line in the file
        for i in file:
            # check if the line has a new line character at the end, remove character if it does
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
            # if at the line after robot coordinates are done, extract rendezvous coordinates and save in variable
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
                    # keep track of how many open spaces available in row
                    if character!='\n' and int(character) == 0:
                        count+=1
                room.insert(0,temp_row)
                # if only 1 open space is available in a row, add to array to keep track of it
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
                    # keep track of how many open spaces available in row
                    if m == 0:
                        count+=1
                room.insert(0,temp)
                # if only 1 open space is available in a row, add to array to keep track of it
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

    # initialize variables to keep track of the time, completion status and room size
    start_time = time.time()
    total = 0
    complete = False
    size = 0

    # determine size according to room for visually outputting the grid
    if len(room) >= 100 and len(room) <= 500:
        size = 4
    elif len(room) >= 50 and len(room) < 100:
        size = 10
    elif len(room) >= 20 and len(room) <50:
        size = 25
    elif len(room) > 0 and len(room) < 20:
        size = 50
    elif len(room) > 500:
        size = 0
    else:
        print("invalid size")
    print("Putting results in a file")

    # initialize a variable to hold which robot's path we are determining
    robot_num = 0
    # check if there is an existing output.txt file
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    f = open("output.txt","x")
    # print out rendezvous point of this room
    f.write("Rendezvous Point: " + "(" + str(goal[1]) + "," + str(goal[0]) + ")\n\n")
    print(("Rendezvous Point: " + "(" + str(goal[1]) + "," + str(goal[0]) + ")\n"))
    # for each robot, determine it's path and output it
    for i in robots_start:

        # initialize an array to hold robot's path and increment robot number
        path = []
        robot_num+=1

        # check if robot start position is an obstacle, if it is, let user know
        if room[i[0]][i[1]] == 1:
            f.write("Robot can not be at an obstacle\n\n")
            print("Robot can not be at an obstacle\n")
            path = [(i[1],i[0])]
        # check if rendezvous point is an obstacle, if it is, let user know
        elif room[goal[0]][goal[1]] == 1:
            f.write("Rendezvous point is at an obstacle\n\n")
            print("\nRendezvous point is at an obstacle\n")
            return
        # if robot and rendezvous point not an obstacle, determine robot's path
        else:
            f.write("\nRobot " + str(robot_num) + " at " + "(" + str(i[1]) + "," + str(i[0]) + ")" + " takes the path:\n\n")
            print("Robot " + str(robot_num) + " at " + "(" + str(i[1]) + "," + str(i[0]) + ")" + " takes the path:\n")
            # perform a* search algorithm to determine robot's path
            path, r_path, moves = a_search(room,i,goal,one_opening)

        # if path output empty, let user know
        if path == []:
            f.write("No path for the robot to take\n\n")
            print("No path for the robot to take\n")
            continue

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

        # output the robot's path to terminal and file
        f.write(str(path)+'\n\n')
        print(str(path) + '\n')

        # output the robot's time to terminal and file
        f.write("--- Time for Robot " +str(robot_num) + " run in seconds: %s ---\n\n" % (time.time() - start_time))
        print("--- Time for Robot " +str(robot_num) + " run in seconds: %s ---\n" % (time.time() - start_time))

        # output the robot's step count to terminal and file
        f.write("--- Number of steps taken by Robot " +str(robot_num) +": " + str(moves[-1]) + " ---\n\n")
        print("--- Number of steps taken by Robot " +str(robot_num) +": " + str(moves[-1]) + " ---\n")

        # add robot's time to total overall time
        total = total + (time.time() - start_time)

        # loop through each row of the room and output it with the changes made above for clear visual of robot's path
        for k in range(len(room)-1,-1,-1):
            line = ''
            for j in room[k]:
                line+=str(j)
            f.write(line)
            f.write('\n')

        # loop through each coordinate in path and change output back to 0 (prep room for next robot)
        for j in path:
            x = j[1]
            y = j[0]
            room[x][y] = 0
    
    # output total time to terminal and file
    f.write("--- Time for Robots in total in seconds: %s ---\n\n" % total)
    print("--- Time for Robots in total in seconds: %s ---\n" % total)

    # output the file path to terminal
    print("Please find results in "+ os.path.dirname(os.path.abspath("output.txt"))+"\output.txt after you close the program\n")

    # if room size is feasible to animate
    if size > 0:

        # initialize colours
        blue = (0,0,255)
        red = (255,0,0)
        green = (0,255,0)
        yellow = (250,234,17)
        white = (255,255,255)
        gray = (128,128,128)
        purple = (153,51,255)
        margin = 5

        # print out the legend for the animation
        print('-----------------------------------------')
        print("LEGEND FOR ANIMATION:")
        print(" Green square is the rendezvous point")
        print(" Robot 1 is blue")
        print(" Robot 2 is red")
        print(" Robot 3 is purple")
        print(" Robot 4 is yellow")
        print('-----------------------------------------')
        print('\n')

        # start animation
        pygame.init()
        screen = pygame.display.set_mode((1000,1000),0,32)
        pygame.display.set_caption('Path_Planning Group 4')
        clock = pygame.time.Clock()
        length = 0

        # while path of robot not complete
        while not complete:
            # if window is closed then close window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    complete = True
                    break
            if complete:
                break
            for path in r_path:
                if len(path) > length:
                    length = len(path)
            symbol = [blue,red,purple,yellow]

            # add obstacles and open spaces to visual
            for row in range(len(room)-1,-1,-1):
                for column in range(len(room[row])):
                    if room[row][column] == 1:
                        pygame.draw.rect(screen, white, [(margin+size)*(column)+size,(margin+size)*(len(room)-row)+margin,size,size])
                    elif row == goal[0] and column == goal[1]:
                        pygame.draw.rect(screen, green, [(margin+size)*(column)+size,(margin+size)*(len(room)-row)+margin,size,size])
                    else:
                        pygame.draw.rect(screen, gray, [(margin+size)*(column)+size,(margin+size)*(len(room)-row)+margin,size,size])
           
            # if window is closed then close window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    complete = True
                    break
            if complete:
                break
            clock.tick(60)
            pygame.display.flip()

            # loop through each step
            for t in range(length):
                s = 0
                # loop through each robot
                for r in range(len(robots_start)):

                    # for each robot, make the visual change for next step
                    if t < len(r_path[r]):
                        pygame.draw.rect(screen,symbol[s],[(margin+size)*r_path[r][t][0]+size,(margin+size)*(len(room)-r_path[r][t][1])+margin,size,size])
                    
                    # delay visual change for ease of viewing
                    if size > 5:
                        pygame.time.delay(50)
                    else:
                        pygame.time.delay(20)
                    
                    # if window is closed then close window
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            complete = True
                            break
                    if complete:
                        break
                    pygame.display.update()
                    s+=1
        pygame.display.quit()
        pygame.quit()
    else:

        # if animation not possible for room size, output info message
        print(" The room is too big for the animation. Please view results in the output file")
        print('\n')

# run the main function of the program
main()
