import curses
import time
import random
from sys import exit

screen = curses.initscr()
screen.keypad(1)
dims = screen.getmaxyx()
score = 0
#life = [' 💛 ', ' 💛 ', ' 💛 ']


def maze():
    curses.start_color()
    curses.initscr()
    curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)

    for i in range(8, 17):  # penis
        screen.addstr(i, 22, "█")
    for i in range(22, 27):
        screen.addstr(8, i, "█")
    for i in range(29, 43):
        screen.addstr(8, i, "█")
    for i in range(46, 68):
        screen.addstr(8, i, "█")
    for i in range(22, 32):
        screen.addstr(17, i, "█")
    for i in range(34, 50):
        screen.addstr(17, i, "█")
    for i in range(52, 68):
        screen.addstr(17, i, "█")
    for i in range(8, 12):
        screen.addstr(i, 68, "█")
    for i in range(14, 18):
        screen.addstr(i, 68, "█")
    for i in range(15, 18):
        screen.addstr(i, 26, "█")
    for i in range(13, 18):
        screen.addstr(i, 36, "█")
    for i in range(8, 12):
        screen.addstr(i, 48, "█")
    for i in range(8, 12):
        screen.addstr(i, 61, "█")
    for i in range(13, 18):
        screen.addstr(i, 57, "█")
    for i in range(54, 58):
        screen.addstr(13, i, "█")


def game():
    curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
    screen.nodelay(1)
    head = [1, 1]
    body = [head[:]]*5
    screen.border()
    direction = 0
    gameover = False
    foodmade = False
    death = False
    deadcell = body[-1][:]
    f = open("snake.txt", "r")
    text = f.readline()
    life = 3

    while not gameover:
        screen.refresh()
        score = len(body)-5
        screen.addstr(0, 1, " Score: " + str(score) + " ")
        title = 'Snake Game'
        screen.addstr(0, (curses.COLS - len(title)) // 2, title)
        screen.addstr(0, 12, " Highscore: " + str(text) + " ")
        screen.addstr(0, 49, " Life:" + str(life))
        if score > int(text):
            with open("snake.txt", "w")as output:
                output.write(str(score))
        while not foodmade:
            y, x = random.randrange(1, dims[0]-1), random.randrange(1, dims[1]-1)
            if screen.inch(y, x) == ord(" "):
                foodmade = True
                screen.addch(y, x, ord("*"))
        while not death:
            for i in range(1, 3):
                y, x = random.randrange(1, dims[0]-1), random.randrange(1, dims[1]-1)
                if screen.inch(y, x) == ord(" "):
                    death = True
                    screen.addch(y, x, ord("@"))

        if deadcell not in body:
            screen.addch(deadcell[0], deadcell[1], " ")
        screen.addch(head[0], head[1], 'o', curses.color_pair(2))

        action = screen.getch()
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

        body[0] = head[:]
        if screen.inch(head[0], head[1]) != ord(" "):
            if screen.inch(head[0], head[1]) == ord("*"):
                foodmade = False
                body.append(body[-1])
            elif screen.inch(head[0], head[1]) == ord("@"):
                life = life - 1
                death = False
                screen.addstr(0, 49, " Life: " + str(life))
                screen.refresh()
                if life == 0:
                    gameover = True
            else:
                gameover = True
        screen.move(dims[0]-1, dims[1]-1)
        screen.refresh()
        if score <= 5:
            speed = 0.13
        elif score > 5 and score < 12:
            speed = 0.08
        elif score >= 12:
            speed = 0.01
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
    while q not in [32, 27]:
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
