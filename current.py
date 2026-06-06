# ============================================================
#  current.py  —  CurrentAccount Class
# ============================================================
#
#  CONCEPTS covered here:
#
#  1. POLYMORPHISM  — Same withdraw() name, totally different
#                     behaviour from SavingsAccount
#  2. INHERITANCE   — Gets all of Account's methods for free
#  3. Method Override — Our own withdraw() with overdraft logic
#
#  KEY DIFFERENCE from SavingsAccount:
#    SavingsAccount → Cannot go below ₹500 (no overdraft)
#    CurrentAccount → CAN go below ₹0 up to overdraft limit
#                     (like a business credit facility)
# ============================================================

from account import Account
from exceptions import InsufficientFundsError, InvalidAmountError


class CurrentAccount(Account):
    """
    A current account for businesses — supports overdraft.

    CONCEPT: Polymorphism in action
    ────────────────────────────────
    Both SavingsAccount and CurrentAccount inherit from Account.
    Both have a withdraw() method.
    But they behave COMPLETELY DIFFERENTLY:

    savings.withdraw(5000)  → checks minimum balance, no overdraft
    current.withdraw(5000)  → allows overdraft up to a limit

    This is polymorphism:
    "Same interface (method name), different behaviour"

    Real-world analogy:
      Both a car and a bicycle have "accelerate()"
      But HOW they accelerate is totally different!
    """

    DEFAULT_OVERDRAFT = 10000.0   # Class variable — default overdraft limit

    def __init__(self, owner_name, initial_deposit=0.0, overdraft_limit=None):

        # Always call parent __init__ first
        super().__init__(owner_name, initial_deposit)

        self.account_type   = "Current"
        self._overdraft_limit = overdraft_limit or CurrentAccount.DEFAULT_OVERDRAFT
        self.transaction_fee  = 5.0    # ₹5 fee per withdrawal (business account)

    @property
    def overdraft_limit(self):
        return self._overdraft_limit

    @overdraft_limit.setter
    def overdraft_limit(self, new_limit):
        """Validate and update overdraft limit."""
        if new_limit < 0:
            raise ValueError("Overdraft limit cannot be negative.")
        self._overdraft_limit = new_limit
        print(f"✅ Overdraft limit updated to ₹{new_limit:.2f}")

    # ──────────────────────────────────────────────────────────
    #  CONCEPT: Polymorphism — Different withdraw() behaviour
    #
    #  SavingsAccount.withdraw() → blocks if below ₹500
    #  CurrentAccount.withdraw() → allows going into negative
    #                              up to the overdraft limit
    #                              but charges a ₹5 fee
    # ──────────────────────────────────────────────────────────
    def withdraw(self, amount):
        """
        Withdraw from current account.
        Rules:
          - Amount must be positive
          - Balance CAN go negative, but not beyond overdraft limit
          - Each withdrawal has a ₹5 transaction fee
        """
        self._validate_amount(amount)
        self._check_frozen()

        # Total cost = withdrawal amount + transaction fee
        total_cost = amount + self.transaction_fee

        # CONCEPT: The overdraft check
        # Effective balance = current balance + overdraft allowance
        # Example: balance = ₹200, overdraft = ₹10000
        #          effective = ₹10200 — can withdraw up to this
        effective_balance = self.balance + self._overdraft_limit

        if total_cost > effective_balance:
            raise InsufficientFundsError(total_cost, effective_balance)

        # All checks passed — debit amount + fee separately
        self._debit(amount, "Withdrawal")
        self._debit(self.transaction_fee, "Transaction fee")

        # CONCEPT: Ternary expression — one-line if/else
        # value = X if condition else Y
        overdraft_msg = f" (Overdraft active ⚠️)" if self.balance < 0 else ""
        print(
            f"✅ ₹{amount:.2f} withdrawn (Fee: ₹{self.transaction_fee:.2f}). "
            f"Balance: ₹{self.balance:.2f}{overdraft_msg}"
        )

    def waive_fee(self):
        """Waive the transaction fee (e.g. for premium customers)."""
        self.transaction_fee = 0.0
        print("✅ Transaction fee waived.")

    def get_account_info(self):
        """Return current-account-specific summary."""
        overdraft_used = max(0, -self.balance)   # How much overdraft is being used
        return (
            f"{self}\n"
            f"  🏧 Overdraft Limit : ₹{self._overdraft_limit:.2f}\n"
            f"  ⚠️  Overdraft Used  : ₹{overdraft_used:.2f}\n"
            f"  💸 Transaction Fee : ₹{self.transaction_fee:.2f}\n"
            f"  📊 Transactions    : {len(self._transaction_history)}"
        )
    
    def to_dict(self):
        """Convert CurrentAccount to dictionary for saving."""
        return {
            "account_type"   : self.account_type,
            "account_number" : self.account_number,
            "owner_name"     : self.owner_name,
            "balance"        : self.balance,
            "overdraft_limit": self._overdraft_limit,
            "transaction_fee": self.transaction_fee,
            "is_frozen"      : self.is_frozen,
            "created_at"     : self.created_at,
            "transactions"   : self._transaction_history,
        }
 
    @classmethod
    def from_dict(cls, data):
        """Rebuild a CurrentAccount from a dictionary."""
        acc = cls(data["owner_name"], overdraft_limit=data["overdraft_limit"])
        acc.account_number       = data["account_number"]
        acc.is_frozen            = data["is_frozen"]
        acc.created_at           = data["created_at"]
        acc.transaction_fee      = data["transaction_fee"]
        acc._transaction_history = data["transactions"]
        acc._Account__balance    = data["balance"]
        return acc