from django.contrib import admin
from .models import Invoice, Project, SubAccount, Vendor, Transaction, Permissions, Return


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ["date", "number"]
    search_fields = ["number"]


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["name", "startDate", "endDate", "status"]
    list_filter = ["status"]
    search_fields = ["name"]


@admin.register(SubAccount)
class SubAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "balance"]
    search_fields = ["name"]


@admin.register(Vendor)
class VendorAdmin(admin.ModelAdmin):
    list_display = ["name", "NIPNumber", "accountNumber"]
    search_fields = ["name", "NIPNumber"]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["date", "title", "amount", "account", "vendor", "project"]
    list_filter = ["vendor", "project"]
    search_fields = ["title"]


@admin.register(Permissions)
class Permissions(admin.ModelAdmin):
    list_display = ["user", "project"]
    search_fields = ["user"]


@admin.register(Return)
class Returns(admin.ModelAdmin):
    list_display = ["date", "title", "amount"]
    search_fields = ["title"]


