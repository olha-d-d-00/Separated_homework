import unittest


class InsufficientFunds(Exception):
    pass

class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive")
        self.balance += amount

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds("Insufficient funds")
        self.balance -= amount

    def transfer(self, other_account, amount):
        if not isinstance(other_account, BankAccount):
            raise TypeError("Other account must be a BankAccount instance")
        self.withdraw(amount)
        other_account.deposit(amount)

    def get_balance(self):
        return self.balance


class BankAccountTestDeposit(unittest.TestCase):
    def test_deposit(self):
        bank_account = BankAccount(100)
        bank_account.deposit(50)
        self.assertEqual(bank_account.get_balance(), 150)

    def test_deposit_when_balance_zero(self):
        bank_account = BankAccount(0)
        bank_account.deposit(50)
        self.assertEqual(bank_account.get_balance(), 50)

    def test_account_replenishment_by_zero(self):
        bank_account = BankAccount(0)
        with self.assertRaises(ValueError) as zero_deposit:
            bank_account.deposit(0)
        self.assertEqual(str(zero_deposit.exception), "Deposit amount must be positive")

    def test_account_replenishment_by_negative_value(self):
        bank_account = BankAccount(0)
        with self.assertRaises(ValueError) as negative_value:
            bank_account.deposit(-100)
        self.assertEqual(str(negative_value.exception), "Deposit amount must be positive")


class BankAccountTestWithdrawal(unittest.TestCase):
    def test_withdrawal(self):
        bank_account = BankAccount(100)
        bank_account.withdraw(50)
        self.assertEqual(bank_account.get_balance(), 50)

    def test_withdrawal_with_negative_value(self):
        bank_account = BankAccount(100)
        with self.assertRaises(ValueError) as negative_value_withdrawal:
            bank_account.withdraw(-10)
        self.assertEqual(str(negative_value_withdrawal.exception), "Withdrawal amount must be positive")


    def test_withdrawal_with_zero_value(self):
        bank_account = BankAccount(100)
        with self.assertRaises(ValueError) as zero_value_withdrawal:
            bank_account.withdraw(0)
        self.assertEqual(str(zero_value_withdrawal.exception), "Withdrawal amount must be positive")

    def test_withdrawal_over_customer_deposit(self):
        bank_account = BankAccount(50)
        with self.assertRaises(InsufficientFunds) as withdrawal_over_balance:
            bank_account.withdraw(150)
        self.assertEqual(str(withdrawal_over_balance.exception), "Insufficient funds")


class BankAccountTestTransfer(unittest.TestCase):
    def test_account_transfer(self):
        sender = BankAccount(100)
        receiver = BankAccount(50)
        sender.transfer(receiver, 20)
        self.assertEqual(sender.get_balance() ,80)
        self.assertEqual(receiver.get_balance(), 70)

    def test_transfer_with_zero(self):
        sender = BankAccount(100)
        receiver = BankAccount(50)
        with self.assertRaises(ValueError) as zero_value:
            sender.transfer(receiver, 50)
        self.assertEqual(str(zero_value.exception), "Withdrawal amount must be positive")

    def test_transfer_with_negative_value(self):
        sender = BankAccount(400)
        receiver = BankAccount(100)
        with self.assertRaises(ValueError) as negative_value:
            sender.transfer(receiver, -10)
        self.assertEqual(str(negative_value.exception), "Withdrawal amount must be positive")