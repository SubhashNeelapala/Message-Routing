from django.db import models

# Create your models here.


class IpAddress(models.Model):
    address=models.CharField(max_length=1000)


class Gateway(models.Model):
    name=models.CharField(max_length=100,unique=True)
    ip_address=models.ManyToManyField(IpAddress)

class Prefix(models.Model):
    prefix_name=models.CharField(max_length=100)
    gateway = models.ForeignKey(Gateway)


