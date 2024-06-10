from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="Home"),
    path('cars/', views.Cars, name="Cars"),
    path('cars/<int:car_model>', views.car_model_view, name="CarModel"),
    path('orders/', views.OrdersAndOrderRows, name="Orders"),
    path('search/', views.search, name='search'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)
