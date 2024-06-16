from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse
from ..models import Invoice
from django.db import IntegrityError
import os


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
            date = request.POST.get("date")
            number = request.POST.get("number")
            description = request.POST.get("description")
            file = request.FILES.get("file")

            invoice = Invoice(date=date, number=number, description=description, file=file)
            invoice.save()

            return JsonResponse({"status": "success"})
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

            date = request.POST.get("date")
            description = request.POST.get("description")
            file = request.FILES.get("file")

            invoice.date = date
            invoice.description = description
            invoice.file = file
            invoice.save()

            return JsonResponse({"status": "success"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})


@require_http_methods(["DELETE"])
@csrf_exempt
def deleteInvoice(request, number):
    if request.user.is_authenticated:
        try:
            invoice = Invoice.objects.get(number=number)
            invoice.delete()

            return JsonResponse({"status": "success"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})