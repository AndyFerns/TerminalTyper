import curses
import time
from .core import WORDS, generate_prompt, acc_calculator, wpm_calculator

# --- Color Palette Constants for easy reference ---
COLOR_DEFAULT = 1
COLOR_CORRECT = 2
COLOR_INCORRECT = 3
COLOR_CURSOR = 4
COLOR_HEADER = 5

def display_header(stdscr):
    """Displays the application header."""
    title = "--- TerminalTyper ---"
    h, w = stdscr.getmaxyx()
    x = w // 2 - len(title) // 2
    stdscr.addstr(0, x, title, curses.color_pair(COLOR_HEADER) | curses.A_BOLD)

def display_menu(stdscr, menu, current_row_idx):
    """Displays the main menu for mode selection."""
    stdscr.erase()
    display_header(stdscr) # Add header to menu screen
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(COLOR_CORRECT))
            stdscr.addstr(y, x, f"> {row} <")
            stdscr.attroff(curses.color_pair(COLOR_CORRECT))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def display_text(stdscr, target, current, y, x):
    """
    Displays the target text with color-coded feedback and a block cursor.
    """
    # Draw the text to be typed
    for i, char in enumerate(target):
        color = curses.color_pair(COLOR_DEFAULT)
        if i < len(current):
            color = curses.color_pair(COLOR_CORRECT) if current[i] == target[i] else curses.color_pair(COLOR_INCORRECT)
        stdscr.addstr(y, x + i, char, color)

    # --- NEW: Draw a block cursor on the current character ---
    # This replaces the default blinking cursor for a cleaner look.
    if len(current) < len(target):
        stdscr.addstr(y, x + len(current), target[len(current)], curses.color_pair(COLOR_CURSOR))

def display_results(stdscr, results):
    """Displays the final results in a formatted box."""
    stdscr.erase()
    display_header(stdscr)
    h, w = stdscr.getmaxyx()
    
    title = "--- Results ---"
    stdscr.addstr(h//2 - 3, w//2 - len(title)//2, title, curses.A_BOLD)
    
    wpm_str = f"WPM: {results['wpm']:.2f}"
    stdscr.addstr(h//2 - 1, w//2 - len(wpm_str)//2, wpm_str)
    
    acc_str = f"Accuracy: {results['accuracy']:.2f}%"
    stdscr.addstr(h//2, w//2 - len(acc_str)//2, acc_str)
    
    time_str = f"Time: {results['time']:.2f}s"
    stdscr.addstr(h//2 + 1, w//2 - len(time_str)//2, time_str)
    
    prompt = "Press any key to continue..."
    stdscr.addstr(h//2 + 3, w//2 - len(prompt)//2, prompt, curses.A_DIM)
    
    stdscr.refresh()
    stdscr.getch()

def typing_test(stdscr, num_words):
    """Runs the main typing test loop and returns the results."""
    curses.curs_set(0) # Hide the default blinking cursor
    prompt_text = generate_prompt(WORDS, num_words=num_words)
    current_text = []
    start_time = 0.0
    wpm = 0

    while True:
        if start_time != 0:
            elapsed_time = max(time.time() - start_time, 1)
            wpm = wpm_calculator(prompt_text, "".join(current_text), elapsed_time)
        accuracy = acc_calculator(prompt_text, "".join(current_text))

        stdscr.erase()
        display_header(stdscr)
        
        # Display live stats
        stats_str = f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%"
        stdscr.addstr(2, 1, stats_str)
        
        # Display the prompt and user input
        display_text(stdscr, prompt_text, "".join(current_text), 5, 1)
        
        # Display instructions
        instructions = "Tab to restart | Esc to exit"
        stdscr.addstr(7, 1, instructions, curses.A_DIM)
        
        stdscr.refresh()

        if "".join(current_text) == prompt_text:
            break

        key = stdscr.getch()
        if start_time == 0:
            start_time = time.time()
        
        if key == 27: return None
        if key == 9: return None
        elif key in (curses.KEY_BACKSPACE, 127):
            if len(current_text) > 0:
                current_text.pop()
        elif 32 <= key <= 126 and len(current_text) < len(prompt_text):
            current_text.append(chr(key))
    
    curses.curs_set(1) # Show the cursor again for the menu
    return {"wpm": wpm, "accuracy": accuracy, "time": time.time() - start_time}

def main(stdscr):
    """The main function that orchestrates the application flow."""
    # --- NEW: Define all our colors upfront ---
    curses.init_pair(COLOR_DEFAULT, curses.COLOR_WHITE, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CORRECT, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(COLOR_INCORRECT, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(COLOR_CURSOR, curses.COLOR_BLACK, curses.COLOR_WHITE) # Black text on white bg
    curses.init_pair(COLOR_HEADER, curses.COLOR_CYAN, curses.COLOR_BLACK)

    menu = ["10 Words", "20 Words", "50 Words", "Exit"]
    word_counts = [10, 20, 50, -1]
    current_row_idx = 0

    while True:
        curses.curs_set(0) # Hide cursor in menu
        display_menu(stdscr, menu, current_row_idx)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if word_counts[current_row_idx] == -1:
                break
            
            # --- Countdown Logic (slightly improved centering) ---
            stdscr.erase()
            display_header(stdscr)
            for i in range(3, 0, -1):
                start_msg = f"Starting in {i}..."
                h, w = stdscr.getmaxyx()
                stdscr.addstr(h//2, w//2 - len(start_msg)//2, start_msg)
                stdscr.refresh()
                time.sleep(1)
            
            results = typing_test(stdscr, word_counts[current_row_idx])

            if results:
                # --- NEW: Call the dedicated results function ---
                display_results(stdscr, results)