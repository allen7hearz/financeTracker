import curses
import time
from art import *
from transaction import FinanceTracker, Transaction, purchase_categories
def display_logo(stdscr):
    logo = text2art("               Finance Manager")
    for i, line in enumerate(logo.split('\n')):
        stdscr.addstr(i + 1, 1, line, curses.color_pair(1))  # Apply color to each line
def main_menu(stdscr):
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Reverse color pair for selected option
    
    tracker = FinanceTracker("data/transactions.json")
    tracker.load_from_file()

    current_row = 0
    
    menu = ['Add Transaction', 'View Transactions', 'Search Transactions', 'Remove Transaction', 'Edit Transaction', 'Exit']

    while True:
        stdscr.clear()
        curses.start_color()
        curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLACK)
        display_logo(stdscr)
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            x = width // 2 - len(row) // 2
            y = height // 2 - len(menu) // 2 + idx
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, row)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == curses.KEY_ENTER or key in [10, 13]:
            if current_row == 0:
                add_transaction(stdscr, tracker)
            elif current_row == 1:
                view_transactions(stdscr, tracker)
            elif current_row == 2:
                search_transactions(stdscr, tracker)
            elif current_row == 3:
                remove_transaction(stdscr, tracker)
            elif current_row == 4:
                edit_transaction(stdscr, tracker)
            elif current_row == 5:
                break

        stdscr.refresh()
        
def choose_category(stdscr, categories):
    current_row = 0
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Choose a Category:")

        for idx, category in enumerate(categories):
            x = 0
            y = idx + 1
            if idx == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, category)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, category)

        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(categories) - 1:
            current_row += 1
        elif key in [10, 13]:  # Enter key
            return categories[current_row]



def add_transaction(stdscr, tracker):
    stdscr.clear()
    stdscr.addstr(0, 0, "Adding New Transaction")

    curses.echo()
    curses.curs_set(1)

    stdscr.addstr(2, 0, "Enter Amount: ")
    amount_input = stdscr.getstr().decode('utf-8')
    amount = float(amount_input) if amount_input else None  # Convert amount to float
    curses.curs_set(0)
    stdscr.addstr(3, 0, "Choose Category:")
    category = choose_category(stdscr, purchase_categories)
    stdscr.clear()  # Clear the screen after selecting the category
    curses.curs_set(1)
    stdscr.addstr(4, 0, "Enter Description: ")
    description = stdscr.getstr().decode('utf-8')

    # Create a Transaction object
    new_transaction = Transaction(amount, category, description)

    # Call add_transaction method of tracker

    curses.curs_set(0)  # Hide cursor

    try:
        tracker.add_transaction(new_transaction)
        tracker.save_to_file()
        stdscr.addstr(6, 0, "Transaction added successfully!")
    except ValueError as e:
        stdscr.addstr(6, 0, str(e))

    stdscr.addstr(8, 0, "Press any key to return to the main menu")
    stdscr.getch()

def view_transactions(stdscr, tracker):
    stdscr.clear()
    stdscr.addstr(0, 0, "View Transactions")

    transactions = tracker.get_transactions()
    page_size = 10
    current_page = 0
    total_pages = (len(transactions) - 1) // page_size + 1
    sort_key = 'date'

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"View Transactions (Page {current_page + 1}/{total_pages})")
        stdscr.addstr(1, 0, f"Sorted by: {sort_key}. Press 's' to change sorting (date, amount, category)")

        sorted_transactions = sorted(transactions, key=lambda x: getattr(x, sort_key))
        start = current_page * page_size
        end = start + page_size

        for idx, transaction in enumerate(sorted_transactions[start:end], start=1):
            stdscr.addstr(idx + 2, 0, str(transaction))

        stdscr.addstr(page_size + 4, 0, "Use < and > to navigate pages. Press q to return to main menu.")

        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('<') and current_page > 0:
            current_page -= 1
        elif key == ord('>') and current_page < total_pages - 1:
            current_page += 1
        elif key == ord('s'):
            stdscr.addstr(page_size + 6, 0, "Enter sort key (date, amount, category): ")
            curses.echo()
            sort_key = stdscr.getstr().decode('utf-8').lower()
            curses.noecho()
            if sort_key not in ['date', 'amount', 'category']:
                sort_key = 'date'  # Default to date if invalid input

def search_transactions(stdscr, tracker):
    stdscr.clear()
    stdscr.addstr(0, 0, "Search Transactions")

    curses.echo()
    curses.curs_set(1)
    stdscr.addstr(2, 0, "Keyword: ")
    keyword = stdscr.getstr().decode('utf-8')
    curses.curs_set(0)

    stdscr.addstr(4, 0, "Category (leave blank for all): ")
    category = stdscr.getstr().decode('utf-8').lower()

    results = tracker.search_transactions(keyword)
    if category:
        results = [t for t in results if t.category.lower() == category]

    for idx, transaction in enumerate(results):
        stdscr.addstr(idx + 6, 0, str(transaction))

    stdscr.addstr(len(results) + 8, 0, "Press any key to return to the main menu")
    stdscr.getch()

def remove_transaction(stdscr, tracker):
    transactions = tracker.get_transactions()
    selected_transaction = choose_transaction(stdscr, transactions, "Choose a Transaction to Remove:")

    if not selected_transaction:
        return

    index = transactions.index(selected_transaction)
    
    stdscr.clear()
    stdscr.addstr(0, 0, "Removing Transaction")

    stdscr.addstr(2, 0, f"Selected Transaction: {selected_transaction}")
    stdscr.addstr(4, 0, "Are you sure you want to remove this transaction? (y/n)")

    key = stdscr.getch()
    if key in [ord('y'), ord('Y')]:
        try:
            tracker.remove_transaction(index)
            tracker.save_to_file()
            stdscr.addstr(6, 0, "Transaction removed successfully!")
        except IndexError as e:
            stdscr.addstr(6, 0, str(e))
    else:
        stdscr.addstr(6, 0, "Transaction removal cancelled.")

    stdscr.addstr(8, 0, "Press any key to return to the main menu")
    stdscr.getch()


def choose_transaction(stdscr, transactions, title="Choose a Transaction:"):
    current_row = 0
    page_size = min(len(transactions), curses.LINES - 4)  # Limit transactions to fit within the terminal window
    current_page = 0
    total_pages = (len(transactions) - 1) // page_size + 1

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, f"{title} (Page {current_page + 1}/{total_pages})")

        start = current_page * page_size
        end = start + page_size

        for idx, transaction in enumerate(transactions[start:end], start=1):
            x = 0
            y = idx + 1
            if start + idx - 1 == current_row:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(y, x, str(transaction))
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(y, x, str(transaction))

        stdscr.addstr(curses.LINES - 2, 0, "Use < and > to navigate pages. Press q to return to main menu.")

        key = stdscr.getch()

        if key == ord('q'):
            return None
        elif key == ord('<') and current_page > 0:
            current_page -= 1
        elif key == ord('>') and current_page < total_pages - 1:
            current_page += 1
        elif key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(transactions) - 1:
            current_row += 1
        elif key in [10, 13]:  # Enter key
            return transactions[current_row]



def edit_transaction(stdscr, tracker):
    transactions = tracker.get_transactions()
    selected_transaction = choose_transaction(stdscr, transactions, "Choose a Transaction to Edit:")

    if not selected_transaction:
        return

    index = transactions.index(selected_transaction)
    
    stdscr.clear()
    stdscr.addstr(0, 0, f"Editing Transaction {index}")

    curses.echo()
    curses.curs_set(1)
    stdscr.addstr(2, 0, f"Current Amount: {selected_transaction.amount}. New Amount (leave blank to keep unchanged): ")
    amount_input = stdscr.getstr().decode('utf-8')
    amount = float(amount_input) if amount_input else None  # Convert amount to float
    curses.curs_set(0)
    stdscr.addstr(3, 0, f"Current Category: {selected_transaction.category}. Press 'c' to change category.")
    key = stdscr.getch()
    if key == ord('c'):
        category = choose_category(stdscr, purchase_categories)
        stdscr.clear()  # Clear the screen after selecting the category
    else:
        category = selected_transaction.category
    curses.curs_set(1)
    stdscr.addstr(4, 0, f"Current Description: {selected_transaction.description}. New Description (leave blank to keep unchanged): ")
    description = stdscr.getstr().decode('utf-8')
    curses.curs_set(0)
    try:
        tracker.edit_transaction(index, amount, category, description if description else None)
        tracker.save_to_file()
        stdscr.addstr(6, 0, "Transaction edited successfully!")
    except (IndexError, ValueError) as e:
        stdscr.addstr(6, 0, str(e))

    stdscr.addstr(8, 0, "Press any key to return to the main menu")
    stdscr.getch()
