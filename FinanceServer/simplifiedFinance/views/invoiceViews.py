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

            if invoice is None:
                return JsonResponse({"status": "error", "message": "Invoice does not exist"})
            else:
                path = invoice.file.path

                if os.path.exists(path):
                    with open(path, "rb") as file:
                        return HttpResponse(file.read(), content_type="application/pdf")
                else:
                    return JsonResponse({"status": "error", "message": "File does not exist"})
        except Invoice.DoesNotExist:
            return JsonResponse({"status": "error", "message": "Invoice does not exist"})
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
    else:
        return JsonResponse({"status": "error", "message": "User is not authenticated"})

