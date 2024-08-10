from django.db import models
from django.core.exceptions import ValidationError

class Account(models.Model):
    """
    Represents a bank account.

    Fields:
    - iban: The unique IBAN identifier for the account.
    - balance: The current balance of the account, defaulting to 0.
    """
    iban = models.CharField(max_length=34, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.iban

class Transaction(models.Model):
    """
    Represents a transaction associated with a bank account.

    Fields:
    - account: The account related to the transaction.
    - date: The date and time when the transaction was created.
    - type: The type of the transaction, which can be 'deposit', 'withdrawal', or 'transfer'.
    - amount: The amount of money involved in the transaction.
    - balance_after: The account balance after the transaction is applied.

    Methods:
    - save: Overrides the save method to update the account balance based on the transaction type.
    """

    DEPOSIT = 'deposit'
    WITHDRAWAL = 'withdrawal'
    TRANSFER = 'transfer'
    
    TRANSACTION_TYPES = [
        (DEPOSIT, 'Deposit'),
        (WITHDRAWAL, 'Withdrawal'),
        (TRANSFER, 'Transfer'),
    ]
    
    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    date = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance_after = models.DecimalField(max_digits=10, decimal_places=2, default=0)


    def save(self, *args, **kwargs):
        """
        Overrides the save method to update the account balance 
        depending on the transaction type before saving the transaction.
        """
        if self.type == self.WITHDRAWAL or self.type == self.TRANSFER:
            self.account.balance -= self.amount
        else:
            self.account.balance += self.amount
        self.balance_after = self.account.balance
        self.account.save()
        super().save(*args, **kwargs)
