from django_filters import rest_framework as django_filters
from .models import Transaction
class TransactionFilter(django_filters.FilterSet):
    start_date = django_filters.DateFilter(field_name="date", lookup_expr='gte')
    end_date = django_filters.DateFilter(field_name="date", lookup_expr='lte')
    type = django_filters.MultipleChoiceFilter(choices=Transaction.TRANSACTION_TYPES)

    class Meta:
        model = Transaction
        fields = ['type', 'start_date', 'end_date']