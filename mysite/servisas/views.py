from django.shortcuts import render
from django.http import HttpResponse
from .models import CarModel, Service, Order, Car, OrderRow
import datetime


def index(request):
    num_cars = CarModel.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status="c").count()
    context = {
        "num_cars": num_cars,
        "num_services": num_services,
        "num_orders": num_orders,
        "year": datetime.datetime.now()
    }
    return render(request, template_name="index.html", context=context)


def Cars(request):
    cars = Car.objects.all()
    context = {
        "cars": cars
    }
    print(cars)
    return render(request, template_name="cars.html", context=context)

def OrdersAndOrderRows(request):
    orders = Order.objects.all().order_by('-date')
    order_rows = OrderRow.objects.all()
    context = {
        "orders": orders,
        "order_rows": order_rows
    }
    return render(request, template_name="orders.html", context=context)