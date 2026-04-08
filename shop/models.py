from django.db import models
from django.urls import reverse
from PIL import Image

class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True, verbose_name="Имя категории")
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_list_by_category', args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name="Категория")
    name = models.CharField(max_length=200, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True, verbose_name="Изображение")
    description = models.TextField(blank=True, verbose_name="Описание")
    
    # Поле для вывода кратких характеристик прямо на карточке в каталоге
    short_features = models.CharField(max_length=255, blank=True, verbose_name="Краткие характеристики (для карточки)")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена")
    available = models.BooleanField(default=True, verbose_name="В наличии")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        # === ИСПРАВЛЕНИЕ: Современный формат индексов для новых версий Django ===
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.slug])

    # Функция для автоматического сжатия главной картинки товара
    def save(self, *args, **kwargs):
        # Сначала сохраняем товар
        super().save(*args, **kwargs)

        # Если картинка есть, открываем её и проверяем размеры
        if self.image:
            img = Image.open(self.image.path)

            if img.height > 800 or img.width > 800:
                output_size = (800, 800)
                img.thumbnail(output_size)
                img.save(self.image.path)

# Таблица для размеров/диаметров
class ProductVariation(models.Model):
    product = models.ForeignKey(Product, related_name='variations', on_delete=models.CASCADE)
    value = models.CharField(max_length=50, verbose_name="Значение вариации")

    class Meta:
        verbose_name = 'Вариация товара'
        verbose_name_plural = 'Вариации товаров'

    def __str__(self):
        return f"{self.product.name} - {self.value}"

# Таблица для дополнительных фотографий
class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/gallery/%Y/%m/%d', verbose_name="Дополнительное фото")

    class Meta:
        verbose_name = 'Дополнительное фото'
        verbose_name_plural = 'Галерея фотографий'