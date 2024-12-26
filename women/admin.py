from typing import Any
from django.contrib import admin, messages
from django.db.models.query import QuerySet
from .models import Women,Category
from django.utils.safestring import mark_safe


class MarriedFilter(admin.SimpleListFilter):
    title = 'Статус женщины'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем'),
        ]
    
    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(hasbend__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(hasbend__isnull=True)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('title', 'time_create', 'is_published', 'post_photo', 'cat',)
    list_display_links = ('title',)
    readonly_fields = ['post_photo']
    ordering = ('time_create', 'title')
    list_editable = ('is_published',)
    list_per_page = 5
    actions = ['set_published', 'set_draft']
    search_fields = ['title', 'cat__name']
    list_filter = [MarriedFilter,'cat__name', 'is_published']
    fields = ['title', 'slug', 'content', 'cat', 'photo', 'post_photo', 'hasbend', 'tags']
    prepopulated_fields = {'slug': ("title",)}
    filter_horizontal = ['tags']

    @admin.display(description="Изображение", ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return "Без фото"


    @admin.action(description="Опубликовать")
    def set_published(self, request, queryset):
        count = queryset.update(is_published=Women.Status.PUBLISHED)
        self.message_user(request, f"{count} записей опубликовано.")

    @admin.action(description="Снять с публикации")
    def set_draft(self, request, queryset):
        count = queryset.update(is_published=Women.Status.DRAFT)
        self.message_user(request, f"{count} снято с публикации.", messages.WARNING)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')