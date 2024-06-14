import os
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from ..models import SubAccount, Vendor, Transaction, Project, Invoice, Permissions
from django.contrib.auth.models import User


@require_http_methods(["GET"])
@csrf_exempt
def isConfigured(reguest):
    try:
        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "r")
        file.close()
        return JsonResponse({"configured": True})
    except FileNotFoundError:
        return JsonResponse({"configured": False})


@require_http_methods(["POST"])
@csrf_exempt
def configure(request):
    try:
        Transaction.objects.all().delete()
        SubAccount.objects.all().delete()
        Vendor.objects.all().delete()
        Permissions.objects.all().delete()
        Project.objects.all().delete()
        Invoice.objects.all().delete()
        User.objects.all().delete()

        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "w")

        organization = request.POST.get("organization")
        address = request.POST.get("address")
        NIP = request.POST.get("NIP")
        accountNumber = request.POST.get("accountNumber")
        accountBalance = request.POST.get("accountBalance")
        treasurerName = request.POST.get("treasurerName")

        treasurerLogin = request.POST.get("treasurerLogin")
        treasurerPassword = request.POST.get("treasurerPassword")

        config = {
            "organization": organization,
            "address": address,
            "NIP": NIP,
            "accountNumber": accountNumber,
            "treasurerName": treasurerName,
            "treasurerLogin": treasurerLogin
        }

        file.write(json.dumps(config))
        file.close()

        SubAccount.objects.create(
            name="Główny rachunek",
            accountNumber=accountNumber,
            balance=accountBalance
        )

        User.objects.create_superuser(username=treasurerLogin, password=treasurerPassword)

        return JsonResponse({"success": True})
    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getConfig(request):
    try:
        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "r")
        config = json.load(file)
        file.close()

        return JsonResponse(config)
    except FileNotFoundError:
        return JsonResponse({"error": "Config file not found"})
