import random
from datetime import datetime

class User:
    def __init__(self, user_id, pin):
        self.user_id = user_id
        self.pin = pin
        self.account = Account()

class Account:
    def __init__(self):
        self.balance = 0
        self.transaction_history = []

    def deposit(self, amount):
        self.balance += amount
        self.add_transaction("Deposit", amount)

    def withdraw(self, amount):
        if amount <= self.balance:
            self.balance -= amount
            self.add_transaction("Withdrawal", amount)
        else:
            print("Insufficient funds!")

    def transfer(self, amount, recipient_account):
        if amount <= self.balance:
            self.balance -= amount
            recipient_account.balance += amount
            self.add_transaction("Transfer to " + str(recipient_account), amount)
        else:
            print("Insufficient funds!")

    def add_transaction(self, transaction_type, amount):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transaction = f"{timestamp} - {transaction_type}: ${amount}"
        self.transaction_history.append(transaction)

class ATM:
    MAX_PIN_RETRIES = 3
    LOCKED_USER_IDS = set()

    def authenticate_user(self, user):
        if user.user_id in self.LOCKED_USER_IDS:
            print("Account is locked. Please contact customer support.")
            return False

        for _ in range(self.MAX_PIN_RETRIES):
            user_id_input = int(input("Enter User ID: "))
            pin_input = int(input("Enter PIN: "))

            if user_id_input == user.user_id and pin_input == user.pin:
                return True
            else:
                print("Authentication failed. Incorrect User ID or PIN. Retries left:", self.MAX_PIN_RETRIES - 1)

        print("Maximum retries reached. Locking account.")
        self.LOCKED_USER_IDS.add(user.user_id)
        return False

    def display_menu(self):
        print("\nATM Menu:")
        print("1. Transactions History")
        print("2. Withdraw")
        print("3. Deposit")
        print("4. Transfer")
        print("5. Quit")

    def perform_transaction(self, user, choice):
        if choice == 1:
            self.display_transaction_history(user.account)
        elif choice == 2:
            amount = float(input("Enter withdrawal amount: $"))
            user.account.withdraw(amount)
        elif choice == 3:
            amount = float(input("Enter deposit amount: $"))
            user.account.deposit(amount)
        elif choice == 4:
            recipient_id = int(input("Enter recipient's User ID: "))
            recipient = self.get_user_by_id(recipient_id)
            if recipient:
                amount = float(input("Enter transfer amount: $"))
                user.account.transfer(amount, recipient.account)
            else:
                print("Recipient not found.")
        elif choice == 5:
            print("Exiting ATM. Thank you!")
            exit()
        else:
            print("Invalid choice. Please select a valid option.")

    def display_transaction_history(self, account):
        print("\nTransaction History:")
        for transaction in account.transaction_history:
            print(transaction)

    def get_user_by_id(self, user_id):
        for user in users:
            if user.user_id == user_id:
                return user
        return None

class Main:
    def run_atm(self):
        atm = ATM()

        # Allow users to create their accounts
        num_users = int(input("Enter the number of users: "))
        for _ in range(num_users):
            user_id = int(input("Enter User ID: "))
            pin = int(input("Enter PIN: "))
            users.append(User(user_id, pin))

        # Main ATM loop
        while True:
            user_id_input = int(input("Enter your User ID: "))
            user = atm.get_user_by_id(user_id_input)

            if user:
                print(f"Welcome back, User ID: {user.user_id}!")
                if atm.authenticate_user(user):
                    while True:
                        atm.display_menu()
                        choice = int(input("Enter your choice (1-5): "))
                        atm.perform_transaction(user, choice)
            else:
                print("User not found. Please enter a valid User ID.")

if __name__ == "__main__":
    users = []  # List to store user accounts
    main = Main()
    main.run_atm()
