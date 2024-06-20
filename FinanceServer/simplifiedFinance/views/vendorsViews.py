from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from ..models import Vendor
from django.db import IntegrityError
from ..operations.vendorsOperations import createVendor as cv


@require_http_methods(["GET"])
@csrf_exempt
def getVendors(request):
    # If the user is authenticated, return all vendors
    try:
        if request.user.is_authenticated:
            vendors = Vendor.objects.all()

            toReturn = []

            for vendor in vendors:
                toReturn.append({
                    "name": vendor.name,
                    "postCode": vendor.postcode,
                    "city": vendor.city,
                    "street": vendor.street,
                    "NIPNumber": vendor.NIPNumber,
                    "accountNumber": vendor.accountNumber
                })

            return JsonResponse({"status": "success", "vendors": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createVendor(request):
    # If the user is authenticated, create a new vendor
    try:
        if request.user.is_authenticated:

            vendor = cv(request)

            return JsonResponse({"status": "success", "message": f"Vendor {vendor.name} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Vendor already exists"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteVendor(request, name):
    # If the user is superuser, delete a vendor
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            vendor = Vendor.objects.get(name=name)
            vendor.delete()
            return JsonResponse({"status": "success", "message": f"Vendor {name} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Vendor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Vendor does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Vendor is in use"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def updateVendor(request, name):
    # If the user is superuser, update a vendor
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            vendor = Vendor.objects.get(name=name)

            if request.POST.get("postCode"):
                vendor.postCode = request.POST.get("postCode")
            if request.POST.get("city"):
                vendor.city = request.POST.get("city")
            if request.POST.get("street"):
                vendor.street = request.POST.get("street")
            if request.POST.get("NIPNumber"):
                vendor.NIPNumber = request.POST.get("NIPNumber")
            if request.POST.get("accountNumber"):
                vendor.accountNumber = request.POST.get("accountNumber")

            vendor.save()

            return JsonResponse({"status": "success", "message": f"Vendor {name} updated"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Vendor.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Vendor does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})
