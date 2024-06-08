from datetime import datetime
import json
purchase_categories = [
    "groceries",
    "utilities",
    "transportation",
    "healthcare",
    "entertainment",
    "housing",
    "clothing",
    "education",
    "personal care",
    "debt repayment"
]

class Transaction:
    def __init__(self, amount, category, description, date=None):
        if date:
            self.date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S.%f")
        else:
            self.date = datetime.now()  # Store the datetime object directly

        # Amount
        if float(amount) >= 0:  # Convert amount to float before comparison
            self.amount = float(amount)
        else:    
            raise ValueError("amount must be greater than or equal to zero")

        # Category
        if category in purchase_categories:
            self.category = category
        else:
            raise ValueError("Category must be one of the predefined purchase categories")

        # Description
        if len(description) < 50:
            self.description = description
        else:
            raise ValueError("Description must be less than 50 characters")

    def __str__(self):
        date_str = self.date.strftime("%Y-%m-%d %H:%M:%S.%f")
        return f"{date_str} | {self.amount} | {self.category} | {self.description}"

# Basic Transaction Test
class FinanceTracker:
    def __init__(self, file_path):
        self.transactions = []
        self.file_path = file_path

    def add_transaction(self, transaction):
        if isinstance(transaction, Transaction):
            self.transactions.append(transaction)
        else:
            raise ValueError("Invalid transaction type")

    def get_transactions(self):
        return self.transactions

    def save_to_file(self):
        try:
            with open(self.file_path, 'w') as file:
                json.dump([{
                    'amount': t.amount,
                    'category': t.category,
                    'description': t.description,
                    'date': t.date.strftime("%Y-%m-%d %H:%M:%S.%f")
                } for t in self.transactions], file)
        except IOError as e:
            print(f"An error occurred while saving to file: {e}")

    def load_from_file(self):
        try:
            with open(self.file_path, 'r') as file:
                try:
                    transactions_data = json.load(file)
                    self.transactions = [Transaction(**data) for data in transactions_data]
                except json.JSONDecodeError:
                    self.transactions = []
                    print("JSON file is empty or corrupted. Starting with an empty list.")
        except FileNotFoundError:
            self.transactions = []
            print("File not found. Starting with an empty list.")
        except IOError as e:
            print(f"An error occurred while loading from file: {e}")

    def remove_transaction(self, index):
        if 0 <= index < len(self.transactions):
            del self.transactions[index]
        else:
            raise IndexError("Transaction index out of range")

    def search_transactions(self, keyword):
        return [t for t in self.transactions if keyword.lower() in t.description.lower() or keyword.lower() in t.category.lower()]

    def edit_transaction(self, index, amount=None, category=None, description=None):
        if 0 <= index < len(self.transactions):
            transaction = self.transactions[index]
            if amount is not None:
                if amount >= 0:
                    transaction.amount = float(amount)
                else:
                    raise ValueError("Amount must be greater than or equal to zero")
            if category is not None:
                if category in purchase_categories:
                    transaction.category = category
                else:
                    raise ValueError("Category must be one of the predefined purchase categories")
            if description is not None:
                if len(description) < 50:
                    transaction.description = description
                else:
                    raise ValueError("Description must be less than 50 characters")
        else:
            raise IndexError("Transaction index out of range")

"""
# Example usage
if __name__ == "__main__":
    tracker = FinanceTracker("data/transactions.json")

    # Load existing transactions
    tracker.load_from_file()

    # Add a new transaction
    try:
        t = Transaction(60, "clothing", "Movie night")
        tracker.add_transaction(t)
    except ValueError as e:
        print(e)

    # Save transactions to file
    tracker.save_to_file()

    # Retrieve and print transactions
    for transaction in tracker.get_transactions():
        print(transaction)

    # Remove a transaction by index
    try:
        tracker.remove_transaction(0)  # Remove the first transaction
    except IndexError as e:
        print(e)

    # Save transactions to file again after removal
    tracker.save_to_file()

    # Retrieve and print transactions again
    for transaction in tracker.get_transactions():
        print(transaction)"""