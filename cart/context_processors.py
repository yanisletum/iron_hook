from .models import Cart

def cart_processor(request):
    total_items = 0
    
    # Если пользователь авторизован — считаем товары из БД
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            total_items = sum(item.quantity for item in cart.items.all())
        except Cart.DoesNotExist:
            total_items = 0
            
    # Если гость — считаем товары из сессии (куки)
    else:
        cart_session = request.session.get('cart', {})
        total_items = sum(item['quantity'] for item in cart_session.values())

    # Эта переменная теперь будет доступна в любом HTML-файле сайта
    return {'cart_total_items': total_items}