import os

from ..models import Invoice
from django.db import IntegrityError


def createInvoice(request, invoiceFile=None):
    # creates a new invoice with the given data

    date = request.POST.get("invoiceDate")
    number = request.POST.get("invoiceNumber")
    description = request.POST.get("invoiceDescription")

    if not date or not number:
        raise ValueError("Missing required fields")

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
