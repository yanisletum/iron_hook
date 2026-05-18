from django.shortcuts import render, get_object_or_404
from .models import Post
import json
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.contrib.auth.models import User
from django.core.files.base import ContentFile


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

@csrf_exempt
@require_http_methods(["POST"])
def api_create_post(request):
    api_key = request.headers.get('X-API-Key')
    if api_key != 'iron-hook-secret-key-2025':
        return JsonResponse({'error': 'Unauthorized'}, status=401)
    
    try:
        data = json.loads(request.body)
        title = data.get('title', '').strip()
        content = data.get('content', '').strip()
        image_b64 = data.get('image_base64', None)
        
        if not title or not content:
            return JsonResponse({'error': 'title и content обязательны'}, status=400)
        
        author = User.objects.filter(is_superuser=True).first()
        if not author:
            return JsonResponse({'error': 'Нет суперпользователя'}, status=500)
        
        post = Post.objects.create(title=title, content=content, author=author)
        
        if image_b64:
            image_data = base64.b64decode(image_b64)
            filename = f"blog_{post.id}.jpg"
            post.image.save(filename, ContentFile(image_data), save=True)
        
        return JsonResponse({
            'success': True,
            'post_id': post.id,
            'title': post.title,
            'url': f'/blog/{post.id}/'
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Неверный JSON'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
