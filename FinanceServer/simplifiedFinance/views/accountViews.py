from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import SubAccount
from django.db import IntegrityError


@require_http_methods(["GET"])
@csrf_exempt
def getAccounts(request):
    # If the user is authenticated, return all organization bank accounts
    try:
        if request.user.is_authenticated:
            accounts = SubAccount.objects.all()

            toReturn = []
            # Serialize the accounts and return them as list of JSONs
            for account in accounts:
                toReturn.append({
                    "name": account.name,
                    "accountNumber": account.accountNumber,
                    "balance": account.balance
                })

            return JsonResponse({"status": "success", "accounts": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createAccount(request):
    # If user is superuser, create a new organization bank account
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            name = request.POST.get("accountName")
            accountNumber = request.POST.get("accountNumber")
            balance = float(request.POST.get("accountBalance"))

            if not name or not accountNumber or not balance:
                return JsonResponse({"status": "error", "message": "Missing required fields"})

            if SubAccount.objects.filter(name=name).exists():
                return JsonResponse({"status": "error", "message": "Account already exists"})
            else:
                account = SubAccount(name=name, accountNumber=accountNumber, balance=balance)
                account.save()

                return JsonResponse({"status": "success", "message": f"Account {name} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except IntegrityError as e:
        return JsonResponse({"status": "error", "message": "Account already exists", "error": str(e)})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteAccount(request, name):
    # If user is superuser, delete an organization bank account
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            account = SubAccount.objects.get(name=name)
            account.delete()
            return JsonResponse({"status": "success", "message": f"Account {name} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except SubAccount.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Account is in use"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
