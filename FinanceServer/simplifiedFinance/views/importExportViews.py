from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Vendor, Invoice, SubAccount, Transaction, Project, Permissions
import pandas as pd
import os


@require_http_methods(["POST"])
@csrf_exempt
def importProjects(request):
    # import projects from a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            projects = pd.read_csv(file)
            counter = 0

            for project in projects:
                name = project.get("name")

                if not Project.objects.filter(name=name).exists():
                    project = Project(name=name,
                                      description=project.get("description"),
                                      startDate=project.get("startDate"),
                                      endDate=project.get("endDate"),
                                      status=project.get("status"))
                    project.save()
                    counter += 1

            return JsonResponse({"status": "success", "message": f"Successfully imported {counter} projects."})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def importVendors(request):
    # import vendors from a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            vendors = pd.read_csv(file)
            counter = 0

            for vendor in vendors:
                name = vendor.get("name")

                if not Vendor.objects.filter(name=name).exists():
                    vendor = Vendor(name=name,
                                    address=vendor.get("address"),
                                    NIPNumber=vendor.get("NIPNumber"),
                                    accountNumber=vendor.get("accountNumber"))
                    vendor.save()
                    counter += 1

            return JsonResponse({"status": "success", "message": f"Successfully imported {counter} vendors."})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def importSubAccounts(request):
    # import subaccounts from a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            subAccounts = pd.read_csv(file)
            counter = 0

            for subAccount in subAccounts:
                name = subAccount.get("name")

                if not SubAccount.objects.filter(name=name).exists():
                    subAccount = SubAccount(name=name,
                                            accountNumber=subAccount.get("accountNumber"),
                                            balance=subAccount.get("balance"))
                    subAccount.save()
                    counter += 1

            return JsonResponse({"status": "success", "message": f"Successfully imported {counter} subaccounts."})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def importTransactions(request):
    # import transactions from a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            transactions = pd.read_csv(file)
            counter = 0

            for transaction in transactions:
                title = transaction.get("title")
                amount = transaction.get("amount")
                date = transaction.get("date")
                account = SubAccount.objects.get(name=transaction.get("account"))
                vendor = Vendor.objects.get(name=transaction.get("vendor"))
                project = Project.objects.get(name=transaction.get("project")) if transaction.get("project") else None
                description = transaction.get("description")
                invoice = Invoice.objects.get(number=transaction.get("invoice")) if transaction.get("invoice") else None

                account.balance += amount
                account.save()

                transaction = Transaction(date=date,
                                          title=title,
                                          amount=amount,
                                          account=account,
                                          vendor=vendor,
                                          project=project,
                                          description=description,
                                          invoice=invoice)
                transaction.save()
                counter += 1

            return JsonResponse({"status": "success", "message": f"Successfully imported {counter} transactions."})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


def pathCheck():
    # Check if the exports directory exists, if not create it
    if not os.path.exists(os.path.join(os.path.dirname(__file__), "..", "exports")):
        os.makedirs(os.path.join(os.path.dirname(__file__), "..", "exports"))


@require_http_methods(["GET"])
@csrf_exempt
def exportProjects(request):
    # export projects to a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            pathCheck()

            projects = Project.objects.all()
            projects = pd.DataFrame(projects.values())
            projects.to_csv(os.path.join(os.path.dirname(__file__), "..", "exports", "projects.csv"), index=False)

            response = HttpResponse(open("projects.csv", "rb"), content_type="application/force-download")
            response["Content-Disposition"] = "attachment; filename=projects.csv"
            return response
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def exportVendors(request):
    # export vendors to a CSV file
    try:
        if request.user.is_authenticated:
            pathCheck()

            vendors = Vendor.objects.all()
            vendors = pd.DataFrame(vendors.values())
            vendors.to_csv(os.path.join(os.path.dirname(__file__), "..", "exports", "vendors.csv"), index=False)

            response = HttpResponse(open("vendors.csv", "rb"), content_type="application/force-download")
            response["Content-Disposition"] = "attachment; filename=vendors.csv"
            return response
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def exportSubAccounts(request):
    # export subaccounts to a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            pathCheck()

            subAccounts = SubAccount.objects.all()
            subAccounts = pd.DataFrame(subAccounts.values())
            subAccounts.to_csv(os.path.join(os.path.dirname(__file__), "..", "exports", "subAccounts.csv"), index=False)

            response = HttpResponse(open("subAccounts.csv", "rb"), content_type="application/force-download")
            response["Content-Disposition"] = "attachment; filename=subAccounts.csv"
            return response
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def exportTransactions(request):
    # export transactions to a CSV file
    try:
        if request.user.is_authenticated:
            pathCheck()

            fromDate = request.GET.get("fromDate")
            toDate = request.GET.get("toDate")
            project = Project.objects.get(name=request.GET.get("project")) if request.GET.get("project") else None

            transactions = Transaction.objects.filter(date__range=[fromDate, toDate])

            if not request.user.is_superuser:
                projects = Permissions.objects.filter(user=request.user)
                transactions = transactions.filter(project=projects)

            transactions = transactions.filter(project=project) if project else transactions

            transactions = pd.DataFrame(transactions.values())
            transactions.to_csv(os.path.join(os.path.dirname(__file__), "..", "exports", "transactions.csv"),
                                index=False)

            response = HttpResponse(open("transactions.csv", "rb"), content_type="application/force-download")
            response["Content-Disposition"] = "attachment; filename=transactions.csv"
            return response
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})