from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('checkout/', views.order_create, name='order_create'),
    
    # === НАШ НОВЫЙ ПУТЬ ДЛЯ КРЕСТИКА (AJAX) ===
    path('remove-ajax/', views.cart_remove_ajax, name='cart_remove_ajax'),
]