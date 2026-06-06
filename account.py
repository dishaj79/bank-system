# ============================================================
#  account.py  —  Abstract Base Account Class
# ============================================================
#
#  CONCEPTS covered here:
#
#  1. ABSTRACTION  — Hide complexity, show only what's needed
#  2. ENCAPSULATION — Bundle data + methods, protect private data
#  3. ABC (Abstract Base Class) — A blueprint that CANNOT be
#     created directly. Forces child classes to implement methods.
#  4. @property — Access private data safely like an attribute
#  5. @abstractmethod — Method that MUST be overridden by children
#  6. __balance (name mangling) — True private variable in Python
# ============================================================

from abc import ABC, abstractmethod   # ABC = Abstract Base Class
from datetime import datetime
from exceptions import(
    InsufficientFundsError,
    InvalidAmountError,
    AccountFrozenError
)

class Account(ABC):
    """
    Abstract Base Class for all bank accounts.
 
    CONCEPT: Abstract Class (Abstraction)
    ─────────────────────────────────────
    An abstract class is a CLASS TEMPLATE — it defines WHAT
    methods must exist, but doesn't fully implement all of them.
 
    You CANNOT do:  acc = Account(...)   ← will raise an error!
    You CAN do:     acc = SavingsAccount(...)  ← child class is fine
 
    Why? Because "Account" is too generic. Every real account
    must be either Savings or Current. ABC enforces this rule.
 
    Think of it like:
      'Shape' is abstract — you can't draw "a shape"
      'Circle' and 'Square' are concrete — you CAN draw these
 
    CONCEPT: Encapsulation
    ──────────────────────
    We HIDE the balance using __balance (double underscore).
    No one can do account.__balance = 99999 from outside.
    They MUST use deposit() and withdraw() — controlled access.
    This protects the data integrity of the account.
    """
 
    # ----------------------------------------------------------
    # CONCEPT: Class variable vs Instance variable
    #
    # Class variable: shared by ALL objects of the class
    # Instance variable (self.x): unique to each object
    #
    # Here, _next_account_number is shared — every new account
    # gets the next number in sequence (like a real bank!)
    # ----------------------------------------------------------
    _next_account_number=1000  # Class variable — shared counter

    def __init__(self, owner_name, initial_deposit=0.0):
        # ── Public attributes (accessible from anywhere) ───────
        self.owner_name = owner_name
        self.account_type="Generic"   # Overridden by child classes
        self.is_frozen=False

        # ── Protected attribute (convention: single underscore _)
        # "Protected" means: please don't access this from outside,
        # but child classes CAN use it. It's a CONVENTION, not enforced.
        self._transaction_history=[]

        # ── Private attribute (double underscore __)
        # CONCEPT: Name Mangling
        # Python renames __balance to _Account__balance internally.
        # This makes it very hard to accidentally access from outside.
        # Access it only through @property methods below.
        self.__balance=0.0

        # ── Auto-generate account number ───────────────────────
        # CONCEPT: Accessing & updating a class variable via self
        self.account_number=f"ACC{Account._next_account_number:04d}"
        Account._next_account_number+=1 # Increment for next account

        self.created_at=datetime.now().strftime("%Y-%m-%d %H:%M")

        # Deposit initial amount if provided
        if initial_deposit>0:
            self._credit(initial_deposit, "Initial Deposit")
        
    # ──────────────────────────────────────────────────────────
    #  CONCEPT: @property decorator
    #
    #  @property turns a METHOD into an ATTRIBUTE-like accessor.
    #  Instead of:  account.get_balance()   (method call)
    #  You write:   account.balance          (looks like attribute)
    #
    #  But the balance is still PROTECTED — no setter means
    #  no one can do: account.balance = 99999
    # ──────────────────────────────────────────────────────────
    @property
    def balance(self):
        """Read-only access to the private balance."""
        return self.__balance
    
    # ──────────────────────────────────────────────────────────
    #  CONCEPT: @abstractmethod
    #
    #  Any method marked @abstractmethod MUST be implemented
    #  by every child class. If a child forgets, Python raises
    #  an error when you try to create that child object.
    #
    #  This is how ABC ENFORCES a contract:
    #  "Every account type MUST have its own withdraw() logic"
    # ──────────────────────────────────────────────────────────
    @abstractmethod
    def withdraw(self, amount):
        """
        Withdraw money. Each account type handles this differently:
        - SavingsAccount: cannot go below zero
        - CurrentAccount: can go below zero (overdraft)
        """
        pass   # 'pass' = no implementation here, child must do it
 
    @abstractmethod
    def get_account_info(self):
        """Return a string summary specific to the account type."""
        pass

    # ──────────────────────────────────────────────────────────
    #  CONCRETE METHODS (fully implemented — shared by all children)
    #
    #  CONCEPT: Code Reuse through Inheritance
    #  deposit(), get_history(), freeze() etc. work the SAME
    #  for all account types, so we write them ONCE here.
    #  Child classes inherit them for free!
    # ──────────────────────────────────────────────────────────

    def deposit(self, amount):
        """Deposit money into the account."""
        self._validate_amount(amount)
        self._check_frozen()
        self._credit(amount,"Deposit")
        print(f"✅ ₹{amount:.2f} deposited. New balance: ₹{self.__balance:.2f}")

    def get_history(self, last_n=None):
        """
        Print transaction history.
        last_n = show only last N transactions (None = show all)
        """
        if not self._transaction_history:
            print("No transactions yet.")
            return
        
        # CONCEPT: Slicing
        # list[-5:]  means "last 5 items"
        # list[:]    means "all items" (copy)
        history = self._transaction_history[-last_n:] if last_n else self._transaction_history
        print(f"\n{'─'*55}")
        print(f"  📜 Transaction History — {self.account_number}")
        print(f"{'─'*55}")

        # CONCEPT: enumerate with start=1 gives 1-based index
        for i, txn in enumerate(history, start=1):
            icon = "⬆️ " if txn["type"] == "credit" else "⬇️ "
            print(
                f"  {i:>2}. {icon} {txn['description']:<20} "
                f"₹{txn['amount']:>10.2f}   "
                f"Balance: ₹{txn['balance']:>10.2f}   "
                f"{txn['date']}"
            )
        print(f"{'─'*55}\n")

        def freeze(self):
            """Freeze the account — no transactions allowed."""
            self.is_frozen=True
            print(f"🔒 Account {self.account_number} has been frozen.")

        def unfreeze(self):
            """Unfreeze the account."""
            self.is_frozen = False
            print(f"🔓 Account {self.account_number} has been unfrozen.")

        def transfer(self, target_account, amount):
            """Transfer money to another account."""
            print(f"\n💸 Transferring ₹{amount:.2f} to {target_account.account_number}...")
            self.withdraw(amount)                              # Uses THIS account's withdraw
            target_account._credit(amount, f"Transfer from {self.account_number}")
            print(f"✅ Transfer complete!")

        # ──────────────────────────────────────────────────────────
        #  PRIVATE / PROTECTED HELPERS
        # ──────────────────────────────────────────────────────────
    
        def _credit(self, amount, description="Credit"):
            """
            Internal method to ADD money to balance.
            Protected (_) because child classes need to call it.
            """
            self.__balance += amount
            self._record_transaction("credit", amount, description)
    
        def _debit(self, amount, description="Debit"):
            """
            Internal method to SUBTRACT money from balance.
            Protected (_) because child classes need to call it.
            """
            self.__balance -= amount
            self._record_transaction("debit", amount, description)
    
        def _record_transaction(self, txn_type, amount, description):
            """Add a transaction entry to history."""
            # CONCEPT: Appending a dictionary to a list
            self._transaction_history.append({
                "type"       : txn_type,
                "amount"     : amount,
                "description": description,
                "balance"    : self.__balance,
                "date"       : datetime.now().strftime("%Y-%m-%d %H:%M"),
            })
    
        def _validate_amount(self, amount):
            """Raise InvalidAmountError if amount is zero or negative."""
            if amount <= 0:
                raise InvalidAmountError(amount)
    
        def _check_frozen(self):
            """Raise AccountFrozenError if account is frozen."""
            if self.is_frozen:
                raise AccountFrozenError(self.account_number)
            
        
        # ──────────────────────────────────────────────────────────
        #  DUNDER METHODS
        #
        #  CONCEPT: Dunder (magic) methods
        #  Methods with double underscores on both sides: __str__, __repr__
        #  Python calls these automatically in certain situations.
        #
        #  __str__  → called when you print(object)
        #  __repr__ → called in the Python shell / debugging
        # ──────────────────────────────────────────────────────────
    
        def __str__(self):
            status = "🔒 Frozen" if self.is_frozen else "✅ Active"
            return (
                f"{'─'*45}\n"
                f"  🏦 {self.account_type} Account\n"
                f"  👤 Owner   : {self.owner_name}\n"
                f"  🔢 Number  : {self.account_number}\n"
                f"  💰 Balance : ₹{self.balance:.2f}\n"
                f"  📅 Opened  : {self.created_at}\n"
                f"  🔑 Status  : {status}\n"
                f"{'─'*45}"
            )
    
        def __repr__(self):
            return f"Account(number={self.account_number}, owner={self.owner_name}, balance={self.balance})"