# ============================================================
#  bank.py  —  The Bank Class (Master Manager)
# ============================================================
#
#  CONCEPTS covered here:
#
#  1. COMPOSITION again — Bank HAS-A list of Customers
#  2. Nested data structures — dict of lists of objects
#  3. JSON persistence — saving/loading complex objects
#  4. List comprehensions + dict comprehensions
#  5. sorted() with key= and lambda functions
#  6. *args and **kwargs — flexible function arguments
#  7. String formatting — professional reports
# ============================================================

import json
import os
from datetime import datetime

from customer import Customer
from savings import SavingsAccount
from current import CurrentAccount
from exceptions import AccountNotFoundError


class Bank:
    """
    The top-level manager — owns all customers and their accounts.

    CONCEPT: Composition at multiple levels
    ────────────────────────────────────────
    Bank HAS-A list of Customers
    Customer HAS-A list of Accounts
    Account HAS-A list of Transactions

    This is called a HIERARCHY OF COMPOSITION.
    It mirrors real life perfectly!

        Bank
         └── Customer (many)
               └── SavingsAccount / CurrentAccount (many)
                     └── Transaction history (many)
    """

    def __init__(self, bank_name, filepath="data/bank_data.json"):
        self.bank_name  = bank_name
        self.filepath   = filepath
        self.founded_on = datetime.now().strftime("%Y-%m-%d")

        # COMPOSITION: Bank HAS-A list of Customer objects
        self._customers = []

        self._load()

    # ──────────────────────────────────────────────────────────
    #  CUSTOMER OPERATIONS
    # ──────────────────────────────────────────────────────────

    def add_customer(self, name, email, phone):
        """
        Register a new customer after validating their details.
        """
        # Use the static method from Customer class for validation
        if not Customer.validate_email(email):
            print(f"⚠️  Invalid email: '{email}'")
            return None

        if not Customer.validate_phone(phone):
            print(f"⚠️  Invalid phone: '{phone}'. Must be 10 digits.")
            return None

        # Check for duplicate email
        # CONCEPT: any() — returns True if ANY item matches condition
        # It's like asking "does anyone in this list have this email?"
        if any(c.email == email for c in self._customers):
            print(f"⚠️  A customer with email '{email}' already exists.")
            return None

        customer = Customer(name, email, phone)
        self._customers.append(customer)
        self._save()
        print(f"✅ Customer '{name}' registered. ID: {customer.customer_id}")
        return customer

    def find_customer(self, **kwargs):
        """
        Find a customer by any attribute.

        CONCEPT: **kwargs (keyword arguments)
        ──────────────────────────────────────
        **kwargs lets a function accept ANY number of
        named arguments. They arrive as a dictionary.

        Examples:
          find_customer(email="disha@gmail.com")
          find_customer(name="Disha")
          find_customer(customer_id="CUS1001")

        Inside the function:
          kwargs = {"email": "disha@gmail.com"}
          key    = "email"
          value  = "disha@gmail.com"

        CONCEPT: getattr(object, attribute_name)
        ─────────────────────────────────────────
        Instead of:  customer.email
        We can do:   getattr(customer, "email")
        This lets us look up attributes DYNAMICALLY
        (when we don't know the attribute name at coding time).
        """
        for key, value in kwargs.items():
            for customer in self._customers:
                # getattr fetches the attribute named by 'key'
                if getattr(customer, key, None) == value:
                    return customer

        return None

    def get_all_customers(self):
        """Return all customers sorted alphabetically by name."""

        # CONCEPT: sorted() with key= parameter
        # sorted() returns a NEW sorted list (doesn't modify original)
        # key= tells it WHAT to sort by
        #
        # CONCEPT: lambda — a tiny anonymous (nameless) function
        # lambda c: c.name   means:  "given c, return c.name"
        # It's a shortcut for:
        #   def get_name(c):
        #       return c.name
        #
        # sorted(list, key=get_name)  ← same as below but longer
        return sorted(self._customers, key=lambda c: c.name)

    def remove_customer(self, customer_id):
        """Remove a customer from the bank."""
        customer = self.find_customer(customer_id=customer_id)
        if not customer:
            print(f"⚠️  Customer '{customer_id}' not found.")
            return
        self._customers.remove(customer)
        self._save()
        print(f"🗑️  Customer '{customer.name}' removed.")

    # ──────────────────────────────────────────────────────────
    #  ACCOUNT SEARCH ACROSS THE WHOLE BANK
    # ──────────────────────────────────────────────────────────

    def find_account(self, account_number):
        """
        Search for an account across ALL customers.

        CONCEPT: Nested iteration
        We loop through customers, and for each customer
        we loop through their accounts — two levels deep.
        """
        for customer in self._customers:
            for account in customer.accounts:
                if account.account_number == account_number:
                    return account, customer   # Return BOTH account and its owner

        raise AccountNotFoundError(account_number)

    # ──────────────────────────────────────────────────────────
    #  REPORTS & STATS
    # ──────────────────────────────────────────────────────────

    def bank_summary(self):
        """Print a complete bank-wide summary."""

        # CONCEPT: List comprehension to flatten nested data
        # We want ALL accounts from ALL customers in one list
        all_accounts = [
            acc
            for customer in self._customers
            for acc in customer.accounts     # nested comprehension
        ]

        total_customers = len(self._customers)
        total_accounts  = len(all_accounts)

        # CONCEPT: sum() with generator + conditional
        total_deposits  = sum(acc.balance for acc in all_accounts if acc.balance > 0)
        total_overdraft = sum(abs(acc.balance) for acc in all_accounts if acc.balance < 0)

        # Count by account type using list comprehension
        savings_count = len([a for a in all_accounts if a.account_type == "Savings"])
        current_count = len([a for a in all_accounts if a.account_type == "Current"])

        print(f"""
╔══════════════════════════════════════════╗
║       🏦  {self.bank_name:<30} ║
╠══════════════════════════════════════════╣
║  👥 Total Customers  : {total_customers:<18} ║
║  💳 Total Accounts   : {total_accounts:<18} ║
║     ├─ Savings       : {savings_count:<18} ║
║     └─ Current       : {current_count:<18} ║
║  💰 Total Deposits   : ₹{total_deposits:<17.2f} ║
║  ⚠️  Total Overdraft  : ₹{total_overdraft:<17.2f} ║
║  📅 Founded          : {self.founded_on:<18} ║
╚══════════════════════════════════════════╝
        """)

    def top_customers(self, n=3):
        """
        Show top N customers by total balance.

        CONCEPT: sorted() with reverse=True
        reverse=True means highest first (descending order)
        """
        if not self._customers:
            print("No customers yet.")
            return

        ranked = sorted(
            self._customers,
            key=lambda c: c.total_balance(),
            reverse=True              # Highest balance first
        )

        print(f"\n🏆 Top {n} Customers by Balance:")
        print(f"{'─'*45}")

        # CONCEPT: min() ensures we don't go out of range
        # If n=5 but only 2 customers, min(5,2) = 2
        for i, customer in enumerate(ranked[:min(n, len(ranked))], start=1):
            print(f"  {i}. {customer.name:<20} ₹{customer.total_balance():>10.2f}")

        print(f"{'─'*45}\n")

    def search_customers(self, keyword):
        """
        Search customers by name (case-insensitive).

        CONCEPT: str.lower() for case-insensitive comparison
        "DISHA".lower() == "disha".lower()  → True
        """
        keyword = keyword.lower()
        results = [c for c in self._customers if keyword in c.name.lower()]

        if not results:
            print(f"🔍 No customers found matching '{keyword}'.")
            return []

        print(f"\n🔍 Found {len(results)} customer(s):")
        for c in results:
            print(f"  {c}")
        return results

    # ──────────────────────────────────────────────────────────
    #  FILE I/O — Save & Load (JSON Persistence)
    # ──────────────────────────────────────────────────────────

    def _save(self):
        """Save entire bank state to JSON file."""
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)

        # CONCEPT: Dict comprehension
        # Similar to list comprehension but builds a dictionary
        # { key: value  for item in iterable }
        data = {
            "bank_name"  : self.bank_name,
            "founded_on" : self.founded_on,
            # List comprehension inside a dict!
            "customers"  : [c.to_dict() for c in self._customers],
        }

        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=2)

    def _load(self):
        """Load bank state from JSON file if it exists."""
        if not os.path.exists(self.filepath):
            return

        try:
            with open(self.filepath, "r") as f:
                data = json.load(f)

            self.bank_name  = data.get("bank_name", self.bank_name)
            self.founded_on = data.get("founded_on", self.founded_on)

            # Rebuild Customer objects from saved dictionaries
            self._customers = []
            for cdata in data.get("customers", []):
                customer = Customer.from_dict(cdata)

                # Rebuild each account from saved data
                for acc_data in cdata.get("accounts", []):
                    if acc_data["account_type"] == "Savings":
                        acc = SavingsAccount.from_dict(acc_data)
                    else:
                        acc = CurrentAccount.from_dict(acc_data)
                    customer._accounts.append(acc)

                self._customers.append(customer)

            print(f"📂 Loaded {len(self._customers)} customer(s) from file.")

        except (json.JSONDecodeError, KeyError) as e:
            print(f"⚠️  Could not load bank data: {e}. Starting fresh.")
            self._customers = []

    # ──────────────────────────────────────────────────────────
    #  DUNDER METHODS
    # ──────────────────────────────────────────────────────────

    def __len__(self):
        """len(bank) → number of customers."""
        return len(self._customers)

    def __str__(self):
        return f"🏦 {self.bank_name} | Customers: {len(self._customers)}"

    def __repr__(self):
        return f"Bank(name={self.bank_name}, customers={len(self._customers)})"