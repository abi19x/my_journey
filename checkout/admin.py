from django.contrib import admin
from .models import Order

# Register your models here.


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'order_total', 'date')
    readonly_fields = ('order_number', 'order_total', 'date')

    fields = (
        'order_number', 'full_name', 'email', 'phone_number',
        'country', 'postcode', 'town_or_city',
        'street_address1', 'street_address2', 'county',
        'order_total', 'date'
    )
    
    ordering = ('-date',)

