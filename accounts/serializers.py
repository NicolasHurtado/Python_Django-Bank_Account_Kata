from rest_framework import serializers
from .models import Account, Transaction

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
    balance = serializers.DecimalField(source='balance_after', max_digits=10, decimal_places=2,read_only=True)
    class Meta:
        model = Transaction
        fields = ['id','type', 'amount', 'account', 'balance']  
