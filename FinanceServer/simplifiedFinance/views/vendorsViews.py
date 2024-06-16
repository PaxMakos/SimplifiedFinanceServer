from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Vendor
from django.core import serializers
from django.db import IntegrityError
from ..operations.vendorsOperations import createVendor


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

        vendor = createVendor(request)

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

                vendor.name = request.POST.get("vendorName")
                vendor.address = request.POST.get("vendorAddress")
                vendor.NIPNumber = request.POST.get("vendorNIPNumber")
                vendor.accountNumber = request.POST.get("vendorAccountNumber")
                vendor.save()

                return JsonResponse({"status": "success"})
            else:
                return JsonResponse({"status": "error", "message": "User is not a superuser"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Vendor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Vendor does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})