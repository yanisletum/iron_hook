from django.shortcuts import render, get_object_or_404
from .models import Post

def post_list(request):
    # Достаем все статьи. Они уже отсортированы по дате благодаря классу Meta в модели
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    # Ищем статью по ID. Если её нет — Django сам выдаст красивую ошибку 404
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

