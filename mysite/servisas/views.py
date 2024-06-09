from django.shortcuts import render
from django.http import HttpResponse
from .models import CarModel, Service, Order
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
