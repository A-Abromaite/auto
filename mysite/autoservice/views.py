from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.http import HttpResponse
from .models import Service, Vehicle, Order, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderCommentForm, UserUpdateForm, ProfileUpdateForm, OrderForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin


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
    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1
    num_services = Service.objects.all().count()
    num_vehicles = Vehicle.objects.all().count()
    num_services_completed = Order.objects.filter(status__exact="i").count()

    context = {
        'num_services': num_services,
        'num_vehicles': num_vehicles,
        'num_services_completed': num_services_completed,
        'num_visits': num_visits,
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

class MyOrderListView(generic.ListView):
    model = Order
    template_name = "my_orders.html"
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
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

class OrderListView(generic.ListView):
    model = Order
    template_name = "orders.html"
    context_object_name = "orders"
    paginate_by = 5

class OrderDetailView(FormMixin, generic.DetailView):
    model = Order
    template_name = "order.html"
    context_object_name = "order"
    form_class = OrderCommentForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

class OrderCreateView(LoginRequiredMixin, generic.CreateView):
    model = Order
    # fields = ['vehicle', 'deadline', 'status']
    success_url = '/autoservice/orders/'
    template_name = 'order_form.html'
    form_class = OrderForm

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Order
    # fields = ['vehicle', 'deadline', 'status']
    # success_url = '/autoservice/orders/'
    template_name = 'order_form.html'
    form_class = OrderForm
    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Order
    context_object_name = "order"
    template_name = "order_delete.html"
    success_url = '/autoservice/orders/'

    def test_func(self):
        return self.get_object().client == self.request.user

class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = 'orderline_form.html'

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        return order.client == self.request.user

    # success_url = '/autoservice/orders/'



    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['pk']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = 'orderline_form.html'

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        return order.client == self.request.user

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['order_id']})

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['order_id'])
        return super().form_valid(form)

class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = OrderLine
    context_object_name = 'orderline'
    template_name = 'orderline_delete.html'

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        return order.client == self.request.user

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['order_id']})