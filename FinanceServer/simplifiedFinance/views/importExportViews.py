from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Vendor, Invoice, SubAccount, Transaction, Project, Permissions
import pandas as pd
import os
from decimal import Decimal as decimal


@require_http_methods(["POST"])
@csrf_exempt
def importProjects(request):
    # import projects from a CSV file
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            projects = pd.read_csv(file)
            counter = 0

            for index, project in projects.iterrows():
                name = project["name"]

                if not Project.objects.filter(name=name).exists():
                    project = Project(name=name,
                                      description=project["description"],
                                      startDate=project["startDate"],
                                      endDate=project["endDate"],
                                      status=project["status"])
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
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            vendors = pd.read_csv(file)
            counter = 0

            for index, vendor in vendors.iterrows():
                name = vendor["name"]

                if not Vendor.objects.filter(name=name).exists():
                    vendor = Vendor(name=name,
                                    postcode=vendor["postCode"],
                                    city=vendor["city"],
                                    street=vendor["street"],
                                    NIPNumber=vendor["NIPNumber"],
                                    accountNumber=vendor["accountNumber"])
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
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            subAccounts = pd.read_csv(file)
            counter = 0

            for index, subAccount in subAccounts.iterrows():
                name = subAccount["name"]

                if not SubAccount.objects.filter(name=name).exists():
                    subAccount = SubAccount(name=name,
                                            accountNumber=subAccount["accountNumber"],
                                            balance=float(subAccount["balance"]))
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
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            file = request.FILES.get("file")
            transactions = pd.read_csv(file)
            counter = 0

            for index, transaction in transactions.iterrows():
                title = transaction["title"]
                amount = float(transaction["amount"])
                date = transaction["date"]
                account = SubAccount.objects.get(name=transaction["account"])
                vendor = Vendor.objects.get(name=transaction["vendor"])
                project = Project.objects.get(name=transaction["project"]) if pd.notna(transaction["project"]) else None
                description = transaction["description"]
                invoice = Invoice.objects.get(number=transaction["invoice"]) if pd.notna(transaction["invoice"]) else None

                transactionSaved = Transaction(date=date,
                                               title=title,
                                               amount=amount,
                                               account=account,
                                               vendor=vendor,
                                               project=project,
                                               description=description,
                                               invoice=invoice)
                transactionSaved.save()

                account.balance += decimal(transactionSaved.amount)
                account.save()

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

            transactions = Transaction.objects.all()
            transactions = transactions.filter(date__gte=fromDate) if fromDate else transactions
            transactions = transactions.filter(date__lte=toDate) if toDate else transactions

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