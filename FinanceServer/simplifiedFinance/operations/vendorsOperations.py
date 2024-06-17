from ..models import Vendor
from django.db import IntegrityError


def createVendor(request):
    name = request.POST.get("vendorName")
    postCode = request.POST.get("vendorPostCode")
    city = request.POST.get("vendorCity")
    street = request.POST.get("vendorStreet")
    NIPNumber = request.POST.get("vendorNIPNumber")
    accountNumber = request.POST.get("vendorAccountNumber")

    if Vendor.objects.filter(name=name).exists():
        raise IntegrityError("Vendor already exists")
    else:
        vendor = Vendor(name=name,
                        postCode=postCode,
                        city=city,
                        street=street,
                        NIPNumber=NIPNumber,
                        accountNumber=accountNumber)
        vendor.save()

        return vendor
