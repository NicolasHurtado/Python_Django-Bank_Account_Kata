from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from django_filters import rest_framework as django_filters
from .filters import TransactionFilter
from .models import Account, Transaction
from .serializers import AccountSerializer, TransactionSerializer, TransactionSerializerBasic
from .pagination import StandardResultsSetPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
    @swagger_auto_schema(
        operation_description="Retrieve a list of transactions, optionally filtered by type or date range.",
        responses={200: TransactionSerializerBasic(many=True)},
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Filter by transaction type (deposit-withdrawal-transfer)", type=openapi.TYPE_STRING),
            openapi.Parameter('start_date', openapi.IN_QUERY, description="Filter transactions after this date (yyyy-mm-dd)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('end_date', openapi.IN_QUERY, description="Filter transactions before this date (yyyy-mm-dd)", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('ordering', openapi.IN_QUERY, description="Sort account statement by date in ascending(date) and descending order(-date).", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ]
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        operation_description="Create a new transaction, ensuring sufficient funds.",
        responses={201: TransactionSerializer(), 400: "Validation error or insufficient funds"}
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

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
