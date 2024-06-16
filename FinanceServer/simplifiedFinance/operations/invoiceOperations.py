from ..models import Invoice
from django.db import IntegrityError


def createInvoice(request):
    date = request.POST.get("invoiceDate")
    number = request.POST.get("invoiceNumber")
    description = request.POST.get("invoiceDescription")

    if Invoice.objects.filter(number=number).exists():
        raise IntegrityError("Invoice already exists")
    else:
        invoice = Invoice(date=date, number=number, description=description, file=request.FILES.get("file"))
        invoice.save()

        return invoice
