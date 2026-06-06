# ============================================================
#  customer.py  —  Customer Class
# ============================================================
#
#  CONCEPTS covered here:
#
#  1. COMPOSITION   — "HAS-A" relationship
#                     A Customer HAS-A list of Accounts
#                     (different from Inheritance = "IS-A")
#  2. @staticmethod — A method that belongs to the class but
#                     doesn't need 'self' or 'cls'
#  3. @classmethod  — Alternative constructor (factory method)
#  4. __len__       — Dunder method: len(customer)
#  5. __contains__  — Dunder method: "ACC1000" in customer
#  6. Encapsulation — Private __customer_id, protected via property
# ============================================================

from datetime import datetime
from savings import SavingsAccount
from current import CurrentAccount
from exceptions import AccountNotFoundError


class Customer:
    """
    Represents a bank customer who can hold multiple accounts.

    CONCEPT: Composition vs Inheritance
    ─────────────────────────────────────
    You've seen Inheritance (IS-A):
      SavingsAccount IS-A Account

    Composition (HAS-A) is different:
      Customer HAS-A list of Accounts

    A Customer is NOT a type of Account.
    A Customer OWNS accounts — that's Composition.

    Real world analogy:
      Inheritance  → A Car IS-A Vehicle
      Composition  → A Car HAS-A Engine, HAS-A Wheels

    Rule of thumb:
      Use Inheritance when: Child IS-A Parent
      Use Composition when: Object HAS-A other object
    """

    # Class variable — auto-increments for each new customer
    _next_customer_id = 1001

    def __init__(self, name, email, phone):

        # ── Private attributes ────────────────────────────────
        self.__customer_id = f"CUS{Customer._next_customer_id:04d}"
        Customer._next_customer_id += 1

        # ── Public attributes ─────────────────────────────────
        self.name      = name
        self.email     = email
        self.phone     = phone
        self.joined_on = datetime.now().strftime("%Y-%m-%d")

        # ── COMPOSITION: Customer HAS-A list of accounts ──────
        # This list will hold SavingsAccount and CurrentAccount objects
        # One customer can have MULTIPLE accounts
        self._accounts = []   # List of Account objects

    # ──────────────────────────────────────────────────────────
    #  @property for read-only access to private customer_id
    # ──────────────────────────────────────────────────────────
    @property
    def customer_id(self):
        return self.__customer_id

    @property
    def accounts(self):
        """Return a COPY of accounts list — protects internal list."""
        # list() creates a new list — caller can't modify the original
        return list(self._accounts)

    # ──────────────────────────────────────────────────────────
    #  ACCOUNT MANAGEMENT — Composition in action
    # ──────────────────────────────────────────────────────────

    def open_savings_account(self, initial_deposit=0.0, interest_rate=None):
        """Create and attach a new SavingsAccount to this customer."""

        # CONCEPT: Composition — we CREATE an account and STORE it
        # The Customer object now "owns" this SavingsAccount
        account = SavingsAccount(self.name, initial_deposit, interest_rate)
        self._accounts.append(account)
        print(f"🏦 Savings account {account.account_number} opened for {self.name}.")
        return account

    def open_current_account(self, initial_deposit=0.0, overdraft_limit=None):
        """Create and attach a new CurrentAccount to this customer."""
        account = CurrentAccount(self.name, initial_deposit, overdraft_limit)
        self._accounts.append(account)
        print(f"🏦 Current account {account.account_number} opened for {self.name}.")
        return account

    def get_account(self, account_number):
        """
        Find and return an account by its account number.

        CONCEPT: next() with a generator expression
        ────────────────────────────────────────────
        Instead of a loop like:
            for acc in self._accounts:
                if acc.account_number == account_number:
                    return acc

        We use next() with a generator — cleaner and faster:
            next((acc for acc in self._accounts if condition), None)

        'None' is the default if nothing is found.
        """
        account = next(
            (acc for acc in self._accounts if acc.account_number == account_number),
            None   # Return None if not found
        )

        if not account:
            raise AccountNotFoundError(account_number)

        return account

    def close_account(self, account_number):
        """Remove an account from this customer."""
        account = self.get_account(account_number)
        self._accounts.remove(account)
        print(f"🗑️  Account {account_number} closed for {self.name}.")

    def total_balance(self):
        """
        Sum of balances across all accounts.

        CONCEPT: sum() with a generator expression
        ───────────────────────────────────────────
        sum(acc.balance for acc in self._accounts)
        is equivalent to:
            total = 0
            for acc in self._accounts:
                total += acc.balance
            return total

        Generator expressions are lazy — they compute one item
        at a time, which is memory efficient for large lists.
        """
        return sum(acc.balance for acc in self._accounts)

    def get_summary(self):
        """Print a full summary of customer and all their accounts."""

        print(f"\n{'═'*50}")
        print(f"  👤 CUSTOMER PROFILE")
        print(f"{'═'*50}")
        print(f"  ID       : {self.__customer_id}")
        print(f"  Name     : {self.name}")
        print(f"  Email    : {self.email}")
        print(f"  Phone    : {self.phone}")
        print(f"  Joined   : {self.joined_on}")
        print(f"  Accounts : {len(self._accounts)}")
        print(f"  Total ₹  : ₹{self.total_balance():.2f}")
        print(f"{'─'*50}")

        if not self._accounts:
            print("  No accounts yet.")
        else:
            for acc in self._accounts:
                print(f"\n{acc.get_account_info()}")

        print(f"{'═'*50}\n")

    # ──────────────────────────────────────────────────────────
    #  CONCEPT: @staticmethod
    #
    #  A static method belongs to the CLASS, not any object.
    #  It doesn't receive 'self' (no access to instance data)
    #  or 'cls' (no access to class data).
    #
    #  Use it for UTILITY functions that are logically related
    #  to the class but don't need object/class state.
    #
    #  Called as: Customer.validate_email("test@gmail.com")
    #             or  customer_obj.validate_email("test@gmail.com")
    # ──────────────────────────────────────────────────────────
    @staticmethod
    def validate_email(email):
        """Check if email has basic valid format."""
        # CONCEPT: 'in' on a string checks for substring
        return "@" in email and "." in email.split("@")[-1]

    @staticmethod
    def validate_phone(phone):
        """Check if phone number has 10 digits."""
        # CONCEPT: str.isdigit() — True if all characters are digits
        # CONCEPT: str.replace() — remove spaces/dashes before checking
        cleaned = phone.replace(" ", "").replace("-", "")
        return cleaned.isdigit() and len(cleaned) == 10

    # ──────────────────────────────────────────────────────────
    #  CONCEPT: @classmethod  (Alternative Constructor)
    #
    #  A class method receives 'cls' (the class itself) instead
    #  of 'self'. It's often used as an ALTERNATIVE CONSTRUCTOR —
    #  a different way to create an object.
    #
    #  Called as: Customer.from_dict(data_dict)
    # ──────────────────────────────────────────────────────────
    @classmethod
    def from_dict(cls, data):
        """
        Create a Customer from a dictionary.
        Useful when loading saved customer data from a file.
        """
        customer = cls(
            name  = data["name"],
            email = data["email"],
            phone = data["phone"],
        )
        return customer

    def to_dict(self):
        """Convert customer info to a dictionary (for saving to file)."""
        return {
            "customer_id" : self.__customer_id,
            "name"        : self.name,
            "email"       : self.email,
            "phone"       : self.phone,
            "joined_on"   : self.joined_on,
            "accounts"    : [acc.to_dict() for acc in self._accounts],
        }

    # ──────────────────────────────────────────────────────────
    #  DUNDER METHODS
    # ──────────────────────────────────────────────────────────

    def __len__(self):
        """
        CONCEPT: __len__ dunder method
        Lets you use len(customer) to get number of accounts.
        Without this: len(customer) → TypeError
        With this:    len(customer) → 2  (if 2 accounts)
        """
        return len(self._accounts)

    def __contains__(self, account_number):
        """
        CONCEPT: __contains__ dunder method
        Lets you use 'in' operator:
          "ACC1000" in customer  → True or False
        Without this: 'in' would check identity, not account number.
        """
        return any(acc.account_number == account_number for acc in self._accounts)

    def __str__(self):
        return (
            f"Customer({self.__customer_id}) | "
            f"{self.name} | "
            f"{len(self._accounts)} account(s) | "
            f"Total: ₹{self.total_balance():.2f}"
        )

    def __repr__(self):
        return f"Customer(id={self.__customer_id}, name={self.name}, email={self.email})"