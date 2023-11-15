import time
import random
import curses
from curses import wrapper

def start_screen(stdsrc):
    stdsrc.clear()
    stdsrc.addstr(1, 2, "WELCOME TO THE SPEED TYPING TEST", curses.color_pair(1))
    stdsrc.addstr("\n  Press any key to begin!")
    stdsrc.refresh()
    stdsrc.getkey()

def display_text(stdsrc, target, current, wpm = 0):
    stdsrc.addstr(target)
    stdsrc.addstr(1, 0, f"WPM: {wpm}")

    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)

        if char != correct_char:
            color = curses.color_pair(2)

        stdsrc.addstr(0, i, char, color)

def load_text():
    with open("text.txt", "r") as f:
        lines = f.readlines()

        return random.choice(lines).strip()

def wpm_test(stdsrc):
    target_text = load_text()
    current_text = []
    wpm = 0
    start_time = time.time()

    stdsrc.nodelay(True)

    while True:
        time_elapsed = max(time.time() - start_time, 1)
        wpm = round((len(current_text) / (time_elapsed / 60)) / 5)

        stdsrc.clear()
        display_text(stdsrc, target_text, current_text, wpm)            
        stdsrc.refresh()

        if "".join(current_text) == target_text:
            stdsrc.nodelay(False)
            break

        try:
            key =  stdsrc.getkey()
        except:
            continue

        if ord(key) == 27:
            break

        if key in ("KEY_BACKSPACE", "\b", "\x7f"):
            if len(current_text > 0):
                current_text.pop()
        elif len(current_text) < len(target_text):
            current_text.append(key)
 

def main(stdsrc):
    # initial color for text and background in terminal
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    start_screen(stdsrc)

    while True:
        wpm_test(stdsrc)

        stdsrc.addstr(2, 0, "You completed the text! Press any key...")
        key = stdsrc.getkey()

        if ord(key) == 27:
            break

wrapper(main)