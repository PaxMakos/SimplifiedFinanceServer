from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Invoice, Project, SubAccount, Vendor, Transaction, Permissions
from django.core import serializers
from django.db import IntegrityError
import os
from ..operations.invoiceOperations import createInvoice
from ..operations.vendorsOperations import createVendor
from ..operations.tranactionOperations import createTransaction


@require_http_methods(["GET"])
@csrf_exempt
def getTransactions(request):
    if request.user.is_authenticated:
        try:
            fromDate = request.GET.get("fromDate")
            toDate = request.GET.get("toDate")

            transactions = Transaction.objects.filter(date__range=[fromDate, toDate])

            if not request.user.is_superuser:
                projects = Permissions.objects.filter(user=request.user)
                transactions = transactions.filter(project=projects)

            data = serializers.serialize("xml", transactions)
            return HttpResponse(data, content_type="application/xml")
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionBasic(request):
    if request.user.is_authenticated:
        try:
            invoice = Invoice.objects.get(number=request.POST.get("invoiceNumber"))

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success", "transaction": transaction.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionWithInvoice(request):
    if request.user.is_authenticated:
        try:
            invoice = createInvoice(request)
            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success", "transaction": transaction.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionNewVendor(request):
    if request.user.is_authenticated:
        try:
            vendor = createVendor(request)
            invoice = Invoice.objects.get(number=request.POST.get("invoiceNumber"))

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success", "transaction": transaction.id, "vendor": vendor.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionFull(request):
    if request.user.is_authenticated:
        try:
            invoice = createInvoice(request)
            vendor = createVendor(request)

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success", "transaction": transaction.id, "vendor": vendor.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def updateTransaction(request, transactionId):
    if request.user.is_authenticated:
        try:
            transaction = Transaction.objects.get(id=transactionId)

            transaction.date = request.POST.get("transactionDate")
            transaction.title = request.POST.get("transactionTitle")
            transaction.amount = float(request.POST.get("transactionAmount"))
            transaction.account = SubAccount.objects.get(name=request.POST.get("accountName"))
            transaction.vendor = Vendor.objects.get(name=request.POST.get("vendorName"))
            transaction.project = Project.objects.get(name=request.POST.get("projectName"))
            transaction.description = request.POST.get("transactionDescription")

            transaction.save()

            return JsonResponse({"status": "success", "transaction": transaction.id})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteTransaction(request, transactionId):
    if request.user.is_authenticated:
        try:
            transaction = Transaction.objects.get(id=transactionId)
            transaction.delete()

            return JsonResponse({"status": "success"})
        except Transaction.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Transaction does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})