from django.contrib import admin
from .models import Member
from .models import Fruit
from .models import VehicleLog

admin.site.register(Member)


@admin.register(Fruit)
class FruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'created_at')
    search_fields = ('name',)
    list_filter = ('created_at',)


@admin.register(VehicleLog)
class VehicleLogAdmin(admin.ModelAdmin):
    list_display = ("license_plate", "vehicle_type", "entry_time", "exit_time", "driver_name")
    list_filter = ("vehicle_type", "entry_time")
    search_fields = ("license_plate", "driver_name")