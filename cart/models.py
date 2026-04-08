from django.db import models
from django.contrib.auth.models import User
from shop.models import Product

class Cart(models.Model):
    # Корзина жестко привязана к одному пользователю (OneToOne)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart', verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'

    def __str__(self):
        return f"Корзина пользователя {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    
    # ---> НОВОЕ ПОЛЕ: ЗАПОМИНАЕМ ВЫБРАННЫЙ РАЗМЕР <---
    variation = models.CharField(max_length=50, blank=True, null=True, verbose_name="Размер/Диаметр")
    
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Товар в корзине'
        verbose_name_plural = 'Товары в корзинах'

    def __str__(self):
        return f"{self.quantity} шт. {self.product.name}"
    

class Order(models.Model):
    # Привязываем заказ к профилю, если человек авторизован (null=True для гостей)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Пользователь")
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    email = models.EmailField(verbose_name="Email")
    city = models.CharField(max_length=100, verbose_name="Город")
    address = models.CharField(max_length=250, verbose_name="Адрес доставки")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Создан")
    paid = models.BooleanField(default=False, verbose_name="Оплачен")

    class Meta:
        ordering = ('-created',) # Новые заказы будут сверху
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return f'Заказ №{self.id}'
    
    def get_total_cost(self):
        return sum(item.price * item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name="Товар")
    
    # ---> НОВОЕ ПОЛЕ ДЛЯ ИСТОРИИ ЗАКАЗОВ <---
    variation = models.CharField(max_length=50, blank=True, null=True, verbose_name="Размер/Диаметр")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена при покупке")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def __str__(self):
        return str(self.id)    

