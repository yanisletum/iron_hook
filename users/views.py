from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from cart.models import Order

def register(request):
    # Защита: если пользователь уже вошел, ему не нужна регистрация
    if request.user.is_authenticated:
        return redirect('users:profile')

    # Если пользователь отправил форму с данными
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) # Сразу авторизуем после регистрации
            return redirect('users:profile')
    else:
        # Если пользователь просто открыл страницу — отдаем пустую форму
        form = UserCreationForm()
        
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    # Достаем из базы все заказы, которые принадлежат текущему пользователю
    # Они уже отсортированы от новых к старым благодаря классу Meta в модели
    orders = Order.objects.filter(user=request.user)
    
    return render(request, 'users/profile.html', {'orders': orders})