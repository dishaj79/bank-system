# 🏦 PyBank India — Python OOP Bank System

A fully featured **command-line Bank Account Management System** built with pure Python.  
Designed as a hands-on project to master **Object-Oriented Programming** and **Python fundamentals**.

---

## ✨ Features

| Feature | Description |
|---|---|
| 👤 Customer Management | Register, search, and manage customers |
| 🏦 Multiple Account Types | Savings (interest + min balance) & Current (overdraft) |
| 💰 Transactions | Deposit, withdraw, transfer between accounts |
| 💹 Interest | Apply interest to savings accounts |
| 🔒 Account Freeze | Freeze/unfreeze accounts |
| 📜 Transaction History | Full history with timestamps |
| 📊 Bank Reports | Stats, top customers by balance |
| 💾 Persistent Storage | Auto-save to JSON — data survives restarts |
| ✅ 48 Unit Tests | Full test coverage across all classes |

---

## 🧠 OOP Concepts Covered

| Concept | Where Used |
|---|---|
| **Abstraction** | `Account` is an Abstract Base Class (ABC) |
| **Encapsulation** | `__balance` is private, accessed via `@property` |
| **Inheritance** | `SavingsAccount` and `CurrentAccount` inherit from `Account` |
| **Polymorphism** | `withdraw()` behaves differently per account type |
| **Composition** | `Customer` HAS-A list of Accounts; `Bank` HAS-A list of Customers |
| **Abstract Methods** | `@abstractmethod` forces child classes to implement `withdraw()` |
| **Dunder Methods** | `__str__`, `__repr__`, `__len__`, `__contains__` |
| **Class Methods** | `from_dict()` as alternative constructors |
| **Static Methods** | `validate_email()`, `validate_phone()` |
| **Properties** | `@property` + `@setter` for controlled access |
| **Custom Exceptions** | `InsufficientFundsError`, `AccountFrozenError`, etc. |

## 🐍 Python Fundamentals Covered

`list comprehensions` · `dict comprehensions` · `lambda` · `sorted()` with `key=` ·  
`**kwargs` · `try/except` · `json` · `os` · `datetime` · `super()` · `getattr()` ·  
`any()` · `sum()` with generators · `enumerate()` · `next()` · `f-strings`

---


## 📁 Project Structure

```
bank-system/
├── main.py          # Entry point — interactive menu
├── account.py       # Abstract Base Class for all accounts
├── savings.py       # SavingsAccount (interest, min balance)
├── current.py       # CurrentAccount (overdraft, fees)
├── customer.py      # Customer class (owns accounts)
├── bank.py          # Bank class (manages everything)
├── exceptions.py    # Custom exception classes
├── tests/
│   └── test_bank.py # 48 unit tests
├── data/
│   └── bank_data.json  # Auto-generated persistent storage
└── README.md
```

---

## 🏗️ Architecture

```
Bank                        ← manages all customers
 └── Customer (HAS-A)       ← owns accounts (Composition)
       ├── SavingsAccount   ← IS-A Account (Inheritance)
       │     └── Transactions
       └── CurrentAccount   ← IS-A Account (Inheritance)
             └── Transactions

Account (ABC)               ← cannot be created directly (Abstraction)
  ├── __balance             ← private (Encapsulation)
  ├── withdraw() abstract   ← must be overridden (Polymorphism)
  └── deposit()             ← shared by all account types
```

---
