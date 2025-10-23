import curses
from .ui import main # Import the new main orchestrator function from ui.py

if __name__ == "__main__":
    """
    The main entry point for the application.
    Initializes curses and runs the UI.
    """
    # curses.wrapper handles all the setup and teardown,
    # ensuring the terminal is restored to a usable state after the program exits.
    curses.wrapper(main)