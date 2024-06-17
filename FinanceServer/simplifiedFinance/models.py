from django.db import models
from django.contrib.auth.models import User
import os
from datetime import datetime


def uploadTo(instance, filename):
    base, extension = os.path.splitext(filename)
    date = datetime.strptime(instance.date, "%Y-%m-%d").date()
    path = f"{date.year}/{date.month}/{instance.number}{extension}"
    return path


# Create your models here.
class Invoice(models.Model):
    date = models.DateField()
    number = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)
    file = models.FileField(upload_to=uploadTo)

    def __str__(self):
        return self.number


PROJECT_STATUS = [
    ("Active", "Active"),
    ("Completed", "Completed"),
]


class Project(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    description = models.TextField(null=True, blank=True)
    startDate = models.DateField()
    endDate = models.DateField()
    status = models.CharField(choices=PROJECT_STATUS, default="Active", max_length=100)

    def __str__(self):
        return self.name


class SubAccount(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    accountNumber = models.CharField(max_length=26)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return self.name


class Vendor(models.Model):
    name = models.CharField(max_length=100, primary_key=True)
    postcode = models.CharField(max_length=6, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
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
    project = models.ForeignKey(Project, on_delete=models.RESTRICT, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    invoice = models.ForeignKey(Invoice, on_delete=models.RESTRICT, null=True, blank=True)

    def __str__(self):
        return self.title


class Permissions(models.Model):
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)


class Return(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.ForeignKey(Project, on_delete=models.RESTRICT)
    title = models.CharField(max_length=100)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    accountToReturn = models.CharField(max_length=26)
    invoice = models.FileField(upload_to="%Y/waiting/")

