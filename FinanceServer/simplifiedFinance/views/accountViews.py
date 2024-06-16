from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import SubAccount
from django.core import serializers
from django.db import IntegrityError


@require_http_methods(["GET"])
@csrf_exempt
def getAccounts(request):
    if request.user.is_authenticated:
        accounts = SubAccount.objects.all()
        data = serializers.serialize("xml", accounts)
        return HttpResponse(data, content_type="application/xml")
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createAccount(request):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            name = request.POST.get("accountName")
            accountNumber = request.POST.get("accountNumber")
            balance = request.POST.get("accountBalance")

            if SubAccount.objects.filter(name=name).exists():
                raise IntegrityError("Account already exists")
            else:
                account = SubAccount(name=name, accountNumber=accountNumber, balance=balance)
                account.save()

                return JsonResponse({"status": "success", "id": account.id})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Account already exists"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteAccount(request, name):
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            account = SubAccount.objects.get(name=name)
            account.delete()
            return JsonResponse({"status": "success"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except SubAccount.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Account does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Account is in use"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
