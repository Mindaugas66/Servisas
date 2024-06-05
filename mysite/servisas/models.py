from django.db import models


# Create your models here.


class CarModel(models.Model):
    make = models.CharField(verbose_name='Car make', max_length=50)
    model = models.CharField(verbose_name='Car model', max_length=50)
    year = models.CharField(verbose_name='Car make year', max_length=10, null=True)

    def __str__(self):
        return f"{self.make} {self.model} {self.year}"

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"


class Car(models.Model):
    license_plate = models.CharField(verbose_name="License Plate", max_length=10)
    VIN_code = models.CharField(verbose_name="VIN Code", max_length=17)
    client = models.CharField(verbose_name="Client name", max_length=50)
    car_model_id = models.ForeignKey(to="CarModel", on_delete=models.SET_NULL, null=True, verbose_name="Car Model ID")

    def __str__(self):
        return f"{self.license_plate} - {self.client}"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class Order(models.Model):
    date = models.DateField(verbose_name="Date")
    car_id = models.ForeignKey(to="Car", on_delete=models.SET_NULL, null=True, verbose_name="Car ID")
    total_sum = models.CharField(verbose_name="Total Sum", max_length=20)

    def __str__(self):
        return f"Order #{self.pk} for {self.car_id}"

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderRow(models.Model):
    service_id = models.ForeignKey(to="Service", on_delete=models.SET_NULL, null=True, verbose_name="Service ID")
    order_id = models.ForeignKey(to="Order", on_delete=models.SET_NULL, null=True, verbose_name="Order ID")
    quantity = models.CharField(verbose_name="Quantity", max_length=10)
    price = models.CharField(verbose_name="Price", max_length=10)

    def __str__(self):
        return f"Service {self.service_id} for Order {self.order_id}"

    class Meta:
        verbose_name = "Order Row"
        verbose_name_plural = "Order Rows"


class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=20)
    price = models.IntegerField(verbose_name="Price €")

    def __str__(self):
        return f"{self.name} - {self.price} €"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"

