from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name = "index"),
    path("vehicles/", views.vehicles, name= "vehicles"),
    path("vehicles/<int:vehicle_id>", views.vehicle, name= "vehicle"),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('myorders/', views.MyOrderListView.as_view(),name="myorders"),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path("orders/", views.OrderListView.as_view(), name= "orders"),
    path("orders/<int:pk>", views.OrderDetailView.as_view(), name="order"),
    path("oders/new", views.OrderCreateView.as_view(), name='order_new'),
    path("orders/<int:pk>/update", views.OrderUpdateView.as_view(), name="order_update"),
    path("orders/<int:pk>/delete", views.OrderDeleteView.as_view(), name="order_delete"),

]