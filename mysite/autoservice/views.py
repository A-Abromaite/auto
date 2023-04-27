from django.shortcuts import render
from django.http import HttpResponse
from .models import Service, VehicleModel, Vehicle, Order, OrderLine

# Create your views here.
def index(request):

    num_services = Service.objects.all().count()
    num_vehicles = Vehicle.objects.all().count()
    num_services_completed = Order.objects.filter(status__exact="i").count()

    context = {
        'num_services': num_services,
        'num_vehicles': num_vehicles,
        'num_services_completed': num_services_completed
    }


    return render(request, "index.html", context=context)