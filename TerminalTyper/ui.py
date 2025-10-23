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
    

def typing_test(stdscr):
    """
    Runs the main typing test loop.
    """
    # Generate the text the user needs to type
    prompt_text = generate_prompt(WORDS, num_words=20)
    current_text = []
    start_time = None
    
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    while True:
        # Prepare the screen for redraw
        stdscr.erase()

        # Display the prompt text
        display_text(stdscr, prompt_text, "".join(current_text), 2, 0)
        
        # Display simple instructions
        stdscr.addstr(4, 0, "Press 'Esc' to exit.", curses.color_pair(3))

        # Refresh the screen to show changes
        stdscr.refresh()

        # Check if the user has completed the text
        if "".join(current_text) == prompt_text:
            break

        # Wait for user input (non-blocking)
        # Using nodelay(True) makes getch non-blocking, but we want to wait for a key.
        # use the default blocking mode.
        key = stdscr.getch()

        # Start the timer on the very first keypress
        if start_time is None:
            start_time = time.time()
        
        # Handle keypresses
        if key == 27: # 27 is the key code for ESC
            break
        # 127 is a common key code for Backspace
        elif key in (curses.KEY_BACKSPACE, 127):
            if len(current_text) > 0:
                current_text.pop()
        # Ensure the key is a valid character to be typed
        elif 32 <= key <= 126: # ASCII range for printable characters
            current_text.append(chr(key))