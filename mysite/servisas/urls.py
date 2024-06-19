from django.urls import path, include
from . import views
from django.conf.urls.static import static
from django.conf import settings

from .views import OrderDetailView

urlpatterns = [
    path('', views.index, name="Home"),
    path('cars/', views.Cars, name="Cars"),
    path('cars/<int:car_model>', views.car_model_view, name="CarModel"),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("myorders/", views.MyOrdersListView.as_view(), name="myorders"),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('order/new', views.NewOrderCreateView.as_view(), name='order_new'),
    path('order/<int:pk>/update', views.UserOrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete', views.UserOrderDeleteView.as_view(), name='order_delete'),

]

