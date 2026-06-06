# ============================================================
#  main.py  —  Entry Point (run this file!)
# ============================================================
#
#  CONCEPTS covered here:
#
#  1. Functions that return values — menus as reusable helpers
#  2. while True + break/continue — main application loop
#  3. Nested while loops — sub-menus
#  4. try/except with multiple exception types
#  5. String .center() .ljust() .rjust() — text formatting
#  6. Global state — one bank, one active_customer across menus
# ============================================================

from bank import Bank
from exceptions import (
    InsufficientFundsError,
    AccountNotFoundError,
    InvalidAmountError,
    AccountFrozenError,
)


# ── GLOBALS ────────────────────────────────────────────────
# CONCEPT: Module-level variables
# These are accessible throughout this file.
# 'bank' is created once and shared by all menu functions.
bank            = Bank("PyBank India")
active_customer = None    # Tracks which customer is "logged in"


# ── DISPLAY HELPERS ────────────────────────────────────────

def header(title):
    """Print a neat section header."""
    print(f"\n{'═'*50}")
    # CONCEPT: str.center(width) — centres text within a width
    print(f"  {title.center(46)}")
    print(f"{'═'*50}")


def pause():
    """Wait for the user to press Enter before continuing."""
    input("\n  Press Enter to continue...")


def get_float(prompt):
    """
    Ask for a number and keep asking until valid.

    CONCEPT: while True loop for input validation
    We loop forever and only 'break' out when we get
    a valid positive number. This prevents the app from
    crashing if the user types "abc" instead of a number.
    """
    while True:
        try:
            # float() converts string → decimal number
            # Raises ValueError if the string isn't a number
            value = float(input(f"  {prompt}: ").strip())
            if value <= 0:
                print("  ⚠️  Amount must be greater than zero.")
            else:
                return value
        except ValueError:
            print("  ⚠️  Please enter a valid number (e.g. 500 or 1500.50).")


# ══════════════════════════════════════════════════════════
#  MAIN MENU
# ══════════════════════════════════════════════════════════

def main_menu():
    print("""
  ┌─────────────────────────────────────┐
  │        🏦  PyBank India             │
  │─────────────────────────────────────│
  │  1.  👤  Register New Customer      │
  │  2.  🔍  Find / Select Customer     │
  │  3.  📋  List All Customers         │
  │  4.  🏆  Top Customers by Balance   │
  │  5.  📊  Bank Summary               │
  │  0.  🚪  Exit                       │
  └─────────────────────────────────────┘
    """)


# ══════════════════════════════════════════════════════════
#  CUSTOMER MENU  (shown after selecting a customer)
# ══════════════════════════════════════════════════════════

def customer_menu(customer):
    print(f"""
  ┌─────────────────────────────────────┐
  │  👤  {customer.name:<32} │
  │  ID: {customer.customer_id:<32} │
  │─────────────────────────────────────│
  │  1.  🏦  Open Savings Account       │
  │  2.  🏦  Open Current Account       │
  │  3.  💰  Deposit                    │
  │  4.  💸  Withdraw                   │
  │  5.  🔄  Transfer Money             │
  │  6.  📋  View Account Details       │
  │  7.  📜  Transaction History        │
  │  8.  💹  Apply Interest (Savings)   │
  │  9.  🔒  Freeze / Unfreeze Account  │
  │  10. 👤  Customer Profile           │
  │  0.  ← Back to Main Menu           │
  └─────────────────────────────────────┘
    """)


# ══════════════════════════════════════════════════════════
#  HANDLER FUNCTIONS — one per menu action
# ══════════════════════════════════════════════════════════

def handle_register():
    """Register a new bank customer."""
    header("Register New Customer")
    name  = input("  Full name  : ").strip()
    email = input("  Email      : ").strip()
    phone = input("  Phone (10d): ").strip()

    if not name:
        print("  ⚠️  Name cannot be empty.")
        return

    bank.add_customer(name, email, phone)


def handle_find_customer():
    """
    Search for a customer and return them.
    Returns the Customer object or None.
    """
    header("Find Customer")
    print("  Search by:  1. Name   2. Email   3. Customer ID")
    choice = input("  Choose: ").strip()

    # CONCEPT: Dictionary as a dispatch table
    # Instead of if/elif/elif, map choices to search keys
    search_map = {"1": "name", "2": "email", "3": "customer_id"}

    if choice not in search_map:
        print("  ⚠️  Invalid choice.")
        return None

    keyword = input(f"  Enter {search_map[choice]}: ").strip()

    # CONCEPT: **unpacking a dictionary into keyword arguments
    # search_map[choice] = "email"
    # keyword            = "disha@gmail.com"
    # This becomes: bank.find_customer(email="disha@gmail.com")
    customer = bank.find_customer(**{search_map[choice]: keyword})

    if customer:
        print(f"\n  ✅ Found: {customer}")
    else:
        print(f"  ⚠️  No customer found.")

    return customer


def handle_open_account(customer):
    """Open a new account for the active customer."""
    header("Open New Account")
    print("  1. Savings Account")
    print("  2. Current Account")
    acc_type = input("  Choose account type: ").strip()

    deposit = get_float("Initial deposit amount (₹)")

    if acc_type == "1":
        customer.open_savings_account(initial_deposit=deposit)
    elif acc_type == "2":
        customer.open_current_account(initial_deposit=deposit)
    else:
        print("  ⚠️  Invalid choice.")


def pick_account(customer):
    """
    Helper — show customer's accounts and let them pick one.
    Returns the selected Account object or None.
    """
    accounts = customer.accounts

    if not accounts:
        print("  ⚠️  No accounts found. Please open an account first.")
        return None

    print("\n  Your accounts:")
    for i, acc in enumerate(accounts, start=1):
        status = "🔒" if acc.is_frozen else "✅"
        print(f"  {i}. {status} {acc.account_number} | {acc.account_type:<8} | ₹{acc.balance:.2f}")

    # CONCEPT: while True for validated selection
    while True:
        try:
            choice = int(input("\n  Select account number: ").strip())
            if 1 <= choice <= len(accounts):
                return accounts[choice - 1]
            print(f"  ⚠️  Enter a number between 1 and {len(accounts)}.")
        except ValueError:
            print("  ⚠️  Please enter a valid number.")


def handle_deposit(customer):
    """Deposit money into one of the customer's accounts."""
    header("Deposit Money")
    account = pick_account(customer)
    if not account:
        return

    amount = get_float("Amount to deposit (₹)")

    # CONCEPT: Multiple exception types in one try/except block
    # We handle EACH error differently
    try:
        account.deposit(amount)
        bank._save()
    except AccountFrozenError as e:
        print(f"  🚫 {e}")
    except InvalidAmountError as e:
        print(f"  🚫 {e}")


def handle_withdraw(customer):
    """Withdraw money from one of the customer's accounts."""
    header("Withdraw Money")
    account = pick_account(customer)
    if not account:
        return

    amount = get_float("Amount to withdraw (₹)")

    try:
        account.withdraw(amount)
        bank._save()
    except InsufficientFundsError as e:
        print(f"  🚫 {e}")
    except AccountFrozenError as e:
        print(f"  🚫 {e}")
    except InvalidAmountError as e:
        print(f"  🚫 {e}")


def handle_transfer(customer):
    """Transfer money between accounts."""
    header("Transfer Money")

    print("  Select SOURCE account (your account to send FROM):")
    source = pick_account(customer)
    if not source:
        return

    dest_num = input("\n  Enter DESTINATION account number (e.g. ACC1002): ").strip()

    # CONCEPT: Unpacking a tuple — find_account returns (account, customer)
    try:
        dest_account, dest_owner = bank.find_account(dest_num)
    except AccountNotFoundError as e:
        print(f"  🚫 {e}")
        return

    print(f"  Sending to: {dest_owner.name} — {dest_account.account_number}")
    amount = get_float("Amount to transfer (₹)")

    try:
        source.transfer(dest_account, amount)
        bank._save()
    except InsufficientFundsError as e:
        print(f"  🚫 {e}")
    except AccountFrozenError as e:
        print(f"  🚫 {e}")


def handle_view_account(customer):
    """Show detailed info for a selected account."""
    header("Account Details")
    account = pick_account(customer)
    if account:
        print(f"\n{account.get_account_info()}")


def handle_history(customer):
    """Show transaction history for a selected account."""
    header("Transaction History")
    account = pick_account(customer)
    if not account:
        return

    print("  Show:  1. All transactions   2. Last 5   3. Last 10")
    choice = input("  Choose: ").strip()

    # CONCEPT: Dictionary mapping choice → value
    limit_map = {"1": None, "2": 5, "3": 10}
    limit = limit_map.get(choice, None)   # .get() returns None if key missing
    account.get_history(last_n=limit)


def handle_interest(customer):
    """Apply interest to a savings account."""
    header("Apply Interest")
    accounts = [a for a in customer.accounts if a.account_type == "Savings"]

    if not accounts:
        print("  ⚠️  No savings accounts found.")
        return

    print("\n  Savings accounts:")
    for i, acc in enumerate(accounts, start=1):
        print(f"  {i}. {acc.account_number} | ₹{acc.balance:.2f} | Rate: {acc.interest_rate*100:.1f}%")

    try:
        choice = int(input("\n  Select: ").strip()) - 1
        if 0 <= choice < len(accounts):
            accounts[choice].apply_interest()
            bank._save()
        else:
            print("  ⚠️  Invalid selection.")
    except ValueError:
        print("  ⚠️  Please enter a valid number.")


def handle_freeze(customer):
    """Freeze or unfreeze an account."""
    header("Freeze / Unfreeze Account")
    account = pick_account(customer)
    if not account:
        return

    if account.is_frozen:
        account.unfreeze()
    else:
        confirm = input(f"  ❓ Freeze {account.account_number}? (y/n): ").strip().lower()
        if confirm == "y":
            account.freeze()

    bank._save()


# ══════════════════════════════════════════════════════════
#  CUSTOMER SESSION LOOP
#  Shown after a customer is selected
# ══════════════════════════════════════════════════════════

def run_customer_session(customer):
    """
    Inner loop — runs while a customer is 'active'.

    CONCEPT: Nested while loops
    The outer loop is the main menu.
    This inner loop is the customer-specific menu.
    '0' breaks out of THIS loop back to the outer loop.
    """
    while True:
        customer_menu(customer)
        choice = input("  Enter choice: ").strip()

        if   choice == "1":  handle_open_account(customer)
        elif choice == "2":  handle_open_account(customer)
        elif choice == "3":  handle_deposit(customer)
        elif choice == "4":  handle_withdraw(customer)
        elif choice == "5":  handle_transfer(customer)
        elif choice == "6":  handle_view_account(customer)
        elif choice == "7":  handle_history(customer)
        elif choice == "8":  handle_interest(customer)
        elif choice == "9":  handle_freeze(customer)
        elif choice == "10": customer.get_summary()
        elif choice == "0":
            print(f"\n  👋 Goodbye, {customer.name}!")
            break   # Exit inner loop → back to main menu
        else:
            print("  ⚠️  Invalid choice.")

        pause()


# ══════════════════════════════════════════════════════════
#  MAIN APPLICATION LOOP
# ══════════════════════════════════════════════════════════

def main():
    print("""
╔══════════════════════════════════════════╗
║                                          ║
║       🏦  Welcome to PyBank India  🏦    ║
║                                          ║
╚══════════════════════════════════════════╝
    """)

    # CONCEPT: Outer while True — keeps app running
    # Only '0' (Exit) triggers break to quit
    while True:
        main_menu()
        choice = input("  Enter choice: ").strip()

        if choice == "1":
            handle_register()
            pause()

        elif choice == "2":
            customer = handle_find_customer()
            if customer:
                go_in = input(f"\n  Open session for {customer.name}? (y/n): ").strip().lower()
                if go_in == "y":
                    # CONCEPT: Calling a function that has its OWN loop
                    run_customer_session(customer)

        elif choice == "3":
            header("All Customers")
            customers = bank.get_all_customers()
            if not customers:
                print("  No customers registered yet.")
            else:
                for i, c in enumerate(customers, start=1):
                    print(f"  {i:>2}. {c}")
            pause()

        elif choice == "4":
            try:
                n = int(input("  How many top customers to show? ").strip())
                bank.top_customers(n)
            except ValueError:
                print("  ⚠️  Please enter a valid number.")
            pause()

        elif choice == "5":
            bank.bank_summary()
            pause()

        elif choice == "0":
            print("\n  👋 Thank you for using PyBank India. Goodbye!\n")
            break   # Exit the outer loop — program ends

        else:
            print("  ⚠️  Invalid choice. Please try again.")


# ══════════════════════════════════════════════════════════
if __name__ == "__main__":
    main()