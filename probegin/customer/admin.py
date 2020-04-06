from django.contrib import admin

from .models import Customer, CustomerDiscount


class CustomerDiscountAdmin(admin.TabularInline):
    model = CustomerDiscount


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    inlines = [CustomerDiscountAdmin]
    list_display = ('id', 'search_name', 'name', 'email_sender', )
