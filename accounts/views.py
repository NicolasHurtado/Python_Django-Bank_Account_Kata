from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as django_filters
from .filters import TransactionFilter
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, TransactionSerializerBasic
from .pagination import StandardResultsSetPagination

class AccountListCreate(generics.ListCreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer



class TransactionListCreate(generics.ListCreateAPIView):
    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializerBasic
    create_serializer_class = TransactionSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return self.create_serializer_class  # Serializador para creación
        return self.serializer_class  # Serializador para listado

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        amount = serializer.validated_data['amount']
        transaction_type = serializer.validated_data['type']

        # Validar fondos antes de crear la transacción
        if transaction_type in [Transaction.WITHDRAWAL, Transaction.TRANSFER] and account.balance < amount:
            raise ValidationError('Insufficient funds for this transaction.')

        # Si la validación es exitosa, se guarda la transacción
        serializer.save()

class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
