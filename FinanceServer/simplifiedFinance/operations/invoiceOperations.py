import os

from ..models import Invoice
from django.db import IntegrityError


def createInvoice(request, invoiceFile=None):
    date = request.POST.get("invoiceDate")
    number = request.POST.get("invoiceNumber")
    description = request.POST.get("invoiceDescription")

    invoice = None

    if Invoice.objects.filter(number=number).exists():
        raise IntegrityError("Invoice already exists")
    else:
        if not invoiceFile:
            invoice = Invoice(date=date, number=number, description=description, file=request.FILES.get("file"))
        else:
            invoice = Invoice(date=date, number=number, description=description, file=invoiceFile)
            os.remove(invoiceFile.path)
        invoice.save()

    return invoice
