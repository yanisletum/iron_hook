from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from shop.models import Product
from .models import Cart, CartItem, Order, OrderItem
from .forms import OrderCreateForm
from django.shortcuts import redirect

def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    
    # 1. Ловим выбранный размер из запроса (если он есть)
    variation = request.GET.get('variation', '') 
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        # 2. Ищем товар именно с ЭТИМ размером!
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart, 
            product=product,
            variation=variation # <--- Сохраняем диаметр
        )
        
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
            
        total_items = sum(item.quantity for item in cart.items.all())
        
    else:
        cart_session = request.session.get('cart', {})
        # 3. Для гостя создаем сложный уникальный ключ, например "5_0.14 мм"
        item_key = f"{product.id}_{variation}" if variation else str(product.id)
        
        if item_key in cart_session:
            cart_session[item_key]['quantity'] += 1
        else:
            cart_session[item_key] = {
                'product_id': product.id,
                'price': str(product.price), 
                'quantity': 1,
                'variation': variation # <--- Сохраняем диаметр гостю
            }
            
        request.session['cart'] = cart_session
        request.session.modified = True
        
        total_items = sum(item['quantity'] for item in cart_session.values())
        
    return JsonResponse({'success': True, 'total_items': total_items})


def cart_remove(request, product_id):
    # 1. Логика для АВТОРИЗОВАННОГО пользователя
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Находим и удаляем конкретный товар из БД
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
            
            total_items = sum(item.quantity for item in cart.items.all())
            total_price = float(sum(item.product.price * item.quantity for item in cart.items.all()))
        except Cart.DoesNotExist:
            total_items = 0
            total_price = 0
            
    # 2. Логика для ГОСТЯ
    else:
        cart_session = request.session.get('cart', {})
        product_id_str = str(product_id)
        
        if product_id_str in cart_session:
            del cart_session[product_id_str]
            request.session['cart'] = cart_session
            request.session.modified = True
            
        total_items = sum(item['quantity'] for item in cart_session.values())
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_session.values())

    return JsonResponse({
        'success': True, 
        'total_items': total_items, 
        'total_price': total_price
    })

def cart_detail(request):
    cart_items = []
    total_price = 0
    
    # 1. Формируем список товаров из БД для авторизованного
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        for item in cart.items.all():
            item_total = float(item.product.price) * item.quantity
            cart_items.append({
                'product': item.product,
                'price': item.product.price,
                'quantity': item.quantity,
                'total_price': item_total,
                'variation': item.variation # <--- Передаем размер в шаблон
            })
            total_price += item_total
            
    # 2. Формируем список товаров из сессии для гостя
    else:
        cart_session = request.session.get('cart', {})
        # Перебираем сложные ключи сессии (теперь они могут быть "5_0.14 мм")
        for key, item_data in cart_session.items():
            product = get_object_or_404(Product, id=item_data['product_id'])
            item_total = float(item_data['price']) * item_data['quantity']
            
            cart_items.append({
                'product': product,
                'price': item_data['price'],
                'quantity': item_data['quantity'],
                'total_price': item_total,
                'variation': item_data.get('variation', '') # <--- Достаем размер
            })
            total_price += item_total
            
    return render(request, 'cart/cart_detail.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })
            
    

def order_create(request):
    cart_items = []
    total_price = 0

    # 1. Собираем товары (как в функции cart_detail)
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            cart_items = cart.items.all()
            for item in cart_items:
                item.total_price = item.product.price * item.quantity
                total_price += float(item.total_price)
        except Cart.DoesNotExist:
            pass
    else:
        cart_session = request.session.get('cart', {})
        products = Product.objects.filter(id__in=cart_session.keys())
        for product in products:
            item = cart_session[str(product.id)]
            item['product'] = product
            item['total_price'] = float(item['price']) * item['quantity']
            cart_items.append(item)
            total_price += item['total_price']

    # Если корзина пуста — отправляем обратно
    if not cart_items:
        return redirect('cart:cart_detail')

    # 2. Обработка формы заказа
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Сохраняем заказ, но пока не коммитим в БД
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save() # Теперь сохраняем сам заказ

            # Переносим товары из Корзины в Заказ и очищаем Корзину
            if request.user.is_authenticated:
                for item in cart_items:
                    OrderItem.objects.create(order=order, product=item.product, price=item.product.price, quantity=item.quantity)
                cart.items.all().delete() # Очищаем БД корзину
            else:
                for item in cart_items:
                    OrderItem.objects.create(order=order, product=item['product'], price=item['price'], quantity=item['quantity'])
                del request.session['cart'] # Очищаем сессию
                request.session.modified = True

            # Отправляем на страницу успешного оформления (ее сделаем позже)
            return render(request, 'cart/order_created.html', {'order': order})
            
    else:
        # Предзаполняем форму, если пользователь авторизован
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {'first_name': request.user.first_name, 'last_name': request.user.last_name, 'email': request.user.email}
        form = OrderCreateForm(initial=initial_data)

    return render(request, 'cart/order_create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

def cart_remove_ajax(request):
    if request.method == 'POST':
        # Читаем данные, которые прислал наш JavaScript при клике на крестик
        data = json.loads(request.body)
        product_id = data.get('product_id')
        variation = data.get('variation', '')

        total_items = 0
        total_price = 0

        # 1. Логика удаления для АВТОРИЗОВАННОГО пользователя
        if request.user.is_authenticated:
            try:
                cart = Cart.objects.get(user=request.user)
                # Удаляем строго конкретный товар с КОНКРЕТНЫМ размером
                CartItem.objects.filter(cart=cart, product_id=product_id, variation=variation).delete()
                
                # Пересчитываем итоги
                total_items = sum(item.quantity for item in cart.items.all())
                total_price = sum(float(item.product.price) * item.quantity for item in cart.items.all())
            except Cart.DoesNotExist:
                pass
                
        # 2. Логика удаления для ГОСТЯ
        else:
            cart_session = request.session.get('cart', {})
            # Собираем тот самый сложный ключ (например "5_0.14 мм" или просто "5")
            item_key = f"{product_id}_{variation}" if variation else str(product_id)

            if item_key in cart_session:
                del cart_session[item_key] # Удаляем из сессии
                request.session['cart'] = cart_session
                request.session.modified = True

            # Пересчитываем итоги
            total_items = sum(item['quantity'] for item in cart_session.values())
            total_price = sum(float(item['price']) * item['quantity'] for item in cart_session.values())

        # Возвращаем новые цифры в браузер, чтобы скрипт обновил страницу без перезагрузки
        return JsonResponse({
            'success': True,
            'cart_len': total_items,
            'cart_total_price': f"{total_price:.2f}" # Округляем до 2 копеек
        })
        
    return JsonResponse({'success': False})