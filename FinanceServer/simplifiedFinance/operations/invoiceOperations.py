from ..models import Invoice


def createInvoice(request):
    date = request.POST.get("invoiceDate")
    number = request.POST.get("invoiceNumber")
    description = request.POST.get("invoiceDescription")

    invoice = Invoice(date=date, number=number, description=description, file=request.FILES.get("file"))
    invoice.save()

    return invoice
