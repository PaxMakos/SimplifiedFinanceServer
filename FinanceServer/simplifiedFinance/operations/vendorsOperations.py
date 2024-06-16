from ..models import Vendor
from django.db import IntegrityError


def createVendor(request):
    name = request.POST.get("vendorName")
    address = request.POST.get("vendorAddress")
    NIPNumber = request.POST.get("vendorNIPNumber")
    accountNumber = request.POST.get("vendorAccountNumber")

    if Vendor.objects.filter(name=name).exists():
        raise IntegrityError("Vendor already exists")
    else:
        vendor = Vendor(name=name, address=address, NIPNumber=NIPNumber, accountNumber=accountNumber)
        vendor.save()

        return vendor
