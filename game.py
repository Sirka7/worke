import time
import curses
import random


def init_curses():
    stdscr = curses.initscr()
    stdscr.keypad(1)
    curses.noecho()
    curses.cbreak()
    curses.curs_set(False)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_BLUE, curses.COLOR_BLACK)
    return stdscr
    

class SnakeGame:

    def __init__(self):
        self.snakemap = []
        self.direc = [0, 1]
        self.create_map()
        self.pause = False
        
    def start(self, ic):
        self.stdscr = ic
        self.stdscr.nodelay(1)
        self.print_map()
        self.loop()

    def create_map(self):  # Erstellen der Map
        snakemap = self.snakemap
        f = open('map.py', 'r')

        for line in f:
            row = []
            line = line[:-1]
            for c in line:
                if c == ' ':
                    row.append(4)
                else:
                    row.append(1)
            snakemap.append(row)


    def print_map(self):   # Zeichnen der Map
        stdscr = self.stdscr
        stdscr.clear()
        snakemap = self.snakemap
        
        for a, line in enumerate(snakemap):
            for b, item in enumerate(line):
                if item == 1:
                    stdscr.addch(a, b, ord("X"), curses.color_pair(1))
                elif item == 4:
                    stdscr.addch(a, b, ord(" "))
                elif item == 3:
                    stdscr.addch(a, b, ord("x"))
        while True:
            starty = random.randint(1, len(snakemap)-1)
            startx = random.randint(1, len(snakemap[0])-1)
            if snakemap[starty][startx] == 4:
                stdscr.addch(starty, startx, ord("x"), curses.color_pair(3))
                snakemap[starty][startx] = 3
                break
     
        stdscr.refresh()


    def direction(self):
        stdscr = self.stdscr
        while True:
            newkey = stdscr.getch()
            if newkey == -1:
                break
            key = newkey
            if key == curses.KEY_UP or key == ord("w"):
                self.direc = [-1, 0]
            elif key == curses.KEY_DOWN or key == ord("s"):
                self.direc = [1, 0]
            elif key == curses.KEY_RIGHT or key == ord("d"):
                self.direc =  [0, 1]
            elif key == curses.KEY_LEFT or key == ord("a"):
                self.direc =  [0, -1]
            elif key == ord(" "):
                self.pause = True




    def loop(self):
        pxy = (10, 5)
        key = None
        snake = [[10, 5],]
        highscore = 0
        stdscr = self.stdscr
        snakemap = self.snakemap

            
        while True:
            
            while self.pause:
                stdscr.nodelay(0)
                while True:
                    pause = stdscr.getch()

                    if pause == ord(" "):
                        self.pause = False
                        stdscr.nodelay(1)
                        time.sleep(0.5)
                        break
                                    
            self.direction()
            direc = self.direc
                        
            pxy = (direc[0] + pxy[0], direc[1] + pxy[1])
            stdscr.addch(pxy[0], pxy[1], ord("O"), curses.color_pair(2))
            snake.append(pxy)
            val = snakemap[pxy[0]][pxy[1]]


            if val == 1: 
                stdscr.addstr(6, 3, "Ende, du hast {} Punkte erreicht!".format(highscore))
                stdscr.refresh()
                break
                
            elif val == 2: 
                stdscr.addstr(6, 2, "Ende, du hast dich mit {} Punkten gefressen!".format(highscore))
                stdscr.refresh()
                break
                        
                        
            elif val == 3:
                snakemap[pxy[0]][pxy[1]] = 2
                while True:
                    new_y = random.randint(1, len(snakemap)-1)
                    new_x = random.randint(1, len(snakemap[0])-1)
                    if snakemap[new_y][new_x] == 4:
                        snakemap[new_y][new_x] = 3
                        break

                stdscr.addch(new_y, new_x, ord("x"), curses.color_pair(3))
                highscore += 9
                stdscr.addstr(len(snakemap)+1, 2, "Du hast {} Punkte!".format(highscore))
                stdscr.refresh()
         
            elif val == 4:
                snakemap[pxy[0]][pxy[1]] = 2
                end_y, end_x = snake[0]
                stdscr.addch(end_y, end_x, ord(" "))
                snakemap[end_y][end_x] = 4
                del snake[0]
                stdscr.refresh()

            if direc[1] == 0:
                time.sleep(0.16)
            else:
                time.sleep(0.13)



def restart(ic):
    stdscr = ic
    stdscr.nodelay(0)
    while True:
        exit = stdscr.getch()

        if exit == ord("n"):
            return True
        elif exit == ord("q"):
            return False 
    
    
try:
    ic = init_curses()
    while True:
        game = SnakeGame()
        game.start(ic)
        if not restart(ic):
            break

finally:
    curses.endwin()


    
