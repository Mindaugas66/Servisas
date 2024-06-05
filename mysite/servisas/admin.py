from django.contrib import admin
from .models import (Car,
                     CarModel,
                     Service,
                     Order,
                     OrderRow)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ['name', 'price']


class CarAdmin(admin.ModelAdmin):
    list_display = ['vin_code', 'client', 'car_model', 'license_plate']
    list_filter = ['client', 'car_model']
    search_fields = ['license_plate', 'vin_code']


class OrderRowInLine(admin.TabularInline):
    model = OrderRow
    extra = 0
    fields = ['service', 'qty']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['car', 'date', 'total']
    inlines = [OrderRowInLine]


class OrderLineAdmin(admin.ModelAdmin):
    list_display = ['order', 'service', 'qty', 'price']


# Register your models here.
admin.site.register(Car, CarAdmin)
admin.site.register(CarModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRow, OrderLineAdmin)
