import curses
import time
import random
from sys import exit

screen = curses.initscr()
screen.keypad(1)
dims = screen.getmaxyx()
score = 0


def maze():
    curses.start_color()
    curses.initscr()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_WHITE, curses.COLOR_BLACK)
    c_1 = curses.color_pair(1)
    c_3 = curses.color_pair(3)
    c_4 = curses.color_pair(4)

    for i in range(4, 9):
        screen.addstr(i, 7, "█", c_3)  # head1
    for i in range(12, 18):
        screen.addstr(i, 7, "█", c_3)
    for i in range(4, 9):
        screen.addstr(i, 26, "█", c_3)
    for i in range(12, 18):
        screen.addstr(i, 26, "█", c_3)
    for i in range(7, 27):
        screen.addstr(4, i, "█", c_3)
    for i in range(7, 27):
        screen.addstr(17, i, "█", c_3)
    for i in range(12, 15):
        screen.addstr(7, i, "█", c_3)  # eyes
    for i in range(19, 22):
        screen.addstr(7, i, "█", c_3)
    for i in range(12, 15):
        screen.addstr(8, i, "█", c_3)
    for i in range(19, 22):
        screen.addstr(8, i, "█", c_3)
    for i in range(11, 23):
        screen.addstr(14, i, "█", c_3)  # mouth
    for i in range(12, 15):
        screen.addstr(i, 11, "█", c_3)
    for i in range(12, 15):
        screen.addstr(i, 22, "█", c_3)
    for i in range(4, 9):
        screen.addstr(i, 45, "█", c_4)  # head2
    for i in range(12, 18):
        screen.addstr(i, 45, "█", c_4)
    for i in range(4, 9):
        screen.addstr(i, 64, "█", c_4)
    for i in range(12, 18):
        screen.addstr(i, 64, "█", c_4)
    for i in range(45, 64):
        screen.addstr(4, i, "█", c_4)
    for i in range(45, 64):
        screen.addstr(17, i, "█", c_4)
    for i in range(50, 53):
        screen.addstr(7, i, "█", c_4)  # eyes
    for i in range(57, 60):
        screen.addstr(7, i, "█", c_4)
    for i in range(50, 53):
        screen.addstr(8, i, "█", c_4)
    for i in range(57, 60):
        screen.addstr(8, i, "█", c_4)
    for i in range(49, 61):
        screen.addstr(14, i, "█", c_4)  # mouth
    for i in range(12, 15):
        screen.addstr(i, 49, "█", c_4)
    for i in range(12, 15):
        screen.addstr(i, 60, "█", c_4)


def game():
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    screen.nodelay(1)
    head = [2, 2]  # snake head
    body = [head[:]]*5  # snake body
    screen.border()
    direction = 0
    gameover = False
    food_made = False
    death = False
    deadcell = body[-1][:]
    f = open("snake.txt", "r")  # highscore txt
    text = f.readline()
    life = 3

    while not gameover:
        screen.refresh()
        score = len(body)-5  # score is calculated from the lenght of the snake
        screen.addstr(0, 1, " Score: " + str(score) + " ")
        title = 'Snake Game'
        screen.addstr(0, (curses.COLS - len(title)) // 2, title)
        screen.addstr(0, 12, " Highscore: " + str(text) + " ")
        screen.addstr(0, 65, " Life: " + "💛 "*life + " ")
        if score > int(text):  # stores the score in the highscore list
            with open("snake.txt", "w")as output:
                output.write(str(score))
        while not food_made:  # checks if there are food on the screen, if not, it creates one
            y, x = random.randrange(1, dims[0]-1), random.randrange(1, dims[1]-1)
            if screen.inch(y, x) == ord(" "):
                food_made = True
                screen.addch(y, x, ord("*"))
        while not death:  # checks if there are traps on the screen, if not, it creates some
            for i in range(1, 10):
                y, x = random.randrange(1, dims[0]-1), random.randrange(1, dims[1]-1)
                if screen.inch(y, x) == ord(" "):
                    death = True
                    screen.addch(y, x, ord("@"))

        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], " ")
        screen.addch(head[0], head[1], 'o', curses.color_pair(2))

        action = screen.getch()  # controls
        if action == curses.KEY_UP and direction != 1:
            direction = 3
        elif action == curses.KEY_DOWN and direction != 3:
            direction = 1
        elif action == curses.KEY_RIGHT and direction != 2:
            direction = 0
        elif action == curses.KEY_LEFT and direction != 0:
            direction = 2
        if direction == 0:
            head[1] += 1
        elif direction == 2:
            head[1] -= 1
        elif direction == 1:
            head[0] += 1
        elif direction == 3:
            head[0] -= 1

        deadcell = body[-1][:]
        for z in range(len(body)-1, 0, -1):
            body[z] = body[z-1]

        body[0] = head[:]  # checks what the snake encounters
        if screen.inch(head[0], head[1]) != ord(" "):
            if screen.inch(head[0], head[1]) == ord("*"):
                food_made = False
                body.append(body[-1])
            elif screen.inch(head[0], head[1]) == ord("@"):
                life = life - 1
                death = False
                if life == 0:
                    gameover = True
            else:
                gameover = True
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        if score <= 5:  # modifies speed based on the score
            speed = 0.15
        elif score > 5 and score < 12:
            speed = 0.10
        elif score >= 12:
            speed = 0.08
        time.sleep(speed)
    screen.clear()
    screen.nodelay(0)
    message1 = "Game Over! You're a loser."
    message2 = "You got " + str(len(body)-5) + " points."
    message3 = "Press space to play again."
    message4 = "Press the red (ESC) button and rest in peace."
    screen.addstr(10, (curses.COLS - len(message1)) // 2, message1)
    screen.addstr(11, (curses.COLS - len(message2)) // 2, message2)
    screen.addstr(13, (curses.COLS - len(message3)) // 2, message3)
    screen.addstr(14, (curses.COLS - len(message4)) // 2, message4)
    screen.refresh()
    q = 0
    while q not in [32, 27]:  # gameover screen
        q = screen.getch()
    if q == 32:
        screen.clear()
        maze()
        game()
    elif q == 27:
        curses.endwin()
        exit()

    screen.getch()
maze()
game()
curses.endwin()
