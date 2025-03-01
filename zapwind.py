import curses
import os
from tkinter import Tk
from tkinter.filedialog import asksaveasfilename

text = ""
filename = ""
theme = "dark"

def display(stdscr, show_shortcuts=False):
    global text, theme
    stdscr.clear()

    if theme == "light":
        stdscr.bkgd(' ', curses.color_pair(1))
    else:
        stdscr.bkgd(' ', curses.color_pair(2))

    height, width = stdscr.getmaxyx()
    stdscr.addstr(height - 2, 0, "  Zapwind ^_^ Hey!", curses.color_pair(15))

    lines = text.split("\n")
    for i, line in enumerate(lines):
        if i < height - 3:
            stdscr.addstr(i, 0, f"{i + 1:3} ", curses.color_pair(4))
            stdscr.addstr(i, 4, line)

    if show_shortcuts:
        shortcuts = [
            "1231",
            "12311",
        ]
        stdscr.addstr(height - 1, 0, "Shortcuts:", curses.color_pair(3))
        for i, shortcut in enumerate(shortcuts):
            stdscr.addstr(height - 1 + i + 1, 0, shortcut)

    stdscr.refresh()

def save_file(file_name):
    global text
    with open(file_name, 'w') as f:
        f.write(text)

def open_file(file_name):
    global text
    with open(file_name, 'r') as f:
        text = f.read()

def new_file():
    global text, filename
    text = ""
    filename = ""

def switch_theme():
    global theme
    theme = "dark" if theme == "light" else "light"

def backspace():
    global text
    text = text[:-1]

def delete():
    global text
    if len(text) > 0:
        text = text[1:]

def save_as():
    root = Tk()
    root.withdraw()
    file_path = asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
        save_file(file_path)

def main(stdscr):
    global text, filename
    curses.curs_set(1)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(4, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    show_shortcuts = False

    while True:
        display(stdscr, show_shortcuts)
        key = stdscr.getch()

        if key == 17:
            save_as()
        elif key == 15:
            file_name = input("Enter file name to open: ")
            if os.path.exists(file_name):
                open_file(file_name)
                filename = file_name
            else:
                stdscr.addstr(5, 0, "File does not exist!")
        elif key == 19:
            if filename:
                save_file(filename)
            else:
                save_as()
        elif key == 14:
            new_file()
        elif key == 20:
            switch_theme()
        elif key == 3:
            show_shortcuts = not show_shortcuts
        elif key == 27:
            break
        elif key == 10:
            text += '\n'
        elif key == 8:
            backspace()
        elif key == 330:
            delete()
        elif key >= 32 and key <= 126:
            text += chr(key)

if __name__ == "__main__":
    curses.wrapper(main)
