from django.contrib import admin
from .models import Category, Product, ProductVariation, ProductImage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

# Блок 1: Для дополнительных ФОТОГРАФИЙ
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3  # Вот твои "лишние" ячейки для фото (по умолчанию будет 3 пустых + основная)

# Блок 2: Для ВАРИАЦИЙ (диаметры, размеры)
class ProductVariationInline(admin.TabularInline):
    model = ProductVariation
    extra = 1  # Здесь оставим одну пустую строку для порядка

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'available']
    prepopulated_fields = {'slug': ('name',)}
    
    # ПОДКЛЮЧАЕМ ОБА БЛОКА ОДНОВРЕМЕННО
    inlines = [ProductImageInline, ProductVariationInline]