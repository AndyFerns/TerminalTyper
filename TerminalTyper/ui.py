import curses
import time
from .core import WORDS, generate_prompt, wpm_calculator, acc_calculator

def display_text(stdscr, target, current, y, x):
    """
    Displays the target text and the user's current text with color-coded feedback.
    Green for correct chars, Red for incorrect, and default for the rest.
    """
    # Add target text characters with appropriate colors
    for i, char in enumerate(target):
        color = curses.color_pair(1) # Green for correct
        if i < len(current):
            if current[i] != target[i]:
                color = curses.color_pair(2) # Red for incorrect
        stdscr.addstr(y, x + i, char, color)

    # Display a blinking cursor at the current typing position
    cursor_y, cursor_x = y, x + len(current)
    stdscr.move(cursor_y, cursor_x)