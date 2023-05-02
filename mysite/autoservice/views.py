from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service, Vehicle, Order
from django.views import generic

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

def vehicles(request):
    context = {
        "vehicles": Vehicle.objects.all()
    }
    return render(request, "vehicles.html", context=context)

def vehicle(request, vehicle_id):
    context = {
        "vehicle": get_object_or_404(Vehicle, pk=vehicle_id)
    }
    return render(request, "vehicle.html", context=context)

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"