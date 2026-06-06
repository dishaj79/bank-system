# ============================================================
#  exceptions.py  —  Custom Exceptions
# ============================================================
#
#  CONCEPT: Custom Exceptions
#
#  Python has built-in exceptions like:
#    - ValueError    (wrong value)
#    - TypeError     (wrong type)
#    - FileNotFoundError  (file missing)
#
#  But in real projects, you create YOUR OWN exceptions.
#  Why? Because "InsufficientFundsError" tells you EXACTLY
#  what went wrong. "ValueError" tells you nothing specific.
#
#  CONCEPT: Inheritance (first taste!)
#  Every custom exception INHERITS from Python's built-in
#  'Exception' class. The (Exception) part means:
#  "My class is a type of Exception"
#
#  Think of it like:
#    Animal        ← parent class
#    Dog(Animal)   ← Dog IS-A Animal (inherits from Animal)
#    Cat(Animal)   ← Cat IS-A Animal
#
#  Similarly:
#    Exception              ← parent class
#    InsufficientFundsError(Exception) ← our custom child class
# ============================================================


class InsufficientFundsError(Exception):
    """
    Raised when a withdrawal or payment exceeds available balance.

    CONCEPT: __init__ with custom message
    We override __init__ to accept extra info (amount, balance)
    and build a helpful error message automatically.
    """
    def __init__(self, amount, balance):
        # 'amount' = what they tried to withdraw
        # 'balance' = what they actually have
        self.amount  = amount
        self.balance = balance
        # super() calls the PARENT class (Exception) __init__
        # We pass our custom message up to it
        # CONCEPT: super() — calls the parent class method
        message = (
            f"Cannot process ₹{amount:.2f}. "
            f"Available balance: ₹{balance:.2f}"
        )
        super().__init__(message)


class AccountNotFoundError(Exception):
    """Raised when searching for an account that doesn't exist."""
    def __init__(self, account_number):
        self.account_number = account_number
        message = f"Account '{account_number}' not found."
        super().__init__(message)


class InvalidAmountError(Exception):
    """Raised when a negative or zero amount is entered."""
    def __init__(self, amount):
        self.amount = amount
        message = f"Invalid amount: ₹{amount}. Amount must be greater than zero."
        super().__init__(message)


class AccountFrozenError(Exception):
    """Raised when trying to transact on a frozen/closed account."""
    def __init__(self, account_number):
        message = f"Account '{account_number}' is frozen. No transactions allowed."
        super().__init__(message)


# ============================================================
#  CONCEPT: How exceptions are USED (preview)
#
#  You RAISE an exception when something goes wrong:
#    raise InsufficientFundsError(5000, 1000)
#
#  You CATCH it with try/except:
#    try:
#        account.withdraw(5000)
#    except InsufficientFundsError as e:
#        print(e)   # prints your custom message
#
#  This is much better than just printing an error message,
#  because OTHER parts of the code can also catch and handle it.
# ============================================================