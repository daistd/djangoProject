from datetime import datetime

from django.db import models
# Create your models here.
from django.utils import timezone

from company.models import Manager, Car, CementType


class Customer(models.Model):
    bin = models.CharField('БИН', max_length=12)
    name = models.CharField('Клиента', max_length=255)
    ceo = models.CharField('Руководитель', max_length=255)
    balance = models.IntegerField('Сальдо', default=0, editable=False)

    def __str__(self):
        return "%s" % self.name


class Order(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер')
    cement = models.ForeignKey(CementType, on_delete=models.CASCADE)
    weight = models.IntegerField('Масса')
    price = models.IntegerField("Цена")
    date = models.DateField('Дата', default=timezone.now, blank=True)
    amount = models.IntegerField("Сумма", default=0)

    def save(self, *args, **kwargs):
        current_amount = 0
        if self.amount != 0:
            current_amount = self.amount
        self.amount = self.weight*self.price
        self.company.balance = self.company.balance + current_amount - self.amount
        self.company.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.date.__str__() + " Компания: " +self.company.name + " масса:" + str(self.weight) + "т. - " +str(self.price)+"тг."


class Payment(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    amount = models.IntegerField("Сумма")
    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.company.balance = self.company.balance + self.amount
        self.company.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.date.__str__() + " Компания: " +self.company.name + " Сумма:" + str(self.amount)
