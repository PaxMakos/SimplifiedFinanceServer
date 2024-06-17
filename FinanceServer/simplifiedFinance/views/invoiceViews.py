from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Invoice, Vendor
from django.db import IntegrityError
import os
from django.db import models
from ..operations.invoiceOperations import createInvoice
from ..operations.invoiceGenerator import generateInvoice as gi
import json


@require_http_methods(["GET"])
@csrf_exempt
def downloadInvoice(request, number):
    if request.user.is_authenticated:
        try:
            invoice = Invoice.objects.get(number=number)

            path = invoice.file.path

            if os.path.exists(path):
                with open(path, "rb") as file:
                    response = HttpResponse(file.read(), content_type="application/force-download")
                    response["Content-Disposition"] = f"attachment; filename={invoice.file.name}"
                    return response
            else:
                return JsonResponse({"status": "error", "message": "File does not exist"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["GET"])
@csrf_exempt
def getInvoice(request, number):
    if request.user.is_authenticated:
        try:
            invoice = Invoice.objects.get(number=number)

            return JsonResponse({
                "status": "success",
                "number": invoice.number,
                "date": invoice.date,
                "description": invoice.description,
                "file": invoice.file.name
            })
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def createInvoice(request):
    if request.user.is_authenticated:
        try:
            invoice = createInvoice(request)

            return JsonResponse({"status": "success", "number": invoice.number})
        except IntegrityError:
            return JsonResponse({"status": "error", "message": "Invoice with this number already exists"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["POST"])
@csrf_exempt
def updateInvoice(request, number):
    if request.user.is_authenticated:
        try:
            invoice = Invoice.objects.get(number=number)

            invoice.date = models.DateField(request.POST.get("invoiceDate"))
            invoice.description = request.POST.get("invoiceDescription")
            invoice.file = request.FILES.get("invoiceFile")
            invoice.save()

            return JsonResponse({"status": "success"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except IntegrityError:
            return JsonResponse({"status": "error", "message": "Invoice with this number already exists"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteInvoice(request, number):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            invoice = Invoice.objects.get(number=number)
            invoice.delete()

            return JsonResponse({"status": "success"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except IntegrityError:
            return JsonResponse({"status": "error", "message": "Invoice is used in transactions"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not superuser"})


@require_http_methods(["GET"])
@csrf_exempt
def generateInvoice(request):
    if request.user.is_authenticated and request.user.is_superuser:
        try:
            invoiceData = {
                "invoiceNumber": request.GET.get("invoiceNumber"),
                "sellDate": request.GET.get("sellDate"),
                "invoiceDate": request.GET.get("invoiceDate"),
                "paymentTo": request.GET.get("paymentTo"),
                "vendorName": request.GET.get("vendorName"),
                "vendorNIP": Vendor.objects.get(name=request.GET.get("vendorName")).NIPNumber,
                "vendorPostCode": Vendor.objects.get(name=request.GET.get("vendorName")).postcode,
                "vendorCity": Vendor.objects.get(name=request.GET.get("vendorName")).city,
                "vendorStreet": Vendor.objects.get(name=request.GET.get("vendorName")).street,
                "products": json.loads(request.GET.get("products"))
            }

            newInvoice = gi(invoiceData)
            invoice = createInvoice(request, newInvoice)

            return JsonResponse({"status": "success", "number": invoice.number})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not superuser"})


