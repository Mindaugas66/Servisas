from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.index, name="index"),
    path('cars/', views.Cars, name="Cars"),
    path('orders/', views.OrdersAndOrderRows, name="Cars"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_URL)