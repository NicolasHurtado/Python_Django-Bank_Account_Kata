from rest_framework import serializers
from .models import Account, Transaction
from rest_framework.exceptions import ValidationError

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'

class TransactionSerializerBasic(serializers.ModelSerializer):
    balance = serializers.CharField(source='balance_after')
    class Meta:
        model = Transaction
        fields = ['date', 'type', 'amount', 'balance']

class TransactionSerializer(serializers.ModelSerializer):
    """
    Serializer for Transaction model.

    - Validates that sufficient funds are available for withdrawal or transfer transactions.
    - Adds a read-only field 'balance' to display the balance after the transaction.
    """
    balance = serializers.DecimalField(source='balance_after', max_digits=10, decimal_places=2,read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','type', 'amount', 'account', 'balance']  
    
    def validate(self, data):
        """
        Ensure that the account has sufficient funds for withdrawals or transfers.
        """
        
        account = data['account']
        amount = data['amount']
        transaction_type = data['type']

        if transaction_type in [Transaction.WITHDRAWAL, Transaction.TRANSFER] and account.balance < amount:
            raise ValidationError('Insufficient funds for this transaction.')

        return data
