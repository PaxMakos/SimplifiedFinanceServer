from ..models import Vendor


def createVendor(request):
    name = request.POST.get("vendorName")
    address = request.POST.get("vendorAddress")
    NIPNumber = request.POST.get("vendorNIPNumber")
    accountNumber = request.POST.get("vendorAccountNumber")

    vendor = Vendor(name=name, address=address, NIPNumber=NIPNumber, accountNumber=accountNumber)
    vendor.save()

    return vendor
