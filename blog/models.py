from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=250, verbose_name="Заголовок")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name="Автор")
    content = models.TextField(verbose_name="Текст статьи")
    image = models.ImageField(upload_to='blog_images/', blank=True, null=True, verbose_name="Изображение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at'] # Свежие статьи будут первыми

    def __str__(self):
        return self.title

