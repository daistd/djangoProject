from datetime import datetime

from django.db import models
# Create your models here.
from django.utils import timezone

from company.models import Manager, Car, CementType


class Customer(models.Model):
    phone = models.CharField('Телефон', max_length=12, null=True)
    name = models.CharField('Клиент', max_length=255)
    ceo = models.CharField('Контактное лицо', max_length=255)
    balance = models.IntegerField('Текущий баланс', default=0)
    kaspi_id = models.CharField('Капси ID', max_length=255, editable=False, null=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.kaspi_id = self.get_kaspi_id()
        return super().save(*args, **kwargs)

    def get_kaspi_id(self):
        return str(self.pk) + self.ceo.strip()

    def __str__(self):
        return "%s" % self.name


class Order(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер')
    cement = models.ForeignKey(CementType, on_delete=models.CASCADE)
    weight = models.IntegerField('Масса')
    price = models.IntegerField("Цена")
    date = models.DateField('Дата поставки', blank=True)
    amount = models.IntegerField("Сумма", default=0)

    def save(self, *args, **kwargs):
        current_amount = 0
        if self.amount != 0:
            current_amount = self.amount
        self.amount = self.weight*self.price
        self.company.balance = self.company.balance + current_amount - self.amount
        self.company.save()
        super().save(*args, **kwargs)
        current_sverka = Sverka.objects.filter(order=self)
        if not current_sverka:
            sverka = Sverka()
        else:
            sverka = current_sverka[0]
        sverka.company = self.company
        sverka.date = self.date
        sverka.order = self
        sverka.cement_type = self.cement
        sverka.car = self.car
        sverka.price = self.price
        sverka.weight = self.weight
        sverka.order_amount = self.amount
        sverka.manager = self.manager
        sverka.balance = self.company.balance
        sverka.kaspi_id = self.company.kaspi_id
        sverka.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.date.__str__() + " Компания: " + self.company.name + " масса:" + str(self.weight) + "т. - " +str(self.price)+"тг."


class PaymentType(models.Model):
    type = models.CharField(max_length=255)

    def __str__(self):
        return self.type


class Payment(models.Model):
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE)
    type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True)
    amount = models.IntegerField("Сумма")
    date = models.DateField(default=timezone.now, blank=True)

    def save(self, *args, **kwargs):
        self.company.balance = self.company.balance + self.amount
        self.company.save()
        super().save(*args, **kwargs)
        current_sverka = Sverka.objects.filter(payment=self)

        if not current_sverka:
            sverka = Sverka()
        else:
            sverka = current_sverka[0]

        sverka.company = self.company
        sverka.date = self.date
        sverka.payment = self
        sverka.payment_type = self.type
        sverka.payment_amount = self.amount
        sverka.manager = self.manager
        sverka.balance = self.company.balance
        sverka.kaspi_id = self.company.kaspi_id
        sverka.save()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.date.__str__() + " Компания: " + self.company.name + " Сумма:" + str(self.amount)


class Sverka(models.Model):
    date = models.DateField('Дата', blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.CASCADE, null=True)
    company = models.ForeignKey(Customer, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)
    weight = models.IntegerField('Масса', null=True)
    price = models.IntegerField("Цена за 1 тоннау", null=True)
    order_amount = models.IntegerField("Сумма Заказа", default=0, null=True)
    manager = models.ForeignKey(Manager, on_delete=models.CASCADE, verbose_name='Менеджер')
    cement_type = models.ForeignKey(CementType, on_delete=models.CASCADE, null=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.CASCADE, null=True)
    payment_amount = models.IntegerField("Сумма Оплаты", null=True)
    balance = models.IntegerField('Сальдо', default=0)
    kaspi_id = models.CharField('Капси перевод', max_length=255)
