from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic

from .models import CarModel, Service, Order, Car, OrderRow
import datetime



def index(request):
    num_cars = CarModel.objects.all().count()
    num_services = Service.objects.all().count()
    num_orders = Order.objects.filter(status="c").count()
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    context = {
        "num_visits": num_visits,
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
    paginator = Paginator(orders, per_page=3)
    page_number = request.GET.get("page")
    paged_orders = paginator.get_page(page_number)
    context = {
        "orders": paged_orders,
        "order_rows": order_rows
    }
    return render(request, template_name="orders.html", context=context)


def car_model_view(request, car_model):
    car_model_instance = get_object_or_404(Car, pk=car_model)
    car_cover = car_model_instance.car_model
    context = {
        "car_cover": car_cover,
        "car_view": car_model_instance,
    }
    return render(request, template_name="car.html", context=context)


class OrderListView(generic.ListView):
    model = Order
    template_name = "Orders.html"
    context_object_name = "Orders"
    paginate_by = 3


def search(request):
    query = request.GET.get('query')
    car_search_results = Car.objects.filter(
        Q(license_plate__icontains=query) |
        Q(vin_code__icontains=query) |
        Q(client__icontains=query) |
        Q(car_model__model__icontains=query) |  # Assuming the CarModel has a 'name' field
        Q(car_model__make__icontains=query)   # Assuming the CarModel has a 'make' field
    )
    context = {
        "query": query,
        "cars": car_search_results,
    }
    return render(request, template_name="search.html", context=context)