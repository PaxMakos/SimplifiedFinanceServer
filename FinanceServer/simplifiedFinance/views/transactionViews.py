from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Invoice, Project, SubAccount, Vendor, Transaction, Permissions
from ..operations.invoiceOperations import createInvoice
from ..operations.vendorsOperations import createVendor
from ..operations.transactionOperations import createTransaction
from datetime import datetime


@require_http_methods(["GET"])
@csrf_exempt
def getTransactions(request):
    # returns transactions that user is authorized to see
    try:
        if request.user.is_authenticated:
            fromDate = request.GET.get("fromDate")
            toDate = request.GET.get("toDate")

            transactions = Transaction.objects.all()

            if fromDate:
                transactions = transactions.filter(date__gte=datetime.strptime(fromDate, "%Y-%m-%d"))

            if toDate:
                transactions = transactions.filter(date__lte=datetime.strptime(toDate, "%Y-%m-%d"))

            if not request.user.is_superuser:
                projects = Permissions.objects.filter(user=request.user)
                transactions = transactions.filter(project=projects)
            toReturn = []

            for transaction in transactions:
                toReturn.append({"id": transaction.id,
                                 "date": transaction.date,
                                 "title": transaction.title,
                                 "amount": transaction.amount,
                                 "account": transaction.account.name,
                                 "vendor": transaction.vendor.name,
                                 "project": transaction.project.name,
                                 "description": transaction.description
                })

            return JsonResponse({"status": "success", "transactions": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionBasic(request):
    # creates a transaction with an existing invoice and vendor
    try:
        if request.user.is_authenticated:
            invoice = Invoice.objects.get(number=request.POST.get("invoiceNumber"))

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success", "message": f"Transaction {transaction.title} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionWithInvoice(request):
    # creates a transaction with a new invoice and existing vendor
    try:
        if request.user.is_authenticated:
            invoice = createInvoice(request)
            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success",
                                 "message": f"Transaction {transaction.title} and invoice {invoice.number} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionNewVendor(request):
    # creates a transaction with a new vendor and existing invoice
    try:
        if request.user.is_authenticated:
            vendor = createVendor(request)
            invoice = Invoice.objects.get(number=request.POST.get("invoiceNumber"))

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success",
                                 "message": f"Transaction {transaction.title} and vendor {vendor.name} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createTransactionFull(request):
    # creates a transaction with a new vendor and invoice
    try:
        if request.user.is_authenticated:
            invoice = createInvoice(request)
            vendor = createVendor(request)

            transaction = createTransaction(request, invoice)

            return JsonResponse({"status": "success",
                                 "message": f"Transaction {transaction.title}, vendor and invoice created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def updateTransaction(request, transactionId):
    # updates a transaction
    try:
        if request.user.is_authenticated:
            transaction = Transaction.objects.get(id=transactionId)

            if request.POST.get("transactionTitle"):
                transaction.title = request.POST.get("transactionTitle")
            if request.POST.get("transactionDate"):
                transaction.date = request.POST.get("transactionDate")
            if request.POST.get("transactionAmount"):
                if transaction.amount != float(request.POST.get("transactionAmount")):
                    account = transaction.account
                    account.balance -= transaction.amount
                    account.balance += float(request.POST.get("transactionAmount"))
                    account.save()
                    transaction.amount = float(request.POST.get("transactionAmount"))
            if request.POST.get("accountName"):
                transaction.account = SubAccount.objects.get(name=request.POST.get("accountName"))
            if request.POST.get("vendorName"):
                transaction.vendor = Vendor.objects.get(name=request.POST.get("vendorName"))
            if request.POST.get("projectName"):
                transaction.project = Project.objects.get(name=request.POST.get("projectName"))
            if request.POST.get("transactionDescription"):
                transaction.description = request.POST.get("transactionDescription")

            transaction.save()

            return JsonResponse({"status": "success", "message": f"Transaction {transaction.title} updated"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Transaction.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteTransaction(request, transactionId):
    # deletes a transaction if user is authenticated
    try:
        if request.user.is_authenticated:
            transaction = Transaction.objects.get(id=transactionId)

            account = transaction.account
            account.balance -= transaction.amount

            transaction.delete()

            return JsonResponse({"status": "success", "message": f"Transaction {transactionId} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Transaction.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Transaction does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
