import curses
import time
from .core import WORDS, generate_prompt, acc_calculator, wpm_calculator

def display_menu(stdscr, menu, current_row_idx):
    """
    Displays the main menu for mode selection.
    """
    stdscr.erase()
    h, w = stdscr.getmaxyx()
    for idx, row in enumerate(menu):
        x = w//2 - len(row)//2
        y = h//2 - len(menu)//2 + idx
        if idx == current_row_idx:
            stdscr.attron(curses.color_pair(1)) # Highlight selected item
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def display_text(stdscr, target, current, y, x):
    """
    Displays the target text and the user's current text with color-coded feedback.
    """
    # Draw the text to be typed, color-coding correct/incorrect characters
    for i, char in enumerate(target):
        color = curses.color_pair(3) # Default/Pending text color
        if i < len(current):
            color = curses.color_pair(1) if current[i] == target[i] else curses.color_pair(2)
        stdscr.addstr(y, x + i, char, color)
    
    # Move the cursor to the current typing position
    stdscr.move(y, x + len(current))

def typing_test(stdscr, num_words):
    """
    Runs the main typing test loop and returns the results.
    """
    prompt_text = generate_prompt(WORDS, num_words=num_words)
    current_text = []
    start_time: float = 0
    wpm = 0

    while True:
        # Calculate real-time stats
        if start_time is not None:
            elapsed_time = max(time.time() - start_time, 1) # Avoid division by zero
            wpm = wpm_calculator(prompt_text, "".join(current_text), elapsed_time)
        
        accuracy = acc_calculator(prompt_text, "".join(current_text))

        # Drawing the UI
        stdscr.erase()
        stdscr.addstr(0, 0, f"WPM: {wpm:.2f} | Accuracy: {accuracy:.2f}%")
        display_text(stdscr, prompt_text, "".join(current_text), 2, 0)
        stdscr.refresh()

        # End condition
        if "".join(current_text) == prompt_text:
            break

        # Get user input
        key = stdscr.getch()

        # Start timer on first keypress
        if start_time is None:
            start_time = time.time()
        
        # Handle keypresses
        if key == 27: # ESC key
            return None # User exited the test
        elif key in (curses.KEY_BACKSPACE, 127):
            if len(current_text) > 0:
                current_text.pop()
        elif 32 <= key <= 126: # Regular printable characters
            current_text.append(chr(key))
    
    # Return final results
    return {
        "wpm": wpm,
        "accuracy": accuracy,
        "time": time.time() - start_time
    }

def main(stdscr):
    """
    The main function that orchestrates the application flow, called by curses.wrapper.
    """
    # Initial curses setup
    curses.curs_set(1) # Show the cursor
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
    curses.init_pair(3, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Menu setup
    menu = ["10 Words", "20 Words", "50 Words", "Exit"]
    word_counts = [10, 20, 50, -1] # -1 corresponds to "Exit"
    current_row_idx = 0

    while True:
        display_menu(stdscr, menu, current_row_idx)
        key = stdscr.getch()

        # Menu navigation
        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            selected_words = word_counts[current_row_idx]
            
            if selected_words == -1: # Exit condition
                break
            
            # --- Countdown Logic ---
            stdscr.erase()
            for i in range(3, 0, -1):
                start_msg = f"Starting in {i}..."
                stdscr.addstr(curses.LINES // 2, (curses.COLS // 2) - len(start_msg) // 2, start_msg)
                stdscr.refresh()
                time.sleep(1)
            
            # Run the test
            results = typing_test(stdscr, selected_words)

            # --- Results Screen ---
            if results:
                stdscr.erase()
                h, w = stdscr.getmaxyx()
                result_str = f"WPM: {results['wpm']:.2f} | Accuracy: {results['accuracy']:.2f}% | Time: {results['time']:.2f}s"
                stdscr.addstr(h//2, w//2 - len(result_str)//2, result_str)
                stdscr.addstr(h//2 + 2, w//2 - 14, "Press any key to continue...")
                stdscr.refresh()
                stdscr.getch() # Wait for a keypress to return to menu