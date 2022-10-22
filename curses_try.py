import curses
import time

def run_prog(screen):
#    stdscr = curses.initscr()
#    screen = stdscr.subwin(23, 79, 0, 0)
    screen.box()
    screen.addstr(5,5, "This is my first string")

    x = 0
    screen.addstr(7,5, "count is")
    while 1 :
        x += 1
        xstr = str(x)
        screen.addstr(7,5, "count is")
        screen.addstr(7,14, xstr)
        screen.refresh()
        time.sleep(1)
    

curses.wrapper(run_prog)
