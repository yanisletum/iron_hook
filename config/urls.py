from django.contrib import admin
from django.urls import path, include, re_path # Добавили re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve # Добавили serve для раздачи файлов

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('shop/', include('shop.urls', namespace='shop')),
    path('blog/', include('blog.urls', namespace='blog')),
    path('users/', include('users.urls', namespace='users')),
    # core оставляем пустым, чтобы главная страница открывалась по адресу 127.0.0.1:8000/
    path('', include('core.urls', namespace='core')),
]

# Если мы в режиме разработки (DEBUG = True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# А этот блок "подстрахует" нас, когда DEBUG = False на твоем компьютере
if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}),
    ]

