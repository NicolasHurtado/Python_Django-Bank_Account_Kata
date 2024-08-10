from django.test import TestCase
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient
from rest_framework import status
from .models import Account, Transaction
from datetime import datetime, timedelta

# Create your tests here.
class TransactionModelTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(iban='ES7921000813610123456789', balance=1000)

    def test_create_deposit_transaction(self):
        """Test the creation of a deposit transaction."""
        response = self.client.post('/api/transactions/', {
            'type': 'deposit',
            'amount': 100,
            'account': self.account.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=response.data['id'])
        self.assertEqual(transaction.balance_after, 1100)

    def test_create_withdrawal_transaction(self):
        """Test the creation of a withdrawal transaction with sufficient funds."""
        response = self.client.post('/api/transactions/', {
            'type': 'withdrawal',
            'amount': 500,
            'account': self.account.id
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=response.data['id'])
        self.assertEqual(transaction.balance_after, 500)

    def test_create_transfer_transaction(self):
        """Test the creation of a transfer transaction with sufficient funds."""
        response = self.client.post('/api/transactions/', {
            'type': 'transfer',
            'amount': 300,
            'account': self.account.id
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        transaction = Transaction.objects.get(id=response.data['id'])
        self.assertEqual(transaction.balance_after, 700)
    
    def test_withdrawal_insufficient_funds(self):
        """Test withdrawal transaction with insufficient funds should fail."""
        response = self.client.post('/api/transactions/', {
            'type': 'withdrawal',
            'amount': 2000,  # Trying to withdraw more than available
            'account': self.account.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)  # No transaction should be created

    def test_transfer_insufficient_funds(self):
        """Test transfer transaction with insufficient funds should fail."""
        response = self.client.post('/api/transactions/', {
            'type': 'transfer',
            'amount': 1500,  # Trying to transfer more than available
            'account': self.account.id
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Transaction.objects.count(), 0)  # No transaction should be created


class TransactionFilterTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.account = Account.objects.create(iban='ES7921000813610123456789', balance=1000)

        # Create transactions to test filters
        Transaction.objects.create(account=self.account, type='deposit', amount=100, balance_after=1100)
        Transaction.objects.create(account=self.account, type='withdrawal', amount=50, balance_after=1050)
        Transaction.objects.create(account=self.account, type='transfer', amount=200, balance_after=850)
        Transaction.objects.create(account=self.account, type='deposit', amount=150, balance_after=1000)

        # Calculate relevant dates for the tests
        self.today = datetime.now().date()
        self.yesterday = self.today - timedelta(days=1)
        self.tomorrow = self.today + timedelta(days=1)

    def test_filter_transactions_by_type(self):
        """Test filtering transactions by type."""
        response = self.client.get('/api/transactions/', {'type': 'deposit'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # There should be 2 deposits
        for transaction in response.data['results']:
            self.assertEqual(transaction['type'], 'deposit')

    def test_filter_transactions_by_date_range(self):
        """Test filtering transactions by date range."""
        # Use the dates calculated in setUp
        response = self.client.get('/api/transactions/', {
            'start_date': self.yesterday.isoformat(), 'end_date': self.tomorrow.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 4)  # There should be 4 transactions in this date range
        for transaction in response.data['results']:
            transaction_date = transaction['date'].split('T')[0]
            self.assertIn(transaction_date, [self.yesterday.isoformat(), self.today.isoformat(), self.tomorrow.isoformat()])

    def test_filter_transactions_by_type_and_date_range(self):
        """Test filtering transactions by type and date range."""
        # Use the dates calculated in setUp
        response = self.client.get('/api/transactions/', {
            'type': 'deposit', 'start_date': self.yesterday.isoformat(), 'end_date': self.tomorrow.isoformat()
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)  # There should be 2 deposits in the date range
        for transaction in response.data['results']:
            transaction_date = transaction['date'].split('T')[0]
            self.assertEqual(transaction['type'], 'deposit')
            self.assertIn(transaction_date, [self.yesterday.isoformat(), self.today.isoformat(), self.tomorrow.isoformat()])