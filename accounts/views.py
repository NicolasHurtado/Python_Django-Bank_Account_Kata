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
    """
    API view to list and create transactions.

    - GET: Retrieve a list of transactions with optional filters for type, date range, and ordering.
    - POST: Create a new transaction, ensuring that there are sufficient funds for withdrawals or transfers.
    """

    queryset = Transaction.objects.all().order_by('-date')
    serializer_class = TransactionSerializerBasic
    create_serializer_class = TransactionSerializer
    filter_backends = [django_filters.DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = TransactionFilter
    ordering_fields = ['date']
    pagination_class = StandardResultsSetPagination

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.request.method == 'POST':
            return self.create_serializer_class 
        return self.serializer_class 
    
    @swagger_auto_schema(
        operation_description="Retrieve a list of transactions, optionally filtered by type or date range.",
        responses={200: TransactionSerializerBasic(many=True)},
        manual_parameters=[
            openapi.Parameter('type', openapi.IN_QUERY, description="Filter by transaction type (deposit, withdrawal, transfer)", type=openapi.TYPE_ARRAY,items=openapi.Items(type=openapi.TYPE_STRING),collection_format='multi'),
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


class AccountDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
