from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from .models import Service, Vehicle, Order
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q

def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Vehicle.objects.filter(Q(plate__icontains=query) | Q(vin__icontains=query) | Q(owner_name__icontains=query) | Q(vehicle_model__make__icontains=query) | Q(vehicle_model__model__icontains=query))
    return render(request, 'search.html', {'vehicles': search_results, 'query': query})


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
    paginator = Paginator(Vehicle.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_vehicles = paginator.get_page(page_number)
    context = {
        "vehicles": paged_vehicles,
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
    paginate_by = 2

class OrderDetailView(generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"