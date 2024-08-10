from django.db import models
from django.core.exceptions import ValidationError

class Account(models.Model):
    iban = models.CharField(max_length=34, unique=True)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.iban

class Transaction(models.Model):
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

    def clean(self):
        print('self.amount ',self.amount)
        print('self.account.balance ',self.account.balance)

        if self.type in [self.WITHDRAWAL, self.TRANSFER] and self.account.balance < self.amount:
            raise ValidationError('Insufficient funds for this transaction.')

    def save(self, *args, **kwargs):
        if self.type == self.WITHDRAWAL or self.type == self.TRANSFER:
            self.account.balance -= self.amount
        else:
            self.account.balance += self.amount
        self.balance_after = self.account.balance
        self.account.save()
        super().save(*args, **kwargs)
