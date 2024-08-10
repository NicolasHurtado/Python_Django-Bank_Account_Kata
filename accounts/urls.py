from django.urls import path
from .views import AccountListCreate, TransactionListCreate, AccountDetail

urlpatterns = [
    path('accounts/', AccountListCreate.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', AccountDetail.as_view(), name='account-detail'),
    path('transactions/', TransactionListCreate.as_view(), name='transaction-list-create'),
]
