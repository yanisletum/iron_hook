from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from django.db.models import Q

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    # === ПРОДВИНУТЫЙ ПОИСК ДЛЯ РУССКОГО ЯЗЫКА ===
    search_query = request.GET.get('q') 
    if search_query:
        words = search_query.strip().split()
        q_objects = Q()
        
        for word in words:
            # Умное отсечение окончаний
            if len(word) > 5:
                search_word = word[:-2]
            elif len(word) > 4:
                search_word = word[:-1]
            else:
                search_word = word
                
            # ОБХОДИМ ОШИБКУ БАЗЫ ДАННЫХ ДЛЯ РУССКОГО ЯЗЫКА
            # Создаем два варианта слова (с маленькой и с большой буквы)
            word_lower = search_word.lower()       # например: "катуш"
            word_cap = search_word.capitalize()    # например: "Катуш"
            
            # Ищем совпадения любого из вариантов в имени товара ИЛИ категории
            q_objects &= (
                Q(name__icontains=word_lower) | Q(name__icontains=word_cap) |
                Q(category__name__icontains=word_lower) | Q(category__name__icontains=word_cap)
            )
            
        products = products.filter(q_objects)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        # Фильтруем товары: оставляем только те, которые относятся к выбранной категории
        products = products.filter(category=category)

    return render(request, 'shop/catalog.html', {
        'category': category,
        'categories': categories,
        'products': products,
        'search_query': search_query
    })

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, available=True)
    return render(request, 'shop/product_detail.html', {'product': product})