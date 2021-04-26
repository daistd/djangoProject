from django.contrib import admin

# Register your models here.
from company.models import CementType, CarType, Car, Manager

admin.site.register(CementType)
admin.site.register(CarType)
admin.site.register(Car)
admin.site.register(Manager)

