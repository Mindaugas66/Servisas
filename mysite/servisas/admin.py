from django.contrib import admin

# Register your models here.
from .models import CarModel, Car, Order, OrderRow, Service


class CarModelAdmin(admin.ModelAdmin):
    list_display = ["make", "model", "year"]


class CarAdmin(admin.ModelAdmin):
    list_display = ["license_plate", "client", "VIN_code", "car_model_id"]
    list_filter = ["client", "car_model_id"]
    search_fields = ["license_plate", "VIN_code"]

class OrderAdmin(admin.ModelAdmin):
    list_display = ["car_id", "date"]


class OrderRowAdmin(admin.ModelAdmin):
    list_display = ["service_id", "order_id", "quantity"]


class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]


admin.site.register(CarModel, CarModelAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderRow, OrderRowAdmin)
admin.site.register(Service, ServiceAdmin)
