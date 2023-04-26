from django.contrib import admin
from .models import (VehicleModel,
                     Service,
                     Vehicle,
                     Order,
                     OrderLine)

class OrderAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "date"]

# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Service)
admin.site.register(Vehicle)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)

