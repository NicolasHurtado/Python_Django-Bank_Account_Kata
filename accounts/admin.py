from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ["id", "iban", "balance"]

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["id", "account", "date", "type", "amount", "balance_after"]