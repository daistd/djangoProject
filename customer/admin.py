from django.contrib import admin
from django.db.models import Sum
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from customer.models import Customer, Order, Payment
from django.contrib.admin import DateFieldListFilter
from django.utils import timezone
from import_export.fields import Field


# admin.site.register(Customer)

class CustomerResource(resources.ModelResource):

    def get_export_headers(self):
        headers = super().get_export_headers()
        for i, h in enumerate(headers):
            new_fields = {
                'name': 'Клиент',
                'balance': 'Баланс',
                'date': 'Дата',
                'order_amount': 'Количество',
                'payment_amount': 'Сумма оплаты'
            }
            if h in new_fields:
                headers[i] = new_fields[h]
        return headers

    date = Field()
    order_amount = Field()
    payment_amount = Field()

    class Meta:
        model = Customer
        widgets = {
            'date': {'format': '%d.%m.%Y'},
        }
        fields = ('date', 'id', 'name', 'balance', 'payment_amount')
        export_order = ('id', 'date', 'name', 'order_amount', 'payment_amount', 'balance',)

        def get_queryset(self):
            return self._meta.model.objects.order_by('-id')

    def dehydrate_date(self, obj):
        return timezone.now().date()

    def dehydrate_order_amount(self, obj):
        amount = Order.objects.filter(company=obj).aggregate(Sum('amount'))
        return amount['amount__sum']

    def dehydrate_payment_amount(self, obj):
        amount = Payment.objects.filter(company=obj).aggregate(Sum('amount'))
        return amount['amount__sum']


class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    list_display = ('id', 'name', 'bin', 'balance')
    list_filter = ('name', 'balance')
    # list_editable = ['balance']


admin.site.register(Customer, CustomerAdmin)


class OrderAdmin(ImportExportModelAdmin):
    list_display = ('company', 'date', 'weight', 'price', 'amount', 'manager_name', 'car_number')
    list_filter = ('date', 'company')
    list_editable = ['date']

    def manager_name(self, obj):
        return obj.manager.name

    manager_name.short_description = "Менеджер"

    def car_number(self, obj):
        return obj.car.number

    car_number.short_description = "Гос. номер авто"


admin.site.register(Order, OrderAdmin)
#
#
# @admin.register(Order)
# class OrderAdminEM(ImportExportModelAdmin):
#     pass


@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('company', 'date', 'amount', 'manager_name')
    list_filter = (('date', DateFieldListFilter), 'company')
    list_editable = ['date']

    def manager_name(self, obj):
        return obj.manager.name
    manager_name.short_description = "Менеджер"

