from django.shortcuts import render
from shop.models import Product
from blog.models import Post

def index(request):
    # Берем 4 последних добавленных товара (сортируем по убыванию ID)
    latest_products = Product.objects.filter(available=True).order_by('-id')[:4]
    
    # Берем 3 последние статьи из блога
    latest_posts = Post.objects.all().order_by('-created_at')[:3]

    return render(request, 'core/index.html', {
        'products': latest_products,
        'latest_posts': latest_posts
    })

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    return render(request, 'core/contact.html')
