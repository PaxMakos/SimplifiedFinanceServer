from django.db import models


# Create your models here.
class Invoice(models.Model):
    file = models.FileField(upload_to="%Y/%m/")
    date = models.DateField()
    number = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.number


PROJECT_STATUS = [
    ("Active", "Active"),
    ("Completed", "Completed"),
]


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(choices=PROJECT_STATUS, default="Active", max_length=100)

    def __str__(self):
        return self.name


class SubAccount(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    accountNumber = models.CharField(max_length=26)
    balance = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    address = models.TextField(null=True, blank=True)
    NIPNumber = models.CharField(max_length=10)
    accountNumber = models.CharField(max_length=26)

    def __str__(self):
        return self.name


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    date = models.DateField()
    title = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    account = models.ForeignKey(SubAccount, on_delete=models.RESTRICT)
    vendor = models.ForeignKey(Vendor, on_delete=models.RESTRICT)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    description = models.TextField(null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.title