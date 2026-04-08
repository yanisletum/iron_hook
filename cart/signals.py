from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from shop.models import Product
from .models import Cart, CartItem

# Этот декоратор заставляет функцию срабатывать каждый раз при логине
@receiver(user_logged_in)
def merge_cart_on_login(sender, user, request, **kwargs):
    # Достаем корзину гостя из сессии
    session_cart = request.session.get('cart', {})
    
    # Если гость ничего не добавлял, просто выходим — делать нечего
    if not session_cart:
        return

    # Находим корзину этого пользователя в БД (или создаем, если он новый)
    cart, created = Cart.objects.get_or_create(user=user)

    # Перебираем все товары из сессионной корзины
    for product_id_str, item_data in session_cart.items():
        try:
            product = Product.objects.get(id=int(product_id_str))
            session_quantity = item_data['quantity']
            
            # Проверяем, лежал ли уже этот товар у пользователя в БД-корзине
            cart_item, item_created = CartItem.objects.get_or_create(
                cart=cart, 
                product=product,
                defaults={'quantity': session_quantity} # Если создаем новый, берем количество из сессии
            )
            
            # Если товар УЖЕ БЫЛ в БД-корзине, мы плюсуем к нему то, что он накликал как гость
            if not item_created:
                cart_item.quantity += session_quantity
                cart_item.save()
                
        except Product.DoesNotExist:
            continue # Если товар почему-то удалили из базы, просто пропускаем его
            
    # Самое важное: очищаем сессионную корзину, чтобы она не дублировалась
    del request.session['cart']
    request.session.modified = True