from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'users'

urlpatterns = [
    # Используем встроенные классы Django для логина и логаута
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # Добавили next_page='/', чтобы после выхода пользователя кидало на главную страницу
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Наши собственные представления для регистрации и профиля
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
]