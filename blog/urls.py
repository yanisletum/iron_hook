from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    
    # Изменили post_id на pk, чтобы оно идеально совпадало с новым views.py
    path('<int:pk>/', views.post_detail, name='post_detail'),
    
    # Заменили твой старый api/create/ на наш новый секретный шлюз
    path('api/publish/', views.publish_post, name='publish_post'),
]