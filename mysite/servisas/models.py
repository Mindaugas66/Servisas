from django.db import models


# Create your models here.
class Service(models.Model):
    name = models.CharField(verbose_name="Name", max_length=100)
    price = models.FloatField(verbose_name="Price")

    def __str__(self):
        return f"{self.name} ({self.price})"

    class Meta:
        verbose_name = "Service"
        verbose_name_plural = "Services"


class CarModel(models.Model):
    make = models.CharField(verbose_name="Make", max_length=50)
    model = models.CharField(verbose_name="Model", max_length=50)
    cover = models.ImageField("Cover", upload_to="covers", null=True, blank=True)

    def __str__(self):
        return f"{self.make} {self.model}"

    class Meta:
        verbose_name = "Car Model"
        verbose_name_plural = "Car Models"


class Car(models.Model):
    license_plate = models.CharField(verbose_name="License Plate", max_length=10)
    vin_code = models.CharField(verbose_name="VIN code", max_length=20, null=True)
    client = models.CharField(verbose_name="Client name", max_length=50)
    car_model = models.ForeignKey(to="CarModel", verbose_name="Car Model", on_delete=models.SET_NULL, null=True,
                                  blank=True)

    def __str__(self):
        return f"{self.car_model} ({self.license_plate})"

    class Meta:
        verbose_name = "Car"
        verbose_name_plural = "Cars"


class Order(models.Model):
    date = models.DateField(verbose_name="Date", auto_now_add=True)
    car = models.ForeignKey(to="Car", verbose_name="Car", on_delete=models.CASCADE, null=True)

    ORDER_STATUS = (
        ('c', 'Completed'),
        ('i', 'In Progress'),
        ('ca', 'Canceled'),
    )

    status = models.CharField(max_length=2, choices=ORDER_STATUS, blank=True, default="i", help_text='Order Status')

    def __str__(self):
        return f"{self.car} {self.date}"

    def total(self):
        result = 0
        for line in self.lines.all():
            result += line.price()
        return result

    class Meta:
        verbose_name = "Order"
        verbose_name_plural = "Orders"


class OrderRow(models.Model):
    order = models.ForeignKey(to="Order", verbose_name="Order", on_delete=models.CASCADE, null=True,
                              related_name='lines')
    service = models.ForeignKey(to="Service", verbose_name="Service", on_delete=models.SET_NULL, null=True, blank=True)
    qty = models.IntegerField(verbose_name="Quantity", default=0)

    def price(self):
        return self.service.price * self.qty

    price.short_description = "Price"

    def __str__(self):
        return f"{self.service} * {self.qty} = {self.price()} ({self.order})"

    class Meta:
        verbose_name = "Order Line"
        verbose_name_plural = "Order Lines"
