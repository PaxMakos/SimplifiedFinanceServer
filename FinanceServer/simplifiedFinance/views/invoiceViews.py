from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Invoice, Vendor
from django.db import IntegrityError
import os
from ..operations.invoiceOperations import createInvoice as ci
from ..operations.invoiceGenerator import generateInvoice as gi
import json


@require_http_methods(["GET"])
@csrf_exempt
def downloadInvoice(request, number):
    # If the user is authenticated, download the invoice file
    try:
        if request.user.is_authenticated:
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


@require_http_methods(["GET"])
@csrf_exempt
def getInvoice(request, number):
    # If the user is authenticated, return the invoice data
    try:
        if request.user.is_authenticated:
            invoice = Invoice.objects.get(number=number)

            return JsonResponse({"status": "success", "invoice": {
                "date": invoice.date,
                "number": invoice.number,
                "description": invoice.description,
                "file": invoice.file.name if invoice.file else None
            }})

    except Invoice.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invoice does not exist"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def getInvoices(request):
    # If the user is authenticated, return all invoices
    try:
        if request.user.is_authenticated:
            invoices = Invoice.objects.all()

            toReturn = []
            # Serialize the invoices and return them as list of JSONs
            for invoice in invoices:
                toReturn.append({
                    "date": invoice.date,
                    "number": invoice.number,
                    "description": invoice.description,
                    "file": invoice.file.name if invoice.file else None
                })

            return JsonResponse({"status": "success", "invoices": toReturn})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def createInvoice(request):
    # If the user is authenticated, create a new invoice
    try:
        if request.user.is_authenticated:
            invoice = ci(request)
            return JsonResponse({"status": "success", "message": f"Invoice {invoice.number} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Invoice with this number already exists"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["POST"])
@csrf_exempt
def updateInvoice(request, number):
    # If the user is authenticated, update the invoice data
    try:
        if request.user.is_authenticated:
            invoice = Invoice.objects.get(number=number)
            date = request.POST.get("date")
            description = request.POST.get("description")
            file = request.FILES.get("file")

            if date:
                invoice.date = date
            if description:
                invoice.description = description
            if file:
                if invoice.file:
                    os.remove(invoice.file.path)
                invoice.file = file

            invoice.save()

            return JsonResponse({"status": "success", "message": f"Invoice {invoice.number} updated"})
        else:
            return JsonResponse({"status": "error", "message": "User is not authenticated"})
    except Invoice.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invoice does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Invoice with this number already exists"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteInvoice(request, number):
    # If the user is superuser, delete the invoice
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            invoice = Invoice.objects.get(number=number)

            if invoice.file:
                os.remove(invoice.file.path)

            invoice.delete()

            return JsonResponse({"status": "success", "message": f"Invoice {number} deleted"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Invoice.DoesNotExist:
        return JsonResponse({"status": "error", "message": "Invoice does not exist"})
    except IntegrityError:
        return JsonResponse({"status": "error", "message": "Invoice is used in transactions"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})


@require_http_methods(["GET"])
@csrf_exempt
def generateInvoice(request):
    # If the user is superuser, generate a new invoice
    try:
        if request.user.is_authenticated and request.user.is_superuser:
            if not request.GET.get("invoiceNumber"):
                return JsonResponse({"status": "error", "message": "Missing invoice number"})
            if not request.GET.get("sellDate"):
                return JsonResponse({"status": "error", "message": "Missing sell date"})
            if not request.GET.get("invoiceDate"):
                return JsonResponse({"status": "error", "message": "Missing invoice date"})
            if not request.GET.get("paymentTo"):
                return JsonResponse({"status": "error", "message": "Missing date of payment"})
            if not request.GET.get("vendorName"):
                return JsonResponse({"status": "error", "message": "Missing vendor name"})
            if not request.GET.get("products"):
                return JsonResponse({"status": "error", "message": "Missing products"})

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
            invoice = ci(request, newInvoice)

            return JsonResponse({"status": "success", "message": f"Invoice {invoice.number} created"})
        else:
            return JsonResponse({"status": "error", "message": "User is not a superuser"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)})

