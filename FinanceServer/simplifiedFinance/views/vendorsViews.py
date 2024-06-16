from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Vendor
from django.core import serializers
from django.db import IntegrityError


@require_http_methods(["GET"])
@csrf_exempt
def getVendors(request):
    if request.user.is_authenticated:
        vendors = Vendor.objects.all()
        data = serializers.serialize("xml", vendors)
        return HttpResponse(data, content_type="application/xml")
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createVendor(request):
    if request.user.is_authenticated:
        name = request.POST.get("name")
        address = request.POST.get("address")
        NIPNumber = request.POST.get("NIPNumber")
        accountNumber = request.POST.get("accountNumber")
        vendor = Vendor(name=name, address=address, NIPNumber=NIPNumber, accountNumber=accountNumber)
        vendor.save()
        return JsonResponse({"status": "success", "id": vendor.id})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteVendor(request, name):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                vendor = Vendor.objects.get(name=name)
                vendor.delete()
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "User is not a superuser"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Vendor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Vendor does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Vendor is in use"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def updateVendor(request, name):
    try:
        if request.user.is_authenticated:
            if request.user.is_superuser:
                vendor = Vendor.objects.get(name=name)
                vendor.name = request.POST.get("name")
                print(name)
                vendor.address = request.POST.get("address")
                vendor.NIPNumber = request.POST.get("NIPNumber")
                vendor.accountNumber = request.POST.get("accountNumber")
                vendor.save()
                print(name)
                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "User is not a superuser"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Vendor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Vendor does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})