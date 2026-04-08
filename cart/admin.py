from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem

# Позволяет видеть товары прямо внутри страницы корзины
class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0
    readonly_fields = ['product', 'quantity'] # В админке мы только смотрим, а не меняем корзины

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'created_at']
    search_fields = ['user__username']
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'city', 'paid', 'created']
    list_filter = ['paid', 'created']
    inlines = [OrderItemInline]
