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
    # check if the app is configured
    try:
        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "r")
        file.close()
        return JsonResponse({"status": "success", "configured": True})
    except FileNotFoundError:
        return JsonResponse({"status": "success", "configured": False})


@require_http_methods(["POST"])
@csrf_exempt
def configure(request):
    # configure the app
    try:
        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "r")
        file.close()
        return JsonResponse({"status": "error", "message": "Configuration already exists"})
    except FileNotFoundError:
        try:
            Transaction.objects.all().delete()
            SubAccount.objects.all().delete()
            Vendor.objects.all().delete()
            Permissions.objects.all().delete()
            Project.objects.all().delete()
            Invoice.objects.all().delete()
            User.objects.all().delete()

            file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "w")

            organisation = request.POST.get("organisation")
            postCode = request.POST.get("postCode")
            city = request.POST.get("city")
            street = request.POST.get("street")
            NIP = request.POST.get("NIP")
            accountNumber = request.POST.get("accountNumber")
            accountBalance = request.POST.get("accountBalance")
            treasurerName = request.POST.get("treasurerName")

            if organisation is None:
                raise Exception("Missing organisation name")
            if postCode is None:
                raise Exception("Missing post code")
            if city is None:
                raise Exception("Missing city")
            if street is None:
                raise Exception("Missing street")
            if NIP is None:
                raise Exception("Missing NIP number")
            if accountNumber is None:
                raise Exception("Missing account number")
            if accountBalance is None:
                raise Exception("Missing account balance")
            if treasurerName is None:
                raise Exception("Missing treasurer name")

            treasurerLogin = request.POST.get("treasurerLogin")
            treasurerPassword = request.POST.get("treasurerPassword")

            if treasurerLogin is None or treasurerPassword is None:
                raise Exception("Missing treasurer login or password")

            config = {
                "organisation": organisation,
                "postCode": postCode,
                "city": city,
                "street": street,
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

            return JsonResponse({"status": "success", "message": "Configuration successful"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getConfig(request):
    # get configuration
    try:
        file = open(os.path.join(os.path.dirname(__file__), "..", "config.json"), "r")
        config = json.load(file)
        file.close()

        return JsonResponse({"status": "success", "configuration": config})
    except FileNotFoundError:
        return JsonResponse({"status": "error", "message": "Configuration not found"})
