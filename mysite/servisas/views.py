from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView
from django.contrib.auth.decorators import login_required
from .models import CarModel, Service, Order, Car, OrderRow
import datetime
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.contrib.auth import password_validation
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm
from django.views.generic.edit import FormMixin, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin


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
    return render(request, template_name="order.html", context=context)


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
    template_name = "order.html"
    context_object_name = "Orders"
    paginate_by = 3


def search(request):
    query = request.GET.get('query')
    car_search_results = Car.objects.filter(
        Q(license_plate__icontains=query) |
        Q(vin_code__icontains=query) |
        Q(client__icontains=query) |
        Q(car_model__model__icontains=query) |  # Assuming the CarModel has a 'name' field
        Q(car_model__make__icontains=query)  # Assuming the CarModel has a 'make' field
    )
    context = {
        "query": query,
        "cars": car_search_results,
    }
    return render(request, template_name="search.html", context=context)


class MyOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "user_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user)


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, f' {username} Is taken!')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'User already exists with {email}!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'User {username} registered!')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords doesnt match!')
            return redirect('register')
    return render(request, 'registration/register.html')


class OrderDetailView(FormMixin, DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse("order", kwargs={"pk": self.object.id})

    # standartinis post metodo perrašymas, naudojant FormMixin, galite kopijuoti tiesiai į savo projektą.
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    # štai čia nurodome, kad knyga bus būtent ta, po kuria komentuojame, o vartotojas bus tas, kuris yra prisijungęs.
    def form_valid(self, form):
        form.instance.book = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super().form_valid(form)


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, f'El. paštas negali būti tuščias!')
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, f'Vartotojas su el. paštu {new_email} jau užregistruotas!')
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Profilis atnaujintas")
            return redirect('profile')

    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)


class NewOrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    fields = ["car", "deadline"]
    success_url = "/myorders/"
    template_name = "order_form.html"

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class UserOrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    fields = ["car", "deadline"]
    template_name = "order_form.html"
    success_url = "/myorders/"

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        instance = self.get_object()
        return instance.client == self.request.user


class UserOrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    success_url = "/myorders/"
    context_object_name = "order"
    template_name = 'order_delete.html'

    def test_func(self):
        instance = self.get_object()
        return instance.client == self.request.user
