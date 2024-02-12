from django.contrib import admin

from .models import Dish, Order, OrderItem

class DishAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'is_available')

admin.site.register(Dish, DishAdmin)
admin.site.register(Order)
admin.site.register(OrderItem)

