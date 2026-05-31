from django.contrib import admin
from .models import Post

def make_published(modeladmin, request, queryset):
    queryset.update(is_draft=False)
make_published.short_description = "Опубликовать выбранные статьи"

def make_draft(modeladmin, request, queryset):
    queryset.update(is_draft=True)
make_draft.short_description = "Перевести в черновики"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'is_draft', 'created_at']
    list_filter = ['is_draft', 'created_at', 'author']
    search_fields = ['title', 'content']
    date_hierarchy = 'created_at'
    actions = [make_published, make_draft]