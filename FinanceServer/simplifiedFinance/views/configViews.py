from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from FinanceServer.simplifiedFinance import models
from django.core.management.base import BaseCommand
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


@require_http_methods(["GET"])
@csrf_exempt
def isConfigured(reguest):
    try:
        file = open ("../config.json", "r")
        file.close()
        return JsonResponse({"configured": True})
    except:
        return JsonResponse({"configured": False})


@require_http_methods(["POST"])
@csrf_exempt
def configure(request):
    try:
        models.SubAccount.objects.all().delete()
        models.Vendor.objects.all().delete()
        models.Transaction.objects.all().delete()
        models.Project.objects.all().delete()
        models.Invoice.objects.all().delete()

        file = open("../config.json", "w")

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

        models.SubAccount.objects.create(
            name="Główny rachunek",
            accountNumber=accountNumber,
            balance=accountBalance
        )

        User.objects.create_superuser(username=treasurerLogin, password=treasurerPassword)

        return JsonResponse({"success": True})
    except:
        return JsonResponse({"success": False})






