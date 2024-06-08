from datetime import datetime

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
    def __init__(self, amount, category, description):
        self.date = datetime.now()  # Store the datetime object directly
        
        # Amount
        if amount >= 0:
            self.amount = float(amount)
        else:
            raise ValueError("Amount must be greater than or equal to zero")
        
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
        # This method returns a string representation of the transaction
        date_str = self.date.strftime("%d-%m-%Y %H:%M:%S")
        return f"{date_str} | {self.amount} | {self.category} | {self.description}"

# Example of creating a transaction
try:
    t = Transaction(100, "groceries", "Weekly grocery shopping")
    print(t)
except ValueError as e:
    print(e)
