from django.contrib import admin
from .models import (VehicleModel,
                     Service,
                     Vehicle,
                     Order,
                     OrderLine)

# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Service)
admin.site.register(Vehicle)
admin.site.register(Order)
admin.site.register(OrderLine)