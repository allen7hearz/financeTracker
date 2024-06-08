import curses
from ui import main_menu
from transaction import FinanceTracker

def main(stdscr):
    # Initialize the finance tracker
    tracker = FinanceTracker("data/transactions.json")

    # Run the main menu
    main_menu(stdscr)

if __name__ == "__main__":
    curses.wrapper(main)