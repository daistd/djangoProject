from django.db import models

# Create your models here.


class CementType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.type


class CarType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.type


class Car(models.Model):
    type = models.ForeignKey(CarType, on_delete=models.CASCADE)
    number = models.CharField(max_length=40)
    driver = models.CharField(max_length=255)

    def __str__(self):
        return "%s" % self.number


class Manager(models.Model):
    name = models.CharField(max_length=255)
    balance = models.IntegerField(default=0)

    def __str__(self):
        return "%s" % self.name
