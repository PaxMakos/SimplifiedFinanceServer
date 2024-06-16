from ..models import Transaction, Vendor, SubAccount, Invoice, Project


def createTransaction(request, invoice=None):
    date = request.POST.get("transactionDate")
    title = request.POST.get("transactionTitle")
    amount = float(request.POST.get("transactionAmount"))
    account = SubAccount.objects.get(name=request.POST.get("accountName"))
    vendor = Vendor.objects.get(name=request.POST.get("vendorName"))
    project = Project.objects.get(name=request.POST.get("projectName"))
    description = request.POST.get("transactionDescription")

    transaction = Transaction(date=date,
                              title=title,
                              amount=amount,
                              account=account,
                              vendor=vendor,
                              project=project,
                              description=description,
                              invoice=invoice)
    transaction.save()

    return transaction
