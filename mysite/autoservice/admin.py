from django.contrib import admin
from .models import (VehicleModel,
                     Service,
                     Vehicle,
                     Order,
                     OrderLine,
                     OrderComment,
                     Profile,
                     )

class OrderLineInLine(admin.TabularInline):
    model = OrderLine
    extra = 0

class VehicleAdmin(admin.ModelAdmin):
    list_display = ["owner_name", "vehicle_model", "plate", "vin"]
    list_filter = ["owner_name", "vehicle_model__make", "vehicle_model__model"]
    search_fields = ["plate", "vin", "vehicle_model__make", "vehicle_model__model"]

class ServiceAdmin(admin.ModelAdmin):
    list_display = ["name", "price"]

class OrderCommentInLine(admin.TabularInline):
    model = OrderComment
    extra = 0



class OrderAdmin(admin.ModelAdmin):
    list_display = ["vehicle", "date", "client", "deadline", "deadline_overdue"]
    inlines = [OrderLineInLine, OrderCommentInLine]
    list_editable = ["client", "deadline"]
# Register your models here.
admin.site.register(VehicleModel)
admin.site.register(Service, ServiceAdmin)
admin.site.register(Vehicle, VehicleAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderLine)
admin.site.register(Profile)

